"""Handlers for various popups and dialogs on zefoy.com."""
from playwright.async_api import Page, Dialog
from .js_injections import (
    REMOVE_AD_OVERLAYS,
    CLOSE_MOBILE_POPUP,
    DISMISS_ALERTS,
    BLOCK_NOTIFICATIONS
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
            '[aria-label*="consent" i]',
            'button.fc-cta-consent',
        ]
        
        for selector in selectors:
            try:
                btn = self.page.locator(selector).first
                if await btn.is_visible(timeout=2000):
                    await btn.click(force=True)
                    self._debug(f"Clicked consent: {selector}")
                    await self.page.wait_for_timeout(1000)
                    return True
            except Exception:
                continue
        
        try:
            consent_btn = self.page.get_by_role("button", name="Consent")
            if await consent_btn.is_visible(timeout=2000):
                await consent_btn.click(force=True)
                self._debug("Clicked consent via role selector")
                return True
        except Exception:
            pass
        
        return False
    
    async def handle_ad_gate(self) -> bool:
        """Click through the 'View a short ad' modal."""
        try:
            ad_btn = self.page.get_by_role("button", name="View a short ad")
            if await ad_btn.is_visible(timeout=3000):
                await ad_btn.click()
                await self.page.wait_for_timeout(2000)
                await self.remove_ad_overlays()
                return True
        except Exception:
            pass
        return False
    
    async def handle_all_popups(self) -> None:
        """Handle all known popups in sequence."""
        await self.inject_blocking_scripts()
        
        # Try consent multiple times
        for _ in range(3):
            if await self.handle_gdpr_consent():
                break
            await self.page.wait_for_timeout(1000)
        
        await self.handle_ad_gate()
        await self.remove_ad_overlays()
        await self.close_mobile_popup()
