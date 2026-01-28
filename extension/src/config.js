// Configuration for Web Note extension
const CONFIG = {
    apiUrl: "http://127.0.0.1:5000/",
    environment: 'development',
    timeout: 10000
};

// Allow overriding config via Chrome storage
chrome.storage.local.get('config', (data) => {
    if (data.config && data.config.apiUrl) {
        CONFIG.apiUrl = data.config.apiUrl;
    }
});