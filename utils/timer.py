"""Rate limit timer utilities."""
import re
import asyncio
from typing import Callable, Awaitable


def parse_wait_time(text: str) -> int:
    """Parse wait time from zefoy status text.
    
    Examples:
        "Please wait 2 minute(s) 57 second(s)" -> 177 seconds
        "Please wait 0 minute(s) 30 seconds" -> 30 seconds
    
    Args:
        text: Status text from zefoy page.
        
    Returns:
        Total seconds to wait, or 0 if ready/not found.
    """
    if "READY" in text.upper():
        return 0
    
    minutes = 0
    seconds = 0
    
    min_match = re.search(r"(\d+)\s*minute", text)
    if min_match:
        minutes = int(min_match.group(1))
    
    sec_match = re.search(r"(\d+)\s*second", text)
    if sec_match:
        seconds = int(sec_match.group(1))
    
    return minutes * 60 + seconds


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
