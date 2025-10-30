# Zotero Integration Scripts

This directory contains scripts and tools for integrating the weird-science repository with the Zotero group library.

## Main Script

**`zotero_exporter.py`** - The primary integration script that:
- Scans the repository for LaTeX projects
- Extracts citations from .tex files
- Parses .bib files
- Fetches items from Zotero API (group 6182921)
- Matches citations to Zotero items
- Generates project-summary.md files
- Creates knowledge-database/ with concept articles

## Usage

### Basic Usage

```bash
# Install dependencies
pip install -r requirements.txt

# Run with default settings
python zotero_exporter.py

# Run with API key for private access
export ZOTERO_API_KEY=your_key_here
python zotero_exporter.py
```

### Command Line Options

```bash
# Dry run (no file generation)
python zotero_exporter.py --dry-run

# Specify custom repository root
python zotero_exporter.py --repo-root /path/to/repo

# Use different Zotero group
python zotero_exporter.py --group-id 1234567

# Combine options
python zotero_exporter.py --group-id 1234567 --api-key YOUR_KEY --dry-run
```

### Environment Variables

- `ZOTERO_API_KEY` - API key for Zotero (optional for public groups)
- `ZOTERO_GROUP_ID` - Zotero group library ID (default: 6182921)

## What It Does

1. **Project Discovery**
   - Finds all directories with README.md and main.tex
   - Examples: formal-ontologies/, general-systems-theory/*/

2. **Citation Extraction**
   - Parses all .tex files for citation commands
   - Supports: \cite{}, \citep{}, \citet{}, \autocite{}, etc.

3. **Bibliography Parsing**
   - Reads all .bib files in each project
   - Extracts: keys, titles, DOIs, authors, years

4. **Zotero Integration**
   - Fetches all items from the Zotero group library
   - Matches citations using DOI or title similarity

5. **Output Generation**
   - Creates project-summary.md in each project folder
   - Builds knowledge-database/ with concept articles
   - Generates markdown with YAML frontmatter

## Output Files

### Project Summaries

Location: `{project}/project-summary.md`

Contains:
- YAML frontmatter with metadata
- List of matched references
- Links to Zotero library items
- DOI links (when available)
- Abstracts (when available)

### Knowledge Database

Location: `knowledge-database/`

Contains:
- README.md with index of all concepts
- concepts/*.md files organized by Zotero tags
- Atomic articles with cross-links

## See Also

- [Full Documentation](../../docs/ZOTERO_INTEGRATION.md)
- [Zotero Group Library](https://www.zotero.org/groups/6182921/)
- [Repository](https://github.com/izzortsi/weird-science)
