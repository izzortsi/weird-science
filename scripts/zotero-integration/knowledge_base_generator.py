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
                # Simple extraction of bibkeys
                pattern = r'@\w+\s*{\s*([^,\s]+)\s*,'
                for match in re.finditer(pattern, content):
                    bibkey = match.group(1)
                    bib_entries[bibkey] = {
                        'key': bibkey,
                        'file': str(bib_file.relative_to(self.repo_root))
                    }
            except Exception as e:
                print(f"Warning: Could not read {bib_file}: {e}", file=sys.stderr)
        
        return bib_entries
    
    def prepare_analysis_data(self) -> Dict:
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
            'bibliography_keys': list(self.bib_entries.keys())
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
    
    def generate(self, force: bool = False) -> None:
        """Main generation workflow."""
        print("=" * 70)
        print("Knowledge Base Generator - Semantic Analysis Orchestration")
        print("=" * 70)
        print(f"Repository: {self.repo_root}")
        print(f"Manifest: {self.manifest_path}")
        print(f"Output: {self.output_dir}")
        print()
        
        # Prepare analysis data
        print("Preparing analysis data...")
        analysis_data = self.prepare_analysis_data()
        print(f"  ✓ Projects: {analysis_data['total_projects']}")
        print(f"  ✓ LaTeX files: {analysis_data['total_latex_files']}")
        print(f"  ✓ Citations: {analysis_data['total_citations']}")
        print(f"  ✓ Zotero items: {analysis_data['total_zotero_items']}")
        print()
        
        # Save analysis data
        analysis_file = self.save_analysis_data(analysis_data)
        print(f"✓ Saved analysis data: {analysis_file}")
        
        # Generate Claude prompt
        print("\nGenerating Claude Code prompt...")
        prompt = self.generate_claude_prompt(analysis_data)
        prompt_file = self.save_claude_prompt(prompt)
        print(f"✓ Saved Claude prompt: {prompt_file}")
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
        
        print(f"✓ Saved integration instructions: {instructions_file}")


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
    
    args = parser.parse_args()
    
    repo_root = Path.cwd()
    manifest_path = Path(args.manifest)
    output_dir = Path(args.output_dir)
    
    generator = KnowledgeBaseGenerator(repo_root, manifest_path, output_dir)
    generator.generate(force=args.force)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
