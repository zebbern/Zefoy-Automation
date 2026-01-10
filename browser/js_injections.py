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
