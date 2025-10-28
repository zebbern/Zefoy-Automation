"""
WebDriver management for Zefoy Automation Bot
Handles Chrome WebDriver initialization and configuration
"""

from typing import Optional
import os
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.remote.webdriver import WebDriver

from src import config
from src import logger
from src.exceptions import DriverInitializationError, NetworkError

# Try to import webdriver_manager, but make it optional
try:
    from webdriver_manager.chrome import ChromeDriverManager
    WEBDRIVER_MANAGER_AVAILABLE = True
except ImportError:
    WEBDRIVER_MANAGER_AVAILABLE = False


class DriverManager:
    """Manages Chrome WebDriver lifecycle and configuration"""
    
    def __init__(self):
        """Initialize the DriverManager"""
        self.driver: Optional[WebDriver] = None
    
    def _configure_options(self) -> Options:
        """
        Configure Chrome options for the WebDriver with aggressive anti-detection
        
        Returns:
            Configured Chrome Options object
        """
        options = Options()
        
        # Use a more realistic user agent (latest Chrome)
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')
        
        # Set logging level
        options.add_argument(f"--log-level={config.LOG_LEVEL}")
        
        # CRITICAL: Anti-detection flags
        options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-blink-features=AutomationControlled')
        
        # Additional stealth arguments
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-browser-side-navigation')
        options.add_argument('--disable-features=IsolateOrigins,site-per-process')
        
        # Make it look more like a real browser
        options.add_argument('--start-maximized')
        options.add_argument('--disable-extensions')
        
        # Use existing Chrome profile if configured (bypasses many protections)
        if config.USE_EXISTING_PROFILE:
            profile_path = self._get_chrome_profile_path()
            if profile_path:
                options.add_argument(f'--user-data-dir={profile_path}')
                options.add_argument('--profile-directory=Default')
                logger.info(f"Using existing Chrome profile: {profile_path}")
            else:
                logger.warning("Could not find Chrome profile, using clean session")
        
        # Block notification pop-ups and set other prefs
        prefs = {
            "profile.default_content_setting_values.notifications": config.NOTIFICATION_PREFERENCE,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.default_content_settings.popups": 0,
            "directory_upgrade": True
        }
        options.add_experimental_option("prefs", prefs)
        
        logger.debug("Chrome options configured with aggressive anti-detection")
        return options
    
    def initialize_driver(self) -> WebDriver:
        """
        Initialize and test the Chrome WebDriver
        
        Returns:
            Configured WebDriver instance
            
        Raises:
            DriverInitializationError: If driver initialization fails
            NetworkError: If network connectivity test fails
        """
        logger.info("Initializing Chrome WebDriver...")
        
        try:
            options = self._configure_options()
            
            # Try different methods to initialize ChromeDriver
            driver_initialized = False
            last_error = None
            
            # Method 1: Try default Chrome first (fastest and most reliable with Selenium 4+)
            if not driver_initialized:
                try:
                    logger.info("Attempting default Chrome initialization...")
                    self.driver = webdriver.Chrome(options=options)
                    driver_initialized = True
                    logger.info("ChromeDriver initialized successfully")
                except Exception as e:
                    logger.warning(f"Default initialization failed: {str(e)}")
                    last_error = e
            
            # Method 2: Only try webdriver-manager if default failed
            if WEBDRIVER_MANAGER_AVAILABLE and not driver_initialized:
                try:
                    logger.info("Attempting ChromeDriver auto-download...")
                    service = ChromeService(ChromeDriverManager().install())
                    self.driver = webdriver.Chrome(service=service, options=options)
                    driver_initialized = True
                    logger.info("ChromeDriver initialized via webdriver-manager")
                except Exception as e:
                    logger.warning(f"webdriver-manager failed: {str(e)}")
                    last_error = e
            
            if not driver_initialized:
                raise last_error or Exception("Failed to initialize ChromeDriver")
            
            logger.debug("WebDriver instance created")
            
            # Anti-detection: Remove webdriver property
            self._apply_stealth_scripts()
            
            # Test network connectivity
            self._test_connectivity()
            
            logger.info("WebDriver initialized successfully")
            return self.driver
            
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {str(e)}")
            error_msg = (
                f"WebDriver initialization failed.\n"
                f"Error: {str(e)}\n\n"
                f"Solutions:\n"
                f"1. Make sure Chrome browser is installed\n"
                f"2. Download ChromeDriver from: https://chromedriver.chromium.org/\n"
                f"3. Add ChromeDriver to your PATH\n"
                f"4. Or run: chromedriveinstall.bat (Windows)"
            )
            raise DriverInitializationError(error_msg)
    
    def _test_connectivity(self) -> None:
        """
        Test network connectivity by loading a known page
        
        Raises:
            NetworkError: If connectivity test fails
        """
        try:
            logger.debug(f"Testing connectivity to {config.TEST_URL}")
            self.driver.get(config.TEST_URL)
            logger.debug("Connectivity test successful")
        except Exception as e:
            logger.error(f"Network connectivity test failed: {str(e)}")
            raise NetworkError("No internet connection or WebDriver error")
    
    def _apply_stealth_scripts(self) -> None:
        """
        Apply aggressive JavaScript stealth to bypass Cloudflare and bot detection
        Removes all automation detection properties
        """
        try:
            # Comprehensive stealth script
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': '''
                    // Remove webdriver property (most important)
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                    
                    // Mock plugins
                    Object.defineProperty(navigator, 'plugins', {
                        get: () => [
                            {name: 'Chrome PDF Plugin', filename: 'internal-pdf-viewer', description: 'Portable Document Format'},
                            {name: 'Chrome PDF Viewer', filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai', description: ''},
                            {name: 'Native Client', filename: 'internal-nacl-plugin', description: ''}
                        ]
                    });
                    
                    // Mock languages
                    Object.defineProperty(navigator, 'languages', {
                        get: () => ['en-US', 'en']
                    });
                    
                    // Mock platform
                    Object.defineProperty(navigator, 'platform', {
                        get: () => 'Win32'
                    });
                    
                    // Add chrome object
                    window.chrome = {
                        runtime: {},
                        loadTimes: function() {},
                        csi: function() {},
                        app: {}
                    };
                    
                    // Mock permissions
                    const originalQuery = window.navigator.permissions.query;
                    window.navigator.permissions.query = (parameters) => (
                        parameters.name === 'notifications' ?
                            Promise.resolve({ state: Notification.permission }) :
                            originalQuery(parameters)
                    );
                    
                    // Hide automation-related properties
                    delete navigator.__proto__.webdriver;
                    
                    // Mock connection
                    Object.defineProperty(navigator, 'connection', {
                        get: () => ({
                            effectiveType: '4g',
                            rtt: 100,
                            downlink: 10,
                            saveData: false
                        })
                    });
                    
                    // Mock hardware concurrency
                    Object.defineProperty(navigator, 'hardwareConcurrency', {
                        get: () => 8
                    });
                    
                    // Mock device memory
                    Object.defineProperty(navigator, 'deviceMemory', {
                        get: () => 8
                    });
                '''
            })
            logger.debug("Aggressive stealth scripts applied successfully")
        except Exception as e:
            logger.warning(f"Could not apply stealth scripts: {str(e)}")
            # Don't fail if stealth scripts don't work
    
    def _get_chrome_profile_path(self) -> Optional[str]:
        """
        Get the default Chrome user data directory path
        
        Returns:
            Path to Chrome profile or None if not found
        """
        if config.CHROME_PROFILE_PATH:
            return config.CHROME_PROFILE_PATH
        
        # Try to find Chrome profile automatically
        if os.name == 'nt':  # Windows
            profile_path = Path(os.environ['LOCALAPPDATA']) / 'Google' / 'Chrome' / 'User Data'
        elif os.name == 'posix':
            if 'darwin' in os.sys.platform:  # macOS
                profile_path = Path.home() / 'Library' / 'Application Support' / 'Google' / 'Chrome'
            else:  # Linux
                profile_path = Path.home() / '.config' / 'google-chrome'
        else:
            return None
        
        if profile_path.exists():
            return str(profile_path)
        
        return None
    
    def navigate_to(self, url: str) -> None:
        """
        Navigate to a URL
        
        Args:
            url: URL to navigate to
            
        Raises:
            DriverInitializationError: If driver is not initialized
        """
        if not self.driver:
            raise DriverInitializationError("Driver not initialized")
        
        logger.info(f"Navigating to {url}")
        self.driver.get(url)
    
    def quit(self) -> None:
        """
        Quit the WebDriver and clean up resources
        """
        if self.driver:
            logger.info("Closing WebDriver")
            try:
                self.driver.quit()
                logger.debug("WebDriver closed successfully")
            except Exception as e:
                logger.warning(f"Error while closing WebDriver: {str(e)}")
            finally:
                self.driver = None
    
    def get_driver(self) -> WebDriver:
        """
        Get the WebDriver instance
        
        Returns:
            WebDriver instance
            
        Raises:
            DriverInitializationError: If driver is not initialized
        """
        if not self.driver:
            raise DriverInitializationError("Driver not initialized. Call initialize_driver() first.")
        return self.driver
    
    def refresh_page(self) -> None:
        """
        Refresh the current page
        
        Raises:
            DriverInitializationError: If driver is not initialized
        """
        if not self.driver:
            raise DriverInitializationError("Driver not initialized")
        
        logger.debug("Refreshing page")
        self.driver.refresh()
    
    def __enter__(self):
        """Context manager entry"""
        self.initialize_driver()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.quit()
