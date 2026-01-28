// Background Service Worker / Script - Compatible with Chrome and Firefox

// API configuration
const API_CONFIG = {
  apiUrl: "http://127.0.0.1:5000/"
};

// Initialize context menu on install
chrome.runtime.onInstalled.addListener(() => {
  try {
    chrome.contextMenus.create({
      id: "web-note-context",
      title: "Save to Web Note",
      contexts: ["selection"],
    });
    console.log('[Web Note] Context menu created');
  } catch (error) {
    console.error('[Web Note] Error creating context menu:', error);
  }
});

// Handle context menu clicks
chrome.contextMenus.onClicked.addListener((info, tab) => {
  try {
    if (info.menuItemId === "web-note-context" && info.selectionText) {
      // Send message to content script to save the selection
      chrome.tabs.sendMessage(tab.id, {
        action: 'saveHighlight',
        text: info.selectionText,
        source: tab.url
      }).catch(error => {
        console.error('[Web Note] Error sending message to content script:', error);
      });
    }
  } catch (error) {
    console.error('[Web Note] Error handling context menu click:', error);
  }
});

// Handle messages from content script (to make API requests, bypassing page CSP)
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'saveHighlight') {
    try {
      // Make the API request from background (not restricted by page CSP)
      fetch(API_CONFIG.apiUrl + 'notes', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: request.userId || '1',
          text: request.text,
          source: request.source
        })
      })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(result => {
        console.log('[Web Note] Highlight saved:', result);
        sendResponse({ success: true, data: result });
      })
      .catch(error => {
        console.error('[Web Note] Error saving highlight:', error);
        sendResponse({ success: false, error: error.message });
      });
      
      // Return true to indicate we'll respond asynchronously
      return true;
    } catch (error) {
      console.error('[Web Note] Error processing saveHighlight request:', error);
      sendResponse({ success: false, error: error.message });
    }
  }
});

console.log('[Web Note] Background script initialized');
