"""Rate limit timer utilities."""
import re
import asyncio
from typing import Callable, Awaitable

# Ban threshold: 24 hours in seconds
BAN_THRESHOLD_SECONDS = 86400


def parse_wait_time(text: str) -> int:
    """Parse wait time from zefoy status text.
    
    Examples:
        "Please wait 2 minute(s) 57 second(s)" -> 177 seconds
        "Please wait 0 minute(s) 30 seconds" -> 30 seconds
        "Please wait 24 hour(s) 0 minute(s)" -> 86400 seconds
    
    Args:
        text: Status text from zefoy page.
        
    Returns:
        Total seconds to wait, or 0 if ready/not found.
    """
    if "READY" in text.upper():
        return 0
    
    hours = 0
    minutes = 0
    seconds = 0
    
    hour_match = re.search(r"(\d+)\s*hour", text)
    if hour_match:
        hours = int(hour_match.group(1))
    
    min_match = re.search(r"(\d+)\s*minute", text)
    if min_match:
        minutes = int(min_match.group(1))
    
    sec_match = re.search(r"(\d+)\s*second", text)
    if sec_match:
        seconds = int(sec_match.group(1))
    
    return hours * 3600 + minutes * 60 + seconds


def is_likely_ban(wait_time: int) -> bool:
    """Check if wait time indicates a likely ban.
    
    Args:
        wait_time: Wait time in seconds.
        
    Returns:
        True if wait time exceeds ban threshold (24 hours).
    """
    return wait_time >= BAN_THRESHOLD_SECONDS


async def wait_with_progress(
    seconds: int,
    callback: Callable[[int], Awaitable[None]] | None = None
) -> None:
    """Wait for the specified seconds with optional progress callback.
    
    Args:
        seconds: Number of seconds to wait.
        callback: Optional async function called each second with remaining time.
    """
    for remaining in range(seconds, 0, -1):
        if callback:
            await callback(remaining)
        await asyncio.sleep(1)
