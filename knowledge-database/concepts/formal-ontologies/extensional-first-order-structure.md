---
title: Extensional First-Order Structure
tags: [formal-ontology, logic, model-theory, semantics]
hierarchy: [formal-ontologies, formal-semantics]
related: [extensional-relational-structure, ontological-commitment, intensional-relation]
zotero_keys: []
---

# Extensional First-Order Structure

## Definition

Let $\mathcal{L}$ be a first-order logical language with vocabulary $V$ and $S = (D, \mathbf{R})$ an [[extensional-relational-structure|extensional relational structure]]. 

An **extensional first-order structure** (also called **model** for $\mathcal{L}$) is a tuple:

$$M = (S, I)$$

where $I$ (called **extensional interpretation function**) is a total function:

$$I : V \to D \cup \mathbf{R}$$

that maps each vocabulary symbol in $V$ to either an element of $D$ or an extensional relation belonging to the set $\mathbf{R}$.

### Key Characteristics

- **Tarskian semantics**: This is the standard model-theoretic semantics for first-order logic
- **Extensional interpretation**: Assigns denotations to non-logical symbols based on current world state
- **No modal content**: Cannot capture intended meaning across possible worlds
- **Snapshot semantics**: Provides interpretation only for a single state of affairs

## Limitations

As Guarino emphasizes, extensional interpretation is insufficient for capturing **intended meaning**. Two key problems arise:

1. **Conceptual ambiguity**: The same linguistic theory could be satisfied by radically different conceptualizations
2. **Modal inadequacy**: Cannot distinguish essential from accidental properties

Without intensional anchoring, two agents might agree on all extensional facts while harboring fundamentally incompatible concepts—precisely because concepts are individuated intensionally, not extensionally.

## Relationship to Intensional Structures

The extensional first-order structure serves as the foundation for the more sophisticated [[ontological-commitment|intensional first-order structure]]:

- **Extensional**: $M = (S, I)$ where $S = (D, \mathbf{R})$
- **Intensional**: $K = (\mathcal{C}, \mathcal{I})$ where $\mathcal{C} = (D, W, \mathfrak{R})$

The transition from extensional to intensional captures the move from:
- Single-world snapshots → Multi-world conceptualizations
- Extensional relations → Intensional relations (functions over worlds)
- Surface agreement → Deep conceptual commitment

## Examples

### Taxonomic Classification

For a biological taxonomy:
- **Vocabulary** $V$: {*mammal*, *dog*, *is-a*, *has-property*}
- **Domain** $D$: {Felix, Fido, Rover, ...}
- **Relations** $\mathbf{R}$: {*is-a* $\subseteq D \times D$, *has-property* $\subseteq D \times D$}

The extensional interpretation $I$ maps:
- *dog* → the set {Fido, Rover, ...} ⊆ $D$
- *is-a* → the subset relation in $\mathbf{R}$

But this doesn't tell us whether "is-a" means taxonomic classification, mereological parthood, or instance-of relationship.

### Enterprise Domain

For an organizational model:
- **Vocabulary** $V$: {*employee*, *department*, *works-for*}
- **Domain** $D$: {Alice, Bob, Engineering, Sales, ...}
- **Relations** $\mathbf{R}$: {*works-for* $\subseteq D \times D$}

An extensional structure captures who currently works for which department, but not:
- What it means to work for a department
- Whether employment is essential or contingent
- How the relation would behave under counterfactual organizational changes

## Philosophical Context

This is standard Tarskian semantics: an interpretation assigns denotations to non-logical symbols. The limitation is not in the mathematics, but in what can be expressed: extensional structures lack the modal resources to capture conceptual content that transcends particular states.

## Key References

### On Truth and Models
*Alfred Tarski*

The foundational work establishing model-theoretic semantics for first-order logic.

### On What Ontology Ought to Be
*Jonathan Schaffer (2008)*

Critiques truthmaker theory and argues for grounding-based ontological commitment, which aligns with the intensional approach.

## Related Concepts

- [[extensional-relational-structure]] - The underlying relational structure $(D, \mathbf{R})$
- [[ontological-commitment]] - The intensional analogue that maps to conceptual relations
- [[intensional-relation]] - What extensional interpretations cannot capture
- [[conceptualization]] - The intensional structure that overcomes extensional limitations

## Bibliography Keys

- Schaffer2008
