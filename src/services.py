"""
Service management for Zefoy Automation Bot
Handles service availability checking and service-specific operations
"""

import os
import random
import time
from typing import Dict, List, Tuple, Optional

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from src import config
from src import logger
from src.actions import SeleniumActions
from src.exceptions import ServiceUnavailableError, ServiceActionError, ScriptExecutionError
from src.validators import validate_username, validate_url


class ServiceStatus:
    """Service status constants"""
    WORKING = "WORKING"
    OFFLINE = "OFFLINE"
    UNKNOWN = "UNKNOWN"


class Service:
    """Represents a Zefoy service with its configuration and status"""
    
    def __init__(self, name: str, button_xpath: str, div_index: int):
        """
        Initialize a service
        
        Args:
            name: Service name
            button_xpath: XPath to service button
            div_index: Service div index for actions
        """
        self.name = name
        self.button_xpath = button_xpath
        self.div_index = div_index
        self.status = ServiceStatus.UNKNOWN
    
    def __repr__(self):
        return f"Service(name={self.name}, status={self.status})"


class ServiceManager:
    """Manages Zefoy services and their operations"""
    
    def __init__(self, driver: WebDriver, driver_manager=None):
        """
        Initialize the ServiceManager
        
        Args:
            driver: Selenium WebDriver instance
            driver_manager: DriverManager instance for stealth refresh
        """
        self.driver = driver
        self.driver_manager = driver_manager
        self.actions = SeleniumActions(driver)
        self.services: Dict[str, Service] = self._initialize_services()
    
    def _initialize_services(self) -> Dict[str, Service]:
        """
        Initialize services from configuration
        
        Returns:
            Dictionary of service name to Service object
        """
        services = {}
        for name, (xpath, div_index) in config.SERVICES.items():
            services[name] = Service(name, xpath, div_index)
        
        logger.debug(f"Initialized {len(services)} services")
        return services
    
    def check_services_availability(self) -> Dict[str, str]:
        """
        Check availability of all services using XPath
        
        Returns:
            Dictionary mapping service name to status
        """
        logger.info("Checking service availability...")
        
        for service in self.services.values():
            try:
                element = self.driver.find_element(By.XPATH, service.button_xpath)
                if element.is_displayed() and element.is_enabled():
                    service.status = ServiceStatus.WORKING
                    logger.debug(f"Service '{service.name}': {ServiceStatus.WORKING}")
                else:
                    service.status = ServiceStatus.OFFLINE
                    logger.debug(f"Service '{service.name}': {ServiceStatus.OFFLINE} (not enabled or visible)")
            except Exception as e:
                service.status = ServiceStatus.OFFLINE
                logger.debug(f"Service '{service.name}': {ServiceStatus.OFFLINE} ({str(e)})")
        
        # Create status summary
        status_dict = {name: svc.status for name, svc in self.services.items()}
        
        working_count = sum(1 for s in status_dict.values() if s == ServiceStatus.WORKING)
        logger.info(f"Service check complete: {working_count}/{len(self.services)} services available")
        
        return status_dict
    
    def get_service(self, service_name: str) -> Service:
        """
        Get a service by name
        
        Args:
            service_name: Name of the service
            
        Returns:
            Service object
            
        Raises:
            ServiceUnavailableError: If service doesn't exist
        """
        if service_name not in self.services:
            raise ServiceUnavailableError(f"Service '{service_name}' does not exist")
        
        return self.services[service_name]
    
    def select_service(self, service_name: str) -> Service:
        """
        Select and activate a service
        
        Args:
            service_name: Name of the service to select
            
        Returns:
            Selected Service object
            
        Raises:
            ServiceUnavailableError: If service selection fails
        """
        service = self.get_service(service_name)
        
        # BYPASS: Allow service to run regardless of detected status
        # Original check removed: if service.status != ServiceStatus.WORKING
        if service.status != ServiceStatus.WORKING:
            logger.warning(f"Service '{service_name}' appears to be {service.status}, but attempting to use it anyway...")
        
        try:
            # Use jQuery trigger click (proven working method from console testing)
            # Get CSS class from the button XPath
            css_class_map = {
                'followers': '.t-followers-button',
                'hearts': '.t-hearts-button',
                'comment_hearts': '.t-chearts-button',
                'views': '.t-views-button',
                'shares': '.t-shares-button',
                'favorites': '.t-favorites-button'
            }
            
            css_selector = css_class_map.get(service_name)
            if css_selector:
                script = f"""
                    var result = $('{css_selector}').first().trigger('click');
                    return result.length > 0;
                """
                success = self.driver.execute_script(script)
                if not success:
                    raise ServiceUnavailableError(f"Could not click service button via jQuery for '{service_name}'")
                logger.info(f"Selected service via jQuery: {service_name}")
            else:
                # Fallback to old XPath method
                self.actions.click_element(
                    By.XPATH,
                    service.button_xpath,
                    description=f"service button for '{service_name}'"
                )
            logger.info(f"Selected service: {service_name}")
            return service
        except Exception as e:
            logger.error(f"Failed to select service '{service_name}': {str(e)}")
            raise ServiceUnavailableError(f"Could not select service '{service_name}': {str(e)}")
    
    def perform_generic_service_action(self, service: Service, video_url: str) -> None:
        """
        Perform a generic service action (for views, likes, shares, etc.)
        Uses proven JavaScript methods from browser console testing
        
        Args:
            service: Service object
            video_url: TikTok video URL
            
        Raises:
            ServiceActionError: If action fails
        """
        logger.info(f"Performing '{service.name}' action for URL: {video_url}")
        
        # Validate URL
        validate_url(video_url)
        
        # Define action steps using working JavaScript methods
        steps = [
            {
                "description": "enter video URL",
                "action": "input_jquery",
                "text": video_url,
                "delay": 0.5
            },
            {
                "description": "click search button",
                "action": "click_search",
                "delay": config.SEARCH_DELAY * 2  # Double wait for search results
            },
            {
                "description": "click send button",
                "action": "click_send"
            }
        ]
        
        # Execute steps
        for step in steps:
            try:
                if step["action"] == "input_jquery":
                    # CRITICAL: Refresh stealth protection before any interaction
                    self._refresh_stealth_protection(delay=0.3)
                    
                    # Use jQuery to set input value (proven working method)
                    script = f"""
                        var input = $('input[placeholder="Enter Video URL"]').filter(':visible').first();
                        if (input.length === 0) return false;
                        input.val(arguments[0]);
                        return true;
                    """
                    success = self.driver.execute_script(script, step["text"])
                    if not success:
                        raise ServiceActionError(service.name, "input", "URL input field not found")
                    logger.info(f"Entered text via jQuery: {step['description']}")
                    
                elif step["action"] == "click_search":
                    # CRITICAL: Refresh stealth protection before search button click
                    self._refresh_stealth_protection(delay=0.5)
                    
                    # Use forced JS click for search button (proven working method)
                    script = """
                        const btn = Array.from(document.querySelectorAll('button[type="submit"], button'))
                            .find(b => /\\bSearch\\b/.test(b.textContent) && (b.offsetParent !== null || b.getBoundingClientRect().width > 0));
                        if (!btn) return false;
                        if (btn.disabled) { btn.disabled = false; btn.removeAttribute('disabled'); }
                        btn.click();
                        btn.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, view: window }));
                        btn.closest('form')?.requestSubmit?.();
                        return true;
                    """
                    success = self.driver.execute_script(script)
                    if not success:
                        raise ServiceActionError(service.name, "search", "Search button not found")
                    logger.info(f"Clicked via forced JS: {step['description']}")
                
                elif step["action"] == "click_send":
                    # Use forced JS click for send button with retry logic for cooldown timer
                    # The send button may not appear immediately due to Zefoy's cooldown/spam protection
                    # When on cooldown, we need to re-search (step 3) and then try send again (step 4)
                    
                    search_script = """
                        const btn = Array.from(document.querySelectorAll('button[type="submit"], button'))
                            .find(b => /\\bSearch\\b/.test(b.textContent) && (b.offsetParent !== null || b.getBoundingClientRect().width > 0));
                        if (!btn) return false;
                        if (btn.disabled) { btn.disabled = false; btn.removeAttribute('disabled'); }
                        btn.click();
                        btn.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, view: window }));
                        btn.closest('form')?.requestSubmit?.();
                        return true;
                    """
                    
                    send_script = """
                        const btn = Array.from(document.querySelectorAll('button[type="submit"], button.wbutton, button'))
                            .find(b => (b.classList.contains('wbutton') || /\\bSend\\b/i.test(b.textContent)) && (b.offsetParent !== null || b.getBoundingClientRect().width > 0));
                        if (!btn) return false;
                        if (btn.disabled) { btn.disabled = false; btn.removeAttribute('disabled'); }
                        btn.click();
                        btn.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, view: window }));
                        btn.closest('form')?.requestSubmit?.();
                        return true;
                    """
                    
                    # Retry loop with 40-second delays
                    max_attempts = 999  # Effectively unlimited retries
                    attempt = 0
                    success = False
                    
                    while not success and attempt < max_attempts:
                        attempt += 1
                        logger.info(f"Attempting to click send button (attempt {attempt})...")
                        
                        # CRITICAL: Refresh stealth protection BEFORE send button click
                        # This fixes the "Browser not supported" error that appears after clicking
                        self._refresh_stealth_protection(delay=0.5)
                        
                        # Try to click send button
                        success = self.driver.execute_script(send_script)
                        
                        if success:
                            logger.info(f"✓ Successfully clicked send button on attempt {attempt}")
                            break
                        else:
                            # Check if there's a cooldown timer on the page and extract wait time
                            timer_script = """
                                // Look for timer text like "Please wait 0 minute(s) 07 second(s)"
                                const bodyText = document.body.innerText;
                                const timerMatch = bodyText.match(/Please wait[\\s\\S]*?(\\d+)\\s*minute.*?(\\d+)\\s*second/i);
                                if (timerMatch) {
                                    const minutes = parseInt(timerMatch[1]);
                                    const seconds = parseInt(timerMatch[2]);
                                    return {
                                        text: timerMatch[0],
                                        totalSeconds: (minutes * 60) + seconds
                                    };
                                }
                                
                                // Try to find any timer pattern
                                const timerPattern = /\\d+:\\d+|\\d+\\s*(second|minute|hour)/i;
                                const allElements = Array.from(document.querySelectorAll('*'));
                                for (const el of allElements) {
                                    if (timerPattern.test(el.textContent) && el.textContent.length < 100) {
                                        return {
                                            text: el.textContent.trim(),
                                            totalSeconds: null
                                        };
                                    }
                                }
                                return null;
                            """
                            timer_info = self.driver.execute_script(timer_script)
                            
                            if timer_info:
                                logger.warning(f"⏳ Cooldown detected: {timer_info['text']}")
                                
                                # Calculate wait time based on detected timer
                                if timer_info['totalSeconds']:
                                    wait_time = timer_info['totalSeconds'] + 5  # Add 5 second buffer
                                    logger.info(f"Waiting {wait_time} seconds (detected cooldown + buffer)...")
                                else:
                                    wait_time = 40  # Default fallback
                                    logger.info(f"Waiting {wait_time} seconds (default)...")
                            else:
                                logger.warning(f"Send button not found (attempt {attempt}). May be on cooldown.")
                                wait_time = 40  # Default fallback
                                logger.info(f"Waiting {wait_time} seconds before retrying...")
                            
                            time.sleep(wait_time)
                            
                            # After cooldown, refresh stealth protection again and re-click search button (step 3)
                            self._refresh_stealth_protection(delay=0.5)
                            
                            logger.info("Re-clicking search button after cooldown...")
                            search_success = self.driver.execute_script(search_script)
                            if search_success:
                                logger.info("✓ Re-clicked search button")
                                time.sleep(5)  # Wait a bit for results
                            else:
                                logger.warning("⚠ Could not re-click search button, will retry send anyway")
                    
                    if not success:
                        raise ServiceActionError(service.name, "send", f"Send button not found after {attempt} attempts")
                    
                elif step["action"] == "input":
                    self.actions.input_text(
                        By.XPATH,
                        step["xpath"],
                        step["text"],
                        clear_first=False,
                        timeout=step.get("timeout"),
                        description=step["description"]
                    )
                    
                elif step["action"] == "click":
                    # Try CSS selector first if available, otherwise use XPath
                    if "css" in step:
                        self.actions.click_element(
                            By.CSS_SELECTOR,
                            step["css"],
                            timeout=step.get("timeout"),
                            description=step["description"]
                        )
                    else:
                        self.actions.click_element(
                            By.XPATH,
                            step["xpath"],
                            timeout=step.get("timeout"),
                            description=step["description"]
                        )

                elif step["action"] == "click_send_button":
                    # CRITICAL: Refresh stealth protection before send button click
                    # This fixes the "Browser not supported" error that appears after clicking
                    if self.driver_manager and hasattr(self.driver_manager, 'refresh_stealth_protection'):
                        self.driver_manager.refresh_stealth_protection()
                    
                    # Try multiple strategies to find the send button (ordered by priority)
                    logger.info("Attempting to find send button with multiple strategies...")
                    
                    strategies = [
                        ("CSS .wbutton", By.CSS_SELECTOR, ".wbutton"),
                        ("XPath div[10] wbutton", By.XPATH, "/html/body/div[10]/div/div/div[1]/div/form/button"),
                        ("XPath send button template", By.XPATH, config.XPATH_TEMPLATES["send_button"].format(div_index=10)),
                        ("CSS button.wbutton", By.CSS_SELECTOR, "button.wbutton"),
                        ("XPath wbutton class", By.XPATH, "//button[contains(@class, 'wbutton')]"),
                        ("XPath DIV10 wbutton", By.XPATH, "/html/body/div[10]//button[contains(@class, 'wbutton')]"),
                    ]
                    
                    button_found = False
                    for strategy_name, by_type, selector in strategies:
                        try:
                            logger.info(f"Trying strategy: {strategy_name}")
                            self.actions.click_element(
                                by_type,
                                selector,
                                timeout=5,  # Short timeout for each strategy
                                description=f"send button ({strategy_name})"
                            )
                            button_found = True
                            logger.info(f"✓ Successfully clicked send button using: {strategy_name}")
                            break
                        except Exception as e:
                            logger.debug(f"✗ Strategy '{strategy_name}' failed: {str(e)}")
                            continue
                    
                    if not button_found:
                        error_msg = f"Failed to find send button after trying {len(strategies)} strategies"
                        logger.error(error_msg)
                        raise ServiceActionError(
                            service_name=service.name,
                            action="click send button",
                            reason=error_msg
                        )

                elif step["action"] == "wait":
                    if "delay" in step:
                        logger.info(f"Waiting {step['delay']} seconds: {step['description']}")
                        time.sleep(step["delay"])

                elif step["action"] == "debug":
                    # Debug: Check div[10] content and look for send button or errors
                    logger.info("=== DEBUG: Checking div[10] after search ===")
                    try:
                        # Get full content of div[10]
                        div10_content = self.actions.driver.execute_script("""
                            var div10 = document.evaluate('/html/body/div[10]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                            return div10 ? div10.innerHTML : 'DIV[10] NOT FOUND';
                        """)
                        logger.info(f"DIV[10] CONTENT: {div10_content[:1000]}...")  # First 1000 chars
                        
                        # Check for error messages
                        error_msgs = self.actions.driver.execute_script("""
                            var errors = document.querySelectorAll('.text-danger, .error, .alert, span[class*="danger"]');
                            var result = [];
                            for (var i = 0; i < errors.length; i++) {
                                if (errors[i].textContent.trim()) {
                                    result.push('ERROR: ' + errors[i].textContent.trim());
                                }
                            }
                            return result.join(' | ');
                        """)
                        logger.info(f"ERROR MESSAGES ON PAGE: {error_msgs if error_msgs else 'None'}")
                        
                        # Look for ALL buttons on the page
                        all_buttons = self.actions.driver.execute_script("""
                            var buttons = document.querySelectorAll('button');
                            var result = [];
                            for (var i = 0; i < buttons.length; i++) {
                                var btn = buttons[i];
                                var info = 'BTN' + i + ': class="' + btn.className + '" text="' + btn.textContent.trim().substring(0, 50) + '"';
                                result.push(info);
                            }
                            return result.join(' | ');
                        """)
                        logger.info(f"ALL BUTTONS ON PAGE: {all_buttons}")
                        
                    except Exception as e:
                        logger.info(f"DEBUG ERROR: {str(e)}")
                    logger.info("=== END DEBUG ===")

                # Apply delay if specified
                if "delay" in step and step["action"] != "wait" and step["action"] != "debug" and step["action"] != "click_send_button":
                    time.sleep(step["delay"])
                    
            except Exception as e:
                logger.error(f"Failed to {step['description']}: {str(e)}")
                raise ServiceActionError(
                    service.name,
                    step["description"],
                    str(e)
                )
        
        # Wait for service cooldown
        self._wait_for_service_cooldown(service.name)
    
    def _refresh_stealth_protection(self, delay: float = 0.5) -> None:
        """
        Refresh stealth protection to prevent bot detection
        
        Args:
            delay: Seconds to wait after refresh for page to settle (default: 0.5)
        """
        logger.info("Refreshing stealth protection...")
        if hasattr(self.driver_manager, 'refresh_stealth_protection'):
            self.driver_manager.refresh_stealth_protection()
        elif hasattr(self.driver, 'refresh_stealth_protection'):
            self.driver.refresh_stealth_protection()
        
        if delay > 0:
            time.sleep(delay)
    
    def _wait_for_service_cooldown(self, service_name: str) -> None:
        """
        Wait for service cooldown period
        
        Args:
            service_name: Name of the service
        """
        if service_name not in config.SERVICE_WAIT_TIMES:
            logger.warning(f"No wait time configured for '{service_name}', using default")
            wait_time = 60
        else:
            min_wait, max_wait = config.SERVICE_WAIT_TIMES[service_name]
            wait_time = random.randint(min_wait, max_wait)
        
        logger.info(f"Service cooldown: waiting {wait_time} seconds")
        self.actions.countdown(wait_time, f"Cooldown for {service_name}")
    
    def handle_comment_hearts(self, target_username: str, target_url: str) -> None:
        """
        Handle the comment hearts service with JavaScript automation
        
        Args:
            target_username: TikTok username (e.g., @test)
            target_url: Target URL
            
        Raises:
            ServiceActionError: If operation fails
            ScriptExecutionError: If script execution fails
        """
        logger.info(f"Handling comment hearts for {target_username}")
        
        # Validate inputs
        target_username = validate_username(target_username)
        validate_url(target_url)
        
        # Load and modify JavaScript
        script_code = self._load_and_modify_script(target_username, target_url)
        
        try:
            while True:
                # Execute input URL JavaScript
                self._execute_input_url_js(target_url)
                self.actions.countdown(1, "Processing")
                
                # Execute click search button JavaScript
                self._execute_click_search_js()
                self.actions.countdown(2, "Waiting for page")
                
                # Check for specific icon
                if self._check_specific_icon():
                    logger.info("Specific icon detected, executing main script")
                    self.actions.execute_script(script_code, description="comment hearts automation")
                    logger.info("Comment hearts script running, keeping session alive...")
                    self._keep_alive()
                else:
                    logger.warning("Specific icon not found, retrying in 60 seconds")
                
                self.actions.countdown(60, "Retry cooldown")
                
        except KeyboardInterrupt:
            logger.info("Comment hearts operation interrupted by user")
        except Exception as e:
            logger.exception(f"Comment hearts operation failed: {str(e)}")
            raise ServiceActionError("comment_hearts", "automation", str(e))
    
    def _load_and_modify_script(self, username: str, url: str) -> str:
        """Load script.js and replace placeholders"""
        script_path = os.path.join(os.getcwd(), config.SCRIPT_JS_PATH)
        
        if not os.path.isfile(script_path):
            raise ScriptExecutionError("script.js", f"File not found at {script_path}")
        
        try:
            with open(script_path, "r", encoding="utf-8") as file:
                script = file.read()
            
            # Replace placeholders
            script = script.replace(config.JS_PLACEHOLDERS["username"], f'"{username}"')
            script = script.replace(config.JS_PLACEHOLDERS["url"], f'"{url}"')
            
            logger.debug("Loaded and modified script.js")
            return script
            
        except Exception as e:
            raise ScriptExecutionError("script.js", f"Failed to read file: {str(e)}")
    
    def _execute_input_url_js(self, url: str) -> None:
        """Execute JavaScript to input URL"""
        js_code = f"""
        const targetURL = "{url}";
        function inputURL(callback) {{
            const urlInput = document.querySelector("body > div.col-sm-5.col-xs-12.p-1.container.t-chearts-menu > div > form > div > input");
            if (urlInput) {{
                urlInput.value = targetURL;
                const event = new Event("input");
                urlInput.dispatchEvent(event);
                console.log('URL inputted successfully!');
                setTimeout(callback, 1000);
            }}
        }}
        inputURL(function() {{}});
        """
        self.actions.execute_script(js_code, description="input URL")
        logger.debug("Executed input URL JavaScript")
    
    def _execute_click_search_js(self) -> None:
        """Execute JavaScript to click search button"""
        js_code = """
        function clickSearchButton(callback) { 
            const searchButton = document.querySelector('form[action="c2VuZC9mb2xsb3dlcnNfdGlrdG9r"] button[type="submit"]'); 
            if (searchButton) { 
                searchButton.click(); 
                setTimeout(callback, 2000); 
            } 
        }
        clickSearchButton(function() {});
        """
        self.actions.execute_script(js_code, description="click search button")
        logger.debug("Executed click search JavaScript")
    
    def _check_specific_icon(self) -> bool:
        """Check if specific icon is present"""
        return self.actions.element_exists(By.CSS_SELECTOR, config.CSS_SELECTORS["specific_icon"])
    
    def _keep_alive(self) -> None:
        """Keep script running indefinitely"""
        logger.info("Keeping script alive. Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(60)
        except KeyboardInterrupt:
            logger.info("Keep-alive interrupted")
