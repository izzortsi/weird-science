# Zotero MCP Docker Setup

This directory contains the Docker configuration for running a local instance of zotero-mcp server and a Flask-based web chat UI for interactive exploration of the Zotero library.

## Quick Start

1. Set your Zotero API credentials:
```bash
export ZOTERO_API_KEY=your_api_key_here
export ZOTERO_GROUP_ID=6182921
```

2. Build and run with Docker Compose:
```bash
docker-compose up -d
```

3. Access the web UI:
```
http://localhost:5000
```

## Components

### zotero-mcp Server
- Provides MCP (Model Context Protocol) interface to Zotero library
- Exposes RESTful API for querying library items
- Handles authentication and caching

### Flask Web UI
- Simple chat interface for querying the Zotero library
- Natural language queries translated to Zotero API calls
- Interactive exploration of references and concepts

## Configuration

Edit `docker-compose.yml` to customize:
- Port mappings
- Environment variables
- Volume mounts
- Resource limits

## Development

To run in development mode:
```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

This enables:
- Hot reload for code changes
- Debug logging
- Volume mounting for live editing
