# Knowledge Database

This directory contains atomic concept articles extracted from the Zotero group library.

## Concepts by Tag

- [formal-ontology](concepts/formal-ontology.md) (example)
- [systems-theory](concepts/systems-theory.md) (example)

*Additional content will be populated when the Zotero exporter runs with access to the library.*

To generate or update this content:

```bash
# Run the exporter script
python scripts/zotero-integration/zotero_exporter.py

# Or use the GitHub Actions workflow (runs daily)
# See: .github/workflows/sync-zotero.yml
```

## Structure

Once populated, this directory will contain:

- **concepts/** - Atomic concept articles organized by Zotero tags
- Each concept file groups related papers from the Zotero library
- Articles include titles, authors, abstracts, and links to Zotero items

## Usage

The knowledge database serves multiple purposes:

1. **Quick Reference** - Browse concepts and find related papers
2. **Literature Discovery** - Explore topics through tagged items
3. **Integration with Projects** - Links between project citations and concepts
4. **Quartz Site** - Content source for the static knowledge base site

## Zotero Group Library

All content is sourced from:
- **Group ID:** 6182921
- **URL:** https://www.zotero.org/groups/6182921/

## Automated Updates

This directory is automatically updated by the GitHub Actions workflow:
- **Schedule:** Daily at 2 AM UTC
- **Workflow:** `.github/workflows/sync-zotero.yml`
- **Manual Trigger:** Available via workflow dispatch

When updates occur:
- New tags create new concept files
- Existing concept files are updated with new items
- The index (this file) is regenerated
