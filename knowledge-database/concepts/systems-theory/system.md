---
title: System
tags: [systems-theory, system, general-systems-theory, relational-structure]
hierarchy: [systems-theory, foundations]
related: [subsystem, relational-structure, valued-relation, input-output-system]
zotero_keys: []
---

# System

## Definition

Let $S$ be a set with cardinality $|S| \geq 2$. Consider a partition $\mathfrak{P}$ of $S$, and a subset $\Gamma_{\mathfrak{P}}$ of $\mathfrak{P}$, with $|\Gamma_{\mathfrak{P}}| = C$.

Define $\mathbf{R} = \{R_k \ | \ k \in \mathbb{N}_{\leq C} \}$ where each $R_k$ is a set of $n_k+1$ distinct $k$-ary relations over $\Gamma_{\mathfrak{P}}$, i.e., for any $R_{ki} \in R_k$ we have $R_{ki} \subseteq \Gamma_{\mathfrak{P}}^k$ and therefore:
$$R_k = \{R_{ki} \subseteq \Gamma_{\mathfrak{P}}^k\ | \ i \in \mathbb{N}_{\leq n_k}\}$$

Define, now, for each $R_k$ and each relation $R_{ki} \in R_k$, a set $P_{ki}$ (possibly empty) of functions $\mathrm{v}_{kij}$ such that, for each $j$, $\mathrm{v}_{kij}: R_{ki} \rightarrow V_{kij}$, where $V_{kij}$ is the set of values for the valued relation $\mathrm{v}_{kij}(R_{ki})$.

Finally, define the set $\mathbf{V} = \{P_{ki} \ | \ k \in \mathbb{N}_{\leq C};\ i \in \mathbb{N}_{\leq n_k} \}$ of sets of valuations. Then a **system** $\mathcal{S}$ is a quadruple:
$$\mathcal{S} = (S,\ \Gamma_{\mathfrak{P}}, \ \mathbf{R},\ \mathbf{V})$$

We call the set $S$ the **underlying set** of $\mathcal{S}$, denoted by $\mathfrak{u}(\mathcal{S})$. We call $\Gamma_{\mathfrak{P}}$ the **set of elements** of $\mathcal{S}$, denoted by $\mathfrak{e}(\mathcal{S})$. We call $\mathbf{R}$ the **set of relations** of $\mathcal{S}$, denoted $\mathfrak{r}(\mathcal{S})$, and $\mathbf{V}$ the **set of valuations** of $\mathcal{S}$, denoted $\mathfrak{v}(\mathcal{S})$.

We say that a non-empty set $s \subset S$ is an element of a system $\mathcal{S}$ iff $s \in \Gamma_{\mathfrak{P}}$, and denote the system-membership relation by $\sqin$. Thus:
$$s \sqin \mathcal{S} \iff s \in \Gamma_{\mathfrak{P}}$$

### Alternative Definitions

**Mesarovic and Takahara's Definition**: A system $S$ is a relation on nonempty sets:
$$S \subseteq \prod\{V_i : i \in I\}$$

**Yi Lin's Multirelation Approach**: A system is an ordered pair $S = (M, R)$ where $M$ is a set of objects and $R$ is a set of relations on $M$.

### Key Characteristics

- Composed of interrelated parts or components
- Forms a cohesive, identifiable whole
- Exhibits properties that emerge from component interactions
- Can be analyzed at multiple levels of abstraction
- Has boundaries that distinguish it from its environment
- May exchange matter, energy, or information with environment
- Can be decomposed into subsystems
- Behavior determined by structure and relationships

## Types of Systems

Systems can be classified along several dimensions:

1. **Openness**:
   - Open systems: Exchange with environment
   - Closed systems: No exchange with environment
   - Isolated systems: No interaction whatsoever

2. **Complexity**:
   - Simple systems: Few components, clear relationships
   - Complicated systems: Many components, deterministic
   - Complex systems: Many components, emergent behavior

3. **Nature**:
   - Physical systems: Material components
   - Abstract systems: Conceptual or mathematical
   - Social systems: Human interactions
   - Biological systems: Living organisms

## Examples

1. **Solar System**:
   - Objects: Sun, planets, moons, asteroids
   - Relations: Gravitational attraction, orbital relationships
   - Properties: Mass, position, velocity

2. **Ecosystem**:
   - Objects: Species, organisms, resources
   - Relations: Predator-prey, competition, symbiosis
   - Properties: Population, energy flow, nutrient cycles

3. **Computer System**:
   - Objects: CPU, memory, storage, I/O devices
   - Relations: Data flow, control signals, dependencies
   - Properties: Performance, capacity, state

4. **Organization**:
   - Objects: Departments, employees, resources
   - Relations: Reporting structure, communication, workflow
   - Properties: Roles, responsibilities, capabilities

## Formal Representation

A system S can be formally represented as:
- S = (O, R) where O is a set of objects and R is a set of relations on O
- Or as a relational structure: S = ⟨D, R₁, R₂, ..., Rₙ⟩
- Or in Mesarovic's framework as a family of valued relations

## Key References

### General Systems Theory: Mathematical Foundations
*Mihajlo D. Mesarović, Yasuhiko Takahara (1975)*
[View in Zotero Library](https://www.zotero.org/groups/6182921/items/TETVGKU7)

Provides the canonical set-theoretic definition of systems as relations on Cartesian products: $S \subseteq \prod\{V_i : i \in I\}$.

### General Systems Theory: A Mathematical Approach
*Yi Lin (1999)*
[View in Zotero Library](https://www.zotero.org/groups/6182921/items/JVAUAL5Q)

Introduces the multirelation approach $S = (M, R)$ emphasizing that "the concept of systems is a generalization of that of structures."

### CONCEPTUAL BASIS FOR A MATHEMATICAL THEORY OF GENERAL SYSTEMS
*Mihajlo D. Mesarovic (1972)*
[View in Zotero Library](https://www.zotero.org/groups/6182921/items/4JSYDZNR)
DOI: [10.1108/eb005295](https://doi.org/10.1108/eb005295)

Reappraises foundations of systems theory, sharpening basic systems concepts and introducing goal-seeking representations within set-theory and abstract mathematics.

## Related Concepts

- [[subsystem]] - Components within a system
- [[nested-system]] - Systems containing other systems
- [[relational-structure]] - Mathematical foundation
- [[valued-relation]] - Formal representation of system relations
- [[input-output-system]] - Systems viewed through I/O behavior
- [[hierarchy]] - Organizational structure of systems

## Bibliography Keys

- bertalanffy1968general
- mesarovic1975general
- klir1985architecture
- wymore1967systems
