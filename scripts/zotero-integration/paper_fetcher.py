#!/usr/bin/env python3
"""
Paper Fetcher - Retrieves paper content from Zotero library.

This module fetches papers cited in LaTeX sources to extract concepts for
knowledge base expansion (Γ → Γ⁺).

Supported sources:
1. Zotero library (metadata, abstracts, attachments)
"""

import os
import re
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, asdict


@dataclass
class PaperContent:
    """Represents the fetched content of a paper."""
    bibkey: str
    title: str
    authors: List[str]
    year: Optional[int]
    abstract: Optional[str]
    keywords: List[str]
    doi: Optional[str]
    url: Optional[str]
    source: str  # Which source provided this data
    full_text_available: bool

    def to_dict(self):
        return asdict(self)


class PaperFetcher:
    """Fetches paper content from Zotero library."""

    def __init__(self, group_id: str = "6182921"):
        """
        Initialize the paper fetcher.

        Args:
            group_id: Zotero group ID
        """
        self.group_id = group_id

        # Cache for fetched papers
        self.cache: Dict[str, PaperContent] = {}

    def fetch_paper_content(self,
                          bibkey: str,
                          zotero_item: Optional[Dict] = None,
                          bib_entry: Optional[Dict] = None) -> Optional[PaperContent]:
        """
        Fetch paper content from Zotero library.

        Args:
            bibkey: Bibliography key
            zotero_item: Zotero item data (if available)
            bib_entry: BibTeX entry data (not used, for compatibility)

        Returns:
            PaperContent if found in Zotero, None otherwise
        """
        # Check cache first
        if bibkey in self.cache:
            return self.cache[bibkey]

        # Only use Zotero library
        if zotero_item:
            content = self._fetch_from_zotero(bibkey, zotero_item)
            if content:
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
                keywords=keywords,
                doi=doi,
                url=url,
                source='zotero',
                full_text_available=len(zotero_item.get('attachments', [])) > 0
            )
        except Exception as e:
            print(f"Warning: Error fetching from Zotero for {bibkey}: {e}", file=sys.stderr)
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

    parser = argparse.ArgumentParser(description="Fetch paper content from Zotero library")
    parser.add_argument('--bibkey', required=True, help='Bibliography key to fetch')

    args = parser.parse_args()

    fetcher = PaperFetcher()

    # Note: This example won't work without actual Zotero data
    # In real use, zotero_item would come from the Zotero manifest
    print(f"PaperFetcher initialized for bibkey: {args.bibkey}")
    print("Note: Requires Zotero manifest data to fetch papers")


if __name__ == '__main__':
    main()
