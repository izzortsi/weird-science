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

# Run the knowledge base generator
python3 scripts/zotero-integration/knowledge_base_generator.py \
  --manifest zotero-cache/zotero-manifest.json

echo
echo "Knowledge database generation completed."
