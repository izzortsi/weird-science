---
title: Intended Models
tags: [formal-ontology, models, conceptualization, semantics]
hierarchy: [formal-ontologies, foundations]
related: [conceptualization, ontological-commitment, extensional-relational-structure, ontology-specification]
zotero_keys: []
---

# Intended Models

## Definition

Intended models are the set of possible states of affairs that are consistent with a conceptualization. They represent the extensional characterization of what we intend to capture when we formalize a domain.

For a conceptualization C, the set I(C) of intended models consists of all extensional relational structures that correspond to possible worlds consistent with our understanding of the domain. These are the "correct" interpretations of the domain according to our conceptual understanding.

### Key Characteristics

- Extensional structures that satisfy the conceptualization
- Represent possible states of affairs in the domain
- May be infinite in number
- Define the semantics of the conceptualization
- Generally cannot be fully captured by finite axiomatization
- Serve as the gold standard for evaluating ontological commitments
- Bridge intensional conceptualization and extensional instances

## Relationship to Formal Ontology

The relationship between key concepts:

1. **Conceptualization C**: Defined by its intended models I(C)
2. **Ontological Commitment K**: Approximates I(C) through logical constraints
3. **Ontology O**: A specific theory whose models K(O) should approximate I(C)

The goal is: I(C) ⊆ K(O), meaning all intended models satisfy the ontology, though the ontology may allow additional unintended models.

## Examples

1. **Arithmetic Domain**:
   - Conceptualization: Natural number arithmetic
   - Intended models: The standard model of natural numbers
   - Note: Peano arithmetic has non-standard models, so K(PA) ⊃ I(C)

2. **Kinship Domain**:
   - Conceptualization: Family relationships
   - Intended models: All valid family tree structures
   - Each model assigns specific people to roles and relationships

3. **Spatial Relations**:
   - Conceptualization: Physical space and containment
   - Intended models: Geometric configurations satisfying spatial constraints
   - Different models might represent different physical arrangements

4. **Business Process**:
   - Conceptualization: Valid workflow sequences
   - Intended models: All legitimate process execution traces
   - Models capture different valid business scenarios

## Theoretical Importance

Intended models are crucial because:
- They provide the extensional definition of conceptualization
- They allow evaluation of whether an ontology adequately captures domain knowledge
- They explain why different ontologies can commit to the same conceptualization
- They clarify the semantic foundation of knowledge representation

## Key References

### A Translation Approach to Portable Ontology Specifications
*Thomas R. Gruber (1993)*

Introduces the notion of intended models as the extensional characterization of conceptualizations, distinguishing between the intensional conceptualization and its extensional realizations.

### Formal Ontology and Information Systems
*Nicola Guarino (1998)*

Provides the formal definition of compatibility between models and ontological commitments, establishing intended models $I_K(\mathcal{L})$ as the set of extensional structures compatible with an intensional commitment $K$.

## Related Concepts

- [[conceptualization]] - Defined by its intended models
- [[ontological-commitment]] - Approximates intended models through logic
- [[extensional-relational-structure]] - The form of intended models
- [[intensional-relational-structure]] - The intensional dual to intended models
- [[ontology-specification]] - Aims to capture intended models

## Bibliography Keys

- gruber1993translation
- guarino1998formal
- guarino1995ontologies
