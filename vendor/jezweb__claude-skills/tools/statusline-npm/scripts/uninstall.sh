#!/bin/bash

# Claude Code Status Line - Uninstallation Script
# Removes custom status line and optionally restores previous configuration

set -e

INSTALL_PATH="$HOME/.claude/statusline.sh"
SETTINGS_FILE="$HOME/.claude/settings.json"

echo "🗑️  Uninstalling Claude Code Custom Status Line..."
echo ""

# Find most recent backup
LATEST_BACKUP=$(ls -t "${INSTALL_PATH}.backup-"* 2>/dev/null | head -1 || echo "")
LATEST_SETTINGS_BACKUP=$(ls -t "${SETTINGS_FILE}.backup-"* 2>/dev/null | head -1 || echo "")

# Remove statusline script
if [[ -f "$INSTALL_PATH" ]]; then
    echo "📝 Removing status line script..."
    rm "$INSTALL_PATH"
    echo "   Removed: $INSTALL_PATH"
else
    echo "⚠️  Status line script not found (already removed?)"
fi

echo ""

# Ask about settings.json
if [[ -f "$SETTINGS_FILE" ]]; then
    echo "⚙️  Settings.json options:"
    echo "   1) Remove statusLine configuration (keep other settings)"
    echo "   2) Restore from backup (if available)"
    echo "   3) Leave settings.json unchanged"
    echo ""
    read -p "Choose option [1-3]: " choice

    case $choice in
        1)
            echo "Removing statusLine from settings.json..."
            jq 'del(.statusLine)' "$SETTINGS_FILE" > "${SETTINGS_FILE}.tmp" && mv "${SETTINGS_FILE}.tmp" "$SETTINGS_FILE"
            echo "   StatusLine configuration removed"
            ;;
        2)
            if [[ -n "$LATEST_SETTINGS_BACKUP" ]]; then
                echo "Restoring from backup: $LATEST_SETTINGS_BACKUP"
                cp "$LATEST_SETTINGS_BACKUP" "$SETTINGS_FILE"
                echo "   Settings restored"
            else
                echo "❌ No backup found. Removing statusLine configuration instead..."
                jq 'del(.statusLine)' "$SETTINGS_FILE" > "${SETTINGS_FILE}.tmp" && mv "${SETTINGS_FILE}.tmp" "$SETTINGS_FILE"
            fi
            ;;
        3)
            echo "Leaving settings.json unchanged"
            ;;
        *)
            echo "Invalid option. Leaving settings.json unchanged"
            ;;
    esac
fi

echo ""

# Ask about backups
if [[ -n "$LATEST_BACKUP" ]] || [[ -n "$LATEST_SETTINGS_BACKUP" ]]; then
    echo "📦 Backup files found:"
    [[ -n "$LATEST_BACKUP" ]] && echo "   • $LATEST_BACKUP"
    [[ -n "$LATEST_SETTINGS_BACKUP" ]] && echo "   • $LATEST_SETTINGS_BACKUP"
    echo ""
    read -p "Delete backup files? [y/N]: " delete_backups

    if [[ "$delete_backups" =~ ^[Yy]$ ]]; then
        [[ -n "$LATEST_BACKUP" ]] && rm "${INSTALL_PATH}.backup-"* 2>/dev/null && echo "   Removed script backups"
        [[ -n "$LATEST_SETTINGS_BACKUP" ]] && rm "${SETTINGS_FILE}.backup-"* 2>/dev/null && echo "   Removed settings backups"
    else
        echo "   Backups preserved"
    fi
fi

echo ""
echo "✅ Uninstallation complete!"
echo ""
echo "🔄 Restart Claude Code for changes to take effect"
echo ""
echo "ℹ️  To reinstall: ./install.sh"
