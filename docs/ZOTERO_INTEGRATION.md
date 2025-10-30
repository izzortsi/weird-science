# Zotero Integration for weird-science

This document describes the Zotero integration system for the weird-science repository.

## Overview

The integration connects the weird-science repository with a Zotero group library (ID: 6182921) to:

1. **Generate project summaries** - Create markdown literature summaries for each project
2. **Build knowledge database** - Generate atomic concept articles from Zotero items
3. **Deploy documentation site** - Build and host a Quartz-based knowledge base
4. **Enable interactive exploration** - Provide a local Docker-based chat UI for querying

## Components

### 1. Python Exporter Script

**Location:** `scripts/zotero-integration/zotero_exporter.py`

The main script that:
- Scans the repository for projects (folders with README.md + main.tex)
- Extracts citation keys from .tex files
- Parses .bib files to map bibkeys to DOIs/titles
- Fetches items from Zotero API
- Matches citations using DOI, title, or bibkey heuristics
- Generates `project-summary.md` files
- Creates knowledge-database/ with concept articles

**Usage:**
```bash
# Basic usage (uses defaults)
python scripts/zotero-integration/zotero_exporter.py

# With API key and custom group
export ZOTERO_API_KEY=your_key_here
export ZOTERO_GROUP_ID=6182921
python scripts/zotero-integration/zotero_exporter.py

# Dry run mode (no file generation)
python scripts/zotero-integration/zotero_exporter.py --dry-run
```

**Environment Variables:**
- `ZOTERO_API_KEY` - Optional API key for private library access
- `ZOTERO_GROUP_ID` - Group library ID (default: 6182921)

### 2. Project Summaries

**Location:** Each project folder gets a `project-summary.md`

Example locations:
- `formal-ontologies/project-summary.md`
- `general-systems-theory/gst-overview/project-summary.md`
- `general-systems-theory/nested-systems/project-summary.md`

**Format:**
```markdown
---
title: Project Title
project: folder-name
date: 2025-10-30
tags: [zotero, literature-review, project-name]
zotero_keys: [KEY1, KEY2, ...]
matched_bibkeys: [bibkey1, bibkey2, ...]
---

# Project Title - Literature Summary

## References

### bibkey1
**Paper Title**
*Authors (Year)*
[View in Zotero Library](https://www.zotero.org/groups/6182921/items/KEY)
DOI: [10.xxxx/yyyy](https://doi.org/10.xxxx/yyyy)
```

### 3. Knowledge Database

**Location:** `knowledge-database/`

Structure:
```
knowledge-database/
├── README.md                    # Index of all concepts
└── concepts/
    ├── systems-theory.md        # Concept articles organized by tags
    ├── ontology.md
    └── ...
```

Each concept file contains:
- Tag/topic name
- List of related Zotero items
- Titles, authors, abstracts
- Links to Zotero and DOIs

### 4. Quartz Site

**Location:** `quartz-site/`

A static site builder configuration for publishing the knowledge base.

**Setup:**
```bash
cd quartz-site
npm install -g quartz-v4
quartz create
quartz build
quartz serve  # Preview locally
```

**Configuration:**
- `quartz.config.ts` - Site configuration
- `quartz.layout.ts` - Layout and components
- Content synced from knowledge-database/

**Deployment:**
Automated via GitHub Actions to GitHub Pages when:
- knowledge-database/ is updated
- project-summary.md files are modified
- Quartz configuration changes

### 5. Docker Tools

**Location:** `tools/zotero-mcp/`

Provides local interactive exploration via:
- **zotero-mcp-server** - Node.js server wrapping Zotero API
- **web-ui** - Flask-based chat interface

**Quick Start:**
```bash
cd tools/zotero-mcp

# Set credentials
export ZOTERO_API_KEY=your_key
export ZOTERO_GROUP_ID=6182921

# Start services
docker-compose up -d

# Access web UI
open http://localhost:5000
```

**Services:**
- `zotero-mcp-server`: Port 3000 - REST API for Zotero
- `web-ui`: Port 5000 - Web interface for searching

**Web UI Features:**
- Search papers by title, author, keywords
- View abstracts and metadata
- Quick links to Zotero items and DOIs
- Tag-based browsing

## GitHub Actions Workflows

### 1. Sync Zotero Library

**File:** `.github/workflows/sync-zotero.yml`

**Trigger:**
- Daily at 2 AM UTC (scheduled)
- Manual dispatch

**Actions:**
1. Runs zotero_exporter.py
2. Commits updated project-summary.md files
3. Commits updated knowledge-database/
4. Pushes changes to repository

**Secrets/Variables Required:**
- `ZOTERO_API_KEY` (optional) - For private access
- `ZOTERO_GROUP_ID` (default: 6182921)

### 2. Build Quartz Site

**File:** `.github/workflows/build-quartz.yml`

**Trigger:**
- Push to dev branch (knowledge-database/ or project-summary.md changes)
- Pull requests
- Manual dispatch

**Actions:**
1. Copies knowledge-database/ to quartz-site/content/
2. Copies project summaries
3. Builds Quartz static site
4. Deploys to GitHub Pages (on dev push)

## Citation Matching Algorithm

The exporter matches bibliography entries to Zotero items using:

1. **DOI matching** (highest priority)
   - Exact match on DOI field
   - Case-insensitive

2. **Title matching** (fallback)
   - Exact title match (case-insensitive)
   - Fuzzy matching using Jaccard similarity (threshold: 0.8)
   - Common words comparison after removing stop words

3. **Future enhancements**
   - Author name matching
   - Year matching as tiebreaker
   - ISBN/ISSN matching for books

## Links

- **Zotero Group Library:** https://www.zotero.org/groups/6182921/
- **Repository:** https://github.com/izzortsi/weird-science
- **Quartz Documentation:** https://quartz.jzhao.xyz/

## License

This integration code is part of the weird-science repository and follows the same license.
