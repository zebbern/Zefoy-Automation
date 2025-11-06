"""
WebDriver management for Zefoy Automation Bot
Handles Chrome WebDriver initialization and configuration
"""

from typing import Optional
import os
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import undetected_chromedriver as uc
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
        
        # Use a more realistic and current user agent
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')
        
        # Set logging level
        options.add_argument(f"--log-level={config.LOG_LEVEL}")
        
        # CRITICAL: Anti-detection flags (compatible format)
        options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-blink-features=AutomationControlled')
        
        # Enhanced anti-detection arguments
        options.add_argument('--disable-web-security')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--disable-features=VizDisplayCompositor')
        options.add_argument('--disable-backgrounding-occluded-windows')
        options.add_argument('--disable-renderer-backgrounding')
        options.add_argument('--disable-background-timer-throttling')
        options.add_argument('--disable-ipc-flooding-protection')
        options.add_argument('--password-store=basic')
        options.add_argument('--use-mock-keychain')
        options.add_argument('--disable-sync')
        options.add_argument('--metrics-recording-only')
        options.add_argument('--mute-audio')
        
        # Additional advanced stealth arguments
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-browser-side-navigation')
        options.add_argument('--disable-features=IsolateOrigins,site-per-process')
        options.add_argument('--disable-features=VizDisplayCompositor,VizHitTestSurfaceLayer')
        options.add_argument('--disable-component-extensions-with-background-pages')
        options.add_argument('--disable-default-apps')
        options.add_argument('--disable-background-networking')
        options.add_argument('--disable-background-mode')
        options.add_argument('--disable-client-side-phishing-detection')
        options.add_argument('--disable-component-update')
        options.add_argument('--disable-domain-reliability')
        options.add_argument('--disable-hang-monitor')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--disable-prompt-on-repost')
        options.add_argument('--disable-translate')
        options.add_argument('--no-first-run')
        options.add_argument('--no-default-browser-check')
        
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
        
        # Enhanced preferences for better stealth
        prefs = {
            "profile.default_content_setting_values.notifications": config.NOTIFICATION_PREFERENCE,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.default_content_settings.popups": 0,
            "directory_upgrade": True,
            "profile.default_content_setting_values.geolocation": 2,
            "profile.default_content_setting_values.media_stream": 2,
            "profile.managed_default_content_settings.images": 1,
            "profile.content_settings.exceptions.automatic_downloads.*.setting": 1,
            "profile.default_content_settings.multiple-automatic-downloads": 1,
            "intl.accept_languages": "en-US,en",
            "webkit.webprefs.fonts.standard.Zyyy": "Arial",
            "webkit.webprefs.fonts.fixed.Zyyy": "Consolas",
            "webkit.webprefs.fonts.serif.Zyyy": "Times New Roman",
            "webkit.webprefs.fonts.sansserif.Zyyy": "Arial"
        }
        options.add_experimental_option("prefs", prefs)
        
        logger.debug("Chrome options configured with enhanced anti-detection")
        return options
    
    def initialize_driver(self) -> WebDriver:
        """
        Initialize and test the Chrome WebDriver with anti-detection priority
        
        Returns:
            Configured WebDriver instance
            
        Raises:
            DriverInitializationError: If driver initialization fails
            NetworkError: If network connectivity test fails
        """
        logger.info("Initializing Chrome WebDriver...")
        
        try:
            # For undetected-chromedriver, use minimal options
            uc_options = uc.ChromeOptions()
            uc_options.add_argument('--start-maximized')
            uc_options.add_argument('--disable-blink-features=AutomationControlled')
            uc_options.add_argument('--no-sandbox')
            uc_options.add_argument('--disable-dev-shm-usage')
            
            # Try different methods to initialize ChromeDriver
            driver_initialized = False
            last_error = None
            
            # Method 1: Try undetected-chromedriver first (best for anti-detection)
            if not driver_initialized:
                try:
                    logger.info("Attempting undetected-chromedriver initialization...")
                    self.driver = uc.Chrome(
                        options=uc_options,
                        use_subprocess=True,
                        version_main=None,  # Auto-detect Chrome version
                        driver_executable_path=None,  # Auto-download if needed
                        browser_executable_path=None,  # Use default Chrome
                        user_data_dir=None,  # Will be set via options if configured
                        suppress_welcome=True,
                        no_sandbox=True,
                        headless=False,
                        keep_alive=True
                    )
                    driver_initialized = True
                    logger.info("Undetected ChromeDriver initialized successfully")
                except Exception as e:
                    logger.warning(f"Undetected ChromeDriver failed: {str(e)}")
                    last_error = e
            
            # Method 2: Try default Chrome as fallback
            if not driver_initialized:
                try:
                    logger.info("Attempting default Chrome initialization...")
                    options = self._configure_options()
                    self.driver = webdriver.Chrome(options=options)
                    driver_initialized = True
                    logger.info("Standard ChromeDriver initialized successfully")
                except Exception as e:
                    logger.warning(f"Default initialization failed: {str(e)}")
                    last_error = e
            
            # Method 3: Try with webdriver-manager as last resort
            if WEBDRIVER_MANAGER_AVAILABLE and not driver_initialized:
                try:
                    logger.info("Attempting ChromeDriver auto-download...")
                    options = self._configure_options()
                    service = Service(ChromeDriverManager().install())
                    self.driver = webdriver.Chrome(service=service, options=options)
                    driver_initialized = True
                    logger.info("ChromeDriver initialized via webdriver-manager")
                except Exception as e:
                    logger.warning(f"webdriver-manager failed: {str(e)}")
                    last_error = e
            
            if not driver_initialized:
                raise last_error or Exception("Failed to initialize ChromeDriver")
            
            logger.debug("WebDriver instance created")
            
            # Enable enhanced stealth scripts
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
        Removes all automation detection properties and mimics real browser behavior
        """
        try:
            # Enhanced comprehensive stealth script - applied to ALL new documents
            stealth_script = '''
                // IMMEDIATE: Remove webdriver property (most critical)
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                    configurable: true
                });
                
                // Remove automation indicators
                delete navigator.__proto__.webdriver;
                delete window.navigator.webdriver;
                delete window.webdriver;
                
                // CRITICAL: Override Object.getOwnPropertyDescriptor to hide webdriver
                const originalGetOwnPropertyDescriptor = Object.getOwnPropertyDescriptor;
                Object.getOwnPropertyDescriptor = function(obj, prop) {
                    if (prop === 'webdriver' && obj === navigator) {
                        return undefined;
                    }
                    return originalGetOwnPropertyDescriptor.apply(this, arguments);
                };
                
                // Mock plugins with realistic entries - only if not already defined
                if (!navigator.plugins || navigator.plugins.length === 0) {
                    Object.defineProperty(navigator, 'plugins', {
                        get: () => [
                            {name: 'Chrome PDF Plugin', filename: 'internal-pdf-viewer', description: 'Portable Document Format'},
                            {name: 'Chrome PDF Viewer', filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai', description: ''},
                            {name: 'Native Client', filename: 'internal-nacl-plugin', description: 'Native Client Executable'},
                            {name: 'Microsoft Edge PDF Plugin', filename: 'internal-pdf-viewer', description: 'Portable Document Format'},
                            {name: 'WebKit built-in PDF', filename: 'internal-pdf-viewer', description: 'Portable Document Format'}
                        ],
                        configurable: true
                    });
                }
                
                // Mock languages realistically
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en']
                });
                
                // Mock platform
                Object.defineProperty(navigator, 'platform', {
                    get: () => 'Win32'
                });
                
                // Add realistic chrome object - CRITICAL for detection bypass
                window.chrome = {
                    runtime: {
                        onConnect: null,
                        onMessage: null
                    },
                    loadTimes: function() {
                        return {
                            commitLoadTime: Date.now() / 1000 - Math.random() * 2,
                            connectionInfo: 'h2',
                            finishDocumentLoadTime: Date.now() / 1000 - Math.random(),
                            finishLoadTime: Date.now() / 1000 - Math.random(),
                            firstPaintAfterLoadTime: 0,
                            firstPaintTime: Date.now() / 1000 - Math.random() * 3,
                            navigationType: 'Other',
                            npnNegotiatedProtocol: 'h2',
                            requestTime: Date.now() / 1000 - Math.random() * 3,
                            startLoadTime: Date.now() / 1000 - Math.random() * 3,
                            wasAlternateProtocolAvailable: false,
                            wasFetchedViaSpdy: true,
                            wasNpnNegotiated: true
                        };
                    },
                    csi: function() {
                        return {
                            pageT: Date.now(),
                            startE: Date.now(),
                            tran: 15
                        };
                    },
                    app: {
                        isInstalled: false,
                        InstallState: {
                            DISABLED: 'disabled',
                            INSTALLED: 'installed',
                            NOT_INSTALLED: 'not_installed'
                        },
                        RunningState: {
                            CANNOT_RUN: 'cannot_run',
                            READY_TO_RUN: 'ready_to_run',
                            RUNNING: 'running'
                        }
                    }
                };
                
                // Mock permissions realistically
                if (navigator.permissions && navigator.permissions.query) {
                    const originalQuery = navigator.permissions.query;
                    navigator.permissions.query = (parameters) => (
                        parameters.name === 'notifications' ?
                            Promise.resolve({ state: Notification.permission }) :
                            originalQuery(parameters)
                    );
                }
                
                // Mock connection with realistic values
                Object.defineProperty(navigator, 'connection', {
                    get: () => ({
                        effectiveType: '4g',
                        rtt: Math.floor(Math.random() * 50) + 50,
                        downlink: Math.floor(Math.random() * 5) + 5,
                        saveData: false,
                        type: 'wifi'
                    })
                });
                
                // Mock hardware concurrency realistically
                Object.defineProperty(navigator, 'hardwareConcurrency', {
                    get: () => Math.max(2, Math.floor(Math.random() * 8) + 4)
                });
                
                // Mock device memory
                Object.defineProperty(navigator, 'deviceMemory', {
                    get: () => Math.pow(2, Math.floor(Math.random() * 3) + 2)
                });
                
                // Mock user agent data
                if (!navigator.userAgentData) {
                    Object.defineProperty(navigator, 'userAgentData', {
                        get: () => ({
                            brands: [
                                { brand: 'Not_A Brand', version: '8' },
                                { brand: 'Chromium', version: '131' },
                                { brand: 'Google Chrome', version: '131' }
                            ],
                            mobile: false,
                            platform: 'Windows'
                        })
                    });
                }
                
                // Mock screen properties with realistic values
                Object.defineProperty(screen, 'availWidth', {
                    get: () => 1920
                });
                Object.defineProperty(screen, 'availHeight', {
                    get: () => 1040
                });
                Object.defineProperty(screen, 'width', {
                    get: () => 1920
                });
                Object.defineProperty(screen, 'height', {
                    get: () => 1080
                });
                Object.defineProperty(screen, 'colorDepth', {
                    get: () => 24
                });
                Object.defineProperty(screen, 'pixelDepth', {
                    get: () => 24
                });
                
                // Override toString methods to hide automation
                const originalToString = Function.prototype.toString;
                Function.prototype.toString = function() {
                    if (this === navigator.webdriver) {
                        return 'function webdriver() { [native code] }';
                    }
                    return originalToString.apply(this, arguments);
                };
                
                // Mock window.outerWidth/Height
                Object.defineProperty(window, 'outerWidth', {
                    get: () => 1920
                });
                Object.defineProperty(window, 'outerHeight', {
                    get: () => 1080
                });
                
                // Hide selenium indicators
                ['selenium', 'webdriver', 'driver'].forEach(prop => {
                    if (window[prop]) delete window[prop];
                    if (document[prop]) delete document[prop];
                });
                
                // CRITICAL: Hide automation flags that detection scripts look for
                Object.defineProperty(window, 'callPhantom', { value: undefined });
                Object.defineProperty(window, '_phantom', { value: undefined });
                Object.defineProperty(window, 'phantom', { value: undefined });
                Object.defineProperty(window, '__nightmare', { value: undefined });
                Object.defineProperty(window, '_selenium', { value: undefined });
                Object.defineProperty(window, 'webdriver', { value: undefined });
                Object.defineProperty(window, 'domAutomation', { value: undefined });
                Object.defineProperty(window, 'domAutomationController', { value: undefined });
            '''
            
            # Apply to all new documents
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': stealth_script
            })
            
            # Also apply immediately to current document
            self.driver.execute_script(stealth_script)
            
            logger.debug("Enhanced stealth scripts applied successfully")
            
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
        Navigate to a URL with enhanced stealth protection
        
        Args:
            url: URL to navigate to
            
        Raises:
            DriverInitializationError: If driver is not initialized
        """
        if not self.driver:
            raise DriverInitializationError("Driver not initialized")
        
        logger.info(f"Navigating to {url}")
        
        # Apply stealth scripts BEFORE navigation to ensure they're active on page load
        self._apply_stealth_scripts()
        
        # Navigate to the URL
        self.driver.get(url)
        
        # Apply additional post-navigation stealth measures
        self._apply_post_navigation_stealth()
        
        logger.debug(f"Successfully navigated to {url} with stealth protection")

    def _apply_post_navigation_stealth(self) -> None:
        """
        Apply additional stealth measures after page navigation
        This ensures detection scripts are overridden even if they load after our initial scripts
        """
        try:
            # Dismiss any alerts or notifications first
            try:
                self.driver.execute_script("""
                    // Close any alert dialogs
                    if (window.alert) {
                        window.alert = function() { return true; };
                    }
                    if (window.confirm) {
                        window.confirm = function() { return true; };
                    }
                """)
                
                # Try to dismiss alert if present
                try:
                    alert = self.driver.switch_to.alert
                    alert.dismiss()
                    logger.info("Dismissed notification alert")
                except:
                    pass  # No alert present
                    
            except Exception as e:
                logger.debug(f"Alert handling: {e}")
            
            # Wait a moment for page to start loading
            import time
            time.sleep(0.5)
            
            # Apply immediate post-load stealth via execute_script (bypasses some detection)
            self.driver.execute_script("""
                // Remove webdriver traces that might reappear
                delete window.webdriver;
                delete window.navigator.webdriver;
                delete navigator.webdriver;
                delete navigator.__proto__.webdriver;
                
                // Override common bot detection methods
                if (window.navigator.permissions && window.navigator.permissions.query) {
                    const originalQuery = window.navigator.permissions.query;
                    window.navigator.permissions.query = function(parameters) {
                        return parameters.name === 'notifications' ? 
                            Promise.resolve({ state: 'default' }) : 
                            originalQuery(parameters);
                    };
                }
                
                // Ensure chrome object exists
                if (!window.chrome) {
                    window.chrome = {
                        runtime: {},
                        loadTimes: function() {
                            return {
                                commitLoadTime: Date.now() / 1000 - Math.random() * 2,
                                connectionInfo: 'h2',
                                finishDocumentLoadTime: Date.now() / 1000 - Math.random(),
                                finishLoadTime: Date.now() / 1000 - Math.random(),
                                navigationType: 'Other',
                                requestTime: Date.now() / 1000 - Math.random() * 3,
                                startLoadTime: Date.now() / 1000 - Math.random() * 3
                            };
                        },
                        csi: function() { return {}; },
                        app: {}
                    };
                }
                
                // Override toString for automation hiding
                const originalToString = Function.prototype.toString;
                Function.prototype.toString = function() {
                    if (this === navigator.webdriver) {
                        return 'function webdriver() { [native code] }';
                    }
                    return originalToString.apply(this, arguments);
                };
                
                // Remove automation indicators from window and document
                ['selenium', 'webdriver', 'driver'].forEach(prop => {
                    try {
                        if (window[prop]) delete window[prop];
                        if (document[prop]) delete document[prop];
                    } catch (e) {}
                });
                
                // Patch common detection vectors
                try {
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined,
                        configurable: true
                    });
                } catch (e) {
                    // Property already defined, try to delete it first
                    try {
                        delete navigator.webdriver;
                        Object.defineProperty(navigator, 'webdriver', {
                            get: () => undefined,
                            configurable: true
                        });
                    } catch (e2) {
                        // Unable to redefine, continue
                    }
                }
                
                // Mock realistic plugins if they were cleared
                if (!navigator.plugins || navigator.plugins.length === 0) {
                    try {
                        Object.defineProperty(navigator, 'plugins', {
                            get: () => [
                                {name: 'Chrome PDF Plugin', filename: 'internal-pdf-viewer'},
                                {name: 'Chrome PDF Viewer', filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai'},
                                {name: 'Native Client', filename: 'internal-nacl-plugin'}
                            ],
                            configurable: true
                        });
                    } catch (e) {
                        // Property already exists, skip
                    }
                }
            """)
            
            logger.debug("Post-navigation stealth measures applied")
            
        except Exception as e:
            logger.warning(f"Could not apply post-navigation stealth: {str(e)}")
    
    def refresh_stealth_protection(self) -> None:
        """
        Re-apply stealth protection - call this before critical actions that might trigger detection
        This is the equivalent of manually pasting stealth scripts in console
        """
        try:
            self.driver.execute_script("""
                console.log('=== REFRESHING STEALTH PROTECTION ===');
                
                // STEP 3: Remove all webdriver traces
                delete window.navigator.webdriver;
                delete navigator.webdriver;
                delete navigator.__proto__.webdriver;
                
                // Override webdriver property completely
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                    configurable: true,
                    enumerable: false
                });
                
                // STEP 4: Advanced stealth measures
                // Fix chrome runtime
                if (!window.chrome) {
                    window.chrome = {
                        runtime: {
                            onConnect: null,
                            onMessage: null
                        }
                    };
                }
                
                // Fix permissions API
                if (navigator.permissions && navigator.permissions.query) {
                    const originalQuery = navigator.permissions.query;
                    navigator.permissions.query = function(parameters) {
                        return parameters.name === 'notifications' ? 
                            Promise.resolve({ state: 'default' }) : 
                            originalQuery(parameters);
                    };
                }
                
                // Mock plugins if empty
                if (!navigator.plugins || navigator.plugins.length === 0) {
                    Object.defineProperty(navigator, 'plugins', {
                        get: () => [
                            {name: 'Chrome PDF Plugin', filename: 'internal-pdf-viewer'},
                            {name: 'Chrome PDF Viewer', filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai'},
                            {name: 'Native Client', filename: 'internal-nacl-plugin'}
                        ],
                        configurable: true
                    });
                }
                
                // Hide automation indicators
                ['selenium', 'webdriver', 'driver'].forEach(prop => {
                    if (window[prop]) delete window[prop];
                    if (document[prop]) delete document[prop];
                });
                
                // Override toString to hide automation
                const originalToString = Function.prototype.toString;
                Function.prototype.toString = function() {
                    if (this.name === 'webdriver') {
                        return 'function webdriver() { [native code] }';
                    }
                    return originalToString.apply(this, arguments);
                };
                
                console.log('=== STEALTH PROTECTION REFRESHED ===');
                return true;
            """)
            logger.info("Refreshed stealth protection before critical action")
        except Exception as e:
            logger.warning(f"Could not refresh stealth protection: {str(e)}")
    
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

