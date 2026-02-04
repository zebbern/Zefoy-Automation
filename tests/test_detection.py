"""
Zefoy Detection Test Script
============================

Tests what anti-bot signals Zefoy can detect from our current automation setup.
Run this to see what's being flagged before implementing bypasses.
"""
import asyncio
import json
from playwright.async_api import async_playwright


# Import our anti-bot bypass scripts
from browser.js_injections import MOUSE_SIMULATION_K9X, GENERATE_CF_OB_TE, SPOOF_FINGERPRINT
from utils.fingerprint import get_spoofed_captcha_encoded


async def test_detection():
    """Test what Zefoy detects about our browser."""
    
    print("\n" + "="*60)
    print("ZEFOY DETECTION TEST (WITH ANTI-BOT BYPASSES)")
    print("="*60 + "\n")
    
    async with async_playwright() as p:
        # Launch with current automation settings
        browser = await p.chromium.launch(
            headless=False,  # Visible for debugging
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-infobars',
                '--no-first-run',
            ]
        )
        
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        )
        
        page = await context.new_page()
        
        # Generate spoofed fingerprint
        print("[Setup] Generating spoofed fingerprint...")
        spoofed_fp = get_spoofed_captcha_encoded()
        print(f"  Generated fingerprint: {len(spoofed_fp)} chars")
        
        # Inject anti-bot bypass scripts BEFORE navigation
        print("\n[Setup] Injecting anti-bot bypass scripts...")
        await page.add_init_script(GENERATE_CF_OB_TE)
        await page.add_init_script(MOUSE_SIMULATION_K9X)
        await page.add_init_script(SPOOF_FINGERPRINT)
        await page.add_init_script(f"window.__zefoy_spoofed_fingerprint = {spoofed_fp!r};")
        print("  Injected cf_ob_te cookie generator")
        print("  Injected K9x! mouse simulation")
        print("  Injected fingerprint spoofer")
        
        # Test 1: Check navigator.webdriver
        print("\n[Test 1] Checking navigator.webdriver...")
        webdriver_check = await page.evaluate("() => navigator.webdriver")
        print(f"  navigator.webdriver = {webdriver_check}")
        if webdriver_check:
            print("  X DETECTED: webdriver is true (bot flag!)")
        else:
            print("  OK webdriver is false")
        
        # Test 2: Navigate to Zefoy
        print("\n[Test 2] Navigating to zefoy.com...")
        await page.goto("https://zefoy.com", wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(3)
        
        # Test 3: Check cf_ob_te cookie
        print("\n[Test 3] Checking cf_ob_te cookie...")
        cookies = await context.cookies()
        cf_ob_te = next((c for c in cookies if c['name'] == 'cf_ob_te'), None)
        if cf_ob_te:
            import base64
            try:
                decoded = base64.b64decode(cf_ob_te['value']).decode()
                print(f"  Cookie value: {decoded[:100]}...")
                if "unknown" in decoded.lower():
                    print("  X Cookie has 'unknown' source - suspicious!")
                else:
                    print("  OK Cookie has proper source!")
            except Exception as e:
                print(f"  Could not decode: {e}")
        else:
            print("  X No cf_ob_te cookie found!")
        
        # Test 4: Check hidden inputs for K9x! data
        print("\n[Test 4] Checking hidden inputs for K9x! mouse data...")
        hidden_inputs = await page.evaluate("""
            () => {
                const inputs = document.querySelectorAll('input[type="hidden"]');
                return Array.from(inputs).map(i => ({
                    name: i.name || i.id,
                    hasValue: !!i.value,
                    valueLength: i.value ? i.value.length : 0,
                    valuePreview: i.value ? i.value.substring(0, 50) : '(empty)'
                }));
            }
        """)
        
        for inp in hidden_inputs:
            if inp['name'] and inp['name'] != 'captcha_encoded':
                if inp['hasValue'] and inp['valueLength'] > 50:
                    print(f"  OK {inp['name']}: Has K9x! data ({inp['valueLength']} chars)")
                elif inp['hasValue']:
                    print(f"  ? {inp['name']}: Short value ({inp['valueLength']} chars)")
                else:
                    print(f"  X {inp['name']}: EMPTY - needs injection!")
        
        # Test 5: Check if K9x generator is available
        print("\n[Test 5] Checking K9x! generator availability...")
        k9x_available = await page.evaluate("() => typeof window.generateK9xMouseData === 'function'")
        if k9x_available:
            print("  OK K9x! generator is available")
            # Generate and show sample
            sample = await page.evaluate("() => window.generateK9xMouseData()")
            print(f"  Sample data: {sample[:60]}...")
        else:
            print("  X K9x! generator NOT available!")
        
        # Test 6: Manually trigger injection
        print("\n[Test 6] Triggering manual injection...")
        inject_available = await page.evaluate("() => typeof window.injectMouseData === 'function'")
        if inject_available:
            await page.evaluate("() => window.injectMouseData()")
            print("  OK Manual injection triggered")
            
            # Re-check hidden inputs
            hidden_inputs_after = await page.evaluate("""
                () => {
                    const inputs = document.querySelectorAll('input[type="hidden"]');
                    return Array.from(inputs).filter(i => i.name !== 'captcha_encoded').map(i => ({
                        name: i.name || i.id,
                        hasValue: !!i.value,
                        valueLength: i.value ? i.value.length : 0
                    }));
                }
            """)
            for inp in hidden_inputs_after:
                if inp['hasValue']:
                    print(f"  OK {inp['name']}: Now has data ({inp['valueLength']} chars)")
                else:
                    print(f"  X {inp['name']}: Still empty!")
        else:
            print("  X Injection function NOT available!")
        
        # Test 7: Check fingerprint spoofing
        print("\n[Test 7] Checking fingerprint spoofing...")
        spoof_available = await page.evaluate("() => typeof window.setSpoofedFingerprint === 'function'")
        if spoof_available:
            print("  OK Fingerprint spoofer is available")
            
            # Check if spoofed fingerprint is set
            has_spoofed = await page.evaluate("() => !!window.__zefoy_spoofed_fingerprint")
            if has_spoofed:
                fp_length = await page.evaluate("() => window.__zefoy_spoofed_fingerprint.length")
                print(f"  OK Spoofed fingerprint set ({fp_length} chars)")
            else:
                print("  X Spoofed fingerprint NOT set!")
            
            # Check captcha_encoded field if exists
            captcha_field = await page.evaluate("""
                () => {
                    const field = document.querySelector('input[name="captcha_encoded"], #captcha_encoded');
                    if (field) {
                        return {
                            exists: true,
                            hasValue: !!field.value,
                            valueLength: field.value ? field.value.length : 0
                        };
                    }
                    return { exists: false };
                }
            """)
            if captcha_field.get('exists'):
                print(f"  Found captcha_encoded field: {captcha_field['valueLength']} chars")
            else:
                print("  Note: captcha_encoded field not on this page (appears during form submission)")
        else:
            print("  X Fingerprint spoofer NOT available!")
        
        print("\n" + "="*60)
        print("TEST COMPLETE - All bypasses active")
        print("="*60)
        
        # Keep browser open briefly
        print("\nBrowser will stay open for 15 seconds...")
        await asyncio.sleep(15)
        
        await browser.close()


if __name__ == "__main__":
    asyncio.run(test_detection())
