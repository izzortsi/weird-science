---
title: World and World State
tags: [formal-ontology, modal-logic, possible-worlds, intensional]
hierarchy: [formal-ontologies, foundations]
related: [intensional-relation, conceptualization, intensional-relational-structure]
zotero_keys: []
---

# World and World State

## Definition

With respect to a specific system $S$ we want to model, a **world state** for $S$ is a maximal observable state of affairs, i.e., a unique assignment of values to all the observable variables that characterize the system.

A **world** is a totally ordered set of world states, corresponding to the system's evolution in time. If we abstract from time for the sake of simplicity, a world state coincides with a world.

### Key Characteristics

- **Maximal observability**: A world state captures all observable variables at a specific granularity level
- **Epistemic humility**: We don't claim to capture all possible states, but rather all states *observable at our chosen level of analysis*
- **Temporal ordering**: A world represents the evolution of world states over time
- **Methodological choice**: The granularity of observation is a deliberate analytical decision

## Relationship to Other Concepts

World states form the foundation for defining [[intensional-relation|intensional relations]] and [[conceptualization|conceptualizations]]. Together with a domain $D$, they form a **domain space** $\langle D, W \rangle$ that captures the space of variability of the universe of discourse.

In the context of [[intensional-relational-structure|intensional relational structures]], world states enable the distinction between:
- **Extensional relations**: Relations that hold in a particular world state
- **Intensional relations**: Functions that map each world state to its corresponding extensional relations

## Examples

### Biological System

For a metabolic system characterized by substrate concentration $S$, enzyme concentration $E$, and product concentration $P$:

- **World states**: Each world state $w \in W$ assigns specific values to $(S(w), E(w), P(w))$
- **World**: The temporal sequence of these concentration assignments
- **Observable variables**: $\{S, E, P\}$

### Organizational System

For an enterprise with employees and departments:

- **World states**: Each configuration of employee assignments, reporting structures, and project allocations
- **World**: The evolution of organizational structure over time
- **Observable variables**: Employee positions, department memberships, project assignments

### Physical System

For von Bertalanffy's general system characterized by variables $Q_1, Q_2, \ldots, Q_n$:

- **World states**: Assignments of specific values to all system variables
- **World**: The trajectory through state space as governed by differential equations
  $$\frac{dQ_i}{dt} = f_i(Q_1, Q_2, \ldots, Q_n)$$

## Philosophical Context

This definition embeds a critical methodological choice: we fix a granularity of observation and declare certain variable configurations "maximal." The epistemic humility here is noteworthy—we do not claim to capture all possible states of $S$, but rather all states *observable at our chosen level of analysis*.

## Key References

### Meaning and Necessity
*Rudolf Carnap (1956)*
DOI: N/A

The classical Carnapian approach to intension treats intensional relations as functions from possible worlds to extensions, providing the philosophical foundation for the world/world-state distinction.

## Related Concepts

- [[intensional-relation]] - Functions defined over world states
- [[conceptualization]] - Structures defined using domain spaces $\langle D, W \rangle$
- [[intensional-relational-structure]] - Uses world states to capture invariant conceptual relations
- [[extensional-relational-structure]] - Captures only a single world state

## Bibliography Keys

- Carnap1956
- Backlund2000a
- Bertalanffy1968
