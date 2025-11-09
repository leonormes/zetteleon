#!/bin/bash
# ProdOS Universal Context Loader - Installation Script
# Creates unified context loading system for immediate LLM operability

set -e  # Exit on any error

echo "🚀 Installing ProdOS Universal Context Loader..."
echo

# Check if script already exists
SCRIPT_PATH="$HOME/.local/bin/prodos-universal-context"
ALIAS_PATH="$HOME/.config/shell/prodos-universal-aliases.zsh"

if [[ -f "$SCRIPT_PATH" ]]; then
    echo "✅ Universal context loader already installed at: $SCRIPT_PATH"
else
    echo "❌ Universal context loader not found - manual installation required"
    echo "   Expected location: $SCRIPT_PATH"
    exit 1
fi

# Check if aliases are configured
if [[ -f "$ALIAS_PATH" ]]; then
    echo "✅ Shell aliases already configured at: $ALIAS_PATH"
else
    echo "❌ Shell aliases not found - manual installation required"
    echo "   Expected location: $ALIAS_PATH"
    exit 1
fi

# Ensure script is executable
chmod +x "$SCRIPT_PATH"
echo "✅ Made script executable"

# Check if aliases are sourced in shell config
ZSHRC="$HOME/.zshrc"
if grep -q "prodos-universal-aliases.zsh" "$ZSHRC" 2>/dev/null; then
    echo "✅ Aliases already sourced in .zshrc"
else
    echo "⚠️  Adding alias source to .zshrc"
    echo "" >> "$ZSHRC"
    echo "# ProdOS Universal Context Loader aliases" >> "$ZSHRC"
    echo "source ~/.config/shell/prodos-universal-aliases.zsh" >> "$ZSHRC"
    echo "✅ Added to shell configuration"
fi

# Create config directory if needed
mkdir -p "$HOME/.config/shell"

echo
echo "🔍 Testing installation..."

# Test system status
echo "Testing system status check..."
if "$SCRIPT_PATH" --status >/dev/null 2>&1; then
    echo "✅ System status check working"
else
    echo "❌ System status check failed"
    exit 1
fi

# Test context generation
echo "Testing context generation..."
if "$SCRIPT_PATH" --save >/dev/null 2>&1; then
    echo "✅ Context generation working"
    CONTEXT_FILE="$HOME/prodos-universal-context.md"
    if [[ -f "$CONTEXT_FILE" ]]; then
        LINES=$(wc -l < "$CONTEXT_FILE")
        SIZE=$(du -h "$CONTEXT_FILE" | cut -f1)
        echo "   Generated: $LINES lines ($SIZE)"
        rm "$CONTEXT_FILE"  # Clean up test file
    fi
else
    echo "❌ Context generation failed"
    exit 1
fi

echo
echo "🎉 ProdOS Universal Context Loader successfully installed!"
echo
echo "📋 Available commands:"
echo "   ctx          - Copy complete context to clipboard"
echo "   ctx-full     - Save context to file"  
echo "   ctx-status   - Show system health"
echo "   llm-ready    - Quick session starter"
echo
echo "🔄 To use immediately:"
echo "   source ~/.config/shell/prodos-universal-aliases.zsh"
echo "   ctx"
echo
echo "💡 After restarting your shell, all commands will be available automatically"
echo
echo "🎯 Test your installation:"
echo "   ctx-status"
echo "   ctx && echo 'Context copied to clipboard - ready for LLM session'"
echo

exit 0