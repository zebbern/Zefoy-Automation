"""JavaScript injection code for removing popups and overlays."""

# Remove all ad iframes and overlays
REMOVE_AD_OVERLAYS = """
() => {
    // Remove ad iframes
    document.querySelectorAll('iframe').forEach(el => el.remove());
    
    // Remove dialog overlays
    document.querySelectorAll('.fc-dialog-overlay').forEach(el => el.remove());
    
    // Remove adsense elements
    document.querySelectorAll('.adsbygoogle').forEach(el => el.remove());
    
    // Remove any full-screen ad containers
    document.querySelectorAll('[class*="fullscreen"]').forEach(el => {
        if (el.querySelector('iframe')) el.remove();
    });
    
    // Remove fc-monetization dialogs
    document.querySelectorAll('.fc-monetization-dialog-container, .fc-message-root').forEach(el => el.remove());
    
    return true;
}
"""

# Close mobile app popup
CLOSE_MOBILE_POPUP = """
() => {
    const closeBtn = document.querySelector('[aria-label="Close shopping anchor"]');
    if (closeBtn) {
        closeBtn.click();
        return true;
    }
    return false;
}
"""

# Auto-dismiss JavaScript alerts
DISMISS_ALERTS = """
window.alert = function() { return true; };
window.confirm = function() { return true; };
"""

# Block notification requests
BLOCK_NOTIFICATIONS = """
Object.defineProperty(Notification, 'permission', { value: 'denied' });
Notification.requestPermission = function() { return Promise.resolve('denied'); };
"""

# Block fc-monetization popups using MutationObserver
BLOCK_FC_POPUPS = """
(() => {
    const cleanPage = () => {
        // Remove all iframes (ads)
        document.querySelectorAll('iframe').forEach(el => el.remove());
        // Remove fc-monetization popups
        document.querySelectorAll('.fc-monetization-dialog-container, .fc-message-root').forEach(el => el.remove());
        document.querySelectorAll('.fc-dialog-overlay').forEach(el => el.remove());
        document.querySelectorAll('.fc-consent-root').forEach(el => el.remove());
        // Remove other ad elements
        document.querySelectorAll('.adsbygoogle').forEach(el => el.remove());
        
        // Auto-click consent button if visible
        document.querySelectorAll('button').forEach(btn => {
            if (btn.textContent.includes('Consent') && btn.offsetParent !== null) {
                btn.click();
            }
        });
    };
    
    // Run after 800ms to let dialogs load
    setTimeout(cleanPage, 800);
    
    // Run on any DOM change
    const observer = new MutationObserver(cleanPage);
    if (document.body) {
        observer.observe(document.body, { childList: true, subtree: true });
    } else {
        document.addEventListener('DOMContentLoaded', () => {
            observer.observe(document.body, { childList: true, subtree: true });
        });
    }
})();
"""
