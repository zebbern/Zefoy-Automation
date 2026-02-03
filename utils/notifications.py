"""
Zefoy-CLI Automation - Discord Notifications
==============================================

Discord webhook notifications for milestones and alerts.

Author: zebbern (https://github.com/zebbern)
Repository: https://github.com/zebbern/Zefoy-Automation
License: MIT
Copyright (c) 2024 zebbern
"""
from __future__ import annotations

import os
from datetime import datetime
from typing import Any

try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False


# Environment variable for webhook URL
WEBHOOK_ENV_VAR = "ZEFOY_DISCORD_WEBHOOK"

# Notification colors (Discord format)
COLOR_SUCCESS = 0x00FF00  # Green
COLOR_WARNING = 0xFFAA00  # Orange
COLOR_ERROR = 0xFF0000    # Red
COLOR_INFO = 0x00AAFF     # Blue
COLOR_MILESTONE = 0xFFD700  # Gold


def get_webhook_url() -> str | None:
    """Get Discord webhook URL from config or environment."""
    # First check config
    try:
        from utils.config import get_config
        config = get_config()
        if config.notification.webhook_url:
            return config.notification.webhook_url
    except Exception:
        pass
    
    # Fallback to environment variable
    return os.environ.get(WEBHOOK_ENV_VAR)


def is_notifications_enabled() -> bool:
    """Check if notifications are enabled (webhook URL is set)."""
    return bool(get_webhook_url()) and AIOHTTP_AVAILABLE


async def send_webhook(
    title: str,
    description: str,
    color: int = COLOR_INFO,
    fields: list[dict[str, Any]] | None = None,
    footer: str | None = None,
    webhook_url: str | None = None,
) -> bool:
    """Send a Discord webhook notification.
    
    Args:
        title: Embed title
        description: Embed description
        color: Embed color (hex as int)
        fields: Optional list of field dicts with name, value, inline
        footer: Optional footer text
        webhook_url: Optional custom webhook URL (uses config/env if None)
        
    Returns:
        True if sent successfully, False otherwise
    """
    url = webhook_url or get_webhook_url()
    if not url or not AIOHTTP_AVAILABLE:
        return False
    
    embed: dict[str, Any] = {
        "title": title,
        "description": description,
        "color": color,
        "timestamp": datetime.utcnow().isoformat(),
    }
    
    if fields:
        embed["fields"] = fields
    
    if footer:
        embed["footer"] = {"text": footer}
    
    payload = {"embeds": [embed]}
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                return resp.status in (200, 204)
    except Exception:
        return False


async def notify_milestone(sent_count: int, service: str, video_url: str) -> bool:
    """Send notification when a milestone is reached.
    
    Args:
        sent_count: Number of successful sends
        service: Service name (Hearts, Favorites, etc)
        video_url: Target video URL
        
    Returns:
        True if sent successfully
    """
    # Only notify at certain milestones
    milestones = [10, 25, 50, 100, 250, 500, 1000]
    if sent_count not in milestones:
        return False
    
    return await send_webhook(
        title=f"🎉 Milestone: {sent_count} {service} Sent!",
        description=f"Reached {sent_count} successful sends!",
        color=COLOR_MILESTONE,
        fields=[
            {"name": "Service", "value": service.capitalize(), "inline": True},
            {"name": "Sent", "value": str(sent_count), "inline": True},
            {"name": "Video", "value": video_url[:50] + "..." if len(video_url) > 50 else video_url, "inline": False},
        ],
    )


async def notify_ban_detected(wait_time: int, service: str) -> bool:
    """Send notification when a potential ban is detected.
    
    Args:
        wait_time: Rate limit time in seconds
        service: Service name
        
    Returns:
        True if sent successfully
    """
    hours = wait_time // 3600
    return await send_webhook(
        title="🚫 Potential Ban Detected!",
        description=f"Rate limit exceeds 24 hours ({hours}h). Automation stopped.",
        color=COLOR_ERROR,
        fields=[
            {"name": "Service", "value": service.capitalize(), "inline": True},
            {"name": "Wait Time", "value": f"{hours} hours", "inline": True},
        ],
        footer="This may be a temporary IP ban. Try again later or use a different network.",
    )


async def notify_session_end(
    service: str,
    sent_count: int,
    attempts: int,
    elapsed_time: str,
    reason: str = "User stopped",
) -> bool:
    """Send notification when session ends.
    
    Args:
        service: Service name
        sent_count: Total successful sends
        attempts: Total attempts made
        elapsed_time: Human-readable elapsed time
        reason: Why session ended
        
    Returns:
        True if sent successfully
    """
    success_rate = (sent_count / attempts * 100) if attempts > 0 else 0
    
    return await send_webhook(
        title="📊 Session Summary",
        description=f"Automation session ended: {reason}",
        color=COLOR_INFO,
        fields=[
            {"name": "Service", "value": service.capitalize(), "inline": True},
            {"name": "Sent", "value": str(sent_count), "inline": True},
            {"name": "Attempts", "value": str(attempts), "inline": True},
            {"name": "Success Rate", "value": f"{success_rate:.1f}%", "inline": True},
            {"name": "Duration", "value": elapsed_time, "inline": True},
        ],
    )


async def notify_error(error: str, service: str) -> bool:
    """Send notification when an error occurs.
    
    Args:
        error: Error message
        service: Service name
        
    Returns:
        True if sent successfully
    """
    return await send_webhook(
        title="❌ Error Occurred",
        description=error[:500],  # Limit error message length
        color=COLOR_ERROR,
        fields=[
            {"name": "Service", "value": service.capitalize(), "inline": True},
        ],
    )
