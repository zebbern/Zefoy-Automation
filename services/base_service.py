"""Base class for zefoy services."""
from __future__ import annotations

import re
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from playwright.async_api import Page

from ..utils.timer import parse_wait_time
from ..utils.colors import dim
from ..browser.js_injections import REMOVE_AD_OVERLAYS


class BaseService(ABC):
    """Abstract base class for zefoy TikTok services."""
    
    SERVICE_NAME: str = ""
    BUTTON_SELECTOR: str = ""
    
    def __init__(self, page: Page, verbose: bool = False) -> None:
        """Initialize the service."""
        self.page = page
        self.verbose = verbose
    
    def _debug(self, msg: str) -> None:
        """Print debug message if verbose mode is on."""
        if self.verbose:
            print(f"  [DEBUG] {msg}")
    
    @abstractmethod
    async def click_service_button(self) -> None:
        """Click the service button to open the form."""
        pass
    
    async def enter_video_url(self, url: str) -> None:
        """Enter TikTok video URL into the search field."""
        await self.page.wait_for_timeout(1000)
        await self.page.evaluate(REMOVE_AD_OVERLAYS)
        
        input_selectors = [
            'input[placeholder="Enter Video URL"]:visible',
            'input[type="search"]:visible',
            'input.form-control:visible',
        ]
        
        searchbox = None
        for selector in input_selectors:
            try:
                elements = self.page.locator(selector)
                count = await elements.count()
                self._debug(f"Found {count} elements for: {selector}")
                
                if count > 0:
                    searchbox = elements.first
                    if await searchbox.is_visible(timeout=2000):
                        break
            except Exception as e:
                self._debug(f"Selector failed: {e}")
                continue
        
        if searchbox is None:
            self._debug("Using JavaScript fallback for input")
            await self.page.evaluate(f'''
                () => {{
                    const inputs = document.querySelectorAll('input[placeholder="Enter Video URL"]');
                    for (const input of inputs) {{
                        if (input.offsetParent !== null) {{
                            input.value = "{url}";
                            input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                            return true;
                        }}
                    }}
                    return false;
                }}
            ''')
            return
        
        await searchbox.fill(url)
    
    async def submit_search(self) -> None:
        """Click the search button."""
        await self.page.wait_for_timeout(500)
        
        search_selectors = [
            'button:has-text("Search"):visible',
            'button[type="submit"]:visible',
            '.btn:has-text("Search"):visible',
        ]
        
        for selector in search_selectors:
            try:
                btn = self.page.locator(selector).first
                if await btn.is_visible(timeout=2000):
                    await btn.click()
                    self._debug(f"Clicked Search using: {selector}")
                    return
            except Exception:
                continue
        
        self._debug("Using JavaScript fallback for search button")
        await self.page.evaluate('''
            () => {
                const buttons = document.querySelectorAll('button');
                for (const btn of buttons) {
                    if (btn.textContent.includes('Search') && btn.offsetParent !== null) {
                        btn.click();
                        return true;
                    }
                }
                return false;
            }
        ''')
    
    async def get_status_text(self) -> str:
        """Get the current status text (timer or ready)."""
        try:
            status_patterns = [
                ("Please wait", r"Please wait \d+ minute.*\d+ second"),
                ("READY", r"READY"),
                ("successfully sent", r"\d+\+ \w+ successfully sent"),
                ("seconds for your next", r"\d+ seconds for your next"),
            ]
            
            for text_hint, pattern in status_patterns:
                try:
                    elements = self.page.locator(f"div:has-text('{text_hint}')")
                    count = await elements.count()
                    
                    for i in range(min(count, 5)):
                        try:
                            el = elements.nth(i)
                            text = await el.inner_text(timeout=500)
                            if re.search(pattern, text, re.I):
                                for line in text.split('\n'):
                                    if re.search(pattern, line, re.I):
                                        return line.strip()
                        except Exception:
                            continue
                except Exception:
                    continue
        except Exception:
            pass
        return ""
    
    async def is_ready(self) -> bool:
        """Check if the service is ready for submission."""
        status = await self.get_status_text()
        return parse_wait_time(status) == 0
    
    async def get_wait_time(self) -> int:
        """Get remaining wait time in seconds."""
        status = await self.get_status_text()
        return parse_wait_time(status)
    
    async def click_send_button(self) -> None:
        """Click the numbered send button after search."""
        await self.page.wait_for_timeout(2000)
        
        selectors = [
            'button.btn-success:visible',
            'button:has-text("1"):visible',
            'button:has-text("25"):visible',
            'button:has-text("50"):visible',
            '.btn-success:visible',
        ]
        
        for selector in selectors:
            try:
                btn = self.page.locator(selector).first
                if await btn.is_visible(timeout=2000):
                    await btn.click()
                    self._debug(f"Clicked send using: {selector}")
                    return
            except Exception:
                continue
        
        self._debug("Using JavaScript fallback for send button")
        await self.page.evaluate('''
            () => {
                const buttons = document.querySelectorAll('button.btn-success, button.btn-primary');
                for (const btn of buttons) {
                    if (btn.offsetParent !== null) {
                        btn.click();
                        return true;
                    }
                }
                return false;
            }
        ''')
    
    async def send(self, video_url: str) -> dict:
        """Full send flow for a TikTok video."""
        await self.page.evaluate(REMOVE_AD_OVERLAYS)
        
        await self.click_service_button()
        await self.page.wait_for_timeout(1000)
        
        print(f"  {dim('Entering video URL...')}")
        await self.enter_video_url(video_url)
        
        print(f"  {dim('Searching...')}")
        await self.submit_search()
        
        await self.page.wait_for_timeout(3000)
        
        status = await self.get_status_text()
        self._debug(f"Status text: {status}")
        wait_time = parse_wait_time(status)
        
        if wait_time > 0 and "success" not in status.lower():
            return {
                "success": False,
                "message": f"Rate limited. Wait {wait_time} seconds.",
                "wait_time": wait_time
            }
        
        print(f"  {dim('Sending...')}")
        await self.click_send_button()
        
        await self.page.wait_for_timeout(2000)
        status = await self.get_status_text()
        
        if "success" in status.lower() or "sent" in status.lower():
            return {
                "success": True,
                "message": status,
                "wait_time": await self.get_wait_time()
            }
        
        return {
            "success": False,
            "message": status or "Unknown error",
            "wait_time": await self.get_wait_time()
        }
