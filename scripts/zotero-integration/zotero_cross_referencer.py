#!/usr/bin/env python3
"""
Zotero Cross-Referencer - Expands concepts via full Zotero library search.

This module implements Phase 3 of the knowledge base expansion (Γ⁺ → Γ⁺⁺)
by cross-referencing existing concepts with the complete Zotero library
to find additional papers, alternative definitions, and extended treatments.
"""

import re
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ConceptReference:
    """Represents a reference to a concept in Zotero literature."""
    zotero_key: str
    title: str
    authors: List[str]
    year: Optional[int]
    context: str  # How the concept is mentioned (title, abstract, tag)
    relevance_score: float  # 0.0 to 1.0
    mention_type: str  # 'definition', 'discussion', 'application', 'comparison'


@dataclass
class ConceptExpansion:
    """Represents the expansion of a concept via Zotero cross-referencing."""
    concept_name: str
    additional_papers: List[ConceptReference]
    alternative_definitions: List[str]
    extended_treatments: List[str]
    related_concepts: Set[str]
    cross_references: Dict[str, List[ConceptReference]]


class ZoteroCrossReferencer:
    """
    Cross-references Γ⁺ concepts with full Zotero library (Γ⁺ → Γ⁺⁺ expansion).

    This class searches the complete Zotero library to find:
    - Papers that discuss existing concepts but weren't cited
    - Alternative definitions and perspectives
    - Extended treatments and applications
    - Related concepts and cross-references
    """

    def __init__(self, zotero_manifest: Dict):
        """
        Initialize the cross-referencer with Zotero library data.

        Args:
            zotero_manifest: Complete Zotero manifest with all items
        """
        self.zotero_items = zotero_manifest.get('items', [])
        self.cited_papers: Set[str] = set()  # Will be populated to avoid duplicates

        # Concept variations and synonyms for better matching
        self.concept_variations = {
            'complexity': ['complex', 'complex systems', 'system complexity'],
            'hierarchy': ['hierarchical', 'hierarchies', 'nested systems'],
            'system': ['systems', 'systemic', 'systems theory'],
            'ontology': ['ontological', 'ontologies', 'formal ontology'],
            'emergence': ['emergent', 'emergent properties'],
            'structure': ['structures', 'structural'],
            'model': ['models', 'modeling', 'modelling'],
            'relation': ['relations', 'relationships', 'relational'],
            'property': ['properties', 'attributes'],
            'behavior': ['behaviour', 'behaviors', 'dynamics'],
            'organization': ['organisation', 'organized', 'organised'],
            'network': ['networks', 'networked', 'networking'],
        }

    def set_cited_papers(self, cited_papers: Set[str]):
        """Set the list of already cited papers to avoid duplicates."""
        self.cited_papers = cited_papers

    def find_additional_papers(self, concept_name: str) -> List[ConceptReference]:
        """
        Find papers in Zotero library that discuss this concept but weren't cited.

        Args:
            concept_name: The concept to search for

        Returns:
            List of ConceptReference objects with relevance scores
        """
        additional_papers = []

        # Generate search terms for the concept
        search_terms = self._generate_search_terms(concept_name)

        for item in self.zotero_items:
            zotero_key = item.get('key', '')

            # Skip if this paper was already cited
            if zotero_key in self.cited_papers:
                continue

            # Search for concept mentions in this paper
            references = self._search_item_for_concept(item, concept_name, search_terms)
            additional_papers.extend(references)

        # Sort by relevance score and return top results
        additional_papers.sort(key=lambda x: x.relevance_score, reverse=True)
        return additional_papers

    def extract_alternative_treatments(self, concept_name: str,
                                     additional_papers: List[ConceptReference]) -> Tuple[List[str], List[str]]:
        """
        Extract alternative definitions and extended treatments from additional papers.

        Args:
            concept_name: The concept being analyzed
            additional_papers: List of papers found in cross-referencing

        Returns:
            Tuple of (alternative_definitions, extended_treatments)
        """
        alternative_definitions = []
        extended_treatments = []

        for ref in additional_papers:
            # Extract content from Zotero item
            zotero_item = self._find_item_by_key(ref.zotero_key)
            if not zotero_item:
                continue

            abstract = zotero_item.get('abstract', '')
            title = zotero_item.get('title', '')

            # Look for explicit definitions
            if ref.mention_type == 'definition':
                definition = self._extract_definition_from_text(abstract, concept_name)
                if definition:
                    alternative_definitions.append(f"{title}: {definition}")

            # Look for extended treatments, applications, or comparisons
            if ref.mention_type in ['discussion', 'application', 'comparison']:
                treatment = self._extract_treatment_from_text(abstract, title, concept_name)
                if treatment:
                    extended_treatments.append(f"{title}: {treatment}")

        return alternative_definitions, extended_treatments

    def build_cross_references(self, concept_name: str,
                            all_concepts: Set[str]) -> Dict[str, List[ConceptReference]]:
        """
        Build cross-references between this concept and other concepts.

        Args:
            concept_name: The primary concept
            all_concepts: Set of all concepts in Γ⁺

        Returns:
            Dictionary mapping related concepts to their shared references
        """
        cross_references = {}

        # Find papers that mention this concept along with other concepts
        for item in self.zotero_items:
            if item.get('key') in self.cited_papers:
                continue

            text_content = self._get_searchable_text(item)
            mentioned_concepts = self._find_mentioned_concepts(text_content, all_concepts)

            if concept_name in mentioned_concepts:
                # This paper mentions the target concept, find what else it mentions
                for other_concept in mentioned_concepts:
                    if other_concept != concept_name:
                        if other_concept not in cross_references:
                            cross_references[other_concept] = []

                        ref = self._create_reference(item, concept_name)
                        cross_references[other_concept].append(ref)

        # Sort references by relevance for each related concept
        for concept in cross_references:
            cross_references[concept].sort(key=lambda x: x.relevance_score, reverse=True)

        return cross_references

    def expand_concept(self, concept_name: str, all_concepts: Set[str]) -> ConceptExpansion:
        """
        Perform complete expansion of a concept via Zotero cross-referencing.

        Args:
            concept_name: The concept to expand
            all_concepts: Set of all concepts in Γ⁺

        Returns:
            ConceptExpansion with all discovered information
        """
        # Step 1: Find additional papers
        additional_papers = self.find_additional_papers(concept_name)

        # Step 2: Extract alternative definitions and treatments
        alt_defs, ext_treatments = self.extract_alternative_treatments(concept_name, additional_papers)

        # Step 3: Build cross-references
        cross_refs = self.build_cross_references(concept_name, all_concepts)

        # Step 4: Extract related concepts from cross-references
        related_concepts = set(cross_refs.keys())

        return ConceptExpansion(
            concept_name=concept_name,
            additional_papers=additional_papers,
            alternative_definitions=alt_defs,
            extended_treatments=ext_treatments,
            related_concepts=related_concepts,
            cross_references=cross_refs
        )

    def _generate_search_terms(self, concept_name: str) -> List[str]:
        """Generate search terms for a concept including variations."""
        terms = [concept_name.lower()]

        # Add variations if available
        if concept_name.lower() in self.concept_variations:
            terms.extend(self.concept_variations[concept_name.lower()])

        # Check reverse mapping (e.g., if 'complex' maps to 'complexity')
        for key, variations in self.concept_variations.items():
            if concept_name.lower() in variations:
                terms.append(key)
                terms.extend([v for v in variations if v != concept_name.lower()])

        return list(set(terms))  # Remove duplicates

    def _search_item_for_concept(self, item: Dict, concept_name: str,
                               search_terms: List[str]) -> List[ConceptReference]:
        """Search a single Zotero item for mentions of the concept."""
        references = []

        title = (item.get('title') or '').lower()
        abstract = (item.get('abstract') or '').lower()
        tags = [tag.lower() for tag in item.get('tags', [])]
        authors_text = ' '.join([
            f"{c.get('first_name', '')} {c.get('last_name', '')}".lower()
            for c in item.get('creators', [])
        ])

        # Search in different contexts with different weights
        contexts = [
            (title, 'title', 0.9),
            (abstract, 'abstract', 0.7),
            (' '.join(tags), 'tags', 0.8),
            (authors_text, 'authors', 0.3)  # Lower weight for authors
        ]

        for text, context, base_weight in contexts:
            for term in search_terms:
                if term in text:
                    # Calculate relevance score based on context and match quality
                    relevance = self._calculate_relevance(text, term, context, base_weight)

                    # Determine mention type
                    mention_type = self._determine_mention_type(text, term, context)

                    if relevance > 0.3:  # Threshold for inclusion
                        ref = ConceptReference(
                            zotero_key=item.get('key', ''),
                            title=item.get('title', ''),
                            authors=self._extract_authors(item),
                            year=self._extract_year(item),
                            context=context,
                            relevance_score=relevance,
                            mention_type=mention_type
                        )
                        references.append(ref)

        return references

    def _calculate_relevance(self, text: str, term: str, context: str, base_weight: float) -> float:
        """Calculate relevance score for a term match."""
        # Exact match gets higher score
        if term == text or f" {term} " in f" {text} ":
            return base_weight * 1.0

        # Partial match gets lower score
        if term in text:
            return base_weight * 0.7

        return 0.0

    def _determine_mention_type(self, text: str, term: str, context: str) -> str:
        """Determine how the concept is mentioned based on context."""
        definition_patterns = [
            r'definition of ' + term,
            term + r' is defined as',
            term + r' refers to',
            r'we define ' + term,
            term + r' can be defined'
        ]

        application_patterns = [
            r'applications? of ' + term,
            r'using ' + term,
            term + r' in practice',
            term + r' applied'
        ]

        comparison_patterns = [
            r'compared to ' + term,
            term + r' versus',
            term + r' differs from',
            r'unlike ' + term
        ]

        # Check for definition
        for pattern in definition_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return 'definition'

        # Check for application
        for pattern in application_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return 'application'

        # Check for comparison
        for pattern in comparison_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return 'comparison'

        # Default to discussion
        return 'discussion'

    def _extract_authors(self, item: Dict) -> List[str]:
        """Extract author names from Zotero item."""
        authors = []
        for creator in item.get('creators', []):
            if creator.get('creatorType') in ['author', 'editor']:
                name = f"{creator.get('firstName', '')} {creator.get('lastName', '')}".strip()
                if name:
                    authors.append(name)
        return authors

    def _extract_year(self, item: Dict) -> Optional[int]:
        """Extract publication year from Zotero item."""
        date_str = item.get('date', '')
        year_match = re.search(r'\b(19|20)\d{2}\b', date_str)
        if year_match:
            return int(year_match.group())
        return None

    def _get_searchable_text(self, item: Dict) -> str:
        """Get all searchable text from a Zotero item."""
        title = item.get('title') or ''
        abstract = item.get('abstract') or ''
        tags = ' '.join(item.get('tags', []))

        return f"{title} {abstract} {tags}".lower()

    def _find_mentioned_concepts(self, text: str, concepts: Set[str]) -> Set[str]:
        """Find which concepts from the set are mentioned in the text."""
        mentioned = set()

        for concept in concepts:
            # Check concept name and variations
            search_terms = [concept.lower()]
            if concept.lower() in self.concept_variations:
                search_terms.extend(self.concept_variations[concept.lower()])

            for term in search_terms:
                if term in text:
                    mentioned.add(concept)
                    break

        return mentioned

    def _find_item_by_key(self, zotero_key: str) -> Optional[Dict]:
        """Find a Zotero item by its key."""
        for item in self.zotero_items:
            if item.get('key') == zotero_key:
                return item
        return None

    def _create_reference(self, item: Dict, concept_name: str) -> ConceptReference:
        """Create a ConceptReference from a Zotero item."""
        return ConceptReference(
            zotero_key=item.get('key', ''),
            title=item.get('title', ''),
            authors=self._extract_authors(item),
            year=self._extract_year(item),
            context='cross-reference',
            relevance_score=0.5,  # Default relevance for cross-references
            mention_type='discussion'
        )

    def _extract_definition_from_text(self, text: str, concept_name: str) -> Optional[str]:
        """Extract a definition of the concept from text."""
        # Look for explicit definition patterns
        patterns = [
            rf'{concept_name} (?:is|can be defined as|refers to) (.+?)(?:[.!?]|\n)',
            rf'(?:definition of|defining) {concept_name} (.+?)(?:[.!?]|\n)',
            rf'{concept_name}: (.+?)(?:[.!?]|\n)',
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                definition = match.group(1).strip()
                # Clean up and return if it looks like a real definition
                if len(definition) > 10 and len(definition) < 500:
                    return definition[:200]  # Limit length

        return None

    def _extract_treatment_from_text(self, abstract: str, title: str, concept_name: str) -> Optional[str]:
        """Extract treatment/discussion of concept from abstract and title."""
        # Combine title and abstract for context
        full_text = f"{title}. {abstract}"

        # Look for sentences that discuss the concept meaningfully
        sentences = re.split(r'[.!?]', full_text)

        for sentence in sentences:
            sentence = sentence.strip()
            if (concept_name.lower() in sentence.lower() and
                len(sentence) > 20 and len(sentence) < 300):
                # Check if this sentence provides meaningful content about the concept
                meaningful_words = ['discuss', 'analyze', 'examine', 'propose', 'develop',
                                  'apply', 'demonstrate', 'show', 'investigate']
                if any(word in sentence.lower() for word in meaningful_words):
                    return sentence

        return None