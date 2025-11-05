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

### Phase 2: Expand to Γ⁺ via Cited Papers
1. **Locate cited papers** in the `cited_papers` section of `analysis-data.json`
2. **Analyze paper content** for each citation found in LaTeX sources:
   - Read the title, abstract, and TLDR (if available)
   - Identify core concepts that the paper introduces or defines
   - Extract key technical terms and theoretical constructs
   - Note concepts that appear repeatedly or are central to the paper's contribution
3. **Extract concepts** from cited papers that should be added to Γ⁺:
   - Concepts that are central to highly-cited or influential papers
   - Concepts that appear in ≥2 different cited papers
   - Concepts that are mentioned (even in passing) in the LaTeX sources
   - Foundational concepts that establish theoretical frameworks
4. **Expand Γ to Γ⁺** by including these paper-derived concepts

**Example:**
```
LaTeX cites: Simon2012 ("The Architecture of Complexity")
→ Read paper content from cited_papers['Simon2012']
→ Extract concepts: {complexity, near-decomposability, hierarchy,
                     stable-intermediate-forms, watchmaker-parable}
→ Add to Γ⁺ (even though not explicitly defined in LaTeX sources)
```

### Phase 3: Cross-reference with Zotero Library (Γ⁺ → Γ⁺⁺)
1. Review remaining Zotero library items (titles, tags, abstracts)
2. For each concept in Γ⁺, search for additional papers in Zotero that:
   - Have the concept in title or tags
   - Are in the same collection as cited papers
   - Provide alternative definitions or perspectives
3. Extract additional definitions and treatments of concepts
4. Build cross-references between different treatments

### Phase 4: Hierarchical Classification
1. Organize Γ⁺⁺ into a hierarchical taxonomy
2. Identify top-level domains (e.g., "systems-theory", "formal-ontologies", "mathematics")
3. Create 2-4 levels of hierarchy where appropriate
4. Group related concepts together

### Phase 5: Generate Atomic Markdown Files
For each concept in Γ⁺⁺, create a Markdown file with:

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

### Phase 6: Generate Summary Files
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
- Mesarovic1975
- Carnap1956
- Lin1987
- Bertalanffy1968
- Backlund2000
- Mesarovic1976
- Takahashi1995
- Schaffer2008
- Mesarovic1972
- Poizat2000
- Mesarovic1970
- Lin2002
- Backlund2000a
- Simon2012
- Lin1999
- Walloth2016

### Sample Zotero Items


### Full Data Files Available
- Complete LaTeX sources in: 17 files
- Zotero manifest: 0 items
- Bibliography: 110 entries

Please proceed with the semantic analysis and knowledge base generation.
