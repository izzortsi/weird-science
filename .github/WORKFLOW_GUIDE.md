# PDF Build Workflow Guide

This document explains how the automated PDF build workflow works in this repository.

## Overview

The workflow automatically builds LaTeX documents into PDFs whenever changes are made to `.tex` files in the topic folders (`general-systems-theory/` or `formal-ontologies/`).

## Workflow Triggers

The workflow runs on:
- **Push to main branch**: Builds PDFs and updates the "latest" release
- **Pull requests to main**: Builds PDFs and creates/updates a PR-specific release
- **Manual trigger**: Can be run manually via GitHub Actions UI

## What Gets Built

The workflow automatically discovers all `main.tex` files in:
- `general-systems-theory/*/main.tex`
- `formal-ontologies/*/main.tex`

Each discovered document is built independently.

## Output Locations

### For Pull Requests
- **Release Tag**: `pr-<number>` (e.g., `pr-42`)
- **Release Name**: "PR #<number> - Built PDFs"
- **Artifacts**: Available as GitHub Actions artifacts (30-day retention)
- **PR Comments**: Automatic comment with download links to the release

### For Main Branch
- **Release Tag**: `latest`
- **Release Name**: "Latest Built PDFs"
- **Updates**: Release is updated with each push to main

## PDF Naming

PDFs are named after their document folder:
- `general-systems-theory/document-1/` → `document-1.pdf`
- `general-systems-theory/document-2/` → `document-2.pdf`

## Adding New Documents

To add a new document:

1. Create a new folder in a topic directory:
   ```
   general-systems-theory/document-3/
   ```

2. Add the required structure:
   ```
   document-3/
   ├── main.tex
   ├── sections/
   │   ├── section1.tex
   │   └── section2.tex
   ├── references/
   │   └── bibliography.bib
   └── README.md
   ```

3. The workflow will automatically discover and build it!

## Troubleshooting

### PDFs Not Building
- Check that `main.tex` exists in the document folder
- Verify LaTeX syntax is correct
- Check workflow logs in GitHub Actions

### Download Links Not Working
- Ensure the release has been created (check Releases page)
- Verify the PDF naming matches the folder name
- Wait for the workflow to complete after pushing changes

## Local Building

To build PDFs locally:

```bash
cd general-systems-theory/document-1/
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

## Workflow Configuration

The workflow is defined in `.github/workflows/build-pdf.yml` and uses:
- `actions/checkout@v4` - Checkout repository
- `actions/upload-artifact@v4` - Upload PDF artifacts
- `ncipollo/release-action@v1` - Create/update releases
- `actions/github-script@v7` - Post PR comments

## Permissions

The workflow requires:
- `contents: write` - To create releases
- `pull-requests: write` - To comment on PRs
