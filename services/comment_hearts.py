"""Comment Hearts service implementation."""
from .base_service import BaseService
from ..browser.js_injections import REMOVE_AD_OVERLAYS


class CommentHeartsService(BaseService):
    """Comment Hearts service for TikTok videos."""
    
    SERVICE_NAME = "Comment Hearts"
    BUTTON_SELECTOR = ".t-chearts-button"
    
    async def click_service_button(self) -> None:
        """Click the Comment Hearts service button."""
        await self.page.evaluate(REMOVE_AD_OVERLAYS)
        
        try:
            await self.page.locator(self.BUTTON_SELECTOR).click(force=True)
        except Exception:
            self._debug("Trying JavaScript click for Comment Hearts button")
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
