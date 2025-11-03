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
**Status:** 🟡 Partially implemented (only uses Zotero metadata)

**Proposed enhancement:**

For each citation in Γ's source LaTeX:
1. Look up paper in Zotero library
2. **Fetch paper content** via:
   - Zotero attachments (PDFs)
   - Semantic Scholar API (abstracts, TLDRs, influential citations)
   - arXiv API (for preprints)
   - CrossRef API (metadata)
3. **Extract concepts** from paper using:
   - Title keywords
   - Abstract analysis
   - Section headings
   - Index terms / keywords
   - Frequently mentioned technical terms
4. **Add to Γ⁺** if concept:
   - Appears in ≥2 cited papers, OR
   - Is central to a highly-cited paper, OR
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

### Step 1: Enhance Paper Fetching

Create `scripts/zotero-integration/paper_fetcher.py`:

```python
class PaperFetcher:
    def __init__(self, zotero_api_key, semantic_scholar_api_key=None):
        self.zotero = pyzotero.zotero.Zotero(...)
        self.s2_api_key = semantic_scholar_api_key

    def fetch_paper_content(self, bibkey: str) -> PaperContent:
        """Fetch full content of a paper from multiple sources"""
        # 1. Try Zotero PDF attachment
        pdf_content = self._fetch_from_zotero_pdf(bibkey)
        if pdf_content:
            return pdf_content

        # 2. Try Semantic Scholar
        s2_content = self._fetch_from_semantic_scholar(bibkey)
        if s2_content:
            return s2_content

        # 3. Try arXiv
        arxiv_content = self._fetch_from_arxiv(bibkey)
        if arxiv_content:
            return arxiv_content

        # 4. Fallback to CrossRef metadata
        return self._fetch_from_crossref(bibkey)

    def extract_concepts_from_paper(self, content: PaperContent) -> List[Concept]:
        """Extract key concepts from paper content"""
        concepts = []

        # Extract from title keywords
        title_concepts = self._extract_title_concepts(content.title)
        concepts.extend(title_concepts)

        # Extract from abstract
        abstract_concepts = self._extract_abstract_concepts(content.abstract)
        concepts.extend(abstract_concepts)

        # Extract from section headings
        section_concepts = self._extract_section_concepts(content.sections)
        concepts.extend(section_concepts)

        # Extract from index terms / keywords
        if content.keywords:
            concepts.extend(content.keywords)

        return self._deduplicate_and_rank(concepts)
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

### Step 4: Add Semantic Scholar Integration

Add to `.github/workflows/knowledge-base-pipeline.yml`:

```yaml
- name: Fetch cited papers via APIs
  env:
    SEMANTIC_SCHOLAR_API_KEY: ${{ secrets.SEMANTIC_SCHOLAR_API_KEY }}
    ZOTERO_API_KEY: ${{ secrets.ZOTERO_API_KEY }}
  run: |
    python scripts/zotero-integration/fetch_cited_papers.py \
      --output knowledge-database/cited-papers-content.json
```

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

1. **Week 1:** Implement PaperFetcher with Semantic Scholar API
2. **Week 2:** Update knowledge_base_generator.py with expansion logic
3. **Week 3:** Integrate into CI/CD pipeline
4. **Week 4:** Test and refine concept extraction
5. **Week 5:** Document and deploy

## Open Questions

1. **How to handle concept overlap?** (e.g., "complexity" defined differently in different fields)
   - Proposal: Create separate articles for different interpretations

2. **Citation threshold for inclusion?** (How many papers must mention a concept?)
   - Proposal: ≥2 cited papers OR ≥1 if mentioned in LaTeX

3. **How deep to go?** (Should we also fetch papers cited BY cited papers?)
   - Proposal: Stop at 1 level deep (papers cited in LaTeX only)

4. **API rate limits?** (Semantic Scholar, CrossRef have limits)
   - Proposal: Cache fetched content, batch requests, use exponential backoff
