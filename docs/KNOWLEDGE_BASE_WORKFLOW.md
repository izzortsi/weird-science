# Knowledge Base Generation Workflow

## Overview

This automated workflow generates a hierarchical, atomic knowledge base from the repository's LaTeX sources and the Zotero group library. The knowledge base consists of Quartz-compatible Markdown files organized by concept hierarchy.

## Workflow Triggers

The knowledge base generation workflow can be triggered in two ways:

### 1. Manual Trigger
- Navigate to Actions → Knowledge Base Generation
- Click "Run workflow"
- Optionally enable "Force full regeneration" to rebuild everything from scratch

### 2. Automatic Trigger
- Merges to the `/dev` branch that modify `.tex` or `.bib` files
- Automatically runs after LaTeX source changes are merged

## Components

### 1. Zotero Sync Script (`zotero_sync.py`)

**Purpose:** Fetches Zotero library metadata and caches PDF attachments locally.

**Features:**
- Fetches all items from Zotero group library (ID: 6182921)
- Downloads PDF attachments to `/zotero-cache/`
- Generates `zotero-manifest.json` with complete metadata:
  - Item metadata (title, authors, DOI, tags, etc.)
  - Attachment information
  - Cached file paths
  - Zotero URLs

**Usage:**
```bash
# Basic usage (public access)
python scripts/zotero-integration/zotero_sync.py

# With API key for private/enhanced access
export ZOTERO_API_KEY=your_key_here
python scripts/zotero-integration/zotero_sync.py \
  --group-id 6182921 \
  --cache-dir zotero-cache \
  --generate-manifest

# Skip PDF downloads (metadata only)
python scripts/zotero-integration/zotero_sync.py --download-pdfs=false
```

**Output:**
- `zotero-cache/zotero-manifest.json` - Complete library manifest
- `zotero-cache/{item-key}/*.pdf` - Cached PDF attachments organized by item

### 2. Knowledge Base Generator (`knowledge_base_generator.py`)

**Purpose:** Orchestrates semantic analysis to generate hierarchical knowledge base.

**Process:**

#### Phase 1: Data Preparation
1. Scans repository for all `.tex` and `.bib` files
2. Extracts citations from LaTeX sources
3. Loads Zotero manifest
4. Prepares structured analysis data

#### Phase 2: Analysis Setup
1. Generates comprehensive prompt for semantic analysis
2. Creates `analysis-data.json` with all extracted information
3. Produces `claude-prompt.md` with detailed instructions

#### Phase 3: Semantic Analysis (via Claude Code)
The generated prompt guides Claude Code to:
1. **Extract Core Concepts (Γ):** Topics, definitions, concepts from LaTeX
2. **Expand to Zotero (Γ⁺):** Include related concepts from library
3. **Hierarchical Classification:** Organize concepts into taxonomy
4. **Generate Atomic Markdown:** Create individual files per concept
5. **Cross-reference:** Build wiki-style links between concepts

#### Phase 4: Output Generation
Claude Code produces:
- Hierarchical directory structure
- Atomic Markdown files for each concept
- Index/summary files at each level
- Metadata with concept relationships

**Usage:**
```bash
# Generate analysis data and prompts
python scripts/zotero-integration/knowledge_base_generator.py

# With custom manifest path
python scripts/zotero-integration/knowledge_base_generator.py \
  --manifest zotero-cache/zotero-manifest.json \
  --output-dir knowledge-database

# Force regeneration
python scripts/zotero-integration/knowledge_base_generator.py --force
```

**Output:**
- `knowledge-database/analysis-data.json` - Structured analysis input
- `knowledge-database/claude-prompt.md` - Prompt for semantic analysis
- `knowledge-database/CLAUDE_INTEGRATION.md` - Integration instructions

## Knowledge Base Structure

The generated knowledge base follows this structure:

```
knowledge-database/
├── README.md                          # Index of all concepts
├── analysis-data.json                 # Analysis metadata
├── claude-prompt.md                   # Generated prompt
├── CLAUDE_INTEGRATION.md              # Integration instructions
└── concepts/
    ├── systems-theory/
    │   ├── index.md                   # Systems theory overview
    │   ├── general-systems.md         # Atomic concept article
    │   ├── complexity/
    │   │   ├── index.md              # Complexity sub-domain
    │   │   ├── emergence.md          # Atomic concept
    │   │   └── self-organization.md  # Atomic concept
    │   └── hierarchy.md              # Atomic concept
    ├── formal-ontologies/
    │   ├── index.md
    │   ├── conceptualization.md
    │   └── ontological-commitment.md
    └── mathematics/
        ├── index.md
        └── set-theory.md
```

## Atomic Markdown Format

Each concept article follows this Quartz-compatible format:

```markdown
---
title: Emergence
tags: [systems-theory, complexity, philosophy]
hierarchy: [systems-theory, complexity]
related: [self-organization, downward-causation]
zotero_keys: [ABCD1234, EFGH5678]
---

# Emergence

## Definition

Emergence refers to properties or patterns that arise from the interaction 
of system components but are not reducible to those components individually.

### Alternative Definitions

[Additional definitions from different sources]

## Examples

1. **Consciousness:** Often cited as emergent from neural activity
2. **Flocking behavior:** Emerges from simple individual bird rules

## Key References

### Emergence in Complex Systems
*Bar-Yam, Y. (1997)*
[View in Zotero](https://www.zotero.org/groups/6182921/items/ABCD1234)
DOI: [10.1007/978-3-642-60363-8](https://doi.org/10.1007/978-3-642-60363-8)

Discusses hierarchical emergence and inter-level relationships in complex 
adaptive systems.

## Related Concepts

- [[self-organization]]
- [[downward-causation]]
- [[holism]]
- [[systems-theory/hierarchy]]

## Bibliography Keys

- bar-yam1997
- holland1998emergence
```

## Concept Sets

### Core Concept Set (Γ)
Concepts explicitly defined or discussed in LaTeX sources:
- Extracted from document text
- Identified through definitions, discussions
- Linked to specific citations in the papers

### Expanded Concept Set (Γ⁺)
Γ plus related concepts from Zotero:
- Items cited in LaTeX sources
- Items sharing tags with Γ concepts
- Semantically related items (via titles/abstracts)
- Forms complete knowledge graph

## Semantic Analysis Guidelines

The semantic analysis (performed by Claude Code) follows these principles:

### 1. Concept Extraction
- Identify explicit definitions in LaTeX
- Extract implicit concepts from context
- Note synonyms and alternative terminology
- Track citations associated with each concept

### 2. Hierarchy Building
- 2-4 levels deep where appropriate
- Top-level domains: broad fields (e.g., systems-theory)
- Mid-level: sub-domains (e.g., complexity)
- Leaf-level: specific concepts (e.g., emergence)

### 3. Cross-Referencing
- Use [[wikilinks]] for internal references
- Ensure bidirectional links where logical
- Link to Zotero items: `https://www.zotero.org/groups/6182921/items/{KEY}`
- Include DOI links where available

### 4. Content Quality
- Prefer multiple short definitions over single long one
- Include concrete examples
- Extract relevant abstract snippets
- Maintain consistent formatting

## Claude Code Integration

### Input to Claude Code
1. Access to repository files (`.tex`, `.bib`)
2. Zotero manifest (`zotero-cache/zotero-manifest.json`)
3. Analysis data (`knowledge-database/analysis-data.json`)
4. Detailed prompt (`knowledge-database/claude-prompt.md`)

### Expected Output from Claude Code
1. Complete directory structure in `knowledge-database/concepts/`
2. All Markdown files for concepts
3. Index files for navigation
4. Updated `knowledge-database/README.md`

### Handoff Process
If Claude Code cannot directly commit:
1. Claude generates all files and provides structure
2. Copilot receives the output
3. Copilot creates/updates files in repository
4. Commits are made via normal workflow
5. Changes trigger Quartz site rebuild

## Running the Complete Workflow

### Prerequisites
```bash
# Install dependencies
pip install -r scripts/zotero-integration/requirements.txt

# Set Zotero credentials (optional, for enhanced access)
export ZOTERO_API_KEY=your_api_key
export ZOTERO_GROUP_ID=6182921
```

### Full Manual Run
```bash
# Step 1: Sync Zotero library and cache PDFs
python scripts/zotero-integration/zotero_sync.py \
  --cache-dir zotero-cache \
  --generate-manifest

# Step 2: Generate knowledge base structure
python scripts/zotero-integration/knowledge_base_generator.py \
  --manifest zotero-cache/zotero-manifest.json \
  --output-dir knowledge-database

# Step 3: Review generated prompts and data
cat knowledge-database/claude-prompt.md
cat knowledge-database/analysis-data.json

# Step 4: Claude Code performs semantic analysis
# (See CLAUDE_INTEGRATION.md for details)

# Step 5: Commit changes
git add knowledge-database/ zotero-cache/zotero-manifest.json
git commit -m "Update knowledge base from LaTeX and Zotero"
git push
```

### Automated Run (GitHub Actions)
The workflow runs automatically on:
- Manual trigger via Actions tab
- Merges to `dev` with `.tex` file changes

The workflow:
1. Checks out repository
2. Installs Python dependencies
3. Runs `zotero_sync.py`
4. Runs `knowledge_base_generator.py`
5. Commits and pushes changes if any
6. Uploads manifest as artifact

## Configuration

### Environment Variables
- `ZOTERO_API_KEY` - API key for Zotero (optional)
- `ZOTERO_GROUP_ID` - Group library ID (default: 6182921)

### GitHub Secrets
Set in repository settings → Secrets and variables → Actions:
- `ZOTERO_API_KEY` (optional, recommended for reliability)

### GitHub Variables
- `ZOTERO_GROUP_ID` (optional, defaults to 6182921)

## Troubleshooting

### Issue: Manifest not generated
**Solution:** Check Zotero API connectivity. Try with API key for authenticated access.

### Issue: No concepts extracted
**Solution:** Ensure `.tex` files exist and contain citations. Check analysis-data.json for input data.

### Issue: PDFs not downloading
**Solution:** PDFs may require API key for access. Some items may not have attachments.

### Issue: Workflow not triggering
**Solution:** 
- Check `.tex` or `.bib` files were modified in the commit
- Ensure merge is to `dev` branch
- Check workflow permissions

## Integration with Quartz

After knowledge base generation:
1. Files in `knowledge-database/` are ready for Quartz
2. The `build-quartz.yml` workflow builds the static site
3. Site deploys to GitHub Pages
4. Browse at: `https://{username}.github.io/{repo}/`

## Next Steps

1. **Review Output:** Check generated files in `knowledge-database/`
2. **Refine Hierarchy:** Adjust structure if needed
3. **Add Cross-links:** Enhance connections between concepts
4. **Enrich Content:** Add examples, clarifications
5. **Keep Updated:** Workflow runs automatically on LaTeX changes

## References

- Zotero API Documentation: https://www.zotero.org/support/dev/web_api/v3/start
- Quartz Documentation: https://quartz.jzhao.xyz/
- Group Library: https://www.zotero.org/groups/6182921/
