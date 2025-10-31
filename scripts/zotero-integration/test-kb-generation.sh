#!/bin/bash
# Test script for knowledge base generation workflow

set -e

echo "======================================================================"
echo "Knowledge Base Generation - Test Suite"
echo "======================================================================"
echo

# Test 1: Python syntax validation
echo "Test 1: Validating Python script syntax..."
python3 -m py_compile scripts/zotero-integration/zotero_sync.py
python3 -m py_compile scripts/zotero-integration/knowledge_base_generator.py
echo "✓ Python syntax valid"
echo

# Test 2: Script help output
echo "Test 2: Testing script help output..."
python3 scripts/zotero-integration/zotero_sync.py --help > /dev/null
python3 scripts/zotero-integration/knowledge_base_generator.py --help > /dev/null
echo "✓ Script help working"
echo

# Test 3: Workflow YAML validation
echo "Test 3: Validating GitHub Actions workflow YAML..."
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/knowledge-base-generation.yml'))"
echo "✓ Workflow YAML valid"
echo

# Test 4: Knowledge base generator execution
echo "Test 4: Running knowledge base generator..."
python3 scripts/zotero-integration/knowledge_base_generator.py > /tmp/kb-gen-output.log 2>&1
exit_code=$?
if [ $exit_code -eq 0 ]; then
    echo "✓ Knowledge base generator executed successfully"
else
    echo "✗ Knowledge base generator failed"
    cat /tmp/kb-gen-output.log
    exit 1
fi
echo

# Test 5: Verify generated files
echo "Test 5: Verifying generated files..."
files=(
    "knowledge-database/analysis-data.json"
    "knowledge-database/claude-prompt.md"
    "knowledge-database/CLAUDE_INTEGRATION.md"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file exists"
    else
        echo "  ✗ $file missing"
        exit 1
    fi
done
echo

# Test 6: Validate JSON files
echo "Test 6: Validating JSON files..."
python3 -c "import json; json.load(open('knowledge-database/analysis-data.json'))"
echo "✓ analysis-data.json is valid JSON"
echo

# Test 7: Check analysis data structure
echo "Test 7: Checking analysis data structure..."
projects=$(python3 -c "import json; data = json.load(open('knowledge-database/analysis-data.json')); print(data['total_projects'])")
echo "  Projects found: $projects"
if [ "$projects" -ge 1 ]; then
    echo "✓ Analysis data contains project information"
else
    echo "✗ No projects found in analysis data"
    exit 1
fi
echo

# Test 8: Verify example files
echo "Test 8: Verifying example output files..."
example_files=(
    "knowledge-database/examples/README.md"
    "knowledge-database/examples/emergence.md"
    "knowledge-database/examples/systems-theory-index.md"
)

for file in "${example_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file exists"
    else
        echo "  ✗ $file missing"
        exit 1
    fi
done
echo

# Test 9: Documentation files
echo "Test 9: Checking documentation..."
doc_files=(
    "docs/KNOWLEDGE_BASE_WORKFLOW.md"
    "scripts/zotero-integration/README.md"
)

for file in "${doc_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file exists"
    else
        echo "  ✗ $file missing"
        exit 1
    fi
done
echo

# Test 10: Verify gitignore entries
echo "Test 10: Checking .gitignore..."
if grep -q "zotero-cache/" .gitignore; then
    echo "✓ .gitignore contains zotero-cache exclusion"
else
    echo "✗ .gitignore missing zotero-cache"
    exit 1
fi
echo

echo "======================================================================"
echo "All tests passed! ✓"
echo "======================================================================"
echo
echo "Summary:"
echo "  - Python scripts: valid syntax and executable"
echo "  - Workflow YAML: valid configuration"
echo "  - Knowledge base generator: produces expected output"
echo "  - Documentation: complete"
echo "  - Example files: present and formatted"
echo
echo "Next steps:"
echo "  1. Test with actual Zotero API access"
echo "  2. Validate Claude Code integration"
echo "  3. Run full workflow in GitHub Actions"
