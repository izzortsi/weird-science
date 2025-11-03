#!/bin/bash
# Wrapper script to generate knowledge database
# Calls the main knowledge base generator script

set -euo pipefail

# Get the repository root directory
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

echo "Generating knowledge database..."
echo "Repository root: $REPO_ROOT"
echo

# Change to repository root
cd "$REPO_ROOT"

# Build command with optional API keys
CMD="python3 scripts/zotero-integration/knowledge_base_generator.py --manifest zotero-cache/zotero-manifest.json"

# Add Zotero API key if available
if [ -n "${ZOTERO_API_KEY:-}" ]; then
    CMD="$CMD --api-key $ZOTERO_API_KEY"
    echo "Using Zotero API key"
fi

# Add Semantic Scholar API key if available (for Γ⁺ expansion)
if [ -n "${SEMANTIC_SCHOLAR_API_KEY:-}" ]; then
    CMD="$CMD --s2-api-key $SEMANTIC_SCHOLAR_API_KEY"
    echo "Using Semantic Scholar API key for Γ⁺ expansion"
else
    echo "No Semantic Scholar API key found - Γ⁺ expansion will be limited"
fi

echo "Running: $CMD"
echo

# Run the knowledge base generator
$CMD

echo
echo "Knowledge database generation completed."
