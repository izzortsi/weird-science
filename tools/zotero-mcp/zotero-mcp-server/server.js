/**
 * Zotero MCP Server
 * 
 * Provides a simple REST API wrapper around the Zotero API
 * for use with the web UI.
 */

const express = require('express');
const cors = require('cors');
const axios = require('axios');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Configuration
const ZOTERO_API_KEY = process.env.ZOTERO_API_KEY;
const ZOTERO_GROUP_ID = process.env.ZOTERO_GROUP_ID || '6182921';
const ZOTERO_BASE_URL = `https://api.zotero.org/groups/${ZOTERO_GROUP_ID}`;

// Middleware
app.use(cors());
app.use(express.json());

// Headers for Zotero API
const getZoteroHeaders = () => {
  const headers = {
    'Content-Type': 'application/json',
  };
  if (ZOTERO_API_KEY) {
    headers['Zotero-API-Key'] = ZOTERO_API_KEY;
  }
  return headers;
};

// Routes

/**
 * Health check endpoint
 */
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    zotero_group_id: ZOTERO_GROUP_ID,
    api_key_configured: !!ZOTERO_API_KEY
  });
});

/**
 * Get all items from the Zotero library
 */
app.get('/items', async (req, res) => {
  try {
    const { limit = 100, start = 0, q, tag } = req.query;
    
    const params = {
      limit,
      start,
      format: 'json'
    };
    
    if (q) params.q = q;
    if (tag) params.tag = tag;
    
    const response = await axios.get(`${ZOTERO_BASE_URL}/items`, {
      headers: getZoteroHeaders(),
      params
    });
    
    res.json(response.data);
  } catch (error) {
    console.error('Error fetching items:', error.message);
    res.status(error.response?.status || 500).json({
      error: 'Failed to fetch items',
      message: error.message
    });
  }
});

/**
 * Get a specific item by key
 */
app.get('/items/:key', async (req, res) => {
  try {
    const { key } = req.params;
    
    const response = await axios.get(`${ZOTERO_BASE_URL}/items/${key}`, {
      headers: getZoteroHeaders()
    });
    
    res.json(response.data);
  } catch (error) {
    console.error(`Error fetching item ${req.params.key}:`, error.message);
    res.status(error.response?.status || 500).json({
      error: 'Failed to fetch item',
      message: error.message
    });
  }
});

/**
 * Search items
 */
app.post('/search', async (req, res) => {
  try {
    const { query, filters = {} } = req.body;
    
    const params = {
      limit: filters.limit || 50,
      format: 'json'
    };
    
    if (query) {
      params.q = query;
    }
    
    if (filters.tag) {
      params.tag = filters.tag;
    }
    
    if (filters.itemType) {
      params.itemType = filters.itemType;
    }
    
    const response = await axios.get(`${ZOTERO_BASE_URL}/items`, {
      headers: getZoteroHeaders(),
      params
    });
    
    res.json(response.data);
  } catch (error) {
    console.error('Error searching items:', error.message);
    res.status(error.response?.status || 500).json({
      error: 'Failed to search items',
      message: error.message
    });
  }
});

/**
 * Get all tags
 */
app.get('/tags', async (req, res) => {
  try {
    const response = await axios.get(`${ZOTERO_BASE_URL}/tags`, {
      headers: getZoteroHeaders(),
      params: { format: 'json' }
    });
    
    res.json(response.data);
  } catch (error) {
    console.error('Error fetching tags:', error.message);
    res.status(error.response?.status || 500).json({
      error: 'Failed to fetch tags',
      message: error.message
    });
  }
});

/**
 * Get collections
 */
app.get('/collections', async (req, res) => {
  try {
    const response = await axios.get(`${ZOTERO_BASE_URL}/collections`, {
      headers: getZoteroHeaders(),
      params: { format: 'json' }
    });
    
    res.json(response.data);
  } catch (error) {
    console.error('Error fetching collections:', error.message);
    res.status(error.response?.status || 500).json({
      error: 'Failed to fetch collections',
      message: error.message
    });
  }
});

// Error handler
app.use((err, req, res, next) => {
  console.error('Unhandled error:', err);
  res.status(500).json({
    error: 'Internal server error',
    message: err.message
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`Zotero MCP Server running on port ${PORT}`);
  console.log(`Zotero Group ID: ${ZOTERO_GROUP_ID}`);
  console.log(`API Key configured: ${!!ZOTERO_API_KEY}`);
});
