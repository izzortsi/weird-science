#!/bin/bash
# Integration test for Zotero integration

set -e

echo "================================"
echo "Zotero Integration Tests"
echo "================================"
echo ""

# Test 1: Python script syntax
echo "Test 1: Checking Python script syntax..."
python3 -m py_compile scripts/zotero-integration/zotero_exporter.py
echo "✓ Python script syntax valid"
echo ""

# Test 2: Script runs with dry-run
echo "Test 2: Running script in dry-run mode..."
python3 scripts/zotero-integration/zotero_exporter.py --dry-run > /tmp/zotero_test.log 2>&1
if grep -q "Zotero integration complete!" /tmp/zotero_test.log; then
    echo "✓ Script completed successfully"
else
    echo "✗ Script did not complete"
    cat /tmp/zotero_test.log
    exit 1
fi
echo ""

# Test 3: Project discovery
echo "Test 3: Checking project discovery..."
if grep -q "Found 3 projects:" /tmp/zotero_test.log; then
    echo "✓ Found expected number of projects"
else
    echo "✗ Project count mismatch"
    exit 1
fi
echo ""

# Test 4: Project summary files exist
echo "Test 4: Checking project summary files..."
for file in \
    "formal-ontologies/project-summary.md" \
    "general-systems-theory/gst-overview/project-summary.md" \
    "general-systems-theory/nested-systems/project-summary.md"
do
    if [ -f "$file" ]; then
        echo "✓ $file exists"
    else
        echo "✗ $file not found"
        exit 1
    fi
done
echo ""

# Test 5: Knowledge database structure
echo "Test 5: Checking knowledge-database structure..."
if [ -d "knowledge-database" ]; then
    echo "✓ knowledge-database/ exists"
else
    echo "✗ knowledge-database/ not found"
    exit 1
fi

if [ -f "knowledge-database/README.md" ]; then
    echo "✓ knowledge-database/README.md exists"
else
    echo "✗ knowledge-database/README.md not found"
    exit 1
fi

if [ -d "knowledge-database/concepts" ]; then
    echo "✓ knowledge-database/concepts/ exists"
else
    echo "✗ knowledge-database/concepts/ not found"
    exit 1
fi
echo ""

# Test 6: Docker files structure
echo "Test 6: Checking Docker setup..."
if [ -f "tools/zotero-mcp/docker-compose.yml" ]; then
    echo "✓ docker-compose.yml exists"
else
    echo "✗ docker-compose.yml not found"
    exit 1
fi

if [ -f "tools/zotero-mcp/zotero-mcp-server/Dockerfile" ]; then
    echo "✓ zotero-mcp-server Dockerfile exists"
else
    echo "✗ zotero-mcp-server Dockerfile not found"
    exit 1
fi

if [ -f "tools/zotero-mcp/web-ui/Dockerfile" ]; then
    echo "✓ web-ui Dockerfile exists"
else
    echo "✗ web-ui Dockerfile not found"
    exit 1
fi
echo ""

# Test 7: Quartz site structure
echo "Test 7: Checking Quartz site..."
if [ -d "quartz-site" ]; then
    echo "✓ quartz-site/ exists"
else
    echo "✗ quartz-site/ not found"
    exit 1
fi

if [ -f "quartz-site/quartz.config.ts" ]; then
    echo "✓ quartz.config.ts exists"
else
    echo "✗ quartz.config.ts not found"
    exit 1
fi

if [ -f "quartz-site/quartz.layout.ts" ]; then
    echo "✓ quartz.layout.ts exists"
else
    echo "✗ quartz.layout.ts not found"
    exit 1
fi
echo ""

# Test 8: GitHub Actions workflows
echo "Test 8: Checking GitHub Actions workflows..."
if [ -f ".github/workflows/sync-zotero.yml" ]; then
    echo "✓ sync-zotero.yml exists"
else
    echo "✗ sync-zotero.yml not found"
    exit 1
fi

if [ -f ".github/workflows/build-quartz.yml" ]; then
    echo "✓ build-quartz.yml exists"
else
    echo "✗ build-quartz.yml not found"
    exit 1
fi
echo ""

# Test 9: Documentation
echo "Test 9: Checking documentation..."
if [ -f "docs/ZOTERO_INTEGRATION.md" ]; then
    echo "✓ ZOTERO_INTEGRATION.md exists"
else
    echo "✗ ZOTERO_INTEGRATION.md not found"
    exit 1
fi

if [ -f "scripts/zotero-integration/README.md" ]; then
    echo "✓ scripts README exists"
else
    echo "✗ scripts README not found"
    exit 1
fi
echo ""

# Test 10: Flask app syntax
echo "Test 10: Checking Flask app syntax..."
python3 -m py_compile tools/zotero-mcp/web-ui/app.py
echo "✓ Flask app syntax valid"
echo ""

echo "================================"
echo "All tests passed! ✓"
echo "================================"
