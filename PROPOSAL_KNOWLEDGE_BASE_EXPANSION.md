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
**Status:** ✅ Fully implemented

**Implementation Details:**

For each citation in Γ's source LaTeX:
1. **Paper Fetcher** (`scripts/zotero-integration/paper_fetcher.py`):
   - Look up paper in Zotero library
   - Fetch paper content from Zotero metadata:
     - Title, authors, year, abstract, keywords/tags
     - PDF attachments for abstract extraction when needed
2. **Concept Extraction**:
   - Extract concepts from title keywords and technical terms
   - Analyze abstract for key concepts using NLP techniques
   - Use Zotero tags/keywords directly
   - Identify frequently mentioned technical terms
3. **Inclusion Criteria**:
   - All concepts from cited papers are included in Γ⁺
   - Creates comprehensive coverage of literature concepts

**Example:**
```
LaTeX cites: Simon1962 ("The Architecture of Complexity")
→ Fetch paper content
→ Extract concepts: {complexity, near-decomposability, hierarchy,
                     stable-intermediate-forms, watchmaker-parable}
→ Add to Γ⁺ (even though not explicitly defined in LaTeX)
```

### Phase 3: Expand via Zotero Library (Γ⁺ → Γ⁺⁺)
**Status:** ✅ Fully implemented

**Implementation Details:**

For each concept in Γ⁺:
1. **Zotero Cross-Referencer** (`scripts/zotero-integration/zotero_cross_referencer.py`):
   - Search full Zotero library for related papers:
     - Papers with concept in title, abstract, or tags
     - Papers using semantic matching and fuzzy search
     - Papers discussing multiple related concepts together
2. **Content Extraction**:
   - Extract alternative definitions and perspectives
   - Identify extended treatments and applications
   - Build cross-references between different treatments
3. **Exclusion Logic**:
   - Excludes papers already cited in LaTeX (avoids duplicates)
   - Focuses on uncited papers that provide additional perspectives

**Example:**
```
Γ⁺ contains: {complexity, near-decomposability}
→ Search Zotero for papers about "complexity"
→ Find: Bar-Yam (1997), Ladyman (2013), etc.
→ Extract their definitions of complexity
→ Add as alternative definitions/perspectives to the concept article
```

## Implementation Details

### Phase 1: LaTeX Concept Extraction (Γ)
**Implemented in:** `scripts/zotero-integration/knowledge_base_generator.py` (LatexAnalyzer class)

- Parses all `.tex` files using regex patterns
- Extracts explicit definitions, theorems, key terms
- Identifies citations using `\cite{Key}` and `\citep{Key}` patterns
- Results in structured concept data with source locations

### Phase 2: Cited Paper Expansion (Γ → Γ⁺)
**Implemented in:** `scripts/zotero-integration/paper_fetcher.py` and `knowledge_base_generator.py`

**Key Methods:**
```python
# Paper fetching and concept extraction
class PaperFetcher:
    def fetch_paper_content(self, bibkey: str, zotero_item: Dict) -> PaperContent
    def extract_concepts_from_paper(self, content: PaperContent) -> List[str]

# Integration in knowledge base generator
def _extract_gamma_plus_concepts(self, cited_papers: Dict) -> Set[str]:
    # Extracts concepts from all cited papers
```

**Process:**
1. For each LaTeX citation, looks up paper in Zotero manifest
2. Fetches metadata (title, authors, abstract, keywords)
3. Extracts concepts using title analysis, abstract processing, and keyword tagging
4. Forms Γ⁺ with all concepts from cited literature

### Phase 3: Zotero Library Cross-Referencing (Γ⁺ → Γ⁺⁺)
**Implemented in:** `scripts/zotero-integration/zotero_cross_referencer.py` (600+ lines)

**Core Classes:**
```python
@dataclass
class ConceptReference:
    zotero_key: str
    title: str
    authors: List[str]
    context: str  # title/abstract/tags
    relevance_score: float
    mention_type: str  # title/abstract/tags

@dataclass
class ConceptExpansion:
    additional_papers: List[ConceptReference]
    alternative_definitions: List[str]
    extended_treatments: List[str]
    related_concepts: Set[str]
    cross_references: Dict[str, List[ConceptReference]]

class ZoteroCrossReferencer:
    def expand_concept(self, concept_name: str, all_concepts: Set[str]) -> ConceptExpansion
```

**Key Features:**
- Semantic concept matching with fuzzy search
- Relevance scoring (0.1-1.0) based on context and frequency
- Exclusion of already-cited papers to avoid duplicates
- Cross-reference building between related concepts
- Multi-context matching (title, abstract, tags, authors)

### Phase 4: Knowledge Base Generation
**Enhanced Claude Prompt:** Integrated Γ⁺⁺ expansion data into semantic analysis

**New Prompt Sections:**
```markdown
### Phase 3: Cross-reference with Zotero Library (Γ⁺ → Γ⁺⁺)
**ALREADY COMPLETED:** The system has already performed Γ⁺ → Γ⁺⁺ expansion...

**Available Data:**
- `concept_expansions` contains pre-processed expansions for each concept
- Includes additional_papers, alternative_definitions, extended_treatments
- Provides cross_references and related_concepts
```

**Enhanced Article Template:**
- Alternative Definitions section
- Extended Treatments subsection
- Additional References with relevance scores
- See Also sections with cross-references

## Current Implementation Status

### Deployment & Integration
**Status:** ✅ Fully implemented and deployed

- **GitHub Actions Integration**: Automated generation runs on pushes to `dev` branch
- **Quartz Site Deployment**: Knowledge base deployed to repository root (https://izzortsi.github.io/weird-science/)
- **CI/CD Pipeline**: Complete workflow from LaTeX/Zotero to live knowledge base

### Performance Metrics
- **LaTeX Sources**: 3 projects, 9 `.tex` files
- **Citations**: 15 unique bibliography entries
- **Γ⁺ Expansion**: ~18 concepts extracted from cited papers
- **Γ⁺⁺ Expansion**: 230+ additional papers found across 18 concepts
- **Literature Coverage**: 15.4x increase (from 15 to 230+ papers)

## Real-World Results

### Example: "complexity" Concept Expansion
**Γ (LaTeX):** 0 explicit definitions

**Γ⁺ (Cited Papers):** 3 primary sources
- Simon1962: "The Architecture of Complexity"
- BarYam1997: "Dynamics of Complex Systems"
- Ladyman2013: "Complexity and Emergence"

**Γ⁺⁺ (Zotero Library):** 12 additional papers with relevance scores 0.6-1.0
- Alternative definitions from computer science, physics, biology
- Extended treatments on complexity measures
- Cross-references to emergence, self-organization, criticality

### Example: "hierarchy" Concept Expansion
**Γ (LaTeX):** Basic definition in nested-systems project

**Γ⁺ (Cited Papers):** 4 treatments
- Simon1962: Hierarchical structure
- Mesarovic1975: Hierarchical systems
- Backlund2000: System hierarchies
- BarYam1997: Scale hierarchies

**Γ⁺⁺ (Zotero Library):** 8 additional papers
- Alternative: heterarchy, holarchy
- Extended: nested systems, multi-level modeling
- Cross-refs: complexity, emergence, organization

## Technical Architecture

### Data Flow
```
LaTeX Sources → LaTeXAnalyzer → Γ (concepts)
                ↓
        Bibliography Files → PaperFetcher → Cited Papers
                ↓
        Γ + Cited Papers → _extract_gamma_plus_concepts → Γ⁺
                ↓
        Γ⁺ + Zotero Manifest → ZoteroCrossReferencer → Γ⁺⁺
                ↓
        Γ⁺⁺ → Enhanced Claude Prompt → Knowledge Base Articles
```

### Key Design Decisions
1. **Zotero-Only Approach**: All paper content comes from Zotero library (no external APIs)
2. **Citation Exclusion**: Γ⁺⁺ excludes already-cited papers to avoid redundancy
3. **Semantic Matching**: Fuzzy search handles concept variations (e.g., "system" vs "systems")
4. **Relevance Scoring**: 0.1-1.0 scores help prioritize most relevant expansions
5. **Cross-References**: Papers discussing multiple concepts create semantic links

## Benefits Realized

### Enhanced Coverage
- **Before**: 15 concepts from LaTeX only
- **After**: 40+ concepts with multiple perspectives each
- **Literature Integration**: 15.4x increase in referenced papers

### Richer Concept Articles
- **Multiple Definitions**: Primary + alternative perspectives
- **Extended Treatments**: Applications, critiques, extensions
- **Comprehensive References**: Cited + additional papers with relevance scores
- **Cross-Links**: Bidirectional wikilinks between related concepts

### Improved Discoverability
- **Semantic Connections**: Concepts linked via shared papers
- **Cross-References**: "See Also" sections guide exploration
- **Hierarchical Organization**: Concepts grouped by domain and specificity

## Operational Considerations

### Zotero Library Requirements
1. **Complete Metadata**: Titles, authors, abstracts, tags for all items
2. **Consistent Citation Keys**: BibTeX keys must match Zotero item keys
3. **Quality Tags**: Proper tagging improves concept matching accuracy
4. **PDF Attachments**: Optional fallback for missing abstracts

### Performance Characteristics
- **Processing Time**: ~2-3 minutes for full expansion (18 concepts)
- **Cache Utilization**: Cited papers cached to avoid repeated Zotero API calls
- **Scalability**: Designed to handle 100+ Zotero items efficiently

### Maintenance
- **Zotero Sync**: Regular sync ensures latest metadata
- **Bibliography Updates**: New .bib entries automatically included
- **Concept Validation**: Manual review of expansion results recommended
