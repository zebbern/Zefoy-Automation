"""Favorites service implementation."""
from services.base_service import BaseService
from browser.js_injections import REMOVE_AD_OVERLAYS


class FavoritesService(BaseService):
    """Favorites service for TikTok videos."""
    
    SERVICE_NAME = "Favorites"
    BUTTON_SELECTOR = ".t-favorites-button"
    
    async def click_service_button(self) -> None:
        """Click the Favorites service button."""
        await self.page.evaluate(REMOVE_AD_OVERLAYS)
        
        try:
            await self.page.locator(self.BUTTON_SELECTOR).click(force=True)
        except Exception:
            self._debug("Trying JavaScript click for Favorites button")
            await self.page.evaluate(f'''
                () => {{
                    const btn = document.querySelector("{self.BUTTON_SELECTOR}");
                    if (btn) {{
                        btn.click();
                        return true;
                    }}
                    return false;
                }}
            ''')
        
        await self.page.wait_for_timeout(1000)
