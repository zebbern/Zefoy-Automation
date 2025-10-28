"""
Zefoy Automation Bot - Main orchestration
Refactored version with clean architecture and separation of concerns

Author: github.com/zebbern
Version: 2.0.0
"""

import os
import sys
import time
from typing import List, Optional
from colorama import Fore

from src import config
from src import logger
from src.driver_manager import DriverManager
from src.services import ServiceManager
from src.actions import SeleniumActions
from src.validators import parse_url_list, validate_service_choice, sanitize_input
from src.exceptions import (
    BotException,
    DriverInitializationError,
    NetworkError,
    ServiceUnavailableError,
    InvalidInputError
)


class ZefoyBot:
    """
    Main bot class that orchestrates all operations
    Manages workflow from initialization to service execution
    """
    
    def __init__(self):
        """Initialize the bot with all required components"""
        self._clear_screen()
        logger.info(f"Starting {config.APP_NAME} v{config.VERSION}")
        
        # Initialize managers
        self.driver_manager: Optional[DriverManager] = None
        self.service_manager: Optional[ServiceManager] = None
        self.actions: Optional[SeleniumActions] = None
        
        # Bot state
        self.selected_service: Optional[str] = None
        self.video_urls: List[str] = []
    
    def _clear_screen(self) -> None:
        """Clear the console screen"""
        print("\033c", end="")
    
    def initialize(self) -> None:
        """
        Initialize all bot components
        
        Raises:
            DriverInitializationError: If WebDriver fails to initialize
            NetworkError: If network connection fails
        """
        try:
            # Initialize driver
            self.driver_manager = DriverManager()
            driver = self.driver_manager.initialize_driver()
            
            # Initialize action handler
            self.actions = SeleniumActions(driver)
            
            # Initialize service manager
            self.service_manager = ServiceManager(driver)
            
            logger.info("Bot initialization complete")
            
        except (DriverInitializationError, NetworkError) as e:
            logger.critical(f"Initialization failed: {str(e)}")
            raise
    
    def start(self) -> None:
        """
        Main entry point for the bot
        Handles the complete workflow from start to finish
        """
        try:
            # Initialize bot components
            self.initialize()
            
            # Navigate to Zefoy
            self.driver_manager.navigate_to(config.ZEFOY_URL)
            
            # Remove consent popup
            self._remove_consent_popup()
            
            # Wait for user to solve CAPTCHA (includes popup removal afterwards)
            self._wait_for_captcha()
            
            # Check service availability
            service_status = self.service_manager.check_services_availability()
            
            # Display services and get user choice
            self._display_services(service_status)
            self.selected_service = self._get_service_choice()
            
            # Get user inputs based on service
            self._get_user_inputs()
            
            # Select the service
            service = self.service_manager.select_service(self.selected_service)
            
            # Run the main loop
            self._run_service_loop(service)
            
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        except BotException as e:
            logger.error(f"Bot error: {str(e)}")
        except Exception as e:
            logger.exception(f"Unexpected error: {str(e)}")
        finally:
            self._cleanup()
    
    def _remove_consent_popup(self) -> None:
        """Remove consent popup if present - tries clicking close button first, then JS removal"""
        from selenium.webdriver.common.by import By
        from selenium.common.exceptions import NoAlertPresentException
        
        # First dismiss any alerts
        try:
            alert = self.driver_manager.driver.switch_to.alert
            alert.dismiss()
            logger.info("Dismissed browser notification alert")
            time.sleep(0.5)
        except NoAlertPresentException:
            pass
        except Exception:
            pass
        
        # Try to click the X button on consent dialog
        close_clicked = False
        try:
            close_button_selectors = [
                'div.fc-consent-root button[aria-label="Close"]',
                'div.fc-consent-root button.fc-close',
                'div.fc-dialog-container button[aria-label="Close"]',
                'div.fc-choice-dialog-header button'
            ]
            
            for selector in close_button_selectors:
                try:
                    close_button = self.driver_manager.driver.find_element(By.CSS_SELECTOR, selector)
                    if close_button.is_displayed():
                        close_button.click()
                        logger.info("Clicked consent dialog close button")
                        close_clicked = True
                        time.sleep(0.5)
                        break
                except Exception:
                    continue
        except Exception as e:
            logger.debug(f"No close button found: {str(e)}")
        
        # If close button worked, we're done
        if close_clicked:
            return
        
        # Otherwise, try JavaScript removal
        try:
            removed = self.actions.remove_element(
                By.CSS_SELECTOR,
                config.CSS_SELECTORS["consent_popup"],
                description="consent popup"
            )
            if removed:
                logger.info("Consent popup removed via JavaScript")
            else:
                logger.debug("Consent popup not found")
        except Exception as e:
            logger.warning(f"Could not remove consent popup: {str(e)}")
    
    def _remove_all_popups(self) -> None:
        """
        Remove all types of popups/overlays using JavaScript injection.
        This includes consent popups, monetization dialogs, and message overlays.
        Also dismisses any browser alerts and clicks close buttons.
        """
        from selenium.webdriver.common.by import By
        from selenium.common.exceptions import NoAlertPresentException
        
        # First, dismiss any browser alerts (notification requests, etc.)
        try:
            alert = self.driver_manager.driver.switch_to.alert
            alert.dismiss()
            logger.info("Dismissed browser alert")
            time.sleep(0.5)
        except NoAlertPresentException:
            pass
        except Exception as e:
            logger.debug(f"No alert to dismiss: {str(e)}")
        
        # Try to click close buttons on consent dialogs
        try:
            close_button_selectors = [
                'div.fc-consent-root button[aria-label="Close"]',
                'div.fc-consent-root button.fc-close',
                'div.fc-dialog-container button[aria-label="Close"]',
                'div.fc-choice-dialog-header button',
                'button.fc-button-close'
            ]
            
            for selector in close_button_selectors:
                try:
                    close_buttons = self.driver_manager.driver.find_elements(By.CSS_SELECTOR, selector)
                    for btn in close_buttons:
                        if btn.is_displayed():
                            btn.click()
                            logger.info(f"Clicked close button: {selector}")
                            time.sleep(0.3)
                            break
                except Exception:
                    continue
        except Exception as e:
            logger.debug(f"No close buttons found: {str(e)}")
        
        # JavaScript to remove multiple popup types
        removal_script = """
        (function() {
            let removedCount = 0;
            const selectors = [
                'body > div.fc-consent-root',
                'body > div.fc-message-root > div.fc-monetization-dialog-container > div.fc-monetization-dialog.fc-dialog',
                'body > div.fc-message-root > div.fc-monetization-dialog-container',
                'body > div.fc-message-root',
                'div.fc-dialog-container',
                'div.fc-consent-root',
                'div.fc-dialog',
                'div.fc-monetization-dialog-container',
                'div[class*="fc-"]'
            ];
            
            selectors.forEach(selector => {
                try {
                    const elements = document.querySelectorAll(selector);
                    elements.forEach(el => {
                        if (el && el.parentNode) {
                            el.parentNode.removeChild(el);
                            removedCount++;
                            console.log('Removed element:', selector);
                        }
                    });
                } catch (e) {
                    console.log('Could not remove:', selector, e);
                }
            });
            
            // Remove any elements with high z-index that might be overlays
            document.querySelectorAll('div').forEach(el => {
                try {
                    const style = window.getComputedStyle(el);
                    const zIndex = parseInt(style.zIndex);
                    // Check if zIndex is a valid number before comparing
                    if (!isNaN(zIndex) && zIndex > 1000 && (el.className.includes('fc-') || el.className.includes('dialog') || el.className.includes('modal'))) {
                        el.parentNode.removeChild(el);
                        removedCount++;
                    }
                } catch(e) {}
            });
            
            return removedCount;
        })();
        """
        
        try:
            removed_count = self.driver_manager.driver.execute_script(removal_script)
            # Handle case where script returns None
            if removed_count is None:
                removed_count = 0
            if removed_count > 0:
                logger.info(f"Removed {removed_count} popup element(s)")
            else:
                logger.debug("No popups found to remove")
        except Exception as e:
            logger.warning(f"Error during popup removal: {str(e)}")
    
    def _wait_for_captcha(self) -> None:
        """Wait for user to solve CAPTCHA and remove popups afterwards"""
        print(Fore.YELLOW + "\n" + "="*60)
        print(Fore.YELLOW + "  Please complete the CAPTCHA on the website")
        print(Fore.YELLOW + "  Press Enter here when done...")
        print(Fore.YELLOW + "="*60 + "\n")
        input()
        logger.info("CAPTCHA completed by user")
        
        # Remove all popups after CAPTCHA completion
        logger.info("Removing post-CAPTCHA popups...")
        time.sleep(1)  # Brief wait for popups to appear
        self._remove_all_popups()
        
        # Wait for page to stabilize after popup removal
        logger.info("Waiting for page to stabilize...")
        time.sleep(2)
    
    def _display_services(self, service_status: dict) -> None:
        """
        Display available services to the user
        
        Args:
            service_status: Dictionary of service names to status
        """
        print(Fore.CYAN + "\n" + "="*60)
        print(Fore.CYAN + "  AVAILABLE SERVICES")
        print(Fore.CYAN + "="*60 + "\n")
        
        for index, (service_name, status) in enumerate(service_status.items(), start=1):
            if status == "WORKING":
                status_color = Fore.GREEN
                status_text = "[✓ WORKING]"
            else:
                status_color = Fore.RED
                status_text = "[✗ OFFLINE]"
            
            print(f"{Fore.BLUE}[{index}] {service_name.ljust(20)} {status_color}{status_text}")
        
        print()
    
    def _get_service_choice(self) -> str:
        """
        Get service choice from user
        
        Returns:
            Selected service name
            
        Raises:
            InvalidInputError: If choice is invalid
        """
        try:
            choice_input = input(Fore.YELLOW + "[-] Choose a service (1-6): ")
            choice = validate_service_choice(choice_input, len(config.SERVICES))
            service_name = list(config.SERVICES.keys())[choice - 1]
            logger.info(f"User selected service: {service_name}")
            return service_name
        except InvalidInputError as e:
            logger.error(f"Invalid service choice: {str(e)}")
            print(Fore.RED + f"[!] {str(e)}")
            sys.exit(1)
    
    def _get_user_inputs(self) -> None:
        """
        Get required inputs from user based on selected service
        
        Raises:
            InvalidInputError: If inputs are invalid
        """
        if self.selected_service == "comment_hearts":
            # Comment hearts needs username and URL
            username = input(Fore.MAGENTA + "[-] Enter target username (e.g., @test): ")
            url = input(Fore.MAGENTA + "[-] Enter target URL: ")
            
            # Store for comment hearts processing
            self.target_username = sanitize_input(username)
            self.target_url = sanitize_input(url)
            
            logger.info(f"User inputs: username={self.target_username}, url={self.target_url}")
        else:
            # Other services need video URLs
            urls_input = input(Fore.MAGENTA + "[-] Enter video URLs separated by spaces: ")
            try:
                self.video_urls = parse_url_list(urls_input)
                logger.info(f"User provided {len(self.video_urls)} URL(s)")
            except InvalidInputError as e:
                logger.error(f"Invalid URL input: {str(e)}")
                print(Fore.RED + f"[!] {str(e)}")
                sys.exit(1)
    
    def _run_service_loop(self, service) -> None:
        """
        Run the main service loop
        
        Args:
            service: Selected service object
        """
        logger.info(f"Starting service loop for '{service.name}'")
        
        try:
            if self.selected_service == "comment_hearts":
                # Comment hearts has special handling
                self.service_manager.handle_comment_hearts(
                    self.target_username,
                    self.target_url
                )
            else:
                # Generic service loop
                while True:
                    for video_url in self.video_urls:
                        # Handle any popups
                        self._handle_generic_popups()
                        
                        # Perform service action
                        self.service_manager.perform_generic_service_action(
                            service,
                            video_url
                        )
                        
                        logger.info(f"Completed action for {video_url}")
                    
                    logger.info("Completed all URLs, restarting loop")
                    
        except KeyboardInterrupt:
            logger.info("Service loop interrupted by user")
            raise
    
    def _handle_generic_popups(self) -> None:
        """Detect and close generic popups"""
        try:
            from selenium.webdriver.common.by import By
            close_buttons = self.driver_manager.driver.find_elements(
                By.XPATH,
                config.CSS_SELECTORS["close_buttons"]
            )
            
            for btn in close_buttons:
                if btn.is_displayed() and btn.is_enabled():
                    self.actions.execute_script(
                        "arguments[0].click();",
                        btn,
                        description="closing popup"
                    )
                    logger.debug("Closed a generic popup")
                    
        except Exception as e:
            logger.debug(f"No generic popups detected: {str(e)}")
    
    def _cleanup(self) -> None:
        """Clean up resources before exit"""
        logger.info("Cleaning up resources")
        if self.driver_manager:
            self.driver_manager.quit()
        logger.info("Bot shutdown complete")


def main():
    """Main entry point"""
    bot = ZefoyBot()
    bot.start()


if __name__ == "__main__":
    main()
