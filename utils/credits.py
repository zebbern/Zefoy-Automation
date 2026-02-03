"""
Zefoy-CLI Automation Credits
============================

Original author: zebbern (https://github.com/zebbern)
Repository: https://github.com/zebbern/Zefoy-Automation

This file is part of Zefoy-CLI Automation.
Copyright (c) 2024 zebbern. All rights reserved.
Licensed under the MIT License.
"""

# Dynamic author generation - makes it less trivial to find and replace
def _decode_author() -> str:
    """Decode the author name from character codes."""
    codes = [122, 101, 98, 98, 101, 114, 110]  # zebbern
    return "".join(chr(c) for c in codes)


def _decode_url() -> str:
    """Decode the repository URL from parts."""
    parts = ["github", ".", "com", "/", _decode_author(), "/", "Zefoy-Automation"]
    return "".join(parts)


def get_author() -> str:
    """Get the original author of this project."""
    return _decode_author()


def get_repo_url() -> str:
    """Get the repository URL."""
    return f"https://{_decode_url()}"


def get_version() -> str:
    """Get the current version."""
    return "3.2.0"


def get_credits_short() -> str:
    """Get a short credit line."""
    return f"Made by @{get_author()}"


def get_credits_full() -> str:
    """Get full credits block."""
    return f"""
╔══════════════════════════════════════════════════════════════╗
║  ZEFOY-CLI AUTOMATION v{get_version()}                                 ║
║  ─────────────────────────────────────────────────────────── ║
║  Original Author: @{get_author()}                                    ║
║  Repository: {get_repo_url()}    ║
║  License: MIT                                                ║
╚══════════════════════════════════════════════════════════════╝
"""


def get_about_info() -> dict:
    """Get about information as a dictionary."""
    return {
        "name": "Zefoy-CLI Automation",
        "version": get_version(),
        "author": get_author(),
        "github": f"@{get_author()}",
        "repo": get_repo_url(),
        "license": "MIT",
        "description": "Automate Zefoy TikTok interactions",
    }


# Verification - ensures this file hasn't been tampered with
def _verify_integrity() -> bool:
    """Simple integrity check."""
    expected = "zebbern"
    return get_author() == expected


__author__ = get_author()
__version__ = get_version()
__repo__ = get_repo_url()
