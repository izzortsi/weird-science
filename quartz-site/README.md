# Quartz Site for weird-science

This directory contains the Quartz configuration and templates for building a static site from the weird-science knowledge base.

## Overview

The Quartz site is automatically built and deployed via GitHub Actions. The workflow:
1. Dynamically initializes Quartz v4 by cloning the framework
2. Copies content from the knowledge-database
3. Builds the static site using `npx quartz build`
4. Deploys to GitHub Pages

## Workflow Details

### Build Process

The GitHub Actions workflow (`.github/workflows/build-quartz.yml`) handles the entire build and deployment:

1. **Initialize Quartz**: Clones the Quartz v4 framework if not already present
   - Uses a shallow clone for speed
   - Copies necessary framework files (quartz/, package.json, etc.)
   - Installs npm dependencies

2. **Setup Content**: Copies markdown files from the repository
   - Copies from `knowledge-database/` directory
   - Collects `project-summary.md` files from all projects
   - Creates an index page if needed

3. **Build**: Runs `npx quartz build` to generate the static site
   - Outputs to `public/` directory
   - Uses configuration from `quartz.config.ts` and `quartz.layout.ts`

4. **Deploy**: Uploads and deploys to GitHub Pages (on push to dev branch)

### Configuration Files

The following files configure the Quartz site appearance and behavior:

- `quartz.config.ts` - Main Quartz configuration
  - Site title: "weird-science Knowledge Base"
  - Base URL: izzortsi.github.io/weird-science
  - Plugin configuration
  - Theme and styling

- `quartz.layout.ts` - Page layout configuration
  - Header, footer, and sidebar components
  - Links to GitHub and Zotero library

### Local Development

To build and preview the site locally:

1. Install dependencies:
```bash
cd quartz-site
npm install
```

2. Setup content:
```bash
mkdir -p content
# Copy your markdown files to content/
```

3. Build the site:
```bash
npx quartz build
```

4. Preview locally:
```bash
npx quartz serve
```

## Requirements

- Node.js >= 22 (required by Quartz v4.5.2)
- npm >= 10.9.2

## Directory Structure

```
quartz-site/
├── README.md           # This file
├── quartz.config.ts    # Quartz configuration
├── quartz.layout.ts    # Layout configuration
├── content/            # Content (generated, gitignored)
├── quartz/             # Quartz framework (generated, gitignored)
├── public/             # Build output (generated, gitignored)
└── node_modules/       # Dependencies (generated, gitignored)
```

Note: Most directories are dynamically generated during the build process and are excluded from git.

## GitHub Actions Integration

The site is automatically built and deployed via GitHub Actions whenever:
- New content is added to knowledge-database/
- Project summaries are updated
- The Zotero library is synchronized
- Changes are pushed to the workflow file itself

The workflow can also be triggered manually via workflow_dispatch.

## Troubleshooting

### Build fails with "afterBody is not iterable"

This error occurs when the layout configuration is incompatible with the Quartz version. Ensure `quartz.layout.ts` includes the `afterBody` field in `sharedPageComponents`.

### Node version mismatch

Quartz v4.5.2 requires Node.js >= 22. The workflow is configured to use Node 22, but local builds may show warnings if using an older version.
