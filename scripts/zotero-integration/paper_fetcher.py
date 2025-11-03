#!/usr/bin/env python3
"""
Paper Fetcher - Retrieves full paper content from multiple sources.

This module fetches papers cited in LaTeX sources to extract concepts for
knowledge base expansion (Γ → Γ⁺).

Supported sources:
1. Zotero library (PDFs, abstracts)
2. Semantic Scholar API (abstracts, TLDRs, citations)
3. arXiv API (preprints)
4. CrossRef API (metadata)
"""

import os
import re
import sys
import json
import time
import requests
from pathlib import Path
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, asdict
from urllib.parse import quote


@dataclass
class PaperContent:
    """Represents the fetched content of a paper."""
    bibkey: str
    title: str
    authors: List[str]
    year: Optional[int]
    abstract: Optional[str]
    tldr: Optional[str]  # Semantic Scholar's AI-generated summary
    keywords: List[str]
    doi: Optional[str]
    arxiv_id: Optional[str]
    url: Optional[str]
    citation_count: int
    influential_citation_count: int
    source: str  # Which API/source provided this data
    full_text_available: bool

    def to_dict(self):
        return asdict(self)


class PaperFetcher:
    """Fetches paper content from multiple sources."""

    def __init__(self,
                 zotero_api_key: Optional[str] = None,
                 semantic_scholar_api_key: Optional[str] = None,
                 group_id: str = "6182921"):
        """
        Initialize the paper fetcher.

        Args:
            zotero_api_key: Zotero API key
            semantic_scholar_api_key: Semantic Scholar API key (optional)
            group_id: Zotero group ID
        """
        self.zotero_api_key = zotero_api_key
        self.s2_api_key = semantic_scholar_api_key
        self.group_id = group_id

        # Rate limiting
        self.last_s2_request = 0
        self.s2_delay = 1.0  # Seconds between S2 requests
        self.last_crossref_request = 0
        self.crossref_delay = 1.0

        # Cache for fetched papers
        self.cache: Dict[str, PaperContent] = {}

    def fetch_paper_content(self,
                          bibkey: str,
                          zotero_item: Optional[Dict] = None,
                          bib_entry: Optional[Dict] = None) -> Optional[PaperContent]:
        """
        Fetch full content of a paper from multiple sources.

        Args:
            bibkey: Bibliography key
            zotero_item: Zotero item data (if available)
            bib_entry: BibTeX entry data (if available)

        Returns:
            PaperContent if found, None otherwise
        """
        # Check cache first
        if bibkey in self.cache:
            return self.cache[bibkey]

        content = None

        # Try Zotero first if we have the item
        if zotero_item:
            content = self._fetch_from_zotero(bibkey, zotero_item)
            if content:
                self.cache[bibkey] = content
                return content

        # Extract DOI or arXiv ID from bib_entry if available
        doi = None
        arxiv_id = None
        if bib_entry:
            doi = bib_entry.get('doi')
            arxiv_id = self._extract_arxiv_id(bib_entry)

        # Try Semantic Scholar
        if doi or (zotero_item and zotero_item.get('doi')):
            doi = doi or zotero_item.get('doi')
            content = self._fetch_from_semantic_scholar(bibkey, doi=doi)
            if content:
                self.cache[bibkey] = content
                return content

        # Try arXiv
        if arxiv_id:
            content = self._fetch_from_arxiv(bibkey, arxiv_id)
            if content:
                self.cache[bibkey] = content
                return content

        # Fallback to CrossRef
        if doi:
            content = self._fetch_from_crossref(bibkey, doi)
            if content:
                self.cache[bibkey] = content
                return content

        # If we have Zotero item but no other data, create minimal PaperContent
        if zotero_item:
            content = self._create_from_zotero_metadata(bibkey, zotero_item)
            self.cache[bibkey] = content
            return content

        return None

    def _fetch_from_zotero(self, bibkey: str, zotero_item: Dict) -> Optional[PaperContent]:
        """Fetch paper content from Zotero item."""
        try:
            # Extract basic metadata
            title = zotero_item.get('title', '')
            abstract = zotero_item.get('abstract')
            doi = zotero_item.get('doi')
            url = zotero_item.get('url')

            # Parse authors
            authors = []
            creators = zotero_item.get('creators', [])
            for creator in creators:
                if creator.get('creator_type') in ['author', 'editor']:
                    name = f"{creator.get('first_name', '')} {creator.get('last_name', '')}".strip()
                    if name:
                        authors.append(name)

            # Extract year
            year = None
            date_str = zotero_item.get('date', '')
            year_match = re.search(r'\b(19|20)\d{2}\b', date_str)
            if year_match:
                year = int(year_match.group())

            # Extract keywords from tags
            keywords = [tag.strip() for tag in zotero_item.get('tags', [])]

            return PaperContent(
                bibkey=bibkey,
                title=title,
                authors=authors,
                year=year,
                abstract=abstract,
                tldr=None,
                keywords=keywords,
                doi=doi,
                arxiv_id=None,
                url=url,
                citation_count=0,
                influential_citation_count=0,
                source='zotero',
                full_text_available=len(zotero_item.get('attachments', [])) > 0
            )
        except Exception as e:
            print(f"Warning: Error fetching from Zotero for {bibkey}: {e}", file=sys.stderr)
            return None

    def _create_from_zotero_metadata(self, bibkey: str, zotero_item: Dict) -> PaperContent:
        """Create minimal PaperContent from Zotero metadata."""
        return self._fetch_from_zotero(bibkey, zotero_item)

    def _fetch_from_semantic_scholar(self,
                                     bibkey: str,
                                     doi: Optional[str] = None,
                                     title: Optional[str] = None) -> Optional[PaperContent]:
        """Fetch paper content from Semantic Scholar API."""
        try:
            # Rate limiting
            now = time.time()
            time_since_last = now - self.last_s2_request
            if time_since_last < self.s2_delay:
                time.sleep(self.s2_delay - time_since_last)

            # Build API URL
            if doi:
                paper_id = f"DOI:{doi}"
            elif title:
                paper_id = f"TITLE:{title}"
            else:
                return None

            url = f"https://api.semanticscholar.org/graph/v1/paper/{quote(paper_id)}"
            params = {
                'fields': 'title,authors,year,abstract,tldr,citationCount,influentialCitationCount,externalIds,url'
            }

            headers = {}
            if self.s2_api_key:
                headers['x-api-key'] = self.s2_api_key

            response = requests.get(url, params=params, headers=headers, timeout=10)
            self.last_s2_request = time.time()

            if response.status_code != 200:
                return None

            data = response.json()

            # Extract data
            authors = [author['name'] for author in data.get('authors', [])]
            external_ids = data.get('externalIds', {})

            return PaperContent(
                bibkey=bibkey,
                title=data.get('title', ''),
                authors=authors,
                year=data.get('year'),
                abstract=data.get('abstract'),
                tldr=data.get('tldr', {}).get('text') if data.get('tldr') else None,
                keywords=[],  # S2 doesn't provide keywords directly
                doi=external_ids.get('DOI'),
                arxiv_id=external_ids.get('ArXiv'),
                url=data.get('url'),
                citation_count=data.get('citationCount', 0),
                influential_citation_count=data.get('influentialCitationCount', 0),
                source='semantic_scholar',
                full_text_available=False
            )

        except Exception as e:
            print(f"Warning: Error fetching from Semantic Scholar for {bibkey}: {e}", file=sys.stderr)
            return None

    def _fetch_from_arxiv(self, bibkey: str, arxiv_id: str) -> Optional[PaperContent]:
        """Fetch paper content from arXiv API."""
        try:
            url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
            response = requests.get(url, timeout=10)

            if response.status_code != 200:
                return None

            # Parse XML response (simplified - would need proper XML parsing)
            content = response.text

            # Extract title
            title_match = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
            title = title_match.group(1).strip() if title_match else ''

            # Extract authors
            author_matches = re.findall(r'<name>(.*?)</name>', content)
            authors = [a.strip() for a in author_matches]

            # Extract abstract
            abstract_match = re.search(r'<summary>(.*?)</summary>', content, re.DOTALL)
            abstract = abstract_match.group(1).strip() if abstract_match else None

            # Extract year from published date
            year = None
            date_match = re.search(r'<published>(\d{4})', content)
            if date_match:
                year = int(date_match.group(1))

            return PaperContent(
                bibkey=bibkey,
                title=title,
                authors=authors,
                year=year,
                abstract=abstract,
                tldr=None,
                keywords=[],
                doi=None,
                arxiv_id=arxiv_id,
                url=f"https://arxiv.org/abs/{arxiv_id}",
                citation_count=0,
                influential_citation_count=0,
                source='arxiv',
                full_text_available=True
            )

        except Exception as e:
            print(f"Warning: Error fetching from arXiv for {bibkey}: {e}", file=sys.stderr)
            return None

    def _fetch_from_crossref(self, bibkey: str, doi: str) -> Optional[PaperContent]:
        """Fetch paper metadata from CrossRef API."""
        try:
            # Rate limiting
            now = time.time()
            time_since_last = now - self.last_crossref_request
            if time_since_last < self.crossref_delay:
                time.sleep(self.crossref_delay - time_since_last)

            url = f"https://api.crossref.org/works/{doi}"
            response = requests.get(url, timeout=10)
            self.last_crossref_request = time.time()

            if response.status_code != 200:
                return None

            data = response.json()['message']

            # Extract authors
            authors = []
            for author in data.get('author', []):
                name = f"{author.get('given', '')} {author.get('family', '')}".strip()
                if name:
                    authors.append(name)

            # Extract year
            year = None
            published = data.get('published-print') or data.get('published-online')
            if published and 'date-parts' in published:
                date_parts = published['date-parts'][0]
                if date_parts:
                    year = date_parts[0]

            # Extract title
            title = ''
            if data.get('title'):
                title = data['title'][0]

            # Extract abstract (if available)
            abstract = data.get('abstract')

            return PaperContent(
                bibkey=bibkey,
                title=title,
                authors=authors,
                year=year,
                abstract=abstract,
                tldr=None,
                keywords=data.get('subject', []),
                doi=doi,
                arxiv_id=None,
                url=data.get('URL'),
                citation_count=data.get('is-referenced-by-count', 0),
                influential_citation_count=0,
                source='crossref',
                full_text_available=False
            )

        except Exception as e:
            print(f"Warning: Error fetching from CrossRef for {bibkey}: {e}", file=sys.stderr)
            return None

    def _extract_arxiv_id(self, bib_entry: Dict) -> Optional[str]:
        """Extract arXiv ID from BibTeX entry."""
        # Look for arXiv ID in various fields
        for field in ['eprint', 'archiveprefix', 'note', 'url']:
            value = bib_entry.get(field, '')
            match = re.search(r'(\d{4}\.\d{4,5})', str(value))
            if match:
                return match.group(1)
        return None

    def extract_concepts_from_paper(self, content: PaperContent) -> List[str]:
        """
        Extract key concepts from paper content.

        This is a heuristic-based extraction. For better results,
        consider using NLP techniques or LLM-based extraction.

        Returns:
            List of concept strings
        """
        concepts = set()

        # Extract from title
        title_concepts = self._extract_title_concepts(content.title)
        concepts.update(title_concepts)

        # Extract from abstract
        if content.abstract:
            abstract_concepts = self._extract_abstract_concepts(content.abstract)
            concepts.update(abstract_concepts)

        # Extract from TLDR
        if content.tldr:
            tldr_concepts = self._extract_abstract_concepts(content.tldr)
            concepts.update(tldr_concepts)

        # Use keywords directly
        concepts.update(content.keywords)

        return list(concepts)

    def _extract_title_concepts(self, title: str) -> Set[str]:
        """Extract concepts from paper title."""
        concepts = set()

        # Remove common words
        stopwords = {'a', 'an', 'the', 'of', 'in', 'on', 'at', 'to', 'for', 'and', 'or', 'but'}

        # Extract significant words (simplified)
        words = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', title)
        for word in words:
            word_lower = word.lower()
            if word_lower not in stopwords and len(word) > 3:
                concepts.add(word_lower)

        return concepts

    def _extract_abstract_concepts(self, abstract: str) -> Set[str]:
        """Extract concepts from abstract."""
        concepts = set()

        # Look for technical terms (capitalized phrases)
        technical_terms = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', abstract)

        # Look for terms in quotes or italics (common for concept definitions)
        quoted_terms = re.findall(r'["\']([^"\']+)["\']', abstract)

        concepts.update(term.lower() for term in technical_terms if len(term) > 3)
        concepts.update(term.lower() for term in quoted_terms if len(term) > 3)

        return concepts

    def save_cache(self, cache_file: Path) -> None:
        """Save the fetched papers cache to a JSON file."""
        cache_data = {bibkey: content.to_dict() for bibkey, content in self.cache.items()}

        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, indent=2, ensure_ascii=False)

        print(f"Saved {len(cache_data)} papers to cache: {cache_file}")

    def load_cache(self, cache_file: Path) -> None:
        """Load previously fetched papers from cache."""
        if not cache_file.exists():
            return

        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)

            for bibkey, data in cache_data.items():
                self.cache[bibkey] = PaperContent(**data)

            print(f"Loaded {len(cache_data)} papers from cache: {cache_file}")

        except Exception as e:
            print(f"Warning: Could not load cache from {cache_file}: {e}", file=sys.stderr)


def main():
    """Example usage of PaperFetcher."""
    import argparse

    parser = argparse.ArgumentParser(description="Fetch paper content from multiple sources")
    parser.add_argument('--bibkey', required=True, help='Bibliography key to fetch')
    parser.add_argument('--doi', help='DOI of the paper')
    parser.add_argument('--arxiv', help='arXiv ID of the paper')
    parser.add_argument('--zotero-api-key', default=os.environ.get('ZOTERO_API_KEY'))
    parser.add_argument('--s2-api-key', default=os.environ.get('SEMANTIC_SCHOLAR_API_KEY'))

    args = parser.parse_args()

    fetcher = PaperFetcher(
        zotero_api_key=args.zotero_api_key,
        semantic_scholar_api_key=args.s2_api_key
    )

    bib_entry = {}
    if args.doi:
        bib_entry['doi'] = args.doi
    if args.arxiv:
        bib_entry['eprint'] = args.arxiv

    content = fetcher.fetch_paper_content(args.bibkey, bib_entry=bib_entry)

    if content:
        print(json.dumps(content.to_dict(), indent=2))

        concepts = fetcher.extract_concepts_from_paper(content)
        print("\nExtracted concepts:")
        for concept in concepts:
            print(f"  - {concept}")
    else:
        print(f"Could not fetch content for {args.bibkey}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
