---
title: Valued Relation
tags: [systems-theory, valued-relation, mathematical-foundations, general-systems-theory]
hierarchy: [systems-theory, mathematical-foundations]
related: [relational-structure, system, set-theoretic-system, input-output-system]
zotero_keys: []
---

# Valued Relation

## Definition

A valued relation is a generalization of ordinary relations where instead of elements simply being related or not (binary), the relation assigns values from some value set to tuples of elements. Formally, a valued relation ρ on sets X₁, X₂, ..., Xₙ with values in set Y is a function:

ρ: X₁ × X₂ × ... × Xₙ → Y

This extends the classical notion of relation (which can be viewed as valued in {true, false}) to arbitrary value sets.

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

Valued relations are central to Mesarovic and Takahara's formalization of general systems theory, providing a mathematical foundation that generalizes both classical systems theory and relational approaches.

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
