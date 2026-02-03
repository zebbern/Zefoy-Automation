"""
Zefoy-CLI Automation - Configuration Module
=============================================

Persistent configuration management with JSON storage.

Author: zebbern (https://github.com/zebbern)
Repository: https://github.com/zebbern/Zefoy-Automation
License: MIT
Copyright (c) 2024 zebbern
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any


# Default config file location
CONFIG_DIR = Path.home() / ".zefoy"
CONFIG_FILE = CONFIG_DIR / "config.json"


@dataclass
class NotificationSettings:
    """Discord notification settings."""
    webhook_url: str = ""
    milestones: list[int] = field(default_factory=lambda: [10, 25, 50, 100, 250, 500, 1000])
    notify_on_errors: bool = True
    send_session_summary: bool = True
    notify_on_ban: bool = True


@dataclass
class AutomationSettings:
    """Automation behavior settings."""
    captcha_max_attempts: int = 25
    auto_retry_delay: int = 3  # Extra seconds after rate limit
    headless_mode: bool = True
    debug_mode: bool = False
    proxy_url: str = ""
    browser_timeout: int = 30  # Seconds to wait for page loads
    auto_solve_captcha: bool = True
    stop_on_ban: bool = True  # Auto-stop when IP ban detected
    max_consecutive_errors: int = 5  # Stop after N consecutive errors
    safe_mode: bool = False  # Enable rate limiting (4 sends/hour)
    safe_mode_delay: int = 900  # Seconds between sends in safe mode (15 min)


@dataclass
class Config:
    """Main configuration container."""
    notification: NotificationSettings = field(default_factory=NotificationSettings)
    automation: AutomationSettings = field(default_factory=AutomationSettings)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert config to dictionary."""
        return {
            "notification": asdict(self.notification),
            "automation": asdict(self.automation),
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Config":
        """Create config from dictionary."""
        config = cls()
        
        if "notification" in data:
            n = data["notification"]
            config.notification = NotificationSettings(
                webhook_url=n.get("webhook_url", ""),
                milestones=n.get("milestones", [10, 25, 50, 100, 250, 500, 1000]),
                notify_on_errors=n.get("notify_on_errors", True),
                send_session_summary=n.get("send_session_summary", True),
                notify_on_ban=n.get("notify_on_ban", True),
            )
        
        if "automation" in data:
            a = data["automation"]
            config.automation = AutomationSettings(
                captcha_max_attempts=a.get("captcha_max_attempts", 25),
                auto_retry_delay=a.get("auto_retry_delay", 3),
                headless_mode=a.get("headless_mode", True),
                debug_mode=a.get("debug_mode", False),
                proxy_url=a.get("proxy_url", ""),
                browser_timeout=a.get("browser_timeout", 30),
                auto_solve_captcha=a.get("auto_solve_captcha", True),
                stop_on_ban=a.get("stop_on_ban", True),
                max_consecutive_errors=a.get("max_consecutive_errors", 5),
                safe_mode=a.get("safe_mode", False),
                safe_mode_delay=a.get("safe_mode_delay", 900),
            )
        
        return config


# Global config instance
_config: Config | None = None


def get_config() -> Config:
    """Get the current configuration (loads from file if needed)."""
    global _config
    if _config is None:
        _config = load_config()
    return _config


def load_config() -> Config:
    """Load configuration from file."""
    global _config
    
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            _config = Config.from_dict(data)
        except (json.JSONDecodeError, OSError):
            _config = Config()
    else:
        _config = Config()
    
    return _config


def save_config(config: Config | None = None) -> bool:
    """Save configuration to file."""
    global _config
    
    if config is not None:
        _config = config
    
    if _config is None:
        return False
    
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(_config.to_dict(), f, indent=2)
        return True
    except OSError:
        return False


def update_config(**kwargs) -> Config:
    """Update specific config values and save.
    
    Examples:
        update_config(webhook_url="https://...")
        update_config(captcha_max_attempts=30, headless_mode=False)
    """
    config = get_config()
    
    # Notification settings
    if "webhook_url" in kwargs:
        config.notification.webhook_url = kwargs["webhook_url"]
    if "milestones" in kwargs:
        config.notification.milestones = kwargs["milestones"]
    if "notify_on_errors" in kwargs:
        config.notification.notify_on_errors = kwargs["notify_on_errors"]
    if "send_session_summary" in kwargs:
        config.notification.send_session_summary = kwargs["send_session_summary"]
    if "notify_on_ban" in kwargs:
        config.notification.notify_on_ban = kwargs["notify_on_ban"]
    
    # Automation settings
    if "captcha_max_attempts" in kwargs:
        config.automation.captcha_max_attempts = kwargs["captcha_max_attempts"]
    if "auto_retry_delay" in kwargs:
        config.automation.auto_retry_delay = kwargs["auto_retry_delay"]
    if "headless_mode" in kwargs:
        config.automation.headless_mode = kwargs["headless_mode"]
    if "debug_mode" in kwargs:
        config.automation.debug_mode = kwargs["debug_mode"]
    if "proxy_url" in kwargs:
        config.automation.proxy_url = kwargs["proxy_url"]
    if "browser_timeout" in kwargs:
        config.automation.browser_timeout = kwargs["browser_timeout"]
    if "auto_solve_captcha" in kwargs:
        config.automation.auto_solve_captcha = kwargs["auto_solve_captcha"]
    if "stop_on_ban" in kwargs:
        config.automation.stop_on_ban = kwargs["stop_on_ban"]
    if "max_consecutive_errors" in kwargs:
        config.automation.max_consecutive_errors = kwargs["max_consecutive_errors"]
    if "safe_mode" in kwargs:
        config.automation.safe_mode = kwargs["safe_mode"]
    if "safe_mode_delay" in kwargs:
        config.automation.safe_mode_delay = kwargs["safe_mode_delay"]
    
    save_config(config)
    return config


def reset_config() -> Config:
    """Reset configuration to defaults."""
    global _config
    _config = Config()
    save_config(_config)
    return _config


def get_config_path() -> Path:
    """Get the path to the config file."""
    return CONFIG_FILE
