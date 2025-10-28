"""
Reusable Selenium actions for Zefoy Automation Bot
Provides high-level abstractions for common browser interactions
"""

import time
from typing import Optional, Callable
from functools import wraps

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
    ElementClickInterceptedException
)

from src import config
from src import logger
from src.exceptions import ElementNotFoundError, TimeoutError as BotTimeoutError


def retry_on_exception(max_retries: int = 3, delay: int = 2, exceptions: tuple = (Exception,)):
    """
    Decorator to retry a function on exception
    
    Args:
        max_retries: Maximum number of retry attempts
        delay: Delay between retries in seconds
        exceptions: Tuple of exceptions to catch
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    logger.warning(
                        f"{func.__name__} failed (attempt {attempt + 1}/{max_retries}): {str(e)}"
                    )
                    if attempt < max_retries - 1:
                        time.sleep(delay)
            logger.error(f"{func.__name__} failed after {max_retries} attempts")
            raise last_exception
        return wrapper
    return decorator


class SeleniumActions:
    """High-level Selenium actions with error handling and retry logic"""
    
    def __init__(self, driver: WebDriver):
        """
        Initialize Selenium actions
        
        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, config.DEFAULT_TIMEOUT)
    
    @retry_on_exception(
        max_retries=config.MAX_RETRIES,
        delay=config.RETRY_DELAY,
        exceptions=(StaleElementReferenceException, NoSuchElementException)
    )
    def find_element(
        self,
        by: By,
        value: str,
        timeout: int = None,
        description: str = None
    ) -> WebElement:
        """
        Find an element with retry logic
        
        Args:
            by: Selenium By locator type
            value: Locator value (XPath, CSS selector, etc.)
            timeout: Custom timeout in seconds
            description: Human-readable element description for logging
            
        Returns:
            WebElement if found
            
        Raises:
            ElementNotFoundError: If element is not found
        """
        timeout = timeout or config.DEFAULT_TIMEOUT
        wait = WebDriverWait(self.driver, timeout)
        
        try:
            element = wait.until(EC.presence_of_element_located((by, value)))
            logger.debug(f"Found element: {description or value}")
            return element
        except TimeoutException:
            error_msg = description or f"element with {by}={value}"
            logger.error(f"Element not found: {error_msg}")
            raise ElementNotFoundError(error_msg, value if by == By.XPATH else None)
    
    @retry_on_exception(
        max_retries=config.MAX_RETRIES,
        delay=config.RETRY_DELAY,
        exceptions=(StaleElementReferenceException, ElementClickInterceptedException)
    )
    def click_element(
        self,
        by: By,
        value: str,
        timeout: int = None,
        description: str = None
    ) -> None:
        """
        Click an element with retry logic
        
        Args:
            by: Selenium By locator type
            value: Locator value
            timeout: Custom timeout in seconds
            description: Human-readable element description
            
        Raises:
            ElementNotFoundError: If element is not found
        """
        timeout = timeout or config.DEFAULT_TIMEOUT
        wait = WebDriverWait(self.driver, timeout)
        
        try:
            element = wait.until(EC.element_to_be_clickable((by, value)))
            element.click()
            logger.info(f"Clicked: {description or value}")
        except TimeoutException:
            error_msg = description or f"element with {by}={value}"
            logger.error(f"Cannot click element: {error_msg}")
            raise ElementNotFoundError(error_msg, value if by == By.XPATH else None)
    
    @retry_on_exception(
        max_retries=config.MAX_RETRIES,
        delay=config.RETRY_DELAY,
        exceptions=(StaleElementReferenceException,)
    )
    def input_text(
        self,
        by: By,
        value: str,
        text: str,
        clear_first: bool = True,
        timeout: int = None,
        description: str = None
    ) -> None:
        """
        Input text into an element
        
        Args:
            by: Selenium By locator type
            value: Locator value
            text: Text to input
            clear_first: Whether to clear existing text first
            timeout: Custom timeout in seconds
            description: Human-readable element description
            
        Raises:
            ElementNotFoundError: If element is not found
        """
        element = self.find_element(by, value, timeout, description)
        
        if clear_first:
            element.clear()
            logger.debug(f"Cleared input field: {description or value}")
        
        element.send_keys(text)
        logger.info(f"Entered text into: {description or value}")
    
    def execute_script(
        self,
        script: str,
        *args,
        description: str = None
    ) -> any:
        """
        Execute JavaScript code
        
        Args:
            script: JavaScript code to execute
            *args: Arguments to pass to the script
            description: Description of what the script does
            
        Returns:
            Result of script execution
        """
        try:
            result = self.driver.execute_script(script, *args)
            logger.debug(f"Executed JavaScript: {description or 'custom script'}")
            return result
        except Exception as e:
            logger.error(f"JavaScript execution failed: {str(e)}")
            raise
    
    def wait_for_element_visible(
        self,
        by: By,
        value: str,
        timeout: int = None
    ) -> bool:
        """
        Wait for an element to become visible
        
        Args:
            by: Selenium By locator type
            value: Locator value
            timeout: Custom timeout in seconds
            
        Returns:
            True if element is visible, False otherwise
        """
        timeout = timeout or config.DEFAULT_TIMEOUT
        wait = WebDriverWait(self.driver, timeout)
        
        try:
            wait.until(EC.visibility_of_element_located((by, value)))
            return True
        except TimeoutException:
            return False
    
    def element_exists(self, by: By, value: str) -> bool:
        """
        Check if an element exists without waiting
        
        Args:
            by: Selenium By locator type
            value: Locator value
            
        Returns:
            True if element exists, False otherwise
        """
        try:
            self.driver.find_element(by, value)
            return True
        except NoSuchElementException:
            return False
    
    def element_is_enabled(self, by: By, value: str) -> bool:
        """
        Check if an element exists and is enabled
        
        Args:
            by: Selenium By locator type
            value: Locator value
            
        Returns:
            True if element exists and is enabled, False otherwise
        """
        try:
            element = self.driver.find_element(by, value)
            return element.is_enabled()
        except NoSuchElementException:
            return False
    
    def remove_element(self, by: By, value: str, description: str = None) -> bool:
        """
        Remove an element from the DOM using JavaScript
        
        Args:
            by: Selenium By locator type
            value: Locator value
            description: Description of the element
            
        Returns:
            True if element was removed, False if not found
        """
        try:
            element = self.driver.find_element(by, value)
            self.execute_script(
                "arguments[0].parentNode.removeChild(arguments[0]);",
                element,
                description=f"removing {description or value}"
            )
            logger.info(f"Removed element: {description or value}")
            return True
        except NoSuchElementException:
            logger.debug(f"Element not found for removal: {description or value}")
            return False
    
    def countdown(self, duration: int, message: str = "Waiting") -> None:
        """
        Display a countdown timer
        
        Args:
            duration: Duration in seconds
            message: Message to display during countdown
        """
        from colorama import Fore
        
        for i in range(duration, 0, -1):
            print(f"\r{Fore.CYAN}{message} for {i} seconds...", end="", flush=True)
            time.sleep(1)
        print()  # New line after countdown
