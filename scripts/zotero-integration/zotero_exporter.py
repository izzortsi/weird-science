#!/usr/bin/env python3
"""
Zotero Integration Script for weird-science repository.

This script:
1. Scans the repository for project folders (containing README.md and main.tex)
2. Extracts citation keys from .tex files
3. Parses .bib files to map bibkeys to DOIs/titles
4. Fetches items from Zotero group library
5. Matches Zotero items to bibliography entries
6. Generates project-summary.md files
7. Creates knowledge-database/ with atomic concept articles
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import requests


@dataclass
class BibEntry:
    """Represents a bibliography entry."""
    key: str
    title: Optional[str] = None
    doi: Optional[str] = None
    author: Optional[str] = None
    year: Optional[str] = None
    type: Optional[str] = None
    raw: str = ""


@dataclass
class ZoteroItem:
    """Represents a Zotero library item."""
    key: str
    title: str
    doi: Optional[str] = None
    authors: List[str] = None
    year: Optional[str] = None
    item_type: Optional[str] = None
    url: Optional[str] = None
    abstract: Optional[str] = None
    tags: List[str] = None
    collections: List[str] = None
    
    def __post_init__(self):
        if self.authors is None:
            self.authors = []
        if self.tags is None:
            self.tags = []
        if self.collections is None:
            self.collections = []


@dataclass
class ProjectInfo:
    """Information about a project folder."""
    path: Path
    name: str
    readme_path: Path
    main_tex_path: Path
    bib_files: List[Path]
    cited_keys: Set[str]
    bib_entries: Dict[str, BibEntry]


class BibParser:
    """Parser for BibTeX files."""
    
    @staticmethod
    def parse_bib_file(filepath: Path) -> Dict[str, BibEntry]:
        """Parse a BibTeX file and return a dictionary of entries."""
        entries = {}
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Warning: Could not read {filepath}: {e}")
            return entries
        
        # Simple regex-based BibTeX parser
        # Match @type{key, ... }
        entry_pattern = r'@(\w+)\s*{\s*([^,\s]+)\s*,(.*?)(?=\n@|\Z)'
        
        for match in re.finditer(entry_pattern, content, re.DOTALL | re.IGNORECASE):
            entry_type = match.group(1)
            key = match.group(2)
            fields_text = match.group(3)
            
            entry = BibEntry(key=key, type=entry_type, raw=match.group(0))
            
            # Extract common fields
            title_match = re.search(r'title\s*=\s*[{"](.+?)[}"]', fields_text, re.DOTALL | re.IGNORECASE)
            if title_match:
                entry.title = BibParser.clean_latex(title_match.group(1))
            
            doi_match = re.search(r'doi\s*=\s*[{"](.+?)[}"]', fields_text, re.IGNORECASE)
            if doi_match:
                entry.doi = doi_match.group(1).strip()
            
            author_match = re.search(r'author\s*=\s*[{"](.+?)[}"]', fields_text, re.DOTALL | re.IGNORECASE)
            if author_match:
                entry.author = author_match.group(1)
            
            year_match = re.search(r'year\s*=\s*[{"]?(\d{4})[}"]?', fields_text, re.IGNORECASE)
            if year_match:
                entry.year = year_match.group(1)
            
            entries[key] = entry
        
        return entries
    
    @staticmethod
    def clean_latex(text: str) -> str:
        """Remove common LaTeX formatting from text."""
        # Remove braces
        text = re.sub(r'[{}]', '', text)
        # Remove common LaTeX commands
        text = re.sub(r'\\[a-zA-Z]+\s*', '', text)
        # Clean up whitespace
        text = ' '.join(text.split())
        return text.strip()


class CitationExtractor:
    """Extracts citation keys from LaTeX files."""
    
    @staticmethod
    def extract_citations_from_file(filepath: Path) -> Set[str]:
        """Extract citation keys from a LaTeX file."""
        citations = set()
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Warning: Could not read {filepath}: {e}")
            return citations
        
        # Match various citation commands: \cite{}, \citep{}, \citet{}, \autocite{}, etc.
        cite_pattern = r'\\(?:cite|citep|citet|autocite|textcite|parencite|footcite)(?:\[.*?\])?\{([^}]+)\}'
        
        for match in re.finditer(cite_pattern, content):
            keys_str = match.group(1)
            # Split by comma for multiple citations
            for key in keys_str.split(','):
                key = key.strip()
                if key:
                    citations.add(key)
        
        return citations


class ZoteroClient:
    """Client for Zotero API."""
    
    def __init__(self, group_id: str, api_key: Optional[str] = None):
        self.group_id = group_id
        self.api_key = api_key
        self.base_url = f"https://api.zotero.org/groups/{group_id}"
        self.headers = {}
        if api_key:
            self.headers['Zotero-API-Key'] = api_key
    
    def get_all_items(self, limit: int = 100) -> List[ZoteroItem]:
        """Fetch all items from the Zotero group library."""
        items = []
        start = 0
        
        while True:
            url = f"{self.base_url}/items"
            params = {
                'start': start,
                'limit': limit,
                'format': 'json'
            }
            
            try:
                response = requests.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                batch = response.json()
                
                if not batch:
                    break
                
                for item_data in batch:
                    item = self._parse_item(item_data)
                    if item:
                        items.append(item)
                
                start += len(batch)
                
                # Check if we've received all items
                if len(batch) < limit:
                    break
                    
            except Exception as e:
                print(f"Error fetching Zotero items: {e}")
                break
        
        return items
    
    def _parse_item(self, data: Dict) -> Optional[ZoteroItem]:
        """Parse a Zotero API item response."""
        if data.get('data', {}).get('itemType') == 'attachment':
            return None
        
        item_data = data.get('data', {})
        key = data.get('key', '')
        
        # Extract authors
        authors = []
        for creator in item_data.get('creators', []):
            if 'lastName' in creator:
                name = creator.get('lastName', '')
                if 'firstName' in creator:
                    name = f"{creator['firstName']} {name}"
                authors.append(name)
        
        # Extract DOI
        doi = item_data.get('DOI', '') or item_data.get('doi', '')
        
        # Extract tags
        tags = [tag.get('tag', '') for tag in item_data.get('tags', [])]
        
        return ZoteroItem(
            key=key,
            title=item_data.get('title', ''),
            doi=doi if doi else None,
            authors=authors,
            year=item_data.get('date', '')[:4] if item_data.get('date') else None,
            item_type=item_data.get('itemType'),
            url=item_data.get('url'),
            abstract=item_data.get('abstractNote'),
            tags=tags,
            collections=data.get('collections', [])
        )


class ProjectScanner:
    """Scans repository for project folders."""
    
    @staticmethod
    def find_projects(repo_root: Path) -> List[ProjectInfo]:
        """Find all project folders containing README.md and main.tex."""
        projects = []
        
        # Look for directories containing both README.md and a .tex file
        for readme in repo_root.rglob('README.md'):
            project_dir = readme.parent
            
            # Skip root README
            if project_dir == repo_root:
                continue
            
            # Look for main.tex or other .tex files
            tex_files = list(project_dir.glob('*.tex'))
            main_tex = project_dir / 'main.tex'
            
            if main_tex.exists():
                tex_file = main_tex
            elif tex_files:
                tex_file = tex_files[0]
            else:
                continue
            
            # Find all .bib files in the project
            bib_files = list(project_dir.rglob('*.bib'))
            
            # Extract citations from all .tex files in the project
            cited_keys = set()
            for tex in project_dir.rglob('*.tex'):
                cited_keys.update(CitationExtractor.extract_citations_from_file(tex))
            
            # Parse bib files
            bib_entries = {}
            for bib_file in bib_files:
                bib_entries.update(BibParser.parse_bib_file(bib_file))
            
            project = ProjectInfo(
                path=project_dir,
                name=project_dir.name,
                readme_path=readme,
                main_tex_path=tex_file,
                bib_files=bib_files,
                cited_keys=cited_keys,
                bib_entries=bib_entries
            )
            
            projects.append(project)
        
        return projects


class ZoteroMatcher:
    """Matches bibliography entries with Zotero items."""
    
    @staticmethod
    def match_items(
        bib_entries: Dict[str, BibEntry],
        zotero_items: List[ZoteroItem],
        cited_keys: Set[str]
    ) -> Dict[str, ZoteroItem]:
        """Match bibliography entries to Zotero items."""
        matches = {}
        
        # Create lookup dictionaries
        zotero_by_doi = {item.doi.lower(): item for item in zotero_items if item.doi}
        zotero_by_title = {item.title.lower(): item for item in zotero_items if item.title}
        
        for bibkey in cited_keys:
            if bibkey not in bib_entries:
                continue
            
            bib_entry = bib_entries[bibkey]
            
            # Try matching by DOI first
            if bib_entry.doi:
                doi_lower = bib_entry.doi.lower()
                if doi_lower in zotero_by_doi:
                    matches[bibkey] = zotero_by_doi[doi_lower]
                    continue
            
            # Try matching by title
            if bib_entry.title:
                title_lower = bib_entry.title.lower()
                # Exact match
                if title_lower in zotero_by_title:
                    matches[bibkey] = zotero_by_title[title_lower]
                    continue
                
                # Fuzzy match (simple substring matching)
                for ztitle, zitem in zotero_by_title.items():
                    if ZoteroMatcher._titles_match(title_lower, ztitle):
                        matches[bibkey] = zitem
                        break
        
        return matches
    
    @staticmethod
    def _titles_match(title1: str, title2: str, threshold: float = 0.8) -> bool:
        """Check if two titles are similar enough to be considered a match."""
        # Simple similarity check based on common words
        words1 = set(re.findall(r'\w+', title1.lower()))
        words2 = set(re.findall(r'\w+', title2.lower()))
        
        if not words1 or not words2:
            return False
        
        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with'}
        words1 = words1 - stop_words
        words2 = words2 - stop_words
        
        if not words1 or not words2:
            return False
        
        intersection = words1 & words2
        union = words1 | words2
        
        jaccard_similarity = len(intersection) / len(union)
        return jaccard_similarity >= threshold


class MarkdownGenerator:
    """Generates markdown files for projects and knowledge base."""
    
    @staticmethod
    def generate_project_summary(
        project: ProjectInfo,
        matches: Dict[str, ZoteroItem],
        group_id: str,
        output_path: Path
    ):
        """Generate project-summary.md for a project."""
        
        # Read README content for context
        readme_content = ""
        try:
            with open(project.readme_path, 'r', encoding='utf-8') as f:
                readme_content = f.read()
        except Exception as e:
            print(f"Warning: Could not read README at {project.readme_path}: {e}")
        
        # Extract title from README (first # heading)
        title_match = re.search(r'^#\s+(.+)$', readme_content, re.MULTILINE)
        title = title_match.group(1) if title_match else project.name
        
        # Build YAML frontmatter
        matched_bibkeys = list(matches.keys())
        zotero_keys = [matches[bk].key for bk in matched_bibkeys]
        
        frontmatter = {
            'title': title,
            'project': project.name,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'tags': ['zotero', 'literature-review', project.name],
            'zotero_keys': zotero_keys,
            'matched_bibkeys': matched_bibkeys
        }
        
        # Build markdown content
        md_content = []
        md_content.append('---')
        for key, value in frontmatter.items():
            if isinstance(value, list):
                md_content.append(f'{key}:')
                for item in value:
                    md_content.append(f'  - {item}')
            else:
                # Quote strings that contain special YAML characters (colons, etc.)
                if isinstance(value, str) and (':' in value or value.startswith(('*', '&', '!', '|', '>', '{', '['))):
                    value = json.dumps(value)
                md_content.append(f'{key}: {value}')
        md_content.append('---')
        md_content.append('')
        md_content.append(f'# {title} - Literature Summary')
        md_content.append('')
        md_content.append('This document provides a summary of the references used in this project, ')
        md_content.append('with links to the corresponding items in the Zotero group library.')
        md_content.append('')
        
        # Add references section
        if matches:
            md_content.append('## References')
            md_content.append('')
            
            # Sort by bibkey
            for bibkey in sorted(matches.keys()):
                zitem = matches[bibkey]
                bib_entry = project.bib_entries.get(bibkey)
                
                # Create reference entry
                authors_str = ', '.join(zitem.authors[:3]) if zitem.authors else 'Unknown'
                if len(zitem.authors) > 3:
                    authors_str += ' et al.'
                
                year_str = f" ({zitem.year})" if zitem.year else ""
                
                md_content.append(f'### {bibkey}')
                md_content.append('')
                md_content.append(f'**{zitem.title}**')
                md_content.append('')
                md_content.append(f'*{authors_str}{year_str}*')
                md_content.append('')
                
                # Add Zotero link
                zotero_url = f'https://www.zotero.org/groups/{group_id}/items/{zitem.key}'
                md_content.append(f'[View in Zotero Library]({zotero_url})')
                md_content.append('')
                
                # Add DOI link if available
                if zitem.doi:
                    md_content.append(f'DOI: [{zitem.doi}](https://doi.org/{zitem.doi})')
                    md_content.append('')
                
                # Add abstract if available
                if zitem.abstract:
                    md_content.append('**Abstract:**')
                    md_content.append('')
                    md_content.append(zitem.abstract)
                    md_content.append('')
                
                md_content.append('---')
                md_content.append('')
        else:
            md_content.append('*No matched references found.*')
            md_content.append('')
        
        # Write to file
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(md_content))
            print(f"Generated: {output_path}")
        except Exception as e:
            print(f"Error writing {output_path}: {e}")
    
    @staticmethod
    def generate_knowledge_base(
        zotero_items: List[ZoteroItem],
        output_dir: Path,
        group_id: str
    ):
        """Generate atomic concept articles in knowledge-database/."""
        
        # Create directories for different categories
        categories_dir = output_dir / 'concepts'
        categories_dir.mkdir(parents=True, exist_ok=True)
        
        # Group items by tags
        items_by_tag = {}
        for item in zotero_items:
            for tag in item.tags:
                if tag not in items_by_tag:
                    items_by_tag[tag] = []
                items_by_tag[tag].append(item)
        
        # Create an index file
        index_content = []
        index_content.append('# Knowledge Database')
        index_content.append('')
        index_content.append('This directory contains atomic concept articles extracted from the Zotero group library.')
        index_content.append('')
        index_content.append('## Concepts by Tag')
        index_content.append('')
        
        for tag in sorted(items_by_tag.keys()):
            # Create sanitized filename
            filename = re.sub(r'[^\w\s-]', '', tag.lower())
            filename = re.sub(r'[-\s]+', '-', filename)
            tag_file = categories_dir / f'{filename}.md'
            
            index_content.append(f'- [{tag}](concepts/{filename}.md) ({len(items_by_tag[tag])} items)')
            
            # Create tag-specific file
            tag_content = []
            tag_content.append(f'# {tag}')
            tag_content.append('')
            tag_content.append(f'Related items from the Zotero library tagged with "{tag}":')
            tag_content.append('')
            
            for item in items_by_tag[tag]:
                authors_str = ', '.join(item.authors[:2]) if item.authors else 'Unknown'
                if len(item.authors) > 2:
                    authors_str += ' et al.'
                year_str = f" ({item.year})" if item.year else ""
                
                tag_content.append(f'## {item.title}')
                tag_content.append('')
                tag_content.append(f'*{authors_str}{year_str}*')
                tag_content.append('')
                
                zotero_url = f'https://www.zotero.org/groups/{group_id}/items/{item.key}'
                tag_content.append(f'[View in Zotero]({zotero_url})')
                
                if item.doi:
                    tag_content.append(f' | [DOI](https://doi.org/{item.doi})')
                
                tag_content.append('')
                
                if item.abstract:
                    # Truncate abstract to first 500 chars
                    abstract = item.abstract[:500]
                    if len(item.abstract) > 500:
                        abstract += '...'
                    tag_content.append(f'{abstract}')
                    tag_content.append('')
                
                tag_content.append('---')
                tag_content.append('')
            
            try:
                with open(tag_file, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(tag_content))
            except Exception as e:
                print(f"Error writing {tag_file}: {e}")
        
        index_content.append('')
        
        # Write index
        index_path = output_dir / 'README.md'
        try:
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(index_content))
            print(f"Generated knowledge base index: {index_path}")
        except Exception as e:
            print(f"Error writing {index_path}: {e}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Export Zotero group library data to markdown summaries'
    )
    parser.add_argument(
        '--group-id',
        default=os.environ.get('ZOTERO_GROUP_ID', '6182921'),
        help='Zotero group ID (default: 6182921 or $ZOTERO_GROUP_ID)'
    )
    parser.add_argument(
        '--api-key',
        default=os.environ.get('ZOTERO_API_KEY'),
        help='Zotero API key (default: $ZOTERO_API_KEY)'
    )
    parser.add_argument(
        '--repo-root',
        type=Path,
        default=Path.cwd(),
        help='Repository root directory (default: current directory)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Run without generating files'
    )
    
    args = parser.parse_args()
    
    print("="*60)
    print("Zotero Integration for weird-science")
    print("="*60)
    print(f"Repository root: {args.repo_root}")
    print(f"Zotero group ID: {args.group_id}")
    print(f"API key: {'Set' if args.api_key else 'Not set (using public access)'}")
    print()
    
    # Step 1: Scan for projects
    print("Step 1: Scanning for projects...")
    projects = ProjectScanner.find_projects(args.repo_root)
    print(f"Found {len(projects)} projects:")
    for project in projects:
        print(f"  - {project.name} ({len(project.cited_keys)} citations)")
    print()
    
    # Step 2: Fetch Zotero items
    print("Step 2: Fetching Zotero items...")
    client = ZoteroClient(args.group_id, args.api_key)
    try:
        zotero_items = client.get_all_items()
        print(f"Fetched {len(zotero_items)} items from Zotero")
    except Exception as e:
        print(f"Error fetching Zotero items: {e}")
        print("Continuing with empty Zotero library...")
        zotero_items = []
    print()
    
    # Step 3: Match and generate summaries
    print("Step 3: Matching citations and generating summaries...")
    for project in projects:
        print(f"\nProcessing project: {project.name}")
        
        # Match citations
        matches = ZoteroMatcher.match_items(
            project.bib_entries,
            zotero_items,
            project.cited_keys
        )
        print(f"  Matched {len(matches)}/{len(project.cited_keys)} citations")
        
        if not args.dry_run:
            # Generate project summary
            summary_path = project.path / 'project-summary.md'
            MarkdownGenerator.generate_project_summary(
                project, matches, args.group_id, summary_path
            )
    
    # Step 4: Knowledge base generation (disabled - use Claude Code instead)
    # The knowledge-database/ atomic concept articles should be generated by Claude Code
    # based on semantic analysis of LaTeX sources (see claude-prompt.md)
    print("\nStep 4: Skipping automated knowledge base generation")
    print("  (Use Claude Code with claude-prompt.md for semantic analysis)")

    print("\n" + "="*60)
    print("Zotero integration complete!")
    print("="*60)


if __name__ == '__main__':
    main()
