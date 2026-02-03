"""Handlers for various popups and dialogs on zefoy.com."""
from playwright.async_api import Page, Dialog
from browser.js_injections import (
    REMOVE_AD_OVERLAYS,
    CLOSE_MOBILE_POPUP,
    DISMISS_ALERTS,
    BLOCK_NOTIFICATIONS,
    BLOCK_FC_POPUPS
)


class PopupHandlers:
    """Collection of popup/dialog handlers for zefoy.com."""
    
    def __init__(self, page: Page, verbose: bool = False) -> None:
        """Initialize popup handlers."""
        self.page = page
        self.verbose = verbose
        self._setup_dialog_handler()
    
    def _debug(self, msg: str) -> None:
        """Print debug message if verbose."""
        if self.verbose:
            print(f"  [DEBUG] {msg}")
    
    def _setup_dialog_handler(self) -> None:
        """Setup automatic dialog dismissal."""
        async def handle_dialog(dialog: Dialog) -> None:
            await dialog.accept()
        self.page.on("dialog", handle_dialog)
    
    async def inject_blocking_scripts(self) -> None:
        """Inject scripts to block popups before they appear."""
        await self.page.add_init_script(DISMISS_ALERTS)
        await self.page.add_init_script(BLOCK_NOTIFICATIONS)
        await self.page.add_init_script(BLOCK_FC_POPUPS)
    
    async def remove_ad_overlays(self) -> bool:
        """Remove all ad iframes and overlays."""
        return await self.page.evaluate(REMOVE_AD_OVERLAYS)
    
    async def close_mobile_popup(self) -> bool:
        """Close the mobile app promotion popup."""
        return await self.page.evaluate(CLOSE_MOBILE_POPUP)
    
    async def handle_gdpr_consent(self) -> bool:
        """Click the consent button on GDPR dialog."""
        selectors = [
            'button:has-text("Consent")',
            '.fc-cta-consent',
            '.fc-button-label:has-text("Consent")',
        ]
        
        for selector in selectors:
            try:
                btn = self.page.locator(selector).first
                if await btn.is_visible(timeout=500):
                    await btn.click(force=True)
                    self._debug(f"Clicked consent: {selector}")
                    await self.page.wait_for_timeout(300)
                    return True
            except Exception:
                continue
        
        return False
    
    async def handle_ad_gate(self) -> bool:
        """Remove the 'Unlock more content' modal by removing it from DOM."""
        try:
            removed = await self.page.evaluate("""
                () => {
                    // Target the exact element first
                    const fcRoot = document.querySelector('body > div.fc-message-root');
                    if (fcRoot) {
                        fcRoot.remove();
                        return true;
                    }
                    
                    // Fallback: remove by class names
                    const selectors = [
                        '.fc-monetization-dialog-container',
                        '.fc-message-root',
                        '.fc-dialog-container',
                        '[class*="fc-"][class*="container"]'
                    ];
                    
                    for (const sel of selectors) {
                        const el = document.querySelector(sel);
                        if (el) {
                            el.remove();
                            return true;
                        }
                    }
                    return false;
                }
            """)
            if removed:
                self._debug("Removed 'Unlock more content' modal")
            return removed
        except Exception as e:
            self._debug(f"Ad gate error: {e}")
            return False
    
    async def handle_all_popups(self) -> None:
        """Handle all known popups efficiently."""
        # Inject the observer that auto-removes popups
        await self.inject_blocking_scripts()
        
        # Explicitly click consent (JS may fire before button is ready)
        await self.handle_gdpr_consent()
        
        # Quick cleanup
        await self.remove_ad_overlays()
