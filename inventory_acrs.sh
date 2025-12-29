#!/bin/bash

# Configuration
SUBSCRIPTION_ID="a085dd04-19aa-4d2b-9a35-e438097d84fc"
OUTPUT_FILE="ACR_Inventory_Typed.md"

# -----------------------------------------------------------------------------
# Data-Centric Parser (Python)
# -----------------------------------------------------------------------------
# This script maps the raw OCI state (MIME types) to our Domain Types.
# 
# DOMAIN TYPES:
# 1. Multi-Arch Index: A root manifest pointing to platform variants.
# 2. Helm Chart: An OCI artifact containing Helm configuration.
# 3. Single Image: A standard container image for a specific architecture.
# -----------------------------------------------------------------------------
cat << 'EOF' > _acr_type_parser.py
import sys, json

def determine_kind(item):
    """
    Derives the Artifact Kind based on strict Type invariants.
    """
    media_type = item.get('mediaType', '')
    config_media_type = item.get('configMediaType', '')
    
    # Invariant 1: The Index Invariant
    # If the media type identifies a list/index, it is a Multi-Arch Root.
    # It does not contain code itself; it points to it.
    if any(x in media_type for x in [
        'manifest.list', 
        'image.index'
    ]):
        return "📦 Multi-Arch Index"

    # Invariant 2: The Helm Invariant
    # Helm charts are identified by their specific Config Media Type.
    # Note: Sometimes arch/os is 'unknown', but the MIME type is the source of truth.
    if config_media_type and 'helm' in config_media_type:
        return "⎈ Helm Chart"

    # Invariant 3: The Image Invariant
    # If it's not the above, it's a standard payload.
    return "🐳 Container Image"

try:
    data = json.load(sys.stdin)
    
    if not data:
        print('| _No artifacts found_ | - | - | - | - |')
    else:
        for item in data:
            # 1. TAGS: Collapse list to string
            tags_list = item.get('tags')
            tags_str = ', '.join(sorted(tags_list)) if tags_list else '_(untagged)_'
            
            # 2. TYPE: Derive from MIME invariants
            kind = determine_kind(item)
            
            # 3. METADATA
            created = item.get('created', '')
            digest = item.get('digest', '')
            short_digest = digest[:12] + '...' if digest else '-'
            
            # 4. ARCHITECTURE
            # If it is a Multi-Arch Index, specific OS/Arch is irrelevant (it contains many).
            # We display "Multi-Platform" to be explicit.
            if "Multi-Arch" in kind:
                arch_display = "*Multi-Platform*"
            else:
                arch = item.get('arch') or 'unknown'
                os_name = item.get('os') or 'unknown'
                arch_display = f"{arch}/{os_name}"
            
            # OUTPUT: Pipe-delimited Markdown row
            print(f'| {tags_str} | {kind} | {created} | {arch_display} | `{short_digest}` |')

except Exception as e:
    # Fail gracefully if JSON is bad, print error as a row for debugging
    print(f'| Error parsing JSON | {str(e)} | - | - | - |')
EOF

# -----------------------------------------------------------------------------
# Main Execution Loop
# -----------------------------------------------------------------------------

# Ensure we are in the correct subscription
echo "Setting Azure subscription context to $SUBSCRIPTION_ID..."
az account set --subscription "$SUBSCRIPTION_ID"

# Initialize Markdown File
echo "# Azure Container Registry Inventory (Typed)" > "$OUTPUT_FILE"
echo "Generated on: $(date)" >> "$OUTPUT_FILE"
echo "Classification Strategy: MIME-Type Invariants" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Get List of ACRs
echo "Fetching list of Azure Container Registries..."
ACR_NAMES=$(az acr list --query "[].name" -o tsv)

if [ -z "$ACR_NAMES" ]; then
    echo "No Container Registries found in this subscription."
    exit 1
fi

for acr in $ACR_NAMES; do
    echo "Processing Registry: $acr"
    echo "## Registry: $acr" >> "$OUTPUT_FILE"
    
    LOGIN_SERVER=$(az acr show --name "$acr" --query "loginServer" -o tsv)
    echo "**Login Server**: 	$LOGIN_SERVER" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    
    echo "  Fetching repositories..."
    REPOS=$(az acr repository list --name "$acr" --output tsv 2>/dev/null)
    
    if [ -z "$REPOS" ]; then
        echo "_No repositories found._" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
    else
        for repo in $REPOS; do
            echo "    Scanning Repository: $repo"
            echo "### Repo: $repo" >> "$OUTPUT_FILE"
            
            # Create Table Header with new 'Type' column
            echo "| Tags | Type | Created Time | Arch/OS | Digest (Prefix) |" >> "$OUTPUT_FILE"
            echo "| --- | --- | --- | --- | --- |" >> "$OUTPUT_FILE"
            
            # Fetch Manifests with specific MIME types needed for our logic
            az acr manifest list-metadata --registry "$acr" --name "$repo" --orderby time_desc --top 5 \
                --query "[].{tags:tags, created:createdTime, digest:digest, arch:architecture, os:os, mediaType:mediaType, configMediaType:configMediaType}" -o json \
                | python3 _acr_type_parser.py >> "$OUTPUT_FILE"
            
            echo "" >> "$OUTPUT_FILE"
        done
    fi
    echo "---" >> "$OUTPUT_FILE"
done

# Cleanup
rm -f _acr_type_parser.py

echo ""
echo "========================================================"
echo "Inventory complete!"
echo "Report saved to: $(pwd)/$OUTPUT_FILE"
echo "========================================================"