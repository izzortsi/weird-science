# Semantic Analysis Task: Knowledge Base Generation from LaTeX and Zotero

## Objective
Analyze the provided LaTeX sources and Zotero library to generate a hierarchical, atomic knowledge base with Quartz-compatible Markdown files.

## Input Data Summary
- **Projects:** 3
- **LaTeX Files:** 17
- **Citations:** 16
- **Zotero Items:** 0
- **Bibliography Entries:** 110

## Projects in Repository

### formal-ontologies
- LaTeX files: 8
- Citations: 6

### nested-systems
- LaTeX files: 6
- Citations: 7

### gst-overview
- LaTeX files: 3
- Citations: 4


## Task Requirements

### Phase 1: Extract Core Concept Set (Γ)
1. Read all LaTeX files in the repository
2. Extract topics, definitions, concepts, and references
3. Identify the core concept set Γ from explicit definitions and discussions
4. For each concept, note:
   - Name and synonyms
   - Definitions found in LaTeX sources
   - References/citations associated with the concept
   - Related concepts mentioned together

### Phase 2: Expand to Zotero Concepts (Γ⁺)
1. Review Zotero library items (titles, tags, abstracts)
2. Identify concepts referenced/cited in LaTeX that appear in Zotero
3. Expand Γ to Γ⁺ by including related concepts from Zotero that:
   - Are cited in the LaTeX sources
   - Share tags with concepts in Γ
   - Are semantically related based on titles and abstracts
   - Form logical connections in the knowledge graph

### Phase 3: Hierarchical Classification
1. Organize Γ⁺ into a hierarchical taxonomy
2. Identify top-level domains (e.g., "systems-theory", "formal-ontologies", "mathematics")
3. Create 2-4 levels of hierarchy where appropriate
4. Group related concepts together

### Phase 4: Generate Atomic Markdown Files
For each concept in Γ⁺, create a Markdown file with:

**Filename:** `knowledge-database/concepts/{hierarchy-path}/{concept-name}.md`

**Structure:**
```markdown
---
title: [Concept Name]
tags: [tag1, tag2, ...]
hierarchy: [parent1, parent2, ...]
related: [related-concept-1, related-concept-2, ...]
zotero_keys: [KEY1, KEY2, ...]
---

# [Concept Name]

## Definition

[Primary definition, if available from LaTeX sources]

### Alternative Definitions

[Additional definitions if found in multiple sources]

## Examples

[Examples from LaTeX sources or Zotero abstracts]

## Key References

### [Reference 1 Title]
*Authors (Year)*
[Zotero Link](https://www.zotero.org/groups/6182921/items/KEY)
[DOI Link if available]

[Abstract or key points]

## Related Concepts

- [[related-concept-1]]
- [[related-concept-2]]

## Bibliography Keys

- bibkey1
- bibkey2
```

### Phase 5: Generate Summary Files
At each level of the hierarchy, create an `index.md` file that:
- Lists all concepts at that level
- Provides brief descriptions
- Links to child concepts and articles

## Output Format

Provide the complete knowledge base structure as:

1. **Directory tree** showing the full hierarchy
2. **Markdown files** for each concept (can be provided as file paths + content)
3. **Metadata summary** listing all concepts with their hierarchy paths

## Important Guidelines

- Use Quartz-compatible Markdown syntax
- Use [[wikilinks]] for internal concept references
- Include granular Zotero links: https://www.zotero.org/groups/6182921/items/[KEY]
- Ensure all cross-references are bidirectional where appropriate
- Maintain consistency in formatting across all files
- Use semantic, lowercase-hyphenated filenames

## Available Data

The following data is available for your analysis:

### Sample Citations
- Walloth2016
- Mesarovic1975
- Takahashi1995
- Bertalanffy1968
- Schaffer2008
- Lin2002
- Simon2012
- Poizat2000
- Lin1987
- Backlund2000
- Lin1999
- Backlund2000a
- Carnap1956
- Mesarovic1972
- Mesarovic1976
- Mesarovic1970

### Sample Zotero Items


### Full Data Files Available
- Complete LaTeX sources in: 17 files
- Zotero manifest: 0 items
- Bibliography: 110 entries

Please proceed with the semantic analysis and knowledge base generation.
