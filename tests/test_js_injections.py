"""Tests for JavaScript injection module."""
import pytest
from zefoy_cli.browser.js_injections import (
    REMOVE_AD_OVERLAYS,
    CLOSE_MOBILE_POPUP,
    DISMISS_ALERTS,
    BLOCK_NOTIFICATIONS
)


def test_remove_ad_overlays_is_non_empty_string():
    """Verify REMOVE_AD_OVERLAYS is a non-empty string."""
    assert isinstance(REMOVE_AD_OVERLAYS, str)
    assert len(REMOVE_AD_OVERLAYS) > 0


def test_close_mobile_popup_is_non_empty_string():
    """Verify CLOSE_MOBILE_POPUP is a non-empty string."""
    assert isinstance(CLOSE_MOBILE_POPUP, str)
    assert len(CLOSE_MOBILE_POPUP) > 0


def test_dismiss_alerts_is_non_empty_string():
    """Verify DISMISS_ALERTS is a non-empty string."""
    assert isinstance(DISMISS_ALERTS, str)
    assert len(DISMISS_ALERTS) > 0


def test_block_notifications_is_non_empty_string():
    """Verify BLOCK_NOTIFICATIONS is a non-empty string."""
    assert isinstance(BLOCK_NOTIFICATIONS, str)
    assert len(BLOCK_NOTIFICATIONS) > 0
