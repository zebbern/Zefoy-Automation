"""
Zefoy-CLI Automation - Browser Automation Module
=================================================

Main Playwright automation class for zefoy.com.

Author: zebbern (https://github.com/zebbern)
Repository: https://github.com/zebbern/Zefoy-Automation
License: MIT
Copyright (c) 2024 zebbern
"""
from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, AsyncGenerator

if TYPE_CHECKING:
    from playwright.async_api import Page, Browser, BrowserContext

from playwright.async_api import async_playwright
from browser.popup_handlers import PopupHandlers
from browser.captcha_solver import CaptchaSolver
from services.hearts import HeartsService
from services.favorites import FavoritesService
from services.comment_hearts import CommentHeartsService
from utils.colors import success, error, dim, info


# Default timeouts (in milliseconds)
DEFAULT_TIMEOUT = 10000  # 10 seconds for element operations
DEFAULT_NAVIGATION_TIMEOUT = 60000  # 60 seconds for navigation


# Service configuration
SERVICES = {
    "hearts": {
        "name": "Hearts",
        "selector": ".t-hearts-button",
        "class": HeartsService,
    },
    "favorites": {
        "name": "Favorites",
        "selector": ".t-favorites-button",
        "class": FavoritesService,
    },
    "chearts": {
        "name": "Comment Hearts",
        "selector": ".t-chearts-button",
        "class": CommentHeartsService,
    },
    "followers": {
        "name": "Followers",
        "selector": ".t-followers-button",
        "class": None,  # Not implemented
    },
    "views": {
        "name": "Views",
        "selector": ".t-views-button",
        "class": None,  # Not implemented
    },
    "shares": {
        "name": "Shares",
        "selector": ".t-shares-button",
        "class": None,  # Not implemented
    },
}


class ZefoyAutomation:
    """Main automation controller for zefoy.com."""
    
    BASE_URL = "https://zefoy.com"
    
    MAIN_PAGE_SELECTORS = [
        ".t-hearts-button",
        ".t-followers-button",
        ".t-views-button",
    ]
    
    def __init__(self, headless: bool = False, verbose: bool = False, proxy: str | None = None) -> None:
        """Initialize the automation controller."""
        self.headless = headless
        self.verbose = verbose
        self.proxy = proxy
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self.popup_handlers: PopupHandlers | None = None
        self.captcha_solver: CaptchaSolver | None = None
        self._playwright = None
        self._available_services: dict[str, bool] = {}
        self._selectable_services: list[str] = []  # Ordered list for selection
    
    async def start(self) -> None:
        """Start the browser and navigate to zefoy."""
        self._playwright = await async_playwright().start()
        
        # Use Firefox for SOCKS5 proxy with auth, Chromium otherwise
        if self.proxy and 'socks' in self.proxy.lower():
            self.browser = await self._playwright.firefox.launch(
                headless=self.headless
            )
        else:
            # Stealth options to avoid bot detection (Chromium only)
            self.browser = await self._playwright.chromium.launch(
                headless=self.headless,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-infobars',
                    '--no-first-run',
                ]
            )
        
        # Use realistic context settings
        context_options = {
            'viewport': {'width': 1280, 'height': 720},
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        }
        
        # Add proxy if provided
        if self.proxy:
            # Parse proxy URL for authentication
            # Format: socks5://user:pass@host:port or http://user:pass@host:port
            import re
            proxy_match = re.match(r'(\w+)://(?:([^:]+):([^@]+)@)?([^:]+):(\d+)', self.proxy)
            if proxy_match:
                scheme, username, password, host, port = proxy_match.groups()
                proxy_config = {'server': f'{scheme}://{host}:{port}'}
                if username and password:
                    proxy_config['username'] = username
                    proxy_config['password'] = password
                context_options['proxy'] = proxy_config
            else:
                context_options['proxy'] = {'server': self.proxy}
        
        self.context = await self.browser.new_context(**context_options)
        self.page = await self.context.new_page()
        
        # Set default timeouts for better reliability
        self.page.set_default_timeout(DEFAULT_TIMEOUT)
        self.page.set_default_navigation_timeout(DEFAULT_NAVIGATION_TIMEOUT)
        
        self.popup_handlers = PopupHandlers(self.page, verbose=self.verbose)
        self.captcha_solver = CaptchaSolver(self.page, verbose=self.verbose)
        
        await self.popup_handlers.inject_blocking_scripts()
        
        await self.page.goto(
            self.BASE_URL,
            wait_until="domcontentloaded",
            timeout=DEFAULT_NAVIGATION_TIMEOUT
        )
    
    async def handle_initial_setup(self) -> None:
        """Handle all initial popups and get to main page."""
        if self.popup_handlers:
            await self.popup_handlers.handle_all_popups()
    
    async def is_on_main_page(self) -> bool:
        """Check if we're on the main page (past CAPTCHA)."""
        if not self.page:
            return False
        
        for selector in self.MAIN_PAGE_SELECTORS:
            try:
                element = self.page.locator(selector)
                if await element.is_visible(timeout=1000):
                    return True
            except Exception:
                continue
        return False
    
    async def detect_available_services(self) -> dict[str, bool]:
        """Detect which services are currently available."""
        if not self.page:
            return {}
        
        available = {}
        self._selectable_services = []
        
        for key, config in SERVICES.items():
            try:
                btn = self.page.locator(config["selector"])
                is_visible = await btn.is_visible(timeout=1000)
                
                if is_visible:
                    classes = await btn.get_attribute("class") or ""
                    is_disabled = "disabled" in classes.lower()
                    is_available = not is_disabled and config["class"] is not None
                    available[key] = is_available
                    if is_available:
                        self._selectable_services.append(key)
                else:
                    available[key] = False
            except Exception:
                available[key] = False
        
        self._available_services = available
        return available
    
    def print_service_status_with_selection(self) -> None:
        """Print the status of all services with selection numbers."""
        print("\n  Service Status:")
        print("  " + "-" * 40)
        
        selection_num = 1
        
        for key, config in SERVICES.items():
            name = config["name"]
            is_available = self._available_services.get(key, False)
            implemented = config["class"] is not None
            
            if is_available:
                # Show selection number for available services
                num_display = info(f"[{selection_num}]")
                status = success("ONLINE")
                print(f"  {num_display} {name:<18} {status}")
                selection_num += 1
            elif not implemented:
                status = dim("NOT IMPLEMENTED")
                print(f"      {name:<18} {status}")
            else:
                status = error("OFFLINE")
                print(f"      {name:<18} {status}")
        
        print("  " + "-" * 40)
    
    def get_service_by_selection(self, selection: int) -> str | None:
        """Get service key by selection number (1-indexed)."""
        idx = selection - 1
        if 0 <= idx < len(self._selectable_services):
            return self._selectable_services[idx]
        return None
    
    def get_selection_count(self) -> int:
        """Get the number of selectable services."""
        return len(self._selectable_services)
    
    async def wait_for_captcha_solved(self, timeout: int = 120) -> bool:
        """Wait for user to solve CAPTCHA on the website."""
        if not self.page:
            return False
        
        if self.popup_handlers:
            await self.popup_handlers.remove_ad_overlays()
        
        for i in range(timeout):
            if self.popup_handlers and i % 5 == 0:
                await self.popup_handlers.remove_ad_overlays()
            
            if await self.is_on_main_page():
                if self.popup_handlers:
                    await self.popup_handlers.handle_all_popups()
                return True
            
            remaining = timeout - i
            mins = remaining // 60
            secs = remaining % 60
            time_str = f"{mins}m {secs}s" if mins > 0 else f"{secs}s"
            print(f"\r  {dim(f'Waiting... {time_str} remaining')}", end="", flush=True)
            await self.page.wait_for_timeout(1000)
        
        return False
    
    async def solve_captcha_manual(self) -> str:
        """Wait for user to solve CAPTCHA on the website."""
        if await self.wait_for_captcha_solved():
            return "solved"
        return "timeout"
    
    async def solve_captcha_auto(self, max_attempts: int = 25, progress_callback=None) -> str:
        """Attempt to auto-solve CAPTCHA using OCR.
        
        Args:
            max_attempts: Maximum OCR attempts (default 25).
            progress_callback: Optional async callback for progress updates.
        
        Returns:
            'solved' if successful
            'manual' if auto-solve failed and manual solving is needed
            'timeout' if manual solving also timed out
        """
        if not self.captcha_solver:
            return "manual"
        
        # First, try auto-solving
        if await self.captcha_solver.solve(max_attempts=max_attempts, progress_callback=progress_callback):
            return "solved"
        
        # Auto-solve failed, fall back to manual
        print("\n  Auto-solve failed. Please solve manually...")
        if await self.wait_for_captcha_solved():
            return "solved"
        
        return "timeout"
    
    async def send_service(self, service_key: str, video_url: str) -> dict:
        """Send a service to a TikTok video."""
        if not self.page:
            return {"success": False, "message": "Page not initialized", "wait_time": 0}
        
        if service_key not in SERVICES:
            return {"success": False, "message": f"Unknown service: {service_key}", "wait_time": 0}
        
        service_config = SERVICES[service_key]
        if service_config["class"] is None:
            return {"success": False, "message": f"Service not implemented: {service_key}", "wait_time": 0}
        
        service = service_config["class"](self.page, verbose=self.verbose)
        return await service.send(video_url)
    
    async def send_hearts(self, video_url: str) -> dict:
        """Send hearts to a TikTok video (legacy method)."""
        return await self.send_service("hearts", video_url)
    
    async def clear_session(self) -> None:
        """Clear cookies and session data to reset tracking."""
        if self.context:
            await self.context.clear_cookies()
            if self.verbose:
                print(f"  {dim('Cleared cookies/session')}")
    
    async def close(self) -> None:
        """Close the browser."""
        try:
            if self.browser:
                await self.browser.close()
            if self._playwright:
                await self._playwright.stop()
        except Exception:
            pass


@asynccontextmanager
async def create_automation(
    headless: bool = False,
    verbose: bool = False,
    proxy: str | None = None
) -> AsyncGenerator[ZefoyAutomation, None]:
    """Context manager for creating and cleaning up ZefoyAutomation.
    
    Usage:
        async with create_automation() as automation:
            await automation.start()
            # ... use automation ...
    """
    automation = ZefoyAutomation(headless=headless, verbose=verbose, proxy=proxy)
    try:
        yield automation
    finally:
        await automation.close()
