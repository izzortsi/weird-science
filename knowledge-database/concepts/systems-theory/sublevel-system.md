---
title: Sublevel System
tags: [systems-theory, hierarchy, multi-scale, decomposition, level-transition]
hierarchy: [systems-theory, hierarchical-organization]
related: [superlevel-system, hierarchy, subsystem, nested-system, hierarchical-decomposition]
zotero_keys: []
---

# Sublevel System

## Definition

Let $\mathcal{S}$ be a system. Consider, for each element $e \in \mathfrak{e}(\mathcal{S}) = E$, a subsystem $\mathcal{S}_e$, with $\bigcup \mathfrak{e}(\mathcal{S}_e) \subset e$. Define, additionally, for each such system the set:

$$\mathfrak{R}_e = \left(\bigcup \mathfrak{r}(\mathcal{S}_e)\right) \cup \left(\bigcup\bigcup \mathfrak{v}(\mathcal{S}_e)\right)$$

Let $\mathfrak{R} = \bigcup_{e \in E} \{\mathfrak{R}_e \}$. 

A system $\mathcal{S}^-$ is said to be on the **(immediate) sublevel** of $\mathcal{S}$ if it has $\bigcup \{\mathfrak{e}(\mathcal{S}_e)\ |\ e \in E\}$ as set of elements and there are functions such that:

i) For each $R \in \bigcup\mathfrak{r}(\mathcal{S}^-)$, there is a natural number $p \leq |\mathfrak{R}|$ and a function $f$ such that, for some $\boldsymbol{\sigma} \in \mathfrak{R}^p$, $R = f(\boldsymbol{\sigma})$

ii) For each $V \in \bigcup\bigcup\mathfrak{v}(\mathcal{S}^-)$, there is a natural number $q \leq |\mathfrak{R}|$ and a function $g$ such that, for some $\boldsymbol{\sigma} \in \mathfrak{R}^q$, $V = g(\boldsymbol{\sigma})$

We denote the immediate sublevel of a system $\mathcal{S}$ by $\slv{\mathcal{S}}$ or $\mathcal{S}^-$. The **$n$-th sublevel** is written as $\slv[n]{\mathcal{S}}$ or $\mathcal{S}^{-n}$.

### Key Idea

A sublevel system is obtained from another system $\mathcal{S}$ by considering **each element of $\mathcal{S}$ as a subsystem**. These subsystems have their own elements. We then define the sublevel system as a system that has the **union of these elements** for its set of elements.

## Partition Refinement

The partition of $\mathcal{S}^-$ **refines** that of $\mathcal{S}$. This means:
- The sublevel has finer granularity than the level above
- Elements at the sublevel correspond to constituent parts of elements at the higher level
- Structure is revealed at increasingly fine scales

Moreover, the properties of the sublevel system are tied to those of the generating subsystems. We do not ask for such properties to depend explicitly on those of $\mathcal{S}$ since these are already taken into consideration when defining the subsystems.

## The Reciprocal Transformation

The sublevel operation effects the reciprocal transformation to [[superlevel-system|superlevel]]:

- **Superlevel**: Aggregates, coarse-grains
- **Sublevel**: Decomposes, refines

Where the superlevel operation identifies emergent macroscopic regularities, the sublevel operation uncovers the **microscopic mechanisms** from which those regularities arise.

### Functional Dependencies

The relations and valuations of $\mathcal{S}^-$ are functionally dependent upon those of the constituent subsystems $\mathcal{S}_e$, but need not be simple compositions thereof—permitting the possibility that inter-level relationships exhibit **genuine novelty** rather than mere reduplication.

## Examples

### Tissue to Cellular Level

Consider tissue as a system:
- **Level $n$**: Tissue with intercellular organization
  - Elements: Functional tissue units (cell aggregates)
  - Relations: Tissue-level signaling, mechanical coupling
  
- **Sublevel $n-1$**: Individual cells
  - Elements: Organelles, molecular complexes  
  - Relations: Intracellular biochemistry, gene regulation
  - Revealed mechanisms: How tissue properties arise from cellular behavior

### Mesoscopic to Molecular Dynamics

For mesoscopic gas flow:
- **Level $n$**: Convection patterns
  - Elements: Convection cells, vortices
  - Relations: Flow interactions, energy cascades
  
- **Sublevel $n-1$**: Molecular dynamics
  - Elements: Individual gas molecules
  - Relations: Collisions, intermolecular forces
  - Revealed mechanisms: Statistical origin of flow patterns

### Organizational to Individual Level

For a department:
- **Level $n$**: Department structure
  - Elements: Teams, project groups
  - Relations: Inter-team coordination, resource allocation
  
- **Sublevel $n-1$**: Individual workers
  - Elements: Skills, tasks, responsibilities
  - Relations: Personal collaborations, task dependencies
  - Revealed mechanisms: How team performance emerges from individual contributions

## Multi-Scale Analysis

The sublevel operation enables **multi-scale analysis** by revealing structure at progressively finer scales:

$$\mathcal{S} \to \mathcal{S}^- \to \mathcal{S}^{-2} \to \mathcal{S}^{-3} \to \cdots$$

At each sublevel, we can ask:
- What are the constituent elements?
- What mechanisms operate at this scale?
- How do properties at this level give rise to behavior at the level above?

## Nested Systems and Infinite Regression

The concept naturally leads to considerations about **nested systems of nested systems**. The very idea of nested system leads to the possibility of infinite hierarchies:

- Going up (superlevels): Increasingly coarse descriptions
- Going down (sublevels): Increasingly fine-grained mechanisms

This potentially infinite regression in both directions reflects the scale-free nature of many complex systems, where structure exists at all scales from microscopic to macroscopic.

## Philosophical Significance

The sublevel operation represents the **revelation of microstructure underlying macroscopic phenomena**. It formalizes the reductionist gesture of understanding wholes by examining their parts, while acknowledging that:

1. Parts have their own structure and dynamics
2. Inter-level relationships can exhibit novelty
3. Multiple levels of description are often necessary for full understanding

This is not merely decomposition, but **scale-sensitive decomposition** that respects the emergent organization at each level.

## Key References

### Theory of Hierarchical, Multilevel, Systems
*Mesarovic & Takahara (1970)*

Foundational work on multistrata systems and level decomposition in hierarchical system theory.

### General Systems Theory
*Yi Lin (2002)*
DOI: [10.1007/b116863](https://doi.org/10.1007/b116863)

Discusses multi-level system decomposition and hierarchical analysis.

## Related Concepts

- [[superlevel-system]] - The dual operation for coarse-graining
- [[subsystem]] - Decomposition without level-transition emphasis
- [[hierarchy]] - Multi-level structures built from level transitions
- [[nested-system]] - Systems embedded in infinite level hierarchies
- [[hierarchical-decomposition]] - Systematic analysis across levels

## Bibliography Keys

- Mesarovic1970
- Lin2002
- Walloth2016
