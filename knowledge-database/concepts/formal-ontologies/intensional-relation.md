---
title: Intensional Relation
tags: [formal-ontology, intensional, conceptual-relation, modal-semantics]
hierarchy: [formal-ontologies, foundations]
related: [world-and-world-state, conceptualization, intensional-relational-structure, extensional-relational-structure]
zotero_keys: []
---

# Intensional Relation

## Definition

Let $S$ be an arbitrary system, $D$ an arbitrary set of distinguished elements of $S$, and $W$ the set of world states for $S$ (also called worlds, or possible worlds). The pair $\langle D, W \rangle$ is called a **domain space** for $S$, as it intuitively fixes the space of variability of the universe of discourse $D$ with respect to the possible states of $S$.

An **intensional relation** (or **conceptual relation**) $\rho^n$ of arity $n$ on $\langle D, W \rangle$ is a total function:

$$\rho^n : W \to 2^{D^n}$$

from the set $W$ into the set of all $n$-ary (extensional) relations on $D$.

### Alternative Names

- Conceptual relation
- Intension (in Carnap's terminology)

### Key Characteristics

- **Functional invariance**: The relation itself does not vary with worlds; it is the function that *determines* how extension varies
- **Conceptual stability**: Encodes the concept that remains stable across counterfactual variations
- **Modal expressivity**: Can distinguish essential from accidental properties
- **World-indexed extensions**: For each world state $w$, produces an extensional relation $\rho^n(w) \subseteq D^n$

## The Carnapian Heritage

This definition instantiates the classical Carnapian approach to intension: an intension is a function from possible worlds to extensions (Carnap 1956). The conceptual relation $\rho^n$ does not *vary* with worlds; rather, it is the very function that *determines* how extension varies with worlds. This is the formal correlate of conceptual stability across counterfactual variation.

## Contrast with Extensional Relations

A purely extensional relation cannot express modal distinctions. It has no resources to distinguish between:
- Properties that are essential (hold in all possible worlds)
- Properties that are accidental (hold only in some worlds)

The intensional framework builds modality into its foundational architecture by treating relations as functions over possible worlds.

## Examples

### Cooperates-With Relation

Following Guarino's human resources example, consider the conceptual relation *cooperates-with*$^2$:

- **Domain**: $D = \{\text{employee}_1, \text{employee}_2, \ldots, \text{employee}_{50000}\}$
- **Worlds**: $W = \{\text{possible organizational states}\}$

The conceptual relation is not merely the set of pairs currently cooperating, but rather the function that specifies, for each possible organizational configuration $w \in W$, which pairs would be cooperating in that configuration.

In world $w_1$ where cooperation requires only shared goals:
$$\text{cooperates-with}^2(w_1) = \{(\text{emp}_i, \text{emp}_j) : \text{emp}_i \text{ and } \text{emp}_j \text{ share goals in } w_1\}$$

**Crucial insight**: We might imagine an alternative concept where cooperation requires both shared goals *and* coordinated action. This would be a *different conceptual relation* $\rho'^2$, even though it might have the same extension in certain worlds.

### Reaction Rate in Biological Systems

For a metabolic system with substrate $S$, enzyme $E$, and product $P$:

$$\text{reaction-rate}^3 : W \to 2^{D^3}$$

For each world state $w$, this relation specifies which triples of (substrate, enzyme, product) entities satisfy the kinetic equation at that state. The relation itself—the functional form of Michaelis-Menten kinetics—is the invariant concept, while its extension varies with concentration states.

### Von Bertalanffy's System Dynamics

When von Bertalanffy characterizes a system through differential equations:
$$\frac{dQ_i}{dt} = f_i(Q_1, Q_2, \ldots, Q_n)$$

Each $f_i$ corresponds to an intensional relation specifying, for each world state (configuration of $Q$ values), what the derivative relationships are. These functional dependencies determine how changes evolve, independent of current values.

## Philosophical Significance

The intensional relation addresses Backlund's observation that different definitional approaches to "system" often disagree about whether certain properties are essential or accidental. A purely extensional definition cannot adjudicate such disputes, for it has no resources to express modal distinctions.

This framework directly addresses von Bertalanffy's concern with identifying genuine systemic properties that transcend particular states.

## Key References

### Meaning and Necessity
*Rudolf Carnap (1956)*
DOI: N/A

The foundational work establishing intensions as functions from possible worlds to extensions.

### The definition of system
*Alexander Backlund (2000)*
[View in Semantic Scholar](https://www.semanticscholar.org/paper/2da035f4c0c7d5da663b4438f8703dfdb1d90de4)
DOI: [10.1108/03684920010322055](https://doi.org/10.1108/03684920010322055)

Observes that different definitional approaches often disagree about essential vs. accidental properties, motivating the need for intensional frameworks.

## Related Concepts

- [[world-and-world-state]] - Provides the domain space for intensional relations
- [[conceptualization]] - Collections of intensional relations form conceptualizations
- [[intensional-relational-structure]] - The triple $(D, W, \mathfrak{R})$ of domain, worlds, and intensional relations
- [[extensional-relational-structure]] - The simpler $(D, \mathbf{R})$ structure lacking modal distinctions
- [[ontological-commitment]] - How intensional relations constrain logical theories

## Bibliography Keys

- Carnap1956
- Backlund2000a
- Bertalanffy1968
