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

### gst-overview
- LaTeX files: 3
- Citations: 4

### nested-systems
- LaTeX files: 6
- Citations: 7

### formal-ontologies
- LaTeX files: 8
- Citations: 6


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
**ALREADY COMPLETED:** The system has already performed Γ⁺ → Γ⁺⁺ expansion and provided results in `concept_expansions`.

**Available Data:**
- `concept_expansions` contains pre-processed expansions for each concept
- For each concept, includes:
  - `additional_papers`: Papers found in Zotero that discuss the concept but weren't cited
  - `alternative_definitions`: Different definitions/perspectives from uncited papers
  - `extended_treatments`: Extended discussions, applications, or critiques
  - `related_concepts`: Other concepts found in the same papers
  - `cross_references`: Papers that discuss multiple concepts together

**Your Task:**
1. **Review the provided `concept_expansions` data** for each concept
2. **Integrate additional papers** into the concept articles:
   - Add "Additional References" sections with the newly discovered papers
   - Include alternative definitions alongside primary definitions
   - Add extended treatments as separate subsections
3. **Build comprehensive cross-references**:
   - Use the `cross_references` data to link concepts that appear together in papers
   - Add "See Also" sections with related concepts
   - Create bidirectional wikilinks between related concepts
4. **Create richer concept articles** that show multiple perspectives and treatments

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

[Additional definitions from concept_expansions data]

## Extended Treatments

[Extended discussions, applications, or critiques from Γ⁺⁺ expansion]

## Examples

[Examples from LaTeX sources or Zotero abstracts]

## Key References

### Primary References
[Cited papers that introduced the concept]

### Additional References (Γ⁺⁺ Expansion)
[Uncited papers found through Zotero cross-referencing]

#### [Additional Paper Title]
*Authors (Year)*
[Zotero Link](https://www.zotero.org/groups/6182921/items/KEY)
[Relevance: X.X] [Context: title/abstract/tags]

[Key points or alternative perspective]

## See Also

[Related concepts found through cross-referencing]
- [[related-concept-1]] (appears together in: Paper1, Paper2)
- [[related-concept-2]] (appears together in: Paper3)

## Related Concepts

[Original related concepts from LaTeX analysis]
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
- Carnap1956
- Mesarovic1970
- Bertalanffy1968
- Lin2002
- Backlund2000a
- Lin1987
- Takahashi1995
- Poizat2000
- Backlund2000
- Walloth2016
- Mesarovic1972
- Schaffer2008
- Lin1999
- Mesarovic1976
- Mesarovic1975
- Simon2012

### Sample Zotero Items


### Full Data Files Available
- Complete LaTeX sources in: 17 files
- Zotero manifest: 0 items
- Bibliography: 110 entries
- Cited papers: 16 papers fetched and processed
- Concept expansions: Γ⁺ → Γ⁺⁺ cross-referencing results (if available)

**Γ⁺⁺ Expansion Data (concept_expansions):**
For each concept that was expanded, you'll find:
- Additional papers from the 93-item Zotero library
- Alternative definitions and perspectives
- Extended treatments and applications
- Cross-references to related concepts

Please proceed with the semantic analysis and knowledge base generation.
```
