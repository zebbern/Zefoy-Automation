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

# K9x! Mouse Movement Simulation - Anti-bot bypass
# This generates realistic mouse movement data that Zefoy checks
# Based on reverse-engineered obfuscation from learn.md
MOUSE_SIMULATION_K9X = """
(() => {
    // Generate K9x! encoded mouse movement state string
    function generateK9xMouseData() {
        const points = [];
        const numPoints = Math.floor(Math.random() * 16) + 12; // 12-28 points
        
        for (let i = 0; i < numPoints; i++) {
            const x = Math.floor(Math.random() * 1850) + 50;  // 50-1900
            const y = Math.floor(Math.random() * 950) + 50;   // 50-1000
            const d = (Math.random() * 2.75 + 0.05).toFixed(4); // delay 0.05-2.8
            const g = Math.random() > 0.65 ? "True" : "False";  // click state
            points.push(`x=${x}&y=${y}&d=${d}&g=${g}`);
        }
        
        const raw = points.join("|");
        
        // XOR encode with rotating key
        let xored = "";
        for (let i = 0; i < raw.length; i++) {
            xored += String.fromCharCode(raw.charCodeAt(i) ^ ((i % 5) + 77));
        }
        
        // Wrap with K9x! markers
        const wrapped = "K9x!" + xored + "K9x!";
        
        // Base64 encode
        const encoded = btoa(wrapped);
        
        // Reverse the string
        let reversed = encoded.split("").reverse().join("");
        
        // Pad to valid base64 length
        while (reversed.length % 4 !== 0) {
            reversed += "=";
        }
        
        return reversed;
    }
    
    // Inject into all hidden inputs
    function injectMouseData() {
        const mouseData = generateK9xMouseData();
        const hiddenInputs = document.querySelectorAll('input[type="hidden"]');
        
        hiddenInputs.forEach(input => {
            // Don't overwrite captcha_encoded or other important fields
            if (!input.value && input.name !== 'captcha_encoded') {
                input.value = mouseData;
            }
        });
        
        // Store for later use
        window.__zefoyMouseData = mouseData;
    }
    
    // Run immediately and on form interactions
    // Delay initial injection to let page load
    setTimeout(injectMouseData, 500);
    setTimeout(injectMouseData, 1500);
    setTimeout(injectMouseData, 3000);
    
    // Re-inject before any form submission
    document.addEventListener('submit', function(e) {
        injectMouseData();
    }, true);
    
    // Re-inject on button clicks (for AJAX submissions)
    document.addEventListener('click', function(e) {
        if (e.target.tagName === 'BUTTON' || e.target.closest('button')) {
            setTimeout(injectMouseData, 50);
        }
    }, true);
    
    // Also re-inject when new elements are added to DOM
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length > 0) {
                setTimeout(injectMouseData, 100);
            }
        });
    });
    
    if (document.body) {
        observer.observe(document.body, { childList: true, subtree: true });
    } else {
        document.addEventListener('DOMContentLoaded', function() {
            observer.observe(document.body, { childList: true, subtree: true });
            injectMouseData();
        });
    }
    
    // Also expose for manual injection
    window.generateK9xMouseData = generateK9xMouseData;
    window.injectMouseData = injectMouseData;
})();
"""


# Generate proper cf_ob_te cookie to avoid anti-bot trap
# Based on reverse-engineered logic from learn.md
GENERATE_CF_OB_TE = """
(() => {
    // List of domains to ignore in stack trace
    const ignoreList = [
        "pagead2.googlesyndication.com",
        "googletagmanager.com",
        "www.googletagmanager.com",
        "ep2.adtrafficquality.google",
        "cdnjs.cloudflare.com",
        "boq-content-ads-contributor"
    ];
    
    // Generate a realistic source for the cookie
    function generateCfObTeCookie() {
        // Simulate a legitimate event source
        const source = "HTMLButtonElement.onclick@https://zefoy.com/:1:1";
        const kod = "DOMContentLoaded";
        
        const payload = `Kod: ${kod}\\nsource: ${source}`;
        const cookieValue = btoa(payload);
        
        // Set cookie with 5 hour expiry
        const expiry = new Date(Date.now() + 5 * 60 * 60 * 1000).toUTCString();
        document.cookie = `cf_ob_te=${cookieValue}; Path=/; Expires=${expiry}`;
        
        return cookieValue;
    }
    
    // Set the cookie immediately
    generateCfObTeCookie();
    
    // Refresh periodically
    setInterval(generateCfObTeCookie, 60000); // Every minute
    
    window.generateCfObTeCookie = generateCfObTeCookie;
})();
"""

# Fingerprint Spoofing Script
# This intercepts form submissions and replaces captcha_encoded with our spoofed version
# The spoofed value is passed from Python via window.__zefoy_spoofed_fingerprint
SPOOF_FINGERPRINT = '''
(() => {
    // This function will be called with our pre-generated spoofed captcha_encoded
    function setSpoofedFingerprint(value) {
        window.__zefoy_spoofed_fingerprint = value;
    }
    
    // Hook into captcha_encoded field updates
    function spoofCaptchaEncoded() {
        const spoofed = window.__zefoy_spoofed_fingerprint;
        if (!spoofed) return false;
        
        // Find all captcha_encoded fields and update them
        const fields = document.querySelectorAll('input[name="captcha_encoded"], #captcha_encoded');
        fields.forEach(field => {
            if (field) {
                field.value = spoofed;
            }
        });
        
        return fields.length > 0;
    }
    
    // Hook form submission to ensure our spoofed fingerprint is used
    document.addEventListener('submit', function(e) {
        spoofCaptchaEncoded();
    }, true);
    
    // Also hook button clicks (for AJAX submissions)
    document.addEventListener('click', function(e) {
        if (e.target.tagName === 'BUTTON' || e.target.closest('button')) {
            setTimeout(spoofCaptchaEncoded, 10);
        }
    }, true);
    
    // Monitor for dynamically added captcha_encoded fields
    const observer = new MutationObserver(function() {
        spoofCaptchaEncoded();
    });
    
    if (document.body) {
        observer.observe(document.body, { childList: true, subtree: true });
    } else {
        document.addEventListener('DOMContentLoaded', function() {
            observer.observe(document.body, { childList: true, subtree: true });
        });
    }
    
    // Expose functions
    window.setSpoofedFingerprint = setSpoofedFingerprint;
    window.spoofCaptchaEncoded = spoofCaptchaEncoded;
})();
'''
