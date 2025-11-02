---
title: Valued Relation
tags: [systems-theory, valued-relation, mathematical-foundations, general-systems-theory]
hierarchy: [systems-theory, mathematical-foundations]
related: [relational-structure, system, set-theoretic-system, input-output-system]
zotero_keys: []
---

# Valued Relation

## Definition

Let $\mathcal{F} = \{S_i\}_{i\in I}$ be a family of sets and $R$ an $n$-ary relation over $\mathcal{F}$, that is, $R \subseteq \prod_{i \in I} S_i$. Let $V$ be another set, called the **set of values**. If $\mathrm{v}$ is a function such that $\mathrm{v}: R \rightarrow V$, we define:

(a) $\mathrm{v}(R) = \{\mathrm{v}(r) \in V\ |\ r \in R\}$

(b) $R_\mathrm{v} = (R, V, \mathrm{v})$ is called an $n$-ary $\mathrm{v}$-valued relation over $\mathcal{F}$

(c) $\mathrm{v}$ is a **valuation** of $R$

If $R_\mathrm{v} = (R, V, \mathrm{v})$, we say that $R$ is the **underlying relation** of $R_\mathrm{v}$.

### Interpretation

In the above definition, the graph of $\mathrm{v}$ is considered as the valued relation. Thus an $n$-ary valued relation over a family $\{S_i\}$ is an $(n+1)$-ary relation with the particularity that it is functional in $V$. The underlying relations account for the 'structure of interactions between objects', whereas the valuations denote the characteristics these interactions have, notably their strength or intensity.

As an example, a weighted digraph is an instance of a 'structure of interactions with values'.

### Key Characteristics

- Generalizes binary (yes/no) relations to multi-valued relations
- Assigns elements from a value set to tuples
- Value set can be any set (real numbers, probabilities, fuzzy values, etc.)
- Provides mathematical foundation for Mesarovic's systems theory
- Enables quantitative system descriptions
- Supports probabilistic and fuzzy system modeling
- More expressive than classical relations

## Special Cases

1. **Classical Relation**: Value set Y = {0, 1} or {true, false}
2. **Fuzzy Relation**: Value set Y = [0, 1] (degrees of membership)
3. **Probabilistic Relation**: Value set Y = [0, 1] (probabilities)
4. **Weighted Relation**: Value set Y = ℝ (real-valued weights)
5. **Labeled Relation**: Value set Y = any finite set of labels

## Examples

1. **Distance Relation**:
   - Sets: Cities × Cities
   - Value set: ℝ⁺ (non-negative reals)
   - ρ(CityA, CityB) = distance between cities in km

2. **Similarity Relation**:
   - Sets: Objects × Objects
   - Value set: [0, 1]
   - ρ(obj₁, obj₂) = degree of similarity

3. **Preference Relation**:
   - Sets: Alternatives × Alternatives
   - Value set: {strongly prefer, prefer, indifferent, ...}
   - ρ(a, b) = preference of a over b

4. **Interaction Strength**:
   - Sets: Neurons × Neurons
   - Value set: ℝ (positive or negative)
   - ρ(n₁, n₂) = synaptic weight from n₁ to n₂

5. **Traffic Flow**:
   - Sets: Locations × Locations × Time
   - Value set: ℕ (number of vehicles)
   - ρ(loc₁, loc₂, t) = vehicles traveling from loc₁ to loc₂ at time t

## Formal Properties

Valued relations can exhibit various properties:

1. **Reflexivity**: ρ(x, x) has specific value for all x
2. **Symmetry**: ρ(x, y) = ρ(y, x)
3. **Transitivity**: Composite relation satisfies transitivity constraint
4. **Completeness**: Defined for all tuples in domain

## Role in Systems Theory

In Mesarovic's General Systems Theory, systems are defined as families of valued relations:

S = {ρᵢ | i ∈ I}

where each ρᵢ is a valued relation on some family of sets. This provides:
- Unified framework for diverse system types
- Mathematical rigor
- Ability to model uncertainty and gradations
- Foundation for hierarchical systems theory

## Operations on Valued Relations

1. **Composition**: Combining relations through intermediate sets
2. **Projection**: Restricting to subset of argument positions
3. **Join**: Combining relations on common domains
4. **Aggregation**: Combining multiple value assessments

## Key References

### General Systems Theory: Mathematical Foundations
*Mihajlo D. Mesarović, Yasuhiko Takahara (1975)*
[View in Zotero Library](https://www.zotero.org/groups/6182921/items/TETVGKU7)

Central to Mesarovic and Takahara's formalization, providing the mathematical foundation for valued relations as the basis of general systems theory.

## Related Concepts

- [[relational-structure]] - Classical relations as special case
- [[system]] - Systems defined via valued relations
- [[set-theoretic-system]] - Set-theoretic foundations
- [[input-output-system]] - I/O behavior as valued relations
- [[fuzzy-set]] - Related concept using [0,1] valuations

## Bibliography Keys

- mesarovic1975general
- mesarovic1989abstract
- klir1985architecture
- zadeh1965fuzzy (for fuzzy relations)
