---
title: Ontology Specification
tags: [formal-ontology, ontology, specification, knowledge-representation]
hierarchy: [formal-ontologies, implementation]
related: [conceptualization, ontological-commitment, intended-models, formal-ontology]
zotero_keys: []
---

# Ontology Specification

## Definition

An ontology specification (or simply "ontology") is a formal, explicit specification of a shared conceptualization. It consists of a logical theory - a set of formulas in a logical language - designed to capture the intended models of a conceptualization.

Formally, an ontology O is a logical theory such that:
- It is expressed in a formal language L
- Its models K(O) approximate the intended models I(C) of conceptualization C
- It makes the conceptualization explicit and machine-processable

### Key Characteristics

- **Formal**: Expressed in a well-defined logical language (FOL, Description Logic, etc.)
- **Explicit**: States assumptions and constraints clearly
- **Shared**: Designed for use by multiple agents or systems
- **Specification**: Describes what exists in the domain and how
- Machine-readable and processable
- Contains vocabulary (terms) and axioms (constraints)
- Multiple ontologies can commit to the same conceptualization

## Components of an Ontology

An ontology typically includes:

1. **Vocabulary**:
   - Concepts/Classes
   - Relations/Properties
   - Individuals/Instances
   - Functions

2. **Axioms**:
   - Definitions
   - Constraints
   - Rules
   - Theorems

3. **Documentation**:
   - Natural language descriptions
   - Examples
   - Usage guidelines

## Examples

1. **SUMO (Suggested Upper Merged Ontology)**:
   - Domain: General upper-level concepts
   - Language: Higher-order logic
   - Thousands of terms and axioms
   - Covers entities, processes, attributes, relations

2. **Gene Ontology (GO)**:
   - Domain: Biological gene function
   - Three sub-ontologies: molecular function, biological process, cellular component
   - Widely used in bioinformatics

3. **DOLCE (Descriptive Ontology for Linguistic and Cognitive Engineering)**:
   - Domain: Upper-level ontology
   - Focus: Cognitive and linguistic categories
   - Distinguishes between enduring and perduring entities

4. **OWL Ontologies**:
   - Language: OWL (Web Ontology Language)
   - Based on Description Logics
   - Used extensively in Semantic Web applications

## Relationship to Other Concepts

```
Conceptualization (abstract, intensional)
         ↓
Ontological Commitment (set of allowed models)
         ↓
Ontology Specification (concrete logical theory)
```

Multiple ontologies can:
- Share the same ontological commitment
- Commit to the same conceptualization
- Differ in axiomatization, language, or granularity

## Design Principles

Good ontology specifications should:
- Clearly capture intended models
- Minimize unintended models
- Be consistent (no contradictions)
- Be complete for intended purposes
- Be computationally tractable
- Be modular and extensible
- Include clear documentation

## Key References

The modern formal definition of ontology as a specification of conceptualization originates from Gruber (1993, 1995) and was refined by Guarino (1998) and others in the formal ontology community.

## Related Concepts

- [[formal-ontology]] - The discipline of building ontologies
- [[conceptualization]] - What the ontology specifies
- [[ontological-commitment]] - The semantic constraints
- [[intended-models]] - What the ontology aims to capture
- [[intensional-relational-structure]] - The underlying conceptual structure

## Bibliography Keys

- gruber1993translation
- gruber1995toward
- guarino1998formal
- guarino1995ontologies
- niles2001towards (SUMO)
- gangemi2002sweetening (DOLCE)
