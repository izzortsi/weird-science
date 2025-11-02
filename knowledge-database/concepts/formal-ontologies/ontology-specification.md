---
title: Ontology Specification
tags: [formal-ontology, ontology, specification, knowledge-representation]
hierarchy: [formal-ontologies, implementation]
related: [conceptualization, ontological-commitment, intended-models, formal-ontology]
zotero_keys: []
---

# Ontology Specification

## Definition

An **ontology** for a conceptualization $\mathcal{C}$ with vocabulary $V$ and ontological commitment $K$ is a logical theory consisting of a set of formulas of $\mathcal{L}$, designed so that the set of its models approximates as well as possible the set of intended models $I_K(\mathcal{L})$ according to $K$.

### Approximation and Axiomatic Incompleteness

The language of "approximation" is significant. An ontology does not *fully capture* a conceptualization but rather constrains the space of models to approach the intended models. This is inevitable: the intensional structure of conceptualizations outstrips what can be expressed in first-order logic (or indeed in most formal languages).

The gap between $\text{Mod}(O)$ (models of ontology $O$) and $I_K(\mathcal{L})$ (intended models) is the measure of our axiomatic incompleteness. A "good" ontology minimizes this gap.

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
