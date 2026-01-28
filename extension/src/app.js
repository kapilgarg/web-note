// Web Note Extension - Compatible with Chrome and Firefox
console.log('[Web Note] app.js loading...');

// Ensure chrome namespace exists (for Firefox compatibility)
if (typeof chrome === 'undefined') {
    var chrome = browser;
    console.log('[Web Note] Using Firefox browser namespace');
}

// Ensure CONFIG is defined (fallback if config.js didn't load)
if (typeof CONFIG === 'undefined') {
    console.warn('[Web Note] CONFIG not found, using fallback');
    window.CONFIG = {
        apiUrl: "http://127.0.0.1:5000/",
        environment: 'development',
        timeout: 10000
    };
} else {
    console.log('[Web Note] CONFIG loaded from config.js:', CONFIG.apiUrl);
}

// Get selected text - supports all browsers
function getSelectedText() {
    return window.getSelection().toString().trim();
}

// Show notification feedback
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.id = 'web-note-notification';
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 12px 16px;
        background-color: ${type === 'success' ? '#4CAF50' : '#f44336'};
        color: white;
        border-radius: 4px;
        font-size: 14px;
        z-index: 10000;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        animation: slideIn 0.3s ease-in-out;
    `;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-in-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Save highlight via API (send to background script to bypass CSP)
async function saveHighlight(text, source) {
    try {
        // Get user ID from storage (default to 1 if not set)
        const data = await chrome.storage.local.get('userId');
        const userId = data.userId || '1';
        
        // Send message to background script to make the API request
        chrome.runtime.sendMessage({
            action: 'saveHighlight',
            text: text,
            source: source,
            userId: userId
        }, (response) => {
            if (response && response.success) {
                showNotification('✓ Highlight saved successfully', 'success');
                console.log('[Web Note] Highlight saved:', response.data);
            } else {
                const errorMsg = response ? response.error : 'Unknown error';
                console.error('[Web Note] Error saving highlight:', errorMsg);
                showNotification('✗ Failed to save highlight', 'error');
            }
        });
        
        return true;
    } catch (error) {
        console.error('[Web Note] Error sending save request:', error);
        showNotification('✗ Failed to save highlight', 'error');
        return false;
    }
}

// Create and manage the save button
let btnSave = null;

function createSaveButton() {
    if (btnSave) return;
    
    btnSave = document.createElement('button');
    btnSave.id = 'web-note-save-btn';
    btnSave.textContent = '+';
    btnSave.style.cssText = `
        position: absolute;
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background-color: #ff6b6b;
        color: white;
        border: none;
        cursor: pointer;
        font-size: 20px;
        font-weight: bold;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        z-index: 9999;
        display: none;
        transition: all 0.2s ease;
    `;
    
    btnSave.addEventListener('mouseover', function() {
        this.style.backgroundColor = '#ff5252';
        this.style.transform = 'scale(1.1)';
    });
    
    btnSave.addEventListener('mouseout', function() {
        this.style.backgroundColor = '#ff6b6b';
        this.style.transform = 'scale(1)';
    });
    
    btnSave.addEventListener('click', async function(event) {
        event.preventDefault();
        const text = getSelectedText();
        if (text) {
            btnSave.textContent = '...';
            btnSave.disabled = true;
            await saveHighlight(text, window.location.href);
            btnSave.textContent = '+';
            btnSave.disabled = false;
            btnSave.style.display = 'none';
        }
    });
    
    document.body.appendChild(btnSave);
}

// Handle text selection
document.addEventListener('mouseup', function(e) {
    const selectedText = getSelectedText();
    createSaveButton();
    
    if (selectedText.length > 0) {
        // Position button near the cursor
        btnSave.style.left = (e.pageX - 16) + 'px';
        btnSave.style.top = (e.pageY - 40) + 'px';
        btnSave.style.display = 'block';
    } else {
        if (btnSave) {
            btnSave.style.display = 'none';
        }
    }
});

// Handle messages from background script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'saveHighlight') {
        saveHighlight(request.text, request.source);
        sendResponse({ status: 'saving' });
    }
});

// Add CSS animation styles
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

console.log('[Web Note] ✓ Extension fully loaded on', window.location.href);
console.log('[Web Note] ✓ API URL:', CONFIG.apiUrl);
console.log('[Web Note] ✓ Ready to save highlights');
