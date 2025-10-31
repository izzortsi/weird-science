# Claude Code Integration Instructions

## Overview
This knowledge base generator has prepared structured data for semantic analysis by Claude Code. The analysis will extract concepts from LaTeX sources and the Zotero library to create a hierarchical, atomic knowledge base.

## Files Generated
1. `analysis-data.json` - Structured data about projects, citations, and Zotero items
2. `claude-prompt.md` - Detailed prompt for Claude Code
3. This instruction file

## Workflow for Claude Code

### Input
Claude Code should:
1. Read all `.tex` files in the repository
2. Read all `.bib` files for bibliography context
3. Access the Zotero manifest at `zotero-cache/zotero-manifest.json`
4. Review the analysis data in `analysis-data.json`

### Processing
Claude Code will:
1. Extract concepts from LaTeX sources (Γ)
2. Expand to related Zotero concepts (Γ⁺)
3. Create hierarchical classification
4. Generate atomic Markdown files for each concept
5. Create index/summary files for navigation

### Output Structure
```
knowledge-database/
├── README.md (updated index)
├── concepts/
│   ├── systems-theory/
│   │   ├── index.md
│   │   ├── general-systems.md
│   │   ├── complexity/
│   │   │   ├── index.md
│   │   │   ├── emergence.md
│   │   │   └── self-organization.md
│   │   └── hierarchy.md
│   ├── formal-ontologies/
│   │   ├── index.md
│   │   ├── conceptualization.md
│   │   └── ontological-commitment.md
│   └── mathematics/
│       ├── index.md
│       └── set-theory.md
└── metadata/
    └── concept-graph.json (optional: graph structure)
```

## Markdown File Format

Each concept file must use this structure:

```markdown
---
title: Concept Name
tags: [tag1, tag2]
hierarchy: [parent1, parent2]
related: [concept1, concept2]
zotero_keys: [KEY1, KEY2]
---

# Concept Name

## Definition
[Primary definition from LaTeX]

### Alternative Definitions
[If multiple definitions exist]

## Examples
[From LaTeX or Zotero abstracts]

## Key References

### Reference Title
*Author et al. (Year)*
[View in Zotero](https://www.zotero.org/groups/6182921/items/KEY)
DOI: [10.xxxx/yyyy](https://doi.org/10.xxxx/yyyy)

[Abstract or summary]

## Related Concepts
- [[related-concept-1]]
- [[related-concept-2]]

## Bibliography Keys
- bibkey1
- bibkey2
```

## Integration Steps

### For Claude Code:
1. Accept the prompt from `claude-prompt.md`
2. Perform semantic analysis as specified
3. Generate complete knowledge base structure
4. Create all Markdown files in `knowledge-database/concepts/`
5. Update `knowledge-database/README.md` with new structure

### For GitHub Copilot (if handoff needed):
1. Receive Claude Code output (directory structure + file contents)
2. Create new branch for knowledge base update
3. Write all generated files to repository
4. Commit changes with descriptive message
5. Create PR with summary of changes

## Quality Checks
- All Markdown files use Quartz-compatible syntax
- All [[wikilinks]] reference valid concept files
- All Zotero links use correct group ID (6182921)
- Hierarchy is consistent across metadata and directory structure
- No orphaned concepts (all should be reachable from index)
- Bidirectional references where appropriate

## Notes
- This is a non-interactive, automated workflow
- Claude Code has the context and tools to complete the full analysis
- The output should be production-ready Markdown for Quartz
- Focus on atomic, well-defined concepts over comprehensive coverage
