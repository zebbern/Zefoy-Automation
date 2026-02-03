"""CAPTCHA solver using OCR for zefoy.com."""
from __future__ import annotations

import asyncio
import io
import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from playwright.async_api import Page

# Lazy imports for optional dependencies
_easyocr_reader = None


def get_ocr_reader():
    """Lazy-load EasyOCR reader to avoid slow startup."""
    global _easyocr_reader
    if _easyocr_reader is None:
        import easyocr
        _easyocr_reader = easyocr.Reader(['en'], gpu=False, verbose=False)
    return _easyocr_reader


class CaptchaSolver:
    """Attempts to auto-solve the zefoy CAPTCHA using OCR."""
    
    def __init__(self, page: Page, verbose: bool = False) -> None:
        """Initialize the CAPTCHA solver."""
        self.page = page
        self.verbose = verbose
    
    def _debug(self, msg: str) -> None:
        """Print debug message if verbose."""
        if self.verbose:
            print(f"  [CAPTCHA] {msg}")
    
    async def get_captcha_image_url(self) -> str | None:
        """Extract the CAPTCHA image URL from the page."""
        result = await self.page.evaluate("""
            () => {
                const img = document.querySelector('img.img-thumbnail.card-img-top');
                return img ? img.src : null;
            }
        """)
        return result
    
    async def download_captcha_image(self) -> bytes | None:
        """Capture the CAPTCHA image by screenshotting the element."""
        try:
            # Find the CAPTCHA image element
            captcha_img = self.page.locator('img.img-thumbnail.card-img-top')
            
            if not await captcha_img.is_visible(timeout=3000):
                self._debug("CAPTCHA image not visible")
                return None
            
            image_url = await self.get_captcha_image_url()
            self._debug(f"Found CAPTCHA at: {image_url[:60] if image_url else 'unknown'}...")
            
            # Wait for image to be fully loaded (check natural dimensions)
            for _ in range(10):  # Try up to 10 times (5 seconds total)
                loaded = await self.page.evaluate("""
                    () => {
                        const img = document.querySelector('img.img-thumbnail.card-img-top');
                        if (img && img.complete && img.naturalWidth > 50) {
                            return true;
                        }
                        return false;
                    }
                """)
                if loaded:
                    break
                await asyncio.sleep(0.5)
            
            # Screenshot the CAPTCHA element directly - more reliable than fetching URL
            screenshot_bytes = await captcha_img.screenshot()
            
            if screenshot_bytes and len(screenshot_bytes) > 5000:  # Real CAPTCHA images are 10KB+
                self._debug(f"Captured screenshot: {len(screenshot_bytes)} bytes")
                return screenshot_bytes
            
            self._debug(f"Screenshot too small: {len(screenshot_bytes) if screenshot_bytes else 0} bytes")
            return None
            
        except Exception as e:
            self._debug(f"Failed to capture CAPTCHA: {e}")
            return None
    
    def preprocess_image(self, image_bytes: bytes) -> bytes:
        """Preprocess the image for better OCR results."""
        from PIL import Image, ImageFilter, ImageOps, ImageEnhance
        
        # Load image
        img = Image.open(io.BytesIO(image_bytes))
        
        # No resize - keep original size for speed
        
        # Convert to grayscale
        img = img.convert('L')
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0)
        
        # Apply slight median filter to reduce wave distortion noise
        img = img.filter(ImageFilter.MedianFilter(size=3))
        
        # Threshold to binary (dark text on white background)
        threshold = 130
        img = img.point(lambda p: 255 if p > threshold else 0)
        
        # Invert if needed (ensure dark text on white background)
        histogram = img.histogram()
        black_pixels = sum(histogram[:128])
        white_pixels = sum(histogram[128:])
        if black_pixels > white_pixels:
            img = ImageOps.invert(img)
        
        # Save to bytes
        output = io.BytesIO()
        img.save(output, format='PNG')
        return output.getvalue()
    
    def ocr_image(self, image_bytes: bytes) -> str:
        """Run OCR on the image and return the detected text."""
        try:
            from PIL import Image
            import numpy as np
            
            reader = get_ocr_reader()
            
            # Convert to numpy array for EasyOCR
            img = Image.open(io.BytesIO(image_bytes))
            img_array = np.array(img)
            
            # Run OCR with lowercase allowlist (captcha only uses lowercase letters)
            results = reader.readtext(
                img_array, 
                detail=0, 
                paragraph=True,
                allowlist='abcdefghijklmnopqrstuvwxyz '
            )
            
            if results:
                # Join all detected text and clean it
                text = ' '.join(results)
                # Remove non-alphabetic characters and spaces
                text = re.sub(r'[^a-zA-Z]', '', text).lower()
                self._debug(f"OCR detected: '{text}'")
                
                # Apply spell check correction
                corrected = self._correct_spelling(text)
                if corrected != text:
                    self._debug(f"Spell corrected: '{text}' -> '{corrected}'")
                    return corrected
                
                return text
            
            self._debug("OCR returned no results")
            return ""
            
        except Exception as e:
            self._debug(f"OCR error: {e}")
            return ""
    
    def _correct_spelling(self, text: str) -> str:
        """Correct common OCR errors using dictionary lookup."""
        try:
            import enchant
            d = enchant.Dict("en_US")
            
            # If word is already valid, return it
            if d.check(text):
                return text
            
            # Get suggestions and pick the closest one
            suggestions = d.suggest(text)
            if suggestions:
                # Filter to similar length words (OCR usually gets length right)
                similar_len = [s.lower() for s in suggestions if abs(len(s) - len(text)) <= 1]
                if similar_len:
                    return similar_len[0]
                return suggestions[0].lower()
            
            return text
        except Exception:
            return text
    
    async def enter_solution(self, text: str) -> bool:
        """Enter the CAPTCHA solution into the input field."""
        if not text:
            return False
        
        try:
            # Find and fill the input field
            input_field = self.page.locator('input[placeholder="Enter the word"]')
            if await input_field.is_visible(timeout=2000):
                await input_field.fill(text)
                self._debug(f"Entered CAPTCHA text: '{text}'")
                return True
        except Exception as e:
            self._debug(f"Failed to enter text: {e}")
        
        return False
    
    async def submit_captcha(self) -> bool:
        """Click the submit button after entering CAPTCHA."""
        try:
            # The submit button is a button with a checkmark icon
            # Try multiple selectors
            selectors = [
                'button:has(.fa-check)',
                'button.btn-primary',
                'button[type="submit"]',
                '.card button.btn',
            ]
            
            for selector in selectors:
                try:
                    btn = self.page.locator(selector).first
                    if await btn.is_visible(timeout=1000):
                        await btn.click()
                        self._debug(f"Clicked submit using: {selector}")
                        return True
                except Exception:
                    continue
            
            # Fallback: use JavaScript to click
            result = await self.page.evaluate("""
                () => {
                    // Find button near the captcha input
                    const input = document.querySelector('input[placeholder="Enter the word"]');
                    if (input) {
                        const container = input.closest('div');
                        const btn = container?.querySelector('button');
                        if (btn) {
                            btn.click();
                            return true;
                        }
                    }
                    // Try any btn-primary button
                    const primaryBtn = document.querySelector('button.btn-primary, button.btn-success');
                    if (primaryBtn) {
                        primaryBtn.click();
                        return true;
                    }
                    return false;
                }
            """)
            return result
            
        except Exception as e:
            self._debug(f"Failed to submit: {e}")
            return False
    
    async def solve(self, max_attempts: int = 25, progress_callback=None) -> bool:
        """
        Attempt to solve the CAPTCHA.
        
        Args:
            max_attempts: Maximum number of solve attempts.
            progress_callback: Optional async callback(attempt, max_attempts, status) for progress updates.
        
        Returns True if solved successfully, False otherwise.
        """
        from utils.colors import dim, success, error, warning
        
        print(f"\n  {dim('Attempting auto-solve CAPTCHA...')}")
        
        for attempt in range(1, max_attempts + 1):
            try:
                self._debug(f"Attempt {attempt}/{max_attempts}")
                
                # Report progress
                if progress_callback:
                    await progress_callback(attempt, max_attempts, "trying")
                
                # Wait for CAPTCHA to be fully rendered
                await asyncio.sleep(1.0)

                # Download the CAPTCHA image
                image_bytes = await self.download_captcha_image()
                if not image_bytes:
                    print(f"  {error('Failed to download CAPTCHA image')}")
                    if attempt < max_attempts:
                        await self._reload_page()
                    continue
                
                # Preprocess the image
                processed = self.preprocess_image(image_bytes)
                
                # Run OCR
                text = self.ocr_image(processed)
                if not text or len(text) < 3:
                    print(f"  {warning(f'OCR failed on attempt {attempt}')}")
                    if attempt < max_attempts:
                        await self._reload_page()
                    continue
                
                print(f"  {dim(f'OCR detected:')} {text}")
                
                # Enter the solution
                if not await self.enter_solution(text):
                    print(f"  {error('Failed to enter solution')}")
                    continue
                
                # Submit
                await asyncio.sleep(0.5)
                await self.submit_captcha()
                
                # Wait and check if we passed
                await self.page.wait_for_timeout(2000)
                
                if await self._is_captcha_solved():
                    print(f"  {success('CAPTCHA solved automatically!')}")
                    return True
                
                print(f"  {warning(f'Solution incorrect, reloading...')}")
                if attempt < max_attempts:
                    await self._reload_page()
            except Exception as e:
                self._debug(f"Attempt {attempt} error: {e}")
                if attempt < max_attempts:
                    try:
                        await self._reload_page()
                    except Exception:
                        pass
        
        print(f"  {error(f'Auto-solve failed after {max_attempts} attempts')}")
        return False
    
    async def _reload_page(self) -> None:
        """Reload the page to get a fresh CAPTCHA."""
        from browser.popup_handlers import PopupHandlers
        
        try:
            self._debug("Refreshing page...")
            await self.page.goto("https://zefoy.com", timeout=5000)
            await self.page.wait_for_load_state("networkidle", timeout=5000)
            await asyncio.sleep(1)
            popup_handler = PopupHandlers(self.page, verbose=self.verbose)
            await popup_handler.handle_all_popups()
            await asyncio.sleep(1)
        except Exception as e:
            self._debug(f"Reload error: {e}")
    
    async def _is_captcha_solved(self) -> bool:
        """Check if the CAPTCHA has been solved (main page visible)."""
        selectors = [
            ".t-hearts-button",
            ".t-followers-button", 
            ".t-views-button",
            ".t-favorites-button",
        ]
        
        for selector in selectors:
            try:
                element = self.page.locator(selector)
                if await element.is_visible(timeout=1000):
                    return True
            except Exception:
                continue
        
        return False
