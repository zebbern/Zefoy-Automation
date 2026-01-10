"""Tests for popup handlers module."""
import pytest
from unittest.mock import MagicMock
from zefoy_cli.browser.popup_handlers import PopupHandlers


def test_popup_handlers_init():
    """Test PopupHandlers initialization."""
    mock_page = MagicMock()
    mock_page.on = MagicMock()
    
    handlers = PopupHandlers(mock_page)
    
    assert handlers.page == mock_page
    mock_page.on.assert_called_once()


def test_popup_handlers_stores_page_reference():
    """Test that PopupHandlers stores the page reference correctly."""
    mock_page = MagicMock()
    
    handlers = PopupHandlers(mock_page)
    
    assert handlers.page is mock_page


def test_popup_handlers_registers_dialog_handler():
    """Test that PopupHandlers registers a dialog event handler."""
    mock_page = MagicMock()
    
    PopupHandlers(mock_page)
    
    # Verify that .on was called with "dialog" as first argument
    call_args = mock_page.on.call_args
    assert call_args[0][0] == "dialog"
