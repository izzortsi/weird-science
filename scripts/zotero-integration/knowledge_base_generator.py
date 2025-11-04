#!/usr/bin/env python3
"""
Knowledge Base Generator - Orchestration for Semantic Analysis.

This script:
1. Reads all relevant .tex and .bib files from the repository
2. Processes the Zotero manifest with item metadata
3. Prepares structured data for semantic analysis
4. Generates prompts for Claude Code to perform:
   - Topic extraction and concept identification (Γ)
   - Expansion to related concepts from Zotero (Γ⁺)
   - Hierarchical classification
   - Atomic Markdown generation with proper linking
5. Processes analysis results to create knowledge base structure
6. Generates summary files at investigation roots
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timezone

# Import PaperFetcher for Γ⁺ expansion
try:
    from paper_fetcher import PaperFetcher, PaperContent
except ImportError:
    # Try relative import
    from .paper_fetcher import PaperFetcher, PaperContent


@dataclass
class LatexSource:
    """Represents a LaTeX source file."""
    path: Path
    project: str
    content: str
    citations: Set[str]


@dataclass
class ConceptData:
    """Represents a concept/topic for the knowledge base."""
    name: str
    hierarchy_path: List[str]  # e.g., ["systems-theory", "complexity", "emergence"]
    definitions: List[str]
    examples: List[str]
    zotero_keys: List[str]
    related_concepts: List[str]
    bibkeys: Set[str]


class LatexAnalyzer:
    """Analyzes LaTeX files to extract structure and citations."""
    
    @staticmethod
    def extract_citations(content: str) -> Set[str]:
        """Extract all citation keys from LaTeX content."""
        citation_patterns = [
            r'\\cite\{([^}]+)\}',
            r'\\citep\{([^}]+)\}',
            r'\\citet\{([^}]+)\}',
            r'\\autocite\{([^}]+)\}',
            r'\\textcite\{([^}]+)\}',
            r'\\parencite\{([^}]+)\}',
        ]
        
        citations = set()
        for pattern in citation_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                # Handle multiple citations in one command
                keys = [k.strip() for k in match.split(',')]
                citations.update(keys)
        
        return citations
    
    @staticmethod
    def find_latex_files(repo_root: Path) -> List[LatexSource]:
        """Find all .tex files and organize by project."""
        sources = []
        
        # Find all main.tex files (indicate project roots)
        project_roots = []
        for tex_file in repo_root.rglob("main.tex"):
            project_dir = tex_file.parent
            # Skip if in hidden or cache directories
            if any(part.startswith('.') for part in project_dir.parts):
                continue
            project_roots.append(project_dir)
        
        # Process each project
        for project_dir in project_roots:
            project_name = project_dir.name
            
            # Find all .tex files in this project
            for tex_file in project_dir.rglob("*.tex"):
                try:
                    content = tex_file.read_text(encoding='utf-8')
                    citations = LatexAnalyzer.extract_citations(content)
                    
                    source = LatexSource(
                        path=tex_file,
                        project=project_name,
                        content=content,
                        citations=citations
                    )
                    sources.append(source)
                    
                except Exception as e:
                    print(f"Warning: Could not read {tex_file}: {e}", file=sys.stderr)
        
        return sources


class KnowledgeBaseGenerator:
    """Orchestrates knowledge base generation from LaTeX and Zotero data."""
    
    def __init__(self, repo_root: Path, manifest_path: Path, output_dir: Path):
        self.repo_root = repo_root
        self.manifest_path = manifest_path
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Load Zotero manifest
        self.manifest = self.load_manifest()

        # Analyze LaTeX sources
        self.latex_sources = LatexAnalyzer.find_latex_files(repo_root)

        # Load bibliography files
        self.bib_entries = self.load_all_bibtex()

        # Initialize PaperFetcher for Γ⁺ expansion
        self.paper_fetcher = PaperFetcher()

        # Load paper cache if it exists
        cache_file = self.output_dir / "cited-papers-cache.json"
        self.paper_fetcher.load_cache(cache_file)
    
    def load_manifest(self) -> Dict:
        """Load the Zotero manifest."""
        if not self.manifest_path.exists():
            print(f"Warning: Manifest not found at {self.manifest_path}", file=sys.stderr)
            return {"items": [], "attachments": []}
        
        with open(self.manifest_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def load_all_bibtex(self) -> Dict[str, Dict]:
        """Load all .bib files from the repository."""
        bib_entries = {}

        for bib_file in self.repo_root.rglob("*.bib"):
            # Skip if in hidden or cache directories
            if any(part.startswith('.') for part in bib_file.parts):
                continue

            try:
                content = bib_file.read_text(encoding='utf-8')

                # Split into individual entries
                # Match @type{key, ... }
                entry_pattern = r'@(\w+)\s*{\s*([^,}\s]+)\s*,([^@]*?)(?=\n@|\n*$)'

                for match in re.finditer(entry_pattern, content, re.DOTALL):
                    entry_type = match.group(1)
                    bibkey = match.group(2).strip()
                    entry_content = match.group(3)

                    if not bibkey:
                        continue

                    # Extract DOI if present
                    doi = None
                    doi_match = re.search(r'doi\s*=\s*[{"]?([^,}"]+)[}"]?', entry_content, re.IGNORECASE)
                    if doi_match:
                        doi = doi_match.group(1).strip()

                    # Extract arXiv ID if present
                    arxiv_id = None
                    arxiv_patterns = [
                        r'eprint\s*=\s*[{"]?(\d{4}\.\d{4,5})[}"]?',
                        r'arxiv[:\s]+(\d{4}\.\d{4,5})',
                    ]
                    for pattern in arxiv_patterns:
                        arxiv_match = re.search(pattern, entry_content, re.IGNORECASE)
                        if arxiv_match:
                            arxiv_id = arxiv_match.group(1).strip()
                            break

                    # Extract title if present
                    title = None
                    title_match = re.search(r'title\s*=\s*\{+([^}]+)\}+', entry_content, re.IGNORECASE)
                    if title_match:
                        title = title_match.group(1).strip()

                    # Extract author if present
                    authors = []
                    author_match = re.search(r'author\s*=\s*[{"]([^}"]+)[}"]', entry_content, re.IGNORECASE)
                    if author_match:
                        author_str = author_match.group(1).strip()
                        # Split by "and" for multiple authors
                        authors = [a.strip() for a in author_str.split(' and ')]

                    # Extract year if present
                    year = None
                    year_match = re.search(r'year\s*=\s*[{"]?(\d{4})[}"]?', entry_content, re.IGNORECASE)
                    if year_match:
                        year = int(year_match.group(1))

                    bib_entries[bibkey] = {
                        'key': bibkey,
                        'type': entry_type,
                        'file': str(bib_file.relative_to(self.repo_root)),
                        'doi': doi,
                        'arxiv_id': arxiv_id,
                        'title': title,
                        'authors': authors,
                        'year': year
                    }

            except Exception as e:
                print(f"Warning: Could not read {bib_file}: {e}", file=sys.stderr)

        return bib_entries
    
    def prepare_analysis_data(self, fetch_papers: bool = True) -> Dict:
        """Prepare structured data for semantic analysis."""
        # Collect all citations from LaTeX sources
        all_citations = set()
        for source in self.latex_sources:
            all_citations.update(source.citations)

        # Organize data by project
        projects_data = {}
        for source in self.latex_sources:
            if source.project not in projects_data:
                projects_data[source.project] = {
                    'name': source.project,
                    'tex_files': [],
                    'citations': set()
                }

            projects_data[source.project]['tex_files'].append({
                'path': str(source.path.relative_to(self.repo_root)),
                'content_length': len(source.content),
                'citations': list(source.citations)
            })
            projects_data[source.project]['citations'].update(source.citations)

        # Convert sets to lists for JSON serialization
        for project_data in projects_data.values():
            project_data['citations'] = list(project_data['citations'])

        # Fetch cited papers for Γ⁺ expansion
        cited_papers = {}
        if fetch_papers and all_citations:
            cited_papers = self.fetch_cited_papers(all_citations)

        analysis_data = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'total_projects': len(projects_data),
            'total_latex_files': len(self.latex_sources),
            'total_citations': len(all_citations),
            'total_zotero_items': len(self.manifest.get('items', [])),
            'total_bib_entries': len(self.bib_entries),
            'projects': list(projects_data.values()),
            'all_citations': list(all_citations),
            'zotero_items_summary': self.summarize_zotero_items(),
            'bibliography_keys': list(self.bib_entries.keys()),
            'cited_papers': cited_papers  # Add cited papers data for Γ⁺ expansion
        }

        return analysis_data
    
    def summarize_zotero_items(self) -> List[Dict]:
        """Create a summary of Zotero items for analysis."""
        items_summary = []

        for item in self.manifest.get('items', []):
            summary = {
                'key': item['key'],
                'title': item['title'],
                'type': item['item_type'],
                'tags': item.get('tags', []),
                'doi': item.get('doi'),
                'has_abstract': bool(item.get('abstract')),
                'num_attachments': len(item.get('attachments', []))
            }
            items_summary.append(summary)

        return items_summary

    def _match_zotero_item_by_metadata(self, bibkey: str) -> Optional[Dict]:
        """
        Match a Zotero item by metadata (title, author, year) when bibkey doesn't match directly.

        Args:
            bibkey: Bibliography key to match

        Returns:
            Matching Zotero item or None
        """
        bib_entry = self.bib_entries.get(bibkey)
        if not bib_entry:
            return None

        # Extract metadata from bib entry
        bib_title = (bib_entry.get('title') or '').lower().strip()
        bib_doi = (bib_entry.get('doi') or '').strip()
        bib_authors = bib_entry.get('authors', [])
        bib_year = bib_entry.get('year')

        # Try DOI match first (most reliable)
        if bib_doi:
            for item in self.manifest.get('items', []):
                item_doi = item.get('doi') or ''
                if item_doi.strip() == bib_doi:
                    return item

        # Try title + author match
        if bib_title:
            for item in self.manifest.get('items', []):
                item_title = item.get('title', '').lower().strip()

                # Check title similarity (simple contains check)
                if bib_title in item_title or item_title in bib_title:
                    # If we have author info, verify it matches
                    if bib_authors:
                        item_creators = item.get('creators', [])
                        item_authors = [f"{c.get('firstName', '')} {c.get('lastName', '')}".strip()
                                      for c in item_creators if c.get('creatorType') == 'author']

                        # Check if any author matches
                        for bib_author in bib_authors:
                            # Extract last name from bib_author (handle "Last, First" or "First Last" format)
                            bib_last_name = bib_author.split(',')[0].strip() if ',' in bib_author else bib_author.split()[-1]

                            for item_author in item_authors:
                                # Extract last name from item_author
                                item_last_name = item_author.split()[-1] if item_author else ''

                                # Match on last name
                                if bib_last_name.lower() == item_last_name.lower():
                                    return item
                    else:
                        # No author info, accept title match
                        return item

        return None

    def fetch_cited_papers(self, citations: Set[str]) -> Dict[str, Optional[Dict]]:
        """
        Fetch content for cited papers (Γ → Γ⁺ expansion).

        Args:
            citations: Set of citation keys from LaTeX sources

        Returns:
            Dictionary mapping bibkey to paper content
        """
        cited_papers = {}

        print(f"\nFetching content for {len(citations)} cited papers...")

        # Create mapping from bibkey to Zotero item
        zotero_items_by_bibkey = {}
        for item in self.manifest.get('items', []):
            # Try to match Zotero item to bibkey
            item_id = item.get('citation_key') or item.get('key')
            if item_id:
                zotero_items_by_bibkey[item_id] = item

        for i, bibkey in enumerate(sorted(citations), 1):
            print(f"  [{i}/{len(citations)}] Fetching {bibkey}...", end=' ')

            # Get Zotero item if available (direct match by key)
            zotero_item = zotero_items_by_bibkey.get(bibkey)

            # If no direct match, try fuzzy matching by metadata
            if not zotero_item:
                zotero_item = self._match_zotero_item_by_metadata(bibkey)

            # Get bib entry if available
            bib_entry = self.bib_entries.get(bibkey)

            # Fetch paper content
            content = self.paper_fetcher.fetch_paper_content(
                bibkey=bibkey,
                zotero_item=zotero_item,
                bib_entry=bib_entry
            )

            if content:
                cited_papers[bibkey] = content.to_dict()
                print(f"OK ({content.source})")
            else:
                cited_papers[bibkey] = None
                print("NOT FOUND")

        # Save cache
        cache_file = self.output_dir / "cited-papers-cache.json"
        self.paper_fetcher.save_cache(cache_file)

        return cited_papers
    
    def generate_claude_prompt(self, analysis_data: Dict) -> str:
        """Generate a detailed prompt for Claude Code semantic analysis."""
        prompt = f"""# Semantic Analysis Task: Knowledge Base Generation from LaTeX and Zotero

## Objective
Analyze the provided LaTeX sources and Zotero library to generate a hierarchical, atomic knowledge base with Quartz-compatible Markdown files.

## Input Data Summary
- **Projects:** {analysis_data['total_projects']}
- **LaTeX Files:** {analysis_data['total_latex_files']}
- **Citations:** {analysis_data['total_citations']}
- **Zotero Items:** {analysis_data['total_zotero_items']}
- **Bibliography Entries:** {analysis_data['total_bib_entries']}

## Projects in Repository
"""
        for project in analysis_data['projects']:
            prompt += f"\n### {project['name']}\n"
            prompt += f"- LaTeX files: {len(project['tex_files'])}\n"
            prompt += f"- Citations: {len(project['citations'])}\n"
        
        prompt += """

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
"""
        
        # Add sample of available data
        prompt += "\n### Sample Citations\n"
        sample_citations = analysis_data['all_citations'][:20]
        for citation in sample_citations:
            prompt += f"- {citation}\n"
        
        prompt += "\n### Sample Zotero Items\n"
        sample_items = analysis_data['zotero_items_summary'][:10]
        for item in sample_items:
            prompt += f"- {item['title']} ({item['type']}) - Tags: {', '.join(item['tags'][:3])}\n"
        
        prompt += f"""

### Full Data Files Available
- Complete LaTeX sources in: {analysis_data['total_latex_files']} files
- Zotero manifest: {analysis_data['total_zotero_items']} items
- Bibliography: {analysis_data['total_bib_entries']} entries

Please proceed with the semantic analysis and knowledge base generation.
"""
        
        return prompt
    
    def save_analysis_data(self, analysis_data: Dict) -> Path:
        """Save analysis data to JSON file."""
        output_file = self.output_dir / "analysis-data.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, indent=2, ensure_ascii=False)
        return output_file
    
    def save_claude_prompt(self, prompt: str) -> Path:
        """Save Claude prompt to file."""
        output_file = self.output_dir / "claude-prompt.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(prompt)
        return output_file
    
    def generate(self, force: bool = False, fetch_papers: bool = True) -> None:
        """Main generation workflow."""
        print("=" * 70)
        print("Knowledge Base Generator - Semantic Analysis Orchestration")
        print("=" * 70)
        print(f"Repository: {self.repo_root}")
        print(f"Manifest: {self.manifest_path}")
        print(f"Output: {self.output_dir}")
        print(f"Cited Paper Expansion: {'enabled' if fetch_papers else 'disabled'}")
        print()

        # Prepare analysis data
        print("Preparing analysis data...")
        analysis_data = self.prepare_analysis_data(fetch_papers=fetch_papers)
        print(f"  * Projects: {analysis_data['total_projects']}")
        print(f"  * LaTeX files: {analysis_data['total_latex_files']}")
        print(f"  * Citations: {analysis_data['total_citations']}")
        print(f"  * Zotero items: {analysis_data['total_zotero_items']}")
        print()

        # Save analysis data
        analysis_file = self.save_analysis_data(analysis_data)
        print(f"* Saved analysis data: {analysis_file}")

        # Generate Claude prompt
        print("\nGenerating Claude Code prompt...")
        prompt = self.generate_claude_prompt(analysis_data)
        prompt_file = self.save_claude_prompt(prompt)
        print(f"* Saved Claude prompt: {prompt_file}")
        print()
        
        # Generate instructions for handoff
        self.generate_handoff_instructions()
        
        print("=" * 70)
        print("Orchestration Complete!")
        print("=" * 70)
        print()
        print("Next Steps:")
        print("1. Review the generated Claude prompt:")
        print(f"   {prompt_file}")
        print()
        print("2. Use Claude Code to perform semantic analysis:")
        print("   - Provide the prompt and access to repository files")
        print("   - Claude will generate the hierarchical knowledge base")
        print()
        print("3. Integration with repository:")
        print("   - Claude Code output will be placed in knowledge-database/")
        print("   - Commit and push changes to trigger Quartz site rebuild")
        print()
    
    def generate_handoff_instructions(self) -> None:
        """Generate detailed instructions for Claude/Copilot handoff."""
        instructions = """# Claude Code Integration Instructions

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
"""
        
        instructions_file = self.output_dir / "CLAUDE_INTEGRATION.md"
        with open(instructions_file, 'w', encoding='utf-8') as f:
            f.write(instructions)

        print(f"* Saved integration instructions: {instructions_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate knowledge base structure from LaTeX and Zotero data"
    )
    parser.add_argument(
        "--group-id",
        default=os.environ.get("ZOTERO_GROUP_ID", "6182921"),
        help="Zotero group ID"
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("ZOTERO_API_KEY"),
        help="Zotero API key"
    )
    parser.add_argument(
        "--manifest",
        default="zotero-cache/zotero-manifest.json",
        help="Path to Zotero manifest file"
    )
    parser.add_argument(
        "--output-dir",
        default="knowledge-database",
        help="Output directory for knowledge base"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force regeneration of all files"
    )
    
    parser.add_argument(
        "--skip-paper-fetch",
        action="store_true",
        help="Skip fetching cited papers (cited paper expansion)"
    )

    args = parser.parse_args()

    repo_root = Path.cwd()
    manifest_path = Path(args.manifest)
    output_dir = Path(args.output_dir)

    generator = KnowledgeBaseGenerator(repo_root, manifest_path, output_dir)
    generator.generate(force=args.force, fetch_papers=not args.skip_paper_fetch)

    return 0


if __name__ == "__main__":
    sys.exit(main())
