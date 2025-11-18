#!/bin/bash
# Conflict Resolution Script for Route Corridor Calculator v2.0 Merge
# This script resolves the deletion conflicts when merging to main

set -e  # Exit on error

echo "╔═══════════════════════════════════════════════════════════════════════"
echo "║        Merge Conflict Resolution - Route Corridor Calculator v2.0    ║"
echo "╚═══════════════════════════════════════════════════════════════════════"
echo ""

# Check if we're in a merge conflict state
if ! git status | grep -q "Unmerged paths\|both deleted\|deleted by"; then
    echo "❌ No merge conflicts detected."
    echo ""
    echo "This script is for resolving conflicts during a merge."
    echo "If you haven't started the merge yet, run:"
    echo "  git checkout main"
    echo "  git merge claude/route-path-calculator-01Hof7xFLKARcqWx1tU3oFuH"
    echo ""
    exit 1
fi

echo "📋 Detected merge conflicts. Resolving..."
echo ""

# List of files that were intentionally deleted
DELETED_FILES=(
    "custom_gpt_upload/GPT_USAGE_GUIDE.md"
    "custom_gpt_upload/README.md"
    "custom_gpt_upload/UPLOAD_CHECKLIST.txt"
    "custom_gpt_upload/custom_gpt_instructions_COMPACT.txt"
    "custom_gpt_upload/custom_gpt_instructions_with_station_knowledge.txt"
)

# Resolve each conflict by confirming deletion
for file in "${DELETED_FILES[@]}"; do
    if git status | grep -q "$file"; then
        echo "✓ Confirming deletion: $file"
        git rm "$file" 2>/dev/null || true
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if all conflicts are resolved
if git status | grep -q "Unmerged paths"; then
    echo "⚠️  Some conflicts remain unresolved:"
    git status --short | grep "^[DU]"
    echo ""
    echo "Please resolve these manually and run:"
    echo "  git commit"
    exit 1
else
    echo "✅ All conflicts resolved!"
    echo ""
    echo "Files marked for deletion:"
    for file in "${DELETED_FILES[@]}"; do
        echo "  ✗ $file"
    done
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Next steps:"
    echo "  1. Review the changes:"
    echo "     git status"
    echo ""
    echo "  2. Complete the merge:"
    echo "     git commit -m \"Merge route corridor calculator v2.0 - remove redundant files\""
    echo ""
    echo "  3. Push to remote:"
    echo "     git push origin main"
    echo ""
fi
