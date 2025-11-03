---
title: Parthood (Enclose Relation)
tags: [systems-theory, mereology, nested-systems, composition]
hierarchy: [systems-theory, composition]
related: [subsystem, supersystem, nested-system, hierarchy]
zotero_keys: []
---

# Parthood (Enclose Relation)

## Definition

Let $\mathcal{S}, \mathcal{S}'$ be systems such that $\mathcal{S}' \sqsubset \mathcal{S}$ (i.e., $\mathcal{S}'$ is a [[subsystem]] of $\mathcal{S}$).

We say that $\mathcal{S}$ **encloses** $\mathcal{S}'$, denoting by $\mathcal{S}' \encl \mathcal{S}$, if additionally:

$$\mathfrak{u}(\mathcal{S}') \sqin \mathfrak{e}(\mathcal{S})$$

If $\mathcal{S}$ encloses $\mathcal{S}'$ we say that the latter is a **part** of the former.

### Key Characteristics

- **Three-fold relation**: Combines mereology (part-whole), functional dependence, and set membership
- **Functional component**: The enclosed system participates directly in the enclosing system's dynamics
- **Level transition**: The enclosed subsystem becomes an element at the next level up
- **Mesodynamic role**: The part has a role in the mesodynamics of the whole

## The Three Aspects of Enclosure

The enclose relation $\encl$ synthesizes three distinct aspects:

1. **Mereological relation** (part-to-whole): $\mathcal{S}'$ is spatially or structurally contained in $\mathcal{S}$

2. **Functional dependencies**: Captured by the subsystem relation $\sqsubset$, where properties of $\mathcal{S}$ depend on properties of $\mathcal{S}'$

3. **Set-theoretic membership**: Captured by $\sqin$, where the underlying set of $\mathcal{S}'$ is an element of $\mathcal{S}$

## Distinction from Mere Subsystem Relation

A system $\mathcal{S}'$ that is merely a [[subsystem]] of $\mathcal{S}$ (i.e., $\mathcal{S}' \sqsubset \mathcal{S}$ but not $\mathcal{S}' \encl \mathcal{S}$) may have no direct role in the mesodynamics of $\mathcal{S}$:

- It is a part of $\mathcal{S}$ in the sense of **occupying a spatial subregion**
- But it is not necessarily a **functional component**

To be enclosed, $\mathcal{S}'$ must additionally be an **element** of $\mathcal{S}$, which means that $\mathcal{S}'$ itself (not merely its elements) participates in the relations that constitute $\mathcal{S}$.

This captures the intuition that in a genuinely [[nested-system|nested system]], **the subsystems at one level become the objects at the next level up**.

## Role in Nested Systems

The enclose relation is essential for defining [[nested-system|nested systems]]. A nested system $\mathcal{S}$ must satisfy:

$$\mathcal{R} \encl \mathcal{S} \encl \mathcal{T}$$

for some systems $\mathcal{R}$ and $\mathcal{T}$. This means $\mathcal{S}$ is:
- **Simultaneously a whole**: It encloses $\mathcal{R}$
- **Simultaneously a part**: It is enclosed by $\mathcal{T}$

## Examples

### Cellular Biology

Consider a cell within a tissue:
- **Subsystem without enclosure**: A spatial region within the cell
  - Occupies space but may not participate in cellular dynamics
  
- **Subsystem with enclosure** (parthood): An organelle (e.g., mitochondrion)
  - The organelle $\mathcal{M}$ is a subsystem: $\mathcal{M} \sqsubset \mathcal{C}$
  - The organelle is also an element: $\mathfrak{u}(\mathcal{M}) \sqin \mathfrak{e}(\mathcal{C})$
  - Therefore: $\mathcal{M} \encl \mathcal{C}$
  - The mitochondrion actively participates in cellular metabolism

### Social Organization

For a company:
- **Subsystem without enclosure**: An informal working group
  - Exists within the company but has no formal organizational role
  
- **Subsystem with enclosure** (parthood): A department
  - The department is functionally dependent on company structure
  - The department is recognized as an organizational unit (element)
  - The department participates in company-level decision-making and workflows

### Physical Systems

For a gas in a container:
- **Subsystem without enclosure**: An arbitrary spatial region
  - We can define it, but it plays no special role in gas dynamics
  
- **Subsystem with enclosure** (parthood): A convection cell
  - The convection cell has its own internal circulation
  - The convection cell is treated as a coherent unit in larger-scale flow patterns
  - The convection cell participates as an element in the overall convective dynamics

## Relationship to Holonic Systems

The parthood concept bears significant affinity to the notion of **holonic systems**. A holon, in the sense of Koestler, is simultaneously a whole and a part:

- Exhibits **autonomy** and **agency** at its own level of organization
- Serves as a **component** of larger organizational structures

The enclose relation formalizes this dual nature: a system that is enclosed is simultaneously:
- Composed of parts (has subsystems that it encloses)
- A part of larger wholes (is enclosed by supersystems)

## Philosophical Significance

The enclose relation captures a crucial insight about nested hierarchies: **level transitions involve both functional dependence and ontological reclassification**.

When we move from one level to another:
1. **Functional aspect**: Higher-level properties depend on lower-level dynamics
2. **Ontological aspect**: Lower-level systems become higher-level objects

This dual character distinguishes genuine nested systems from mere compositional hierarchies.

## Key References

### Emergent Nested Systems
*C. Walloth (2016)*
[View in Semantic Scholar](https://www.semanticscholar.org/paper/d8815976588d5ccf34df1b7ceb73f2d5afbdd4c8)
DOI: [10.1007/978-3-319-27550-5](https://doi.org/10.1007/978-3-319-27550-5)

Discusses the enclose relation in the context of emergent phenomena in nested system hierarchies, emphasizing how "enclosed by, and enclosing" relationships structure complex systems.

## Related Concepts

- [[subsystem]] - The functional dependence aspect of parthood
- [[supersystem]] - What encloses a part
- [[nested-system]] - Systems defined by the enclose relation
- [[hierarchy]] - Multi-level structures built from enclose relations
- [[superlevel-system]] - Level transitions in hierarchical systems

## Bibliography Keys

- Walloth2016
- Mesarovic1970
- Mesarovic1976
