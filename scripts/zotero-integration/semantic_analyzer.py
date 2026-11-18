#!/usr/bin/env python3
"""
Automated Semantic Analyzer for Knowledge Base Generation.

This script performs automated semantic analysis without using external APIs.
It extracts concepts from LaTeX sources and cited papers using local NLP
and heuristic methods.
"""

import re
import json
import yaml
from pathlib import Path
from typing import Dict, List, Set
from dataclasses import dataclass, field
from collections import defaultdict, Counter


@dataclass
class Concept:
    """Represents a concept extracted from sources."""
    name: str
    category: str
    definitions: List[str] = field(default_factory=list)
    sources: Set[str] = field(default_factory=set)
    related_concepts: Set[str] = field(default_factory=set)
    citations: Set[str] = field(default_factory=set)
    keywords: Set[str] = field(default_factory=set)

    def to_markdown(self, hierarchy: List[str]) -> str:
        """Generate markdown content for this concept."""
        related_links = '\n'.join([f"- [[{c}]]" for c in sorted(self.related_concepts)])
        citations_list = '\n'.join([f"- {c}" for c in sorted(self.citations)])

        # Generate YAML front matter using yaml library for proper escaping
        frontmatter = {
            'title': self.name,
            'tags': sorted(self.keywords),
            'hierarchy': hierarchy,
            'related': sorted(self.related_concepts)
        }
        yaml_str = yaml.safe_dump(frontmatter, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        content = f"""---
{yaml_str}---

# {self.name}

## Definition

{self.definitions[0] if self.definitions else 'Definition to be added.'}

"""

        if len(self.definitions) > 1:
            content += "### Alternative Definitions\n\n"
            for i, defn in enumerate(self.definitions[1:], 1):
                content += f"{i}. {defn}\n\n"

        if self.related_concepts:
            content += f"""## Related Concepts

{related_links}

"""

        if self.citations:
            content += f"""## Bibliography Keys

{citations_list}
"""

        return content


class SemanticAnalyzer:
    """Performs automated semantic analysis of LaTeX and PDF content."""

    def __init__(self, repo_root: Path, output_dir: Path):
        self.repo_root = repo_root
        self.output_dir = output_dir
        self.concepts: Dict[str, Concept] = {}
        self.categories: Dict[str, List[str]] = defaultdict(list)

    def analyze(self, analysis_data_path: Path):
        """Main analysis entry point."""
        print("="*70)
        print("Automated Semantic Analysis - Knowledge Base Generation")
        print("="*70)

        # Load analysis data
        with open(analysis_data_path, 'r', encoding='utf-8') as f:
            analysis_data = json.load(f)

        print(f"\nAnalyzing {analysis_data['total_latex_files']} LaTeX files...")

        # Phase 1: Extract core concepts (Γ) from LaTeX
        self._extract_latex_concepts(analysis_data)

        # Phase 2: Expand with cited papers (Γ → Γ⁺)
        print(f"\nExpanding with {len(analysis_data.get('cited_papers', {}))} cited papers...")
        self._expand_with_cited_papers(analysis_data)

        # Phase 3: Organize hierarchy
        print("\nOrganizing concept hierarchy...")
        self._organize_hierarchy()

        # Phase 4: Generate markdown files
        print("\nGenerating markdown files...")
        self._generate_markdown_files()

        print(f"\n✅ Generated {len(self.concepts)} concept articles")
        print("="*70)

    def _extract_latex_concepts(self, analysis_data: Dict):
        """Extract concepts from LaTeX sources (Phase 1: Γ)."""
        for project in analysis_data.get('projects', []):
            project_name = project['name']

            for tex_file in project['tex_files']:
                file_path = self.repo_root / tex_file['path']
                if not file_path.exists():
                    continue

                content = file_path.read_text(encoding='utf-8', errors='ignore')

                # Extract definitions
                self._extract_definitions(content, tex_file['path'], project_name)

                # Extract section titles as concepts
                self._extract_section_concepts(content, tex_file['path'], project_name)

                # Track citations
                for citation in tex_file.get('citations', []):
                    self._add_citation_context(citation, content, tex_file['path'])

    def _extract_latex_arg(self, text: str, start_pos: int) -> tuple:
        """
        Extract a LaTeX argument with proper brace matching.
        
        Handles nested braces correctly by counting brace depth.
        Returns (argument_text, end_position) or (None, start_pos) if no valid argument.
        
        Args:
            text: The full text to parse
            start_pos: Position where the opening brace should be
            
        Returns:
            Tuple of (extracted argument text, position after closing brace)
        """
        if start_pos >= len(text) or text[start_pos] != '{':
            return None, start_pos
        
        depth = 1
        pos = start_pos + 1
        arg_start = pos
        
        while pos < len(text) and depth > 0:
            if text[pos] == '\\':
                # Skip escaped characters
                pos += 2
                continue
            elif text[pos] == '{':
                depth += 1
            elif text[pos] == '}':
                depth -= 1
            pos += 1
        
        if depth == 0:
            return text[arg_start:pos-1], pos
        else:
            # Unmatched braces
            return None, start_pos

    def _extract_definitions(self, content: str, source: str, category: str):
        """
        Extract explicit definitions from LaTeX content.
        
        This method uses proper brace matching to handle nested braces in
        LaTeX definitions like: \\definition{term}{text with \\emph{nested} braces}
        """
        # Find all occurrences of \definition command
        pattern = r'\\definition'
        for match in re.finditer(pattern, content):
            pos = match.end()
            
            # Skip whitespace
            while pos < len(content) and content[pos].isspace():
                pos += 1
            
            # Extract first argument (term)
            term, pos = self._extract_latex_arg(content, pos)
            if term is None:
                continue
            
            # Skip whitespace
            while pos < len(content) and content[pos].isspace():
                pos += 1
            
            # Extract second argument (definition)
            definition, _ = self._extract_latex_arg(content, pos)
            if definition is None:
                continue
            
            # Add the concept
            self._add_concept(term.strip(), definition.strip(), source, category)

        # Pattern: "X is defined as Y" or "X is a Y that"
        text_def_patterns = [
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+is\s+defined\s+as\s+([^.]+)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+is\s+a\s+([^.]+)',
            r'A\s+([a-z]+(?:\s+[a-z]+)*)\s+is\s+([^.]+)',
        ]

        for pattern in text_def_patterns:
            for match in re.finditer(pattern, content):
                term = match.group(1).strip()
                definition = match.group(2).strip()
                if len(term) > 2 and len(definition) > 10:
                    self._add_concept(term, f"{term} is {definition}", source, category)

    def _extract_section_concepts(self, content: str, source: str, category: str):
        """Extract concepts from section and subsection titles."""
        # Match \section{Title}, \subsection{Title}, and \subsubsection{Title}
        section_pattern = r'\\(?:sub){0,2}section\{([^}]+)\}'
        for match in re.finditer(section_pattern, content):
            title = match.group(1).strip()
            # Remove LaTeX commands
            title = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', title)
            title = re.sub(r'\\[a-zA-Z]+', '', title)

            if len(title) > 3 and not title.isdigit():
                # Add as concept with title as definition
                self._add_concept(title, f"Section: {title}", source, category, is_weak=True)

    def _add_citation_context(self, citation: str, content: str, source: str):
        """Find context around citations to understand related concepts."""
        # Find sentences containing the citation
        cite_pattern = rf'\\cite\{{{re.escape(citation)}\}}'
        for match in re.finditer(cite_pattern, content):
            start = max(0, match.start() - 200)
            end = min(len(content), match.end() + 200)
            context = content[start:end]

            # Extract capitalized terms near citation (potential concepts)
            terms = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', context)
            for term in terms:
                if term in self.concepts:
                    self.concepts[term].citations.add(citation)

    def _expand_with_cited_papers(self, analysis_data: Dict):
        """Expand concepts with cited papers (Phase 2: Γ⁺)."""
        cited_papers = analysis_data.get('cited_papers', {})

        for bibkey, paper_data in cited_papers.items():
            if not paper_data:
                continue

            title = paper_data.get('title', '')
            abstract = paper_data.get('abstract', '')
            keywords = paper_data.get('keywords', [])

            # Extract concepts from paper title
            title_concepts = self._extract_title_concepts(title)
            for concept in title_concepts:
                self._add_concept(
                    concept,
                    f"Concept from: {title}",
                    f"paper:{bibkey}",
                    "cited-papers",
                    is_weak=True
                )
                if concept in self.concepts:
                    self.concepts[concept].citations.add(bibkey)
            # Extract from abstract
            if abstract:
                abstract_concepts = self._extract_abstract_concepts(abstract)
                for concept in abstract_concepts:
                    self._add_concept(
                        concept,
                        f"From abstract of: {title}",
                        f"paper:{bibkey}",
                        "cited-papers",
                        is_weak=True
                    )
                    if concept in self.concepts:
                        self.concepts[concept].citations.add(bibkey)

            # Add keywords as concepts
            for keyword in keywords:
                if keyword and len(keyword) > 2:
                    self._add_concept(
                        keyword,
                        f"Keyword from: {title}",
                        f"paper:{bibkey}",
                        "cited-papers",
                        is_weak=True
                    )

    def _extract_title_concepts(self, title: str) -> Set[str]:
        """Extract potential concepts from paper title."""
        concepts = set()

        # Remove common words
        stopwords = {'the', 'a', 'an', 'of', 'in', 'on', 'at', 'to', 'for', 'and', 'or'}

        # Extract capitalized multi-word terms
        terms = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', title)
        for term in terms:
            if term.lower() not in stopwords and len(term) > 3:
                concepts.add(term)

        # Extract technical hyphenated terms
        hyphenated = re.findall(r'\b[a-z]+-[a-z]+\b', title.lower())
        concepts.update(h for h in hyphenated if len(h) > 5)

        return concepts

    def _extract_abstract_concepts(self, abstract: str) -> Set[str]:
        """Extract concepts from abstract using heuristics."""
        concepts = set()

        # Find quoted terms (often new concepts)
        quoted = re.findall(r'["\']([^"\']{4,40})["\']', abstract)
        concepts.update(q for q in quoted if len(q.split()) <= 4)

        # Find italicized terms (LaTeX: \textit{term})
        italics = re.findall(r'\\textit\{([^}]+)\}', abstract)
        concepts.update(italics)

        # Find bold terms
        bold = re.findall(r'\\textbf\{([^}]+)\}', abstract)
        concepts.update(bold)

        # Find capitalized terms (potential proper nouns/concepts)
        capitalized = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2}\b', abstract)
        stopwords = {'The', 'A', 'An', 'This', 'These', 'That', 'Those', 'We', 'In', 'On'}
        concepts.update(c for c in capitalized if c not in stopwords and len(c) > 3)

        return concepts

    def _add_concept(self, name: str, definition: str, source: str, category: str, is_weak: bool = False):
        """Add or update a concept."""
        # Normalize name
        name = name.strip()
        name = re.sub(r'\s+', ' ', name)

        # Skip if too short or looks like noise
        if len(name) < 3 or name.isdigit():
            return

        # Skip common words that aren't concepts
        skip_words = {'the', 'and', 'for', 'with', 'this', 'that', 'from', 'have', 'been'}
        if name.lower() in skip_words:
            return

        if name not in self.concepts:
            self.concepts[name] = Concept(
                name=name,
                category=category,
                definitions=[definition] if not is_weak else [],
                sources={source},
                citations=set(),
                keywords=set()
            )
            self.categories[category].append(name)
        else:
            concept = self.concepts[name]
            concept.sources.add(source)
            if not is_weak and definition not in concept.definitions:
                concept.definitions.append(definition)
            # Merge categories (prefer non-cited-papers)
            if category != "cited-papers" and concept.category == "cited-papers":
                # Remove from old category
                if name in self.categories[concept.category]:
                    self.categories[concept.category].remove(name)
                # Update concept category
                concept.category = category
                # Add to new category if not already there
                if name not in self.categories[category]:
                    self.categories[category].append(name)

    def _organize_hierarchy(self):
        """Organize concepts into hierarchical structure."""
        # Build indices for sources and citations
        source_to_concepts = defaultdict(set)
        citation_to_concepts = defaultdict(set)
        for name, concept in self.concepts.items():
            for source in concept.sources:
                source_to_concepts[source].add(name)
            for citation in concept.citations:
                citation_to_concepts[citation].add(name)

        # For each concept, find related concepts efficiently
        for name, concept in self.concepts.items():
            related = set()
            # Related by shared sources
            for source in concept.sources:
                related.update(source_to_concepts[source])
            # Related by shared citations (at least 2)
            citation_counts = Counter()
            for citation in concept.citations:
                for other_name in citation_to_concepts[citation]:
                    if other_name != name:
                        citation_counts[other_name] += 1
            for other_name, count in citation_counts.items():
                if count >= 2:
                    related.add(other_name)
            # Remove self
            related.discard(name)
            concept.related_concepts.update(related)

        # Name containment check (hierarchy hint) - keep O(n²)
        concept_names = list(self.concepts.keys())
        for i, name in enumerate(concept_names):
            concept = self.concepts[name]
            for j, other_name in enumerate(concept_names):
                if i == j:
                    continue
                if name.lower() in other_name.lower() or other_name.lower() in name.lower():
                    if len(name) < len(other_name):
                        concept.related_concepts.add(other_name)
    def _generate_markdown_files(self):
        """Generate markdown files for all concepts."""
        concepts_dir = self.output_dir / "concepts"

        # Group concepts by category
        for category, concept_names in self.categories.items():
            category_slug = category.lower().replace(' ', '-').replace('_', '-')
            category_dir = concepts_dir / category_slug
            category_dir.mkdir(parents=True, exist_ok=True)

            # Generate concept files
            for concept_name in concept_names:
                concept = self.concepts[concept_name]

                # Skip weak concepts with no definitions
                if not concept.definitions:
                    continue

                # Create filename
                filename = concept_name.lower().replace(' ', '-').replace('_', '-')
                filename = re.sub(r'[^a-z0-9-]', '', filename)
                filename = re.sub(r'-+', '-', filename).strip('-')

                if not filename:
                    continue

                # Avoid filename collisions by appending a numeric suffix if needed
                filepath = category_dir / f"{filename}.md"
                counter = 1
                while filepath.exists():
                    filepath = category_dir / f"{filename}-{counter}.md"
                    counter += 1

                # Generate markdown
                hierarchy = [category_slug]
                markdown = concept.to_markdown(filepath, hierarchy)

                # Write file
                filepath.write_text(markdown, encoding='utf-8')

            # Generate index file for category
            self._generate_category_index(category_dir, category, concept_names)

        # Generate root index
        self._generate_root_index(concepts_dir)

    def _generate_category_index(self, category_dir: Path, category: str, concept_names: List[str]):
        """Generate index.md for a category."""
        # Filter to concepts with definitions
        valid_concepts = [name for name in concept_names if self.concepts[name].definitions]

        if not valid_concepts:
            return

        category_title = category.replace('-', ' ').replace('_', ' ').title()

        content = f"""---
title: {category_title}
---

# {category_title}

This section contains {len(valid_concepts)} concepts related to {category_title.lower()}.

## Concepts

"""

        for concept_name in sorted(valid_concepts):
            concept = self.concepts[concept_name]
            filename = concept_name.lower().replace(' ', '-').replace('_', '-')
            filename = re.sub(r'[^a-z0-9-]', '', filename)
            filename = re.sub(r'-+', '-', filename).strip('-')

            if filename:
                # Get first sentence of definition
                first_def = concept.definitions[0] if concept.definitions else ""
                first_sentence = first_def.split('.')[0] + '.' if first_def else ""

                content += f"- [[{filename}|{concept_name}]]: {first_sentence}\n"

        index_path = category_dir / "index.md"
        index_path.write_text(content, encoding='utf-8')

    def _generate_root_index(self, concepts_dir: Path):
        """Generate root index.md for all concepts."""
        content = """---
title: Knowledge Base
---

# Knowledge Base

This knowledge base was automatically generated from LaTeX sources and cited papers.

## Categories

"""

        for category in sorted(self.categories.keys()):
            category_slug = category.lower().replace(' ', '-').replace('_', '-')
            category_title = category.replace('-', ' ').replace('_', ' ').title()

            # Count concepts with definitions
            valid_count = sum(1 for name in self.categories[category]
                            if self.concepts[name].definitions)

            if valid_count > 0:
                content += f"- [[{category_slug}/index|{category_title}]] ({valid_count} concepts)\n"

        content += f"\n\n---\n\n*Total concepts: {len([c for c in self.concepts.values() if c.definitions])}*\n"

        index_path = concepts_dir / "index.md"
        index_path.write_text(content, encoding='utf-8')


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Automated semantic analysis for knowledge base generation"
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
        help="Repository root directory"
    )
    parser.add_argument(
        "--analysis-data",
        type=Path,
        required=True,
        help="Path to analysis-data.json"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("knowledge-database"),
        help="Output directory for knowledge base"
    )

    args = parser.parse_args()

    analyzer = SemanticAnalyzer(args.repo_root, args.output_dir)
    analyzer.analyze(args.analysis_data)

    print("\n✅ Automated semantic analysis complete!")


if __name__ == '__main__':
    main()
