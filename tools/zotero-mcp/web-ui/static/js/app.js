// Zotero Library Explorer - Client-side JavaScript

const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const resultsDiv = document.getElementById('results');
const loadingDiv = document.getElementById('loading');

// Search on button click
searchBtn.addEventListener('click', performSearch);

// Search on Enter key
searchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        performSearch();
    }
});

async function performSearch() {
    const query = searchInput.value.trim();
    
    if (!query) {
        return;
    }
    
    // Show loading, hide results
    loadingDiv.style.display = 'block';
    resultsDiv.style.display = 'none';
    
    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query }),
        });
        
        const data = await response.json();
        
        // Hide loading
        loadingDiv.style.display = 'none';
        resultsDiv.style.display = 'block';
        
        if (data.success) {
            displayResults(data.results);
        } else {
            displayError(data.error || 'An error occurred while searching');
        }
    } catch (error) {
        loadingDiv.style.display = 'none';
        resultsDiv.style.display = 'block';
        displayError('Failed to connect to the server. Please try again.');
        console.error('Search error:', error);
    }
}

function displayResults(results) {
    if (results.length === 0) {
        resultsDiv.innerHTML = `
            <div class="no-results">
                <h3>No results found</h3>
                <p>Try a different search query or browse by tags.</p>
            </div>
        `;
        return;
    }
    
    const html = results.map(item => {
        const zoteroUrl = `https://www.zotero.org/groups/6182921/items/${item.key}`;
        const doiLink = item.doi ? 
            `<a href="https://doi.org/${item.doi}" target="_blank">DOI: ${item.doi}</a>` : '';
        const urlLink = item.url ? 
            `<a href="${item.url}" target="_blank">External Link</a>` : '';
        
        return `
            <div class="result-item">
                <h3>${escapeHtml(item.title)}</h3>
                <div class="result-meta">
                    <span class="result-type">${escapeHtml(item.type)}</span>
                    ${escapeHtml(item.authors)} (${escapeHtml(item.year)})
                </div>
                ${item.abstract ? `<div class="result-abstract">${escapeHtml(item.abstract)}</div>` : ''}
                <div class="result-links">
                    <a href="${zoteroUrl}" target="_blank">View in Zotero</a>
                    ${doiLink}
                    ${urlLink}
                </div>
            </div>
        `;
    }).join('');
    
    resultsDiv.innerHTML = `
        <div style="margin-bottom: 1rem; color: var(--text-gray);">
            Found ${results.length} result${results.length !== 1 ? 's' : ''}
        </div>
        ${html}
    `;
}

function displayError(message) {
    resultsDiv.innerHTML = `
        <div class="error-message">
            <strong>Error:</strong> ${escapeHtml(message)}
        </div>
    `;
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return String(text).replace(/[&<>"']/g, (m) => map[m]);
}

// Check server health on load
async function checkHealth() {
    try {
        const response = await fetch('/health');
        const data = await response.json();
        console.log('Server health:', data);
    } catch (error) {
        console.error('Health check failed:', error);
    }
}

// Run health check when page loads
checkHealth();
