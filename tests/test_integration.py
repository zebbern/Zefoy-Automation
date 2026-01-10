"""Integration tests for zefoy automation.

These tests require manual CAPTCHA solving and are not run in CI.
Run with: pytest zefoy_cli/tests/test_integration.py -v -s
"""
import pytest
from zefoy_cli.browser.automation import ZefoyAutomation


@pytest.mark.skip(reason="Requires manual CAPTCHA solving")
@pytest.mark.asyncio
async def test_full_hearts_flow():
    """Test the full hearts automation flow.
    
    This test requires manual intervention to solve the CAPTCHA.
    It should be run in headed mode with -s flag.
    """
    automation = ZefoyAutomation(headless=False)
    
    try:
        await automation.start()
        await automation.handle_initial_setup()
        await automation.solve_captcha_manual()
        
        result = await automation.send_hearts("https://vm.tiktok.com/ZNRh8mDeP/")
        
        assert "success" in result
        assert "message" in result
        assert "wait_time" in result
        
    finally:
        await automation.close()


@pytest.mark.skip(reason="Requires manual CAPTCHA solving")
@pytest.mark.asyncio
async def test_automation_can_start():
    """Test that automation can start and navigate to zefoy."""
    automation = ZefoyAutomation(headless=False)
    
    try:
        await automation.start()
        assert automation.page is not None
        assert automation.browser is not None
        assert automation.popup_handlers is not None
    finally:
        await automation.close()
