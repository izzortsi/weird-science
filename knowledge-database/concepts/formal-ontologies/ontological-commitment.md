---
title: Ontological Commitment
tags: [formal-ontology, ontological-commitment, logical-theory, conceptualization]
hierarchy: [formal-ontologies, foundations]
related: [conceptualization, intended-models, ontology-specification, intensional-relational-structure]
zotero_keys: []
---

# Ontological Commitment

## Definition

An ontological commitment is an agreement to use shared vocabulary in a coherent and consistent way with respect to a conceptualization. More formally, an ontological commitment K is the set of models of a logical theory - it approximates the intended models of a conceptualization.

Given a logical language L, an ontological commitment K(L) specifies the set of all models of L that are consistent with the conceptualization. The ontological commitment acts as a bridge between:
- The conceptualization C (intensional, abstract understanding)
- The logical theory T (formal specification)

### Key Characteristics

- Represents the semantic constraints imposed by a logical theory
- Independent of specific axiomatization (multiple theories can share the same commitment)
- Approximates intended models of a conceptualization
- Defined as the set of models satisfying the logical constraints
- Allows for multiple ontologies with the same commitment but different specifications
- More abstract than a specific ontology specification
- Enables comparison of different formalizations of the same domain

## Relationship Between Components

The relationship can be understood as:
1. **Conceptualization (C)**: What we intend to represent
2. **Ontological Commitment (K)**: The set of models allowed by our logical constraints
3. **Ontology (O)**: A specific logical theory that realizes this commitment

Ideally: K(O) ⊆ I(C), where I(C) is the set of intended models of C.

## Examples

1. **Temporal Ontologies**:
   - Conceptualization: Time as a continuous flow
   - Ontological Commitment: Models where time is linearly ordered
   - Different ontologies: discrete time intervals vs. continuous time points

2. **Part-Whole Relations**:
   - Conceptualization: Physical parthood
   - Ontological Commitment: Models satisfying transitivity and anti-symmetry
   - Different ontologies: mereology with different axioms for fusion/sum

3. **Classification Systems**:
   - Conceptualization: Hierarchical organization
   - Ontological Commitment: Models with transitive is-a relations
   - Different ontologies: strict hierarchies vs. multiple inheritance

## Key References

The concept of ontological commitment was formalized by Gruber (1993) and refined by Guarino (1998), providing a clear separation between:
- What we intend to represent (conceptualization)
- What our logic allows (ontological commitment)
- How we specify it (ontology)

This distinction is crucial for understanding ontology alignment, merging, and comparison.

## Related Concepts

- [[conceptualization]] - What the commitment approximates
- [[intended-models]] - The ideal models of the conceptualization
- [[ontology-specification]] - The logical theory realizing the commitment
- [[intensional-relational-structure]] - The structure underlying conceptualizations
- [[formal-ontology]] - The discipline studying these relationships

## Bibliography Keys

- gruber1993translation
- guarino1998formal
- guarino1995ontologies
