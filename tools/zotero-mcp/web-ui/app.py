"""
Flask Web UI for Zotero Library Exploration

A simple chat-like interface for querying the Zotero library
via the zotero-mcp server.
"""

import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Configuration
ZOTERO_MCP_URL = os.environ.get('ZOTERO_MCP_URL', 'http://localhost:3000')


@app.route('/')
def index():
    """Render the main chat interface."""
    return render_template('index.html')


@app.route('/api/search', methods=['POST'])
def search():
    """Search the Zotero library."""
    data = request.json
    query = data.get('query', '')
    
    try:
        response = requests.post(
            f'{ZOTERO_MCP_URL}/search',
            json={'query': query},
            timeout=10
        )
        response.raise_for_status()
        items = response.json()
        
        # Format items for display
        results = []
        for item in items:
            item_data = item.get('data', {})
            
            # Extract authors
            authors = []
            for creator in item_data.get('creators', []):
                if 'lastName' in creator:
                    name = creator.get('lastName', '')
                    if 'firstName' in creator:
                        name = f"{creator['firstName']} {name}"
                    authors.append(name)
            
            results.append({
                'key': item.get('key', ''),
                'title': item_data.get('title', 'Untitled'),
                'authors': ', '.join(authors) if authors else 'Unknown',
                'year': item_data.get('date', '')[:4] if item_data.get('date') else 'N/A',
                'type': item_data.get('itemType', 'unknown'),
                'abstract': item_data.get('abstractNote', '')[:200] + '...' if item_data.get('abstractNote') else '',
                'doi': item_data.get('DOI', ''),
                'url': item_data.get('url', '')
            })
        
        return jsonify({
            'success': True,
            'results': results,
            'count': len(results)
        })
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            'success': False,
            'error': f'Failed to connect to Zotero MCP server: {str(e)}'
        }), 500


@app.route('/api/item/<key>')
def get_item(key):
    """Get details for a specific item."""
    try:
        response = requests.get(
            f'{ZOTERO_MCP_URL}/items/{key}',
            timeout=10
        )
        response.raise_for_status()
        return jsonify(response.json())
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            'error': f'Failed to fetch item: {str(e)}'
        }), 500


@app.route('/api/tags')
def get_tags():
    """Get all tags from the library."""
    try:
        response = requests.get(
            f'{ZOTERO_MCP_URL}/tags',
            timeout=10
        )
        response.raise_for_status()
        return jsonify(response.json())
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            'error': f'Failed to fetch tags: {str(e)}'
        }), 500


@app.route('/health')
def health():
    """Health check endpoint."""
    try:
        response = requests.get(f'{ZOTERO_MCP_URL}/health', timeout=5)
        mcp_status = response.json() if response.ok else {'status': 'error'}
    except:
        mcp_status = {'status': 'unreachable'}
    
    return jsonify({
        'status': 'ok',
        'mcp_server': mcp_status
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
