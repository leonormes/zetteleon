#!/bin/bash

# Configuration
SUBSCRIPTION_ID="a085dd04-19aa-4d2b-9a35-e438097d84fc"
OUTPUT_FILE="ACR_Inventory.md"

# Helper Python script for parsing
cat << 'EOF' > _acr_parser.py
import sys, json

try:
    # Read from stdin
    data = json.load(sys.stdin)
    
    if not data:
        print('| _No artifacts found_ | - | - | - |')
    else:
        for item in data:
            tags_list = item.get('tags')
            if tags_list:
                # Sort tags to be deterministic
                tags_list.sort()
                # Join with comma
                tags_str = ', '.join(tags_list)
            else:
                tags_str = '_(untagged)_'
            
            created = item.get('created', '')
            digest = item.get('digest', '')
            short_digest = digest[:12] + '...' if digest else '-'
            
            # Handle potential nulls
            arch = item.get('arch')
            if not arch: arch = 'unknown'
            
            os_name = item.get('os')
            if not os_name: os_name = 'unknown'
            
            # Print Markdown table row
            print(f'| {tags_str} | {created} | {arch}/{os_name} | `{short_digest}` |')

except Exception as e:
    # Fail gracefully if JSON is bad
    pass
EOF

# Ensure we are in the correct subscription
echo "Setting Azure subscription context to $SUBSCRIPTION_ID..."
az account set --subscription "$SUBSCRIPTION_ID"

# Initialize Markdown File
echo "# Azure Container Registry Inventory" > "$OUTPUT_FILE"
echo "Generated on: $(date)" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Get List of ACRs
echo "Fetching list of Azure Container Registries..."
ACR_NAMES=$(az acr list --query "[].name" -o tsv)

if [ -z "$ACR_NAMES" ]; then
    echo "No Container Registries found in this subscription."
    exit 1
fi

for acr in $ACR_NAMES;
 do
    echo "Processing Registry: $acr"
    echo "## Registry: $acr" >> "$OUTPUT_FILE"
    
    # Get Registry Login Server
    LOGIN_SERVER=$(az acr show --name "$acr" --query "loginServer" -o tsv)
    echo "**Login Server**: 	$LOGIN_SERVER" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    
    # List Repositories
    echo "  Fetching repositories..."
    REPOS=$(az acr repository list --name "$acr" --output tsv 2>/dev/null)
    
    if [ -z "$REPOS" ]; then
        echo "_No repositories found._" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
    else
        for repo in $REPOS;
         do
            echo "    Scanning Repository: $repo"
            echo "### Repo: $repo" >> "$OUTPUT_FILE"
            
            # Create Table Header
            echo "| Tags | Created Time | Arch/OS | Digest (Prefix) |" >> "$OUTPUT_FILE"
            echo "| --- | --- | --- | --- |" >> "$OUTPUT_FILE"
            
            # Fetch latest 5 manifests with metadata
            # We use list-metadata to get architecture/os which show-tags doesn't provide fully
            az acr manifest list-metadata --name "$acr" --repository "$repo" --orderby time_desc --top 5 \
                --query "[].{tags:tags, created:createdTime, digest:digest, arch:architecture, os:os}" -o json \
                | python3 _acr_parser.py >> "$OUTPUT_FILE"
            
            echo "" >> "$OUTPUT_FILE"
        done
    fi
    echo "---" >> "$OUTPUT_FILE"
done

# Cleanup
rm -f _acr_parser.py

echo ""
echo "========================================================"
echo "Inventory complete!"
echo "Report saved to: $(pwd)/$OUTPUT_FILE"
echo "========================================================"
