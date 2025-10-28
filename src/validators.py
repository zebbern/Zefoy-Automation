"""
Input validation utilities for Zefoy Automation Bot
Ensures user inputs are valid and safe
"""

import re
from typing import List, Tuple
from urllib.parse import urlparse

from src.exceptions import InvalidInputError
from src import logger


def validate_url(url: str) -> bool:
    """
    Validate if the provided string is a valid URL
    
    Args:
        url: URL string to validate
        
    Returns:
        True if valid, False otherwise
        
    Raises:
        InvalidInputError: If URL is invalid
    """
    if not url or not isinstance(url, str):
        raise InvalidInputError("URL cannot be empty")
    
    url = url.strip()
    
    try:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            raise InvalidInputError(f"Invalid URL format: {url}")
        
        if result.scheme not in ['http', 'https']:
            raise InvalidInputError(f"URL must use http or https protocol: {url}")
        
        logger.debug(f"Validated URL: {url}")
        return True
        
    except Exception as e:
        raise InvalidInputError(f"Invalid URL: {url} - {str(e)}")


def validate_urls(urls: List[str]) -> List[str]:
    """
    Validate a list of URLs
    
    Args:
        urls: List of URL strings
        
    Returns:
        List of validated URLs
        
    Raises:
        InvalidInputError: If any URL is invalid
    """
    if not urls:
        raise InvalidInputError("At least one URL is required")
    
    validated = []
    for url in urls:
        url = url.strip()
        if url:
            validate_url(url)
            validated.append(url)
    
    if not validated:
        raise InvalidInputError("No valid URLs provided")
    
    logger.info(f"Validated {len(validated)} URL(s)")
    return validated


def validate_username(username: str) -> str:
    """
    Validate TikTok username format
    
    Args:
        username: Username to validate
        
    Returns:
        Validated username
        
    Raises:
        InvalidInputError: If username is invalid
    """
    if not username or not isinstance(username, str):
        raise InvalidInputError("Username cannot be empty")
    
    username = username.strip()
    
    # TikTok usernames start with @ and contain alphanumeric, underscore, or dot
    if not username.startswith('@'):
        raise InvalidInputError(f"Username must start with @: {username}")
    
    # Remove @ for pattern matching
    username_part = username[1:]
    
    if not username_part:
        raise InvalidInputError("Username cannot be just @")
    
    # TikTok username pattern: alphanumeric, underscore, dot (2-24 chars)
    pattern = r'^[a-zA-Z0-9_.]{2,24}$'
    if not re.match(pattern, username_part):
        raise InvalidInputError(
            f"Invalid username format: {username}. "
            "Must contain 2-24 alphanumeric characters, underscores, or dots"
        )
    
    logger.debug(f"Validated username: {username}")
    return username


def validate_service_choice(choice: str, max_services: int) -> int:
    """
    Validate service choice input
    
    Args:
        choice: User's choice as string
        max_services: Maximum number of available services
        
    Returns:
        Validated choice as integer
        
    Raises:
        InvalidInputError: If choice is invalid
    """
    try:
        choice_int = int(choice.strip())
    except (ValueError, AttributeError):
        raise InvalidInputError(f"Invalid choice: must be a number between 1 and {max_services}")
    
    if choice_int < 1 or choice_int > max_services:
        raise InvalidInputError(f"Choice must be between 1 and {max_services}")
    
    logger.debug(f"Validated service choice: {choice_int}")
    return choice_int


def sanitize_input(user_input: str) -> str:
    """
    Sanitize user input by removing potentially dangerous characters
    
    Args:
        user_input: Raw user input
        
    Returns:
        Sanitized input
    """
    if not user_input:
        return ""
    
    # Remove any script tags or HTML
    sanitized = re.sub(r'<[^>]*>', '', user_input)
    
    # Remove null bytes
    sanitized = sanitized.replace('\x00', '')
    
    # Strip whitespace
    sanitized = sanitized.strip()
    
    return sanitized


def parse_url_list(urls_input: str) -> List[str]:
    """
    Parse space-separated URL list from user input
    
    Args:
        urls_input: Space-separated URLs as string
        
    Returns:
        List of validated URLs
        
    Raises:
        InvalidInputError: If input is invalid
    """
    if not urls_input:
        raise InvalidInputError("URL input cannot be empty")
    
    # Sanitize input
    urls_input = sanitize_input(urls_input)
    
    # Split by whitespace
    urls = urls_input.split()
    
    # Validate all URLs
    return validate_urls(urls)


def validate_wait_time(min_wait: int, max_wait: int) -> Tuple[int, int]:
    """
    Validate wait time bounds
    
    Args:
        min_wait: Minimum wait time
        max_wait: Maximum wait time
        
    Returns:
        Tuple of (min_wait, max_wait)
        
    Raises:
        InvalidInputError: If wait times are invalid
    """
    if not isinstance(min_wait, int) or not isinstance(max_wait, int):
        raise InvalidInputError("Wait times must be integers")
    
    if min_wait < 0 or max_wait < 0:
        raise InvalidInputError("Wait times cannot be negative")
    
    if min_wait > max_wait:
        raise InvalidInputError(f"Minimum wait ({min_wait}) cannot exceed maximum wait ({max_wait})")
    
    return (min_wait, max_wait)
