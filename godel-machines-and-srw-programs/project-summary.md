---
title: Gödel Machines and Self-Rewriting Programs
project: godel-machines-and-srw-programs
date: 2025-11-13
tags:
  - zotero
  - literature-review
  - self-modifying-systems
  - godel-machines
  - artificial-general-intelligence
  - recursive-self-improvement
zotero_keys:
  - 78HTLZ5S
  - WFB8I6Z3
matched_bibkeys:
  - Zhang2025
  - Wang2025
---

# Gödel Machines and Self-Rewriting Programs

## Project Summary

This project investigates the theoretical foundations and practical implementations of self-rewriting systems that can modify their own code and behavior, culminating in Gödel machines - universal problem solvers capable of recursive self-improvement. The investigation builds upon recent advances in practical implementations of Gödel machine concepts through evolutionary approaches and open-ended self-improvement [[#Zhang2025|(Zhang et al., 2025)]].

Contemporary implementations of Gödel machines represent a practical realization of Schmidhuber's theoretical framework, using empirical validation through coding benchmarks rather than formal proof search. These systems iteratively modify their own code while improving their ability to perform future modifications, creating a feedback loop of recursive self-improvement [[#Wang2025|(Wang et al., 2025)]]. Unlike traditional AI systems constrained by fixed architectures, these modern Gödel machines can fundamentally alter their own structure, algorithms, and learning mechanisms.

The research examines the critical challenge of evaluating self-modification potential, addressing the "MetaproductivityPerformance Mismatch" between an agent's self-improvement capabilities and its current benchmark performance. By developing metrics like the Clade Metaproductivity (CMP) that aggregate the potential of an agent's descendants, modern implementations can approximate the behavior of theoretically optimal self-improving machines under practical constraints [[#Wang2025|(Wang et al., 2025)]].

The project explores how evolutionary principles, inspired by Darwinian natural selection and open-endedness research, can create systems that continuously generate novel self-modifications while maintaining safety through empirical validation and sandboxed execution environments [[#Zhang2025|(Zhang et al., 2025)]].

## References

### Zhang2025

**Darwin Godel Machine: Open-Ended Evolution of Self-Improving Agents**

*Jenny Zhang, Shengran Hu, Cong Lu, Robert Lange, Jeff Clune (2025)*

[View in Zotero Library](https://www.zotero.org/groups/6182921/items/78HTLZ5S)
 | DOI: [10.48550/arXiv.2505.22954](https://doi.org/10.48550/arXiv.2505.22954)

A practical implementation of Gödel machine concepts using evolutionary approaches and open-ended exploration. The system automatically improves its coding capabilities from 20.0% to 50.0% on SWE-bench through self-modification and empirical validation.

---

### Wang2025

**Huxley-Gödel Machine: Human-Level Coding Agent Development by an Approximation of the Optimal Self-Improving Machine**

*Wenyi Wang, Piotr Piękos, Li Nanbo, Firas Laakom, Yimeng Chen, Mateusz Ostaszewski, Mingchen Zhuge, Jürgen Schmidhuber (2025)*

[View in Zotero Library](https://www.zotero.org/groups/6182921/items/WFB8I6Z3)
 | DOI: [10.48550/arXiv.2510.21614](https://doi.org/10.48550/arXiv.2510.21614)

Addresses the MetaproductivityPerformance Mismatch in self-improving systems by introducing Clade Metaproductivity (CMP) metrics. Demonstrates human-level performance on coding benchmarks through approximations of optimal self-improving machines.

---