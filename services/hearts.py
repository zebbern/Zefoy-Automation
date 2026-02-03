"""Hearts service implementation."""
from services.base_service import BaseService
from browser.js_injections import REMOVE_AD_OVERLAYS


class HeartsService(BaseService):
    """Hearts (likes) service for TikTok videos."""
    
    SERVICE_NAME = "Hearts"
    BUTTON_SELECTOR = ".t-hearts-button"
    
    async def click_service_button(self) -> None:
        """Click the Hearts service button."""
        await self.page.evaluate(REMOVE_AD_OVERLAYS)
        
        print(f"  💖 Opening {self.SERVICE_NAME} panel...")
        
        try:
            await self.page.locator(self.BUTTON_SELECTOR).click(force=True)
        except Exception:
            self._debug("Trying JavaScript click for Hearts button")
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
