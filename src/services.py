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
    
    def __init__(self, driver: WebDriver):
        """
        Initialize the ServiceManager
        
        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver
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
            ServiceUnavailableError: If service is not available
        """
        service = self.get_service(service_name)
        
        if service.status != ServiceStatus.WORKING:
            raise ServiceUnavailableError(
                f"Service '{service_name}' is not available (status: {service.status})"
            )
        
        try:
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
        
        Args:
            service: Service object
            video_url: TikTok video URL
            
        Raises:
            ServiceActionError: If action fails
        """
        logger.info(f"Performing '{service.name}' action for URL: {video_url}")
        
        # Validate URL
        validate_url(video_url)
        
        # Define action steps
        steps = [
            {
                "description": "clear URL input",
                "xpath": config.XPATH_TEMPLATES["url_input"].format(div_index=service.div_index),
                "action": "clear"
            },
            {
                "description": "enter video URL",
                "xpath": config.XPATH_TEMPLATES["url_input"].format(div_index=service.div_index),
                "action": "input",
                "text": video_url
            },
            {
                "description": "click search button",
                "xpath": config.XPATH_TEMPLATES["search_button"].format(div_index=service.div_index),
                "action": "click",
                "delay": config.SEARCH_DELAY
            },
            {
                "description": "click send button",
                "xpath": config.XPATH_TEMPLATES["send_button"].format(div_index=service.div_index),
                "action": "click"
            }
        ]
        
        # Execute steps
        for step in steps:
            try:
                if step["action"] == "clear":
                    element = self.actions.find_element(
                        By.XPATH,
                        step["xpath"],
                        description=step["description"]
                    )
                    element.clear()
                    logger.debug(f"Successfully {step['description']}")
                    
                elif step["action"] == "input":
                    self.actions.input_text(
                        By.XPATH,
                        step["xpath"],
                        step["text"],
                        clear_first=False,
                        description=step["description"]
                    )
                    
                elif step["action"] == "click":
                    self.actions.click_element(
                        By.XPATH,
                        step["xpath"],
                        description=step["description"]
                    )
                    
                    # Apply delay if specified
                    if "delay" in step:
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
