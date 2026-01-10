"""Tests for service implementations."""
import pytest
from zefoy_cli.services.hearts import HeartsService
from zefoy_cli.services.base_service import BaseService


def test_hearts_service_name():
    """Test Hearts service has correct SERVICE_NAME."""
    assert HeartsService.SERVICE_NAME == "Hearts"


def test_hearts_service_button_selector():
    """Test Hearts service has correct BUTTON_SELECTOR."""
    assert HeartsService.BUTTON_SELECTOR == ".t-hearts-button"


def test_hearts_service_inherits_base_service():
    """Test Hearts service inherits from BaseService."""
    assert issubclass(HeartsService, BaseService)
