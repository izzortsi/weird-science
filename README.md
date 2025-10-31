# weird-science

Repository dedicated to organizing and versioning study topics in systems theory, formal ontologies, and related areas. These materials serve as stepping-stones for future paper development.

## 📚 Study Topics

### General Systems Theory

Collection of documents exploring systems theory, complexity, and emergent phenomena.

#### Foundations of General Systems Theory: A Survey of Formal Definitions
[![PDF](https://img.shields.io/badge/PDF-Download-blue?logo=adobe-acrobat-reader)](https://github.com/izzortsi/weird-science/releases/download/latest/gst-overview.pdf)

A systematic compilation of foundational definitions of systems and major theoretical insights drawn from the mathematical literature on General Systems Theory.

[View Document →](./general-systems-theory/gst-overview/)

#### Non-well-founded Hierarchies of Nested Systems
[![PDF](https://img.shields.io/badge/PDF-Download-blue?logo=adobe-acrobat-reader)](https://github.com/izzortsi/weird-science/releases/download/latest/nested-systems.pdf)

A systematic investigation of the definitional foundations of complex systems, articulating a formalism grounded in the recursive nesting of subsystems and examining emergence as a structural phenomenon arising from inter-level functional dependencies.

[View Document →](./general-systems-theory/nested-systems/)

### Formal Ontologies

Collection of documents on formal ontologies and knowledge representation.

#### Definitional Architectures: From Conceptualization to Ontology
[![PDF](https://img.shields.io/badge/PDF-Download-blue?logo=adobe-acrobat-reader)](https://github.com/izzortsi/weird-science/releases/download/latest/formal-ontologies.pdf)

A philosophical excavation of formal system concepts, tracing the conceptual trajectory from extensional mathematical structures through intensional conceptualizations to formal ontologies, situated within the broader discourse of General Systems Theory.

[View Document →](./formal-ontologies/)

## 📁 Repository Structure

```
weird-science/
├── general-systems-theory/
│   ├── gst-overview/
│   │   ├── README.md
│   │   ├── main.tex
│   │   ├── sections/
│   │   │   ├── foundational-definitions.tex
│   │   │   └── theoretical-insights.tex
│   │   └── references/
│   │       └── bibliography.bib
│   └── nested-systems/
│       ├── README.md
│       ├── main.tex
│       ├── sections/
│       │   ├── introduction.tex
│       │   ├── preliminaries.tex
│       │   ├── systems.tex
│       │   ├── subsystems.tex
│       │   └── hierarchies.tex
│       └── references/
│           └── bibliography.bib
└── formal-ontologies/
    ├── README.md
    ├── main.tex
    ├── sections/
    │   ├── introduction.tex
    │   ├── extensional-foundations.tex
    │   ├── intensional-turn.tex
    │   ├── ontological-commitment.tex
    │   ├── intended-models.tex
    │   ├── ontology-specification.tex
    │   └── conclusion.tex
    └── references/
        └── bibliography.bib
```

Each document folder contains:
- `main.tex` - Main LaTeX document
- `sections/` - LaTeX source files organized by section
- `references/` - Bibliography files and reference materials
- `README.md` - Document-specific information

## 🔨 Building PDFs

PDFs are automatically built via GitHub Actions on every push to `dev` and for pull requests. You can:

- **Download the latest PDFs** from the [Releases](../../releases/latest) page
- **Build locally** by running `pdflatex` in each document directory
- **View PR-specific builds** as artifacts on pull request pages

## 📚 Zotero Integration

This repository is integrated with a [Zotero group library](https://www.zotero.org/groups/6182921/) to maintain literature references and generate knowledge artifacts:

- **Project Summaries** - Each project folder contains a `project-summary.md` with references matched to the Zotero library
- **Knowledge Database** - The `knowledge-database/` directory contains atomic concept articles organized hierarchically
- **Automated Generation** - GitHub Actions workflow generates knowledge base from LaTeX sources and Zotero data
- **Semantic Analysis** - Extracts concepts (Γ) from LaTeX and expands to related Zotero items (Γ⁺)
- **Interactive Exploration** - Local Docker setup provides a web UI for querying the Zotero library

For details, see:
- [Knowledge Base Workflow](docs/KNOWLEDGE_BASE_WORKFLOW.md) - Automated generation process
- [Zotero Integration](docs/ZOTERO_INTEGRATION.md) - Complete integration guide

### Quick Start

```bash
# Generate knowledge base from LaTeX and Zotero
python scripts/zotero-integration/zotero_sync.py
python scripts/zotero-integration/knowledge_base_generator.py

# Or use the automated workflow (in GitHub Actions)
# Triggers on: manual dispatch or merges to dev with .tex changes

# Run local exploration UI
cd tools/zotero-mcp
docker-compose up -d
# Access at http://localhost:5000
```

## 🤝 Contributing

This repository uses comprehensive LaTeX .gitignore rules to keep auxiliary files out of version control while preserving source files and important assets.
