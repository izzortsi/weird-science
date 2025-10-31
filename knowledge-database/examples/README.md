# Example Output Structure

This directory contains example outputs from the knowledge base generation workflow to illustrate the expected structure and format.

## Directory Structure

After Claude Code performs semantic analysis, the knowledge base should follow this structure:

```
knowledge-database/
├── README.md                          # Updated index of all concepts
├── analysis-data.json                 # Analysis metadata
├── claude-prompt.md                   # Generated prompt
├── CLAUDE_INTEGRATION.md              # Integration instructions
└── concepts/
    ├── systems-theory/
    │   ├── index.md                   # Systems theory domain overview
    │   ├── general-systems.md         # Atomic concept article
    │   ├── complexity/
    │   │   ├── index.md              # Complexity sub-domain
    │   │   ├── emergence.md          # Example atomic concept
    │   │   └── self-organization.md  # Example atomic concept
    │   └── hierarchy.md              # Atomic concept article
    ├── formal-ontologies/
    │   ├── index.md
    │   ├── conceptualization.md
    │   └── ontological-commitment.md
    └── mathematics/
        ├── index.md
        └── set-theory.md
```

## Example Files

See this `examples/` directory for sample concept articles showing the expected format:
- `emergence.md` - Complete atomic concept article
- `systems-theory-index.md` - Domain index file
