"""
Custom exceptions for Zefoy Automation Bot
Provides specific exception types for better error handling
"""


class BotException(Exception):
    """Base exception for all bot-related errors"""
    pass


class DriverInitializationError(BotException):
    """Raised when WebDriver fails to initialize"""
    pass


class NetworkError(BotException):
    """Raised when network connection fails"""
    pass


class ServiceUnavailableError(BotException):
    """Raised when a selected service is not available"""
    pass


class ElementNotFoundError(BotException):
    """Raised when a required element cannot be found on the page"""
    def __init__(self, element_description: str, xpath: str = None):
        self.element_description = element_description
        self.xpath = xpath
        message = f"Element not found: {element_description}"
        if xpath:
            message += f" (XPath: {xpath})"
        super().__init__(message)


class TimeoutError(BotException):
    """Raised when an operation times out"""
    def __init__(self, operation: str, timeout: int):
        self.operation = operation
        self.timeout = timeout
        super().__init__(f"Operation '{operation}' timed out after {timeout} seconds")


class InvalidInputError(BotException):
    """Raised when user input is invalid"""
    pass


class ScriptExecutionError(BotException):
    """Raised when JavaScript execution fails"""
    def __init__(self, script_name: str, error: str):
        self.script_name = script_name
        self.error = error
        super().__init__(f"Failed to execute {script_name}: {error}")


class CaptchaError(BotException):
    """Raised when CAPTCHA handling fails"""
    pass


class ServiceActionError(BotException):
    """Raised when a service action fails"""
    def __init__(self, service_name: str, action: str, reason: str):
        self.service_name = service_name
        self.action = action
        self.reason = reason
        super().__init__(f"Failed to {action} for service '{service_name}': {reason}")
