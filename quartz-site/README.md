# Quartz Site for weird-science

This directory contains the Quartz configuration and templates for building a static site from the weird-science knowledge base.

## Setup

1. Install Quartz v4:
```bash
npm install -g quartz-v4
```

2. Initialize Quartz (if not already done):
```bash
quartz create
```

3. Build the site:
```bash
quartz build
```

4. Preview locally:
```bash
quartz serve
```

## Directory Structure

```
quartz-site/
├── content/           # Content will be symlinked/copied from knowledge-database/
├── quartz.config.ts   # Quartz configuration
├── quartz.layout.ts   # Layout configuration
└── README.md         # This file
```

## Configuration

The Quartz configuration is customized for the weird-science repository:
- Site title: "weird-science Knowledge Base"
- Content sourced from knowledge-database/
- Integrated with Zotero references
- Custom theme matching the repository aesthetic

## GitHub Actions Integration

The site is automatically built and deployed via GitHub Actions whenever:
- New content is added to knowledge-database/
- Project summaries are updated
- The Zotero library is synchronized
