"""Tests for timer utilities module."""
import pytest
from zefoy_cli.utils.timer import parse_wait_time


class TestParseWaitTime:
    """Tests for parse_wait_time function."""
    
    def test_parse_minutes_and_seconds(self):
        """Test parsing a message with both minutes and seconds."""
        text = "Please wait 2 minute(s) 57 second(s) before trying again."
        assert parse_wait_time(text) == 177
    
    def test_parse_zero_minutes(self):
        """Test parsing a message with zero minutes."""
        text = "Please wait 0 minute(s) 30 seconds"
        assert parse_wait_time(text) == 30
    
    def test_parse_ready_status(self):
        """Test parsing the READY status."""
        text = "Next Submit: READY....!"
        assert parse_wait_time(text) == 0
    
    def test_parse_ready_lowercase(self):
        """Test parsing ready status case insensitively."""
        text = "Status: ready"
        assert parse_wait_time(text) == 0
    
    def test_parse_empty_string(self):
        """Test parsing an empty string returns 0."""
        assert parse_wait_time("") == 0
    
    def test_parse_no_match(self):
        """Test parsing a success message returns 0."""
        assert parse_wait_time("25+ Hearts successfully sent.") == 0
    
    def test_parse_only_minutes(self):
        """Test parsing message with only minutes."""
        text = "Please wait 3 minutes"
        assert parse_wait_time(text) == 180
    
    def test_parse_only_seconds(self):
        """Test parsing message with only seconds."""
        text = "Please wait 45 seconds"
        assert parse_wait_time(text) == 45
