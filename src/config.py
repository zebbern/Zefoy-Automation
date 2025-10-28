"""
Configuration settings for Zefoy Automation Bot
Contains all URLs, XPaths, wait times, and service definitions
"""

# Application Settings
APP_NAME = "Zefoy Automation Bot"
VERSION = "2.0.0"

# URLs
ZEFOY_URL = "https://zefoy.com"
TEST_URL = "https://www.google.com"

# Browser Settings
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
LOG_LEVEL = 3  # Chrome log level (3 = WARNING)

# Use existing Chrome profile (helps bypass Cloudflare)
# Set to False to use a clean session (recommended if Chrome is open)
USE_EXISTING_PROFILE = False
CHROME_PROFILE_PATH = None  # Will auto-detect default profile

# Notification Settings
NOTIFICATION_PREFERENCE = 2  # 1: Allow, 2: Block

# Timeout Settings (in seconds)
DEFAULT_TIMEOUT = 10
PAGE_LOAD_TIMEOUT = 3
SEARCH_DELAY = 3

# Service Wait Times (min, max) in seconds
SERVICE_WAIT_TIMES = {
    "followers": (125, 135),
    "hearts": (125, 135),
    "comment_hearts": (70, 70),
    "views": (125, 135),
    "shares": (85, 100),
    "favorites": (125, 135),
}

# Service Configuration
# Format: "service_name": (button_xpath, div_index)
SERVICES = {
    "followers": (
        "/html/body/div[3]/div/div[2]/div/div/div[2]/div/button",
        4
    ),
    "hearts": (
        "/html/body/div[3]/div/div[2]/div/div/div[3]/div/button",
        5
    ),
    "comment_hearts": (
        "/html/body/div[3]/div/div[2]/div/div/div[4]/div/button",
        6
    ),
    "views": (
        "/html/body/div[3]/div/div[2]/div/div/div[6]/div/button",
        7
    ),
    "shares": (
        "/html/body/div[3]/div/div[2]/div/div/div[7]/div/button",
        8
    ),
    "favorites": (
        "/html/body/div[3]/div/div[2]/div/div/div[8]/div/button",
        9
    ),
}

# XPath Templates for Actions
# Use .format() to replace {div_index} with actual value
XPATH_TEMPLATES = {
    "url_input": "/html/body/div[{div_index}]/div/form/div/input",
    "search_button": "/html/body/div[{div_index}]/div/form/div/div/button",
    "send_button": "/html/body/div[{div_index}]/div/div/div[1]/div/form/button",
}

# CSS Selectors
CSS_SELECTORS = {
    "consent_popup": "body > div.fc-consent-root",
    "monetization_dialog": "body > div.fc-message-root > div.fc-monetization-dialog-container > div.fc-monetization-dialog.fc-dialog",
    "monetization_container": "body > div.fc-message-root > div.fc-monetization-dialog-container",
    "specific_icon": "#c2VuZC9mb2xsb3dlcnNfdGlrdG9r > div.row.text-light.d-flex.justify-content-center > div > form > button > i",
    "url_input_comment_hearts": "body > div.col-sm-5.col-xs-12.p-1.container.t-chearts-menu > div > form > div > input",
    "search_button_comment_hearts": 'form[action="c2VuZC9mb2xsb3dlcnNfdGlrdG9r"] button[type="submit"]',
    "w_button": ".wbutton",
    "close_buttons": "//button[text()='Close'] | //button[contains(@class, 'close')] | //button[contains(@aria-label, 'Close')]",
}

# Script Paths
SCRIPT_JS_PATH = "script.js"

# JavaScript Placeholders
JS_PLACEHOLDERS = {
    "username": '"@test"',
    "url": '"https://link.com"',
}

# Retry Settings
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

# Logging Settings
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = "zefoy_bot.log"
LOG_MAX_BYTES = 10 * 1024 * 1024  # 10 MB
LOG_BACKUP_COUNT = 5

# Color Codes (for console output)
class Colors:
    """ANSI color codes for console output"""
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
