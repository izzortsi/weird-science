# Proposal: Enhanced Knowledge Base Concept Expansion

## Problem Statement

Currently, the knowledge base generation only extracts concepts **explicitly defined** in LaTeX sources (Γ). This misses:

1. Concepts discussed in **cited papers** (e.g., "complexity" from Simon's "Architecture of Complexity")
2. Related concepts from the **broader Zotero library**
3. Semantic connections between concepts across the literature

## Proposed Solution: Three-Phase Expansion

### Phase 1: Extract Core Concepts from LaTeX (Γ)
**Current implementation:** ✅ Already working

- Parse all `.tex` files
- Extract explicit definitions, theorems, key terms
- Extract citations (`\cite{Key}`, `\citep{Key}`)
- Result: **Γ** = {concept₁, concept₂, ...}

### Phase 2: Expand via Cited Papers (Γ → Γ⁺)
**Status:** 🟡 Partially implemented (basic Zotero integration exists)

**Proposed enhancement:**

For each citation in Γ's source LaTeX:
1. Look up paper in Zotero library
2. **Fetch paper content** from Zotero library:
   - Metadata (title, authors, year)
   - Abstract (from metadata or PDF extraction)
   - Keywords/tags from Zotero
   - PDF attachments for text extraction
3. **Extract concepts** from paper using:
   - Title keywords and technical terms
   - Abstract analysis for key concepts
   - Zotero tags/keywords
   - Frequently mentioned technical terms in abstract
4. **Add to Γ⁺** if concept:
   - Appears in ≥2 cited papers, OR
   - Is central to a highly-cited paper (based on Zotero metadata), OR
   - Is explicitly referenced in LaTeX (even if not defined)

**Example:**
```
LaTeX cites: Simon1962 ("The Architecture of Complexity")
→ Fetch paper content
→ Extract concepts: {complexity, near-decomposability, hierarchy,
                     stable-intermediate-forms, watchmaker-parable}
→ Add to Γ⁺ (even though not explicitly defined in LaTeX)
```

### Phase 3: Expand via Zotero Library (Γ⁺ → Γ⁺⁺)
**Status:** ❌ Not implemented

**Proposed implementation:**

For each concept in Γ⁺:
1. Search Zotero library for related papers:
   - Papers with concept in title/tags
   - Papers citing papers that define the concept
   - Papers in same collection
2. Extract definitions/treatments of the concept
3. Build cross-references between different treatments

**Example:**
```
Γ⁺ contains: {complexity, near-decomposability}
→ Search Zotero for papers about "complexity"
→ Find: Bar-Yam (1997), Ladyman (2013), etc.
→ Extract their definitions of complexity
→ Add as alternative definitions/perspectives to the concept article
```

## Implementation Plan

### Step 1: Enhance Paper Fetching (Zotero-Only)

Enhance `scripts/zotero-integration/paper_fetcher.py`:

```python
class PaperFetcher:
    def __init__(self, group_id: str = "6182921"):
        """
        Initialize the paper fetcher for Zotero library access.

        Args:
            group_id: Zotero group ID
        """
        self.group_id = group_id

    def fetch_paper_content(self, bibkey: str, zotero_item: Dict) -> PaperContent:
        """Fetch paper content from Zotero library"""
        # Extract content from Zotero item metadata
        content = self._fetch_from_zotero(bibkey, zotero_item)

        # Try to extract abstract from PDF attachment if not in metadata
        if not content.abstract and content.full_text_available:
            pdf_abstract = self._extract_abstract_from_attachment(zotero_item)
            if pdf_abstract:
                content.abstract = pdf_abstract

        return content

    def extract_concepts_from_paper(self, content: PaperContent) -> List[str]:
        """Extract key concepts from paper content"""
        concepts = set()

        # Extract from title keywords
        title_concepts = self._extract_title_concepts(content.title)
        concepts.update(title_concepts)

        # Extract from abstract
        if content.abstract:
            abstract_concepts = self._extract_abstract_concepts(content.abstract)
            concepts.update(abstract_concepts)

        # Use keywords from Zotero tags directly
        concepts.update(content.keywords)

        return list(concepts)
```

### Step 2: Modify Knowledge Base Generator

Update `scripts/zotero-integration/knowledge_base_generator.py`:

```python
class KnowledgeBaseGenerator:
    def generate(self):
        # Phase 1: Extract Γ from LaTeX
        gamma = self._extract_concepts_from_latex()

        # Phase 2: Expand to Γ⁺ via cited papers
        gamma_plus = self._expand_via_citations(gamma)

        # Phase 3: Expand to Γ⁺⁺ via Zotero library
        gamma_plus_plus = self._expand_via_zotero_library(gamma_plus)

        # Generate atomic articles for all concepts
        self._generate_atomic_articles(gamma_plus_plus)

    def _expand_via_citations(self, gamma: Set[Concept]) -> Set[Concept]:
        """Expand concept set by reading cited papers"""
        gamma_plus = gamma.copy()

        for concept in gamma:
            for citation in concept.citations:
                # Fetch paper content
                paper = self.paper_fetcher.fetch_paper_content(citation)

                # Extract concepts from paper
                paper_concepts = self.paper_fetcher.extract_concepts_from_paper(paper)

                # Add concepts that meet inclusion criteria
                for pc in paper_concepts:
                    if self._should_include(pc, gamma, gamma_plus):
                        gamma_plus.add(pc)

        return gamma_plus

    def _should_include(self, concept: Concept, gamma: Set, gamma_plus: Set) -> bool:
        """Determine if concept should be included in Γ⁺"""
        # Include if mentioned in ≥2 cited papers
        if concept.citation_count >= 2:
            return True

        # Include if central to a highly-cited paper
        if concept.centrality_score > 0.7 and concept.paper_citations > 100:
            return True

        # Include if explicitly referenced in LaTeX (even if not defined)
        if concept.mentioned_in_latex:
            return True

        return False
```

### Step 3: Update Claude Prompt

Modify `knowledge-database/claude-prompt.md`:

```markdown
### Phase 2: Expand to Γ⁺ via Cited Papers

For each citation found in LaTeX sources:

1. **Locate the paper** in Zotero library
2. **Analyze paper content** (provided in `analysis-data.json` under `cited_papers`)
3. **Extract core concepts** that the paper introduces/defines:
   - Look at title keywords
   - Analyze abstract for key terms
   - Identify concepts in section headings
   - Note concepts that appear repeatedly
4. **Add to Γ⁺** if the concept:
   - Is central to the paper's contribution
   - Appears in multiple cited papers
   - Is mentioned (even in passing) in the LaTeX sources

**Example:**
LaTeX cites Simon's "Architecture of Complexity"
→ Extract from paper: {complexity, near-decomposability, hierarchy, stable-intermediate-forms}
→ Add to Γ⁺ even if not explicitly defined in LaTeX

### Phase 3: Cross-reference with Zotero Library

For each concept in Γ⁺:

1. **Search Zotero library** for papers addressing this concept
2. **Extract alternative definitions** and perspectives
3. **Build rich concept articles** with multiple viewpoints
4. **Establish cross-references** between related concepts
```

### Step 4: Zotero Library Integration

The system uses only the Zotero library for paper content. Ensure:
1. Papers are synced to Zotero with complete metadata
2. Abstracts are included in Zotero items or available in PDF attachments
3. Tags/keywords are properly set in Zotero
4. Citation keys match bibliography entries
5. PDF attachments are available for abstract extraction when needed

## Benefits

### Richer Knowledge Base
- Captures concepts from the literature, not just LaTeX sources
- Includes standard terminology even if not formally defined in your work
- Provides multiple perspectives on each concept

### Better Semantic Connections
- Links concepts across papers
- Shows evolution of ideas through citations
- Reveals relationships not explicit in LaTeX

### More Complete Coverage
- Concepts like "emergence", "complexity", "mereology" are included
- Standard GST concepts are properly represented
- Interdisciplinary connections are visible

## Example: Before vs After

### Current (Γ only)
From LaTeX files directly:
```
{system, subsystem, hierarchy, valued-relation,
 extensional-relational-structure, intensional-relational-structure,
 conceptualization, ontological-commitment, ...}
```
**Count:** ~15 concepts

### Proposed (Γ → Γ⁺ → Γ⁺⁺)

**From LaTeX (Γ):** 15 concepts

**From cited papers (Γ⁺):**
- Simon (1962): +{complexity, near-decomposability, stable-intermediate-forms, span-of-attention}
- Mesarovic (1975): +{goal-seeking-system, abstract-system, coordination}
- Backlund (2000): +{system-property, isolation, connectivity}
- Bertalanffy (1968): +{open-system, equifinality, isomorphism, wholeness}

**From Zotero library (Γ⁺⁺):**
- Papers on "complexity": +{emergence, self-organization, criticality}
- Papers on "hierarchy": +{heterarchy, holarchy, nestedness}
- Papers on "ontology": +{formal-ontology, ontology-alignment, ontology-merging}

**Total:** 40-50 concepts with multiple perspectives

## Implementation Timeline

1. **Week 1:** Enhance PaperFetcher with PDF abstract extraction
2. **Week 2:** Update knowledge_base_generator.py with expansion logic
3. **Week 3:** Integrate into CI/CD pipeline
4. **Week 4:** Test and refine concept extraction from Zotero content
5. **Week 5:** Document and deploy

## Open Questions

1. **How to handle concept overlap?** (e.g., "complexity" defined differently in different fields)
   - Proposal: Create separate articles for different interpretations

2. **Citation threshold for inclusion?** (How many papers must mention a concept?)
   - Proposal: ≥1 cited papers OR ≥1 if mentioned in LaTeX

3. **How deep to go?** (Should we also fetch papers cited BY cited papers?)
   - Proposal: Stop at 1 level deep (papers cited in LaTeX only)

4. **Zotero library completeness?** (What if cited papers aren't in Zotero?)
   - Proposal: Manual curation to ensure all cited papers are added to Zotero library with proper metadata and attachments

5. **PDF extraction quality?** (How reliable is abstract extraction from PDFs?)
   - Proposal: Use metadata abstracts when available, fall back to PDF extraction only when necessary
