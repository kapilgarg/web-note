// Background Service Worker for Manifest V3

// Initialize context menu
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "web-note-context",
    title: "Save to Web Note",
    contexts: ["selection"],
  });
});

// Handle context menu clicks
chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "web-note-context" && info.selectionText) {
    // Send message to content script to save the selection
    chrome.tabs.sendMessage(tab.id, {
      action: 'saveHighlight',
      text: info.selectionText,
      source: tab.url
    }).catch(error => console.error('Error sending message:', error));
  }
});

console.log('Web Note background service worker initialized');