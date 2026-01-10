"""Console colors and formatting utilities."""
import sys


class Colors:
    """ANSI color codes for console output."""
    
    # Reset
    RESET = "\033[0m"
    
    # Regular colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Bright colors
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"
    
    # Styles
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"
    
    @classmethod
    def supports_color(cls) -> bool:
        """Check if terminal supports colors."""
        # Windows terminal now supports colors in most cases
        if sys.platform == "win32":
            return True
        # Unix terminals usually support colors
        return hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()


# Shorthand functions for common colors
def success(text: str) -> str:
    """Green text for success messages."""
    return f"{Colors.BRIGHT_GREEN}{text}{Colors.RESET}"


def error(text: str) -> str:
    """Red text for error messages."""
    return f"{Colors.BRIGHT_RED}{text}{Colors.RESET}"


def warning(text: str) -> str:
    """Yellow text for warnings."""
    return f"{Colors.BRIGHT_YELLOW}{text}{Colors.RESET}"


def info(text: str) -> str:
    """Cyan text for info."""
    return f"{Colors.BRIGHT_CYAN}{text}{Colors.RESET}"


def dim(text: str) -> str:
    """Dim text for less important info."""
    return f"{Colors.DIM}{text}{Colors.RESET}"


def bold(text: str) -> str:
    """Bold text for emphasis."""
    return f"{Colors.BOLD}{text}{Colors.RESET}"


def header(text: str) -> str:
    """Magenta text for headers."""
    return f"{Colors.BRIGHT_MAGENTA}{Colors.BOLD}{text}{Colors.RESET}"
