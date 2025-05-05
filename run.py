# Developed by: github.com/zebbern
 
import time
import random
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from colorama import init, Fore

init(autoreset=True)

class Bot:
    def __init__(self):
        self.clear_screen()
        self.initialize_driver()
        self.setup_service_xpaths()
        self.service_wait_times = { # Custom wait times for each service with bounds
            "followers": (125, 135),
            "hearts": (125, 135),
            "comment_hearts": (70, 70),  # Fixed to 70 seconds as per requirement
            "views": (125, 135),
            "shares": (85, 100),
            "favorites": (125, 135),
        }

    def clear_screen(self): # Escape sequence to clear the screen
        print("\033c", end="")

    def initialize_driver(self): # Set up Chrome options for WebDriver, including user agent and logging level
        print(Fore.YELLOW + "[~] Loading driver, please wait...")
        options = Options()
        options.add_argument("--log-level=3")
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        # Block notification pop-ups
        prefs = {
            "profile.default_content_setting_values.notifications": 2  # 1: Allow, 2: Block
        }
        options.add_experimental_option("prefs", prefs)
        
        try:
            self.driver = webdriver.Chrome(options=options)
            self.driver.get("https://www.google.com")  # Attempt to open a known page
            print(Fore.GREEN + "[+] Driver loaded successfully\n")
        except Exception as e:
            print(Fore.RED + "[!] No internet connection or WebDriver error")
            exit(1)

    def setup_service_xpaths(self): # Define the base URL and xpaths for different services to interact with
        self.url = "https://zefoy.com"
        self.services = {
            "followers": ("/html/body/div[6]/div/div[2]/div/div/div[2]/div/button", 7),
            "hearts": ("/html/body/div[6]/div/div[2]/div/div/div[3]/div/button", 8),
            "comment_hearts": ("/html/body/div[6]/div/div[2]/div/div/div[4]/div/button", 9),
            "views": ("/html/body/div[6]/div/div[2]/div/div/div[5]/div/button", 10),
            "shares": ("/html/body/div[6]/div/div[2]/div/div/div[6]/div/button", 11),
            "favorites": ("/html/body/div[6]/div/div[2]/div/div/div[7]/div/button", 12),
        }

    def check_services(self): # Check each service's availability by attempting to find its web element
        for service, (xpath, div_index) in self.services.items():
            try:
                element = self.driver.find_element(By.XPATH, xpath)
                if element.is_enabled():
                    self.services[service] = (xpath, div_index, Fore.GREEN + "[WORKING]")
                else:
                    self.services[service] = (xpath, div_index, Fore.RED + "[OFFLINE]")
            except NoSuchElementException:
                self.services[service] = (xpath, div_index, Fore.RED + "[OFFLINE]")
        
        # Remove marking 'comment_hearts' as not implemented to enable functionality
        if "comment_hearts" in self.services:
            xpath, div_index = self.services["comment_hearts"][:2]
            # Verify if the element exists and is enabled
            try:
                element = self.driver.find_element(By.XPATH, xpath)
                if element.is_enabled():
                    self.services["comment_hearts"] = (xpath, div_index, Fore.GREEN + "[WORKING]")
                else:
                    self.services["comment_hearts"] = (xpath, div_index, Fore.RED + "[OFFLINE]")
            except NoSuchElementException:
                self.services["comment_hearts"] = (xpath, div_index, Fore.RED + "[OFFLINE]")

    def start(self): # Main method to start the bot, load the page, and handle user interactions
        self.driver.get(self.url)
        self.remove_consent_popup()  # Remove pop-up after initial page load
        print(Fore.YELLOW + "Please complete the captcha on the website and press Enter here when done...")
        input()
        self.remove_consent_popup()  # Remove pop-up again after captcha
        self.check_services()
        self.choose_service_and_url()
        try:
            while True:
                if self.service_name == "comment_hearts":
                    self.handle_comment_hearts()
                    # Do not break; keep the script running to allow script.js to operate
                    # Alternatively, enter an infinite loop to keep the script alive
                    self.keep_running()
                else:
                    for video_url in self.video_urls:
                        self.handle_generic_popups()  # Handle any generic pop-ups before each action
                        self.perform_service_action(video_url)
        except KeyboardInterrupt:
            print(Fore.RED + "\n[!] Script terminated by user.")
        finally:
            self.driver.quit()

    def choose_service_and_url(self): # Display services to the user for selection and accept video URLs as input
        for index, (service, details) in enumerate(self.services.items(), start=1):
            _, div_index, status = details if len(details) == 3 else (*details, "[STATUS UNKNOWN]")
            print(Fore.BLUE + f"[{index}] {service.ljust(20)} {status}")
        
        try:
            choice = int(input(Fore.YELLOW + "[-] Choose an option: "))
            if choice < 1 or choice > len(self.services):
                raise ValueError
            self.service_name = list(self.services.keys())[choice - 1]
        except (ValueError, IndexError):
            print(Fore.RED + "[!] Invalid choice. Exiting.")
            exit(1)
        
        if self.service_name != "comment_hearts":
            urls_input = input(Fore.MAGENTA + "[-] Enter video URLs separated by a space: ")
            self.video_urls = urls_input.split()
        
        try:
            _, self.div_index, status = self.services[self.service_name]
            if "[WORKING]" not in status:
                print(Fore.RED + f"[!] Selected service '{self.service_name}' is not available.")
                exit(1)
            self.driver.find_element(By.XPATH, self.services[self.service_name][0]).click()
            print(Fore.GREEN + f"[+] Selected service '{self.service_name}'.")
        except NoSuchElementException:
            print(Fore.RED + f"[!] Service button for '{self.service_name}' not found.")
            exit(1)

    def perform_service_action(self, video_url): # Perform the action for the chosen service on the provided video URL
        print(Fore.CYAN + f"[+] Switching URL link to \"{video_url}\"")
        actions = [
            ("clear the URL input", f"/html/body/div[{self.div_index}]/div/form/div/input", "clear"),
            ("enter the video URL", f"/html/body/div[{self.div_index}]/div/form/div/input", "send_keys"),
            ("click the search button", f"/html/body/div[{self.div_index}]/div/form/div/div/button", "click"),
            ("click the send button", f"/html/body/div[{self.div_index}]/div/div/div[1]/div/form/button", "click"),
        ]

        for action_desc, xpath, action_type in actions:
            try:
                element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
                if action_type == "clear":
                    element.clear()
                elif action_type == "send_keys":
                    element.send_keys(video_url)
                element.click()
                print(Fore.GREEN + f"[+] Successfully {action_desc}.")
                if action_desc == "click the search button":
                    time.sleep(3)  # Delay after clicking the search button based on load times
            except TimeoutException:
                print(Fore.RED + f"[!] Timeout: Could not {action_desc} within the specified period.")
            except NoSuchElementException:
                print(Fore.RED + f"[!] Element for {action_desc} not found.")
            except Exception as e:
                print(Fore.RED + f"[!] An error occurred during '{action_desc}': {e}")

        # Custom wait time for each service after actions
        min_wait, max_wait = self.service_wait_times[self.service_name]
        wait_time = random.randint(min_wait, max_wait)
        self.countdown_timer(wait_time)

    def handle_comment_hearts(self):
        """
        Handle the 'comment_hearts' service by executing the additional JavaScript,
        checking for the specific icon, and then running script.js.
        """
        print(Fore.BLUE + "[*] Handling 'comment_hearts' service.")
        
        # Prompt user for inputs
        target_username = input(Fore.MAGENTA + "[-] Enter target username (e.g., @test): ").strip()
        target_url = input(Fore.MAGENTA + "[-] Enter target URL (e.g., https://link.com): ").strip()
        
        # Validate inputs
        if not target_username or not target_url:
            print(Fore.RED + "[!] Both target username and target URL are required. Exiting.")
            exit(1)
        
        # Read and modify the JavaScript from script.js
        script_path = os.path.join(os.getcwd(), "script.js")
        if not os.path.isfile(script_path):
            print(Fore.RED + f"[!] 'script.js' not found at {script_path}. Please ensure the file exists.")
            exit(1)
        
        try:
            with open(script_path, "r", encoding="utf-8") as file:
                js_code = file.read()
        except Exception as e:
            print(Fore.RED + f"[!] Failed to read 'script.js': {e}")
            exit(1)
        
        # Replace placeholders with user inputs
        js_code = js_code.replace('"@test"', f'"{target_username}"')
        js_code = js_code.replace('"https://link.com"', f'"{target_url}"')
        
        print(Fore.GREEN + "[+] JavaScript code prepared for execution.")
        
        # Define the additional JavaScript to input the URL
        input_url_js = f"""
        const targetURL = "{target_url}";
        function inputURL(callback) {{
            const urlInput = document.querySelector("body > div.col-sm-5.col-xs-12.p-1.container.t-chearts-menu > div > form > div > input");
            if (urlInput) {{
                urlInput.value = targetURL; // Input the target URL
                const event = new Event("input"); // Trigger the input event
                urlInput.dispatchEvent(event);
                console.log(`URL "{target_url}" inputted successfully!`);
                setTimeout(callback, 1000); // Wait 1 second before moving to the next step
            }} else {{
                console.log("URL input field not found.");
            }}
        }}
        inputURL(function() {{}});
        """
        
        # Define the 'clickSearchButton' JavaScript
        click_search_js = """
        function clickSearchButton(callback) { 
            const searchButton = document.querySelector('form[action="c2VuZC9mb2xsb3dlcnNfdGlrdG9r"] button[type="submit"]'); 
            if (searchButton) { 
                searchButton.click(); 
                setTimeout(callback, 2000); 
            } 
        }
        clickSearchButton(function() {});
        """
        
        try:
            while True:
                # Execute the inputURL JavaScript
                self.driver.execute_script(input_url_js)
                print(Fore.GREEN + "[+] Executed inputURL JavaScript.")
                
                # Wait for 1 second
                self.countdown_timer(1)
                
                # Execute the clickSearchButton JavaScript
                self.driver.execute_script(click_search_js)
                print(Fore.GREEN + "[+] Executed clickSearchButton JavaScript.")
                
                # Wait for 2 seconds to allow any page updates
                self.countdown_timer(2)
                
                # Check for the presence of the specific icon
                try:
                    # Use CSS Selector to find the <i> element
                    icon_element = self.driver.find_element(By.CSS_SELECTOR, "#c2VuZC9mb2xsb3dlcnNfdGlrdG9r > div.row.text-light.d-flex.justify-content-center > div > form > button > i")
                    if icon_element.is_displayed():
                        print(Fore.GREEN + "[+] Specific icon detected. Executing script.js.")
                        
                        # Execute the modified script.js
                        self.driver.execute_script(js_code)
                        print(Fore.GREEN + "[+] script.js executed successfully.")
                        
                        # Keep the Python script running to allow script.js to operate via setInterval
                        self.keep_running()
                except NoSuchElementException:
                    print(Fore.YELLOW + "[~] Specific icon not found. Will retry in 60 seconds.")
                except Exception as e:
                    print(Fore.RED + f"[!] An error occurred while checking the specific icon: {e}")
                
                # Wait for 60 seconds before retrying
                self.countdown_timer(60)
        except KeyboardInterrupt:
            print(Fore.RED + "\n[!] 'comment_hearts' script terminated by user.")
        except Exception as e:
            print(Fore.RED + f"[!] An error occurred during 'comment_hearts' handling: {e}")

    def keep_running(self):
        """
        Keeps the Python script running indefinitely to allow script.js to operate.
        This method enters an infinite loop, periodically checking for termination signals.
        """
        print(Fore.CYAN + "[*] script.js is now running. Press Ctrl+C to terminate the script.")
        try:
            while True:
                time.sleep(60)  # Sleep for 60 seconds intervals
        except KeyboardInterrupt:
            print(Fore.RED + "\n[!] Script terminated by user.")
            self.driver.quit()
            exit(0)
        except Exception as e:
            print(Fore.RED + f"[!] An unexpected error occurred: {e}")
            self.driver.quit()
            exit(1)

    def countdown_timer(self, duration): # Display a countdown timer for the specified duration
        for i in range(duration, 0, -1):
            print(Fore.CYAN + f"\rWaiting for {i} seconds to proceed...", end="")
            time.sleep(1)
        print()

    def remove_consent_popup(self):
        """
        Remove the consent pop-up by deleting the 'div.fc-consent-root' element from the DOM.
        """
        try:
            # Wait until the consent pop-up is present
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.fc-consent-root"))
            )
            # Execute JavaScript to remove the consent pop-up element
            self.driver.execute_script("""
                var consentPopup = document.querySelector('body > div.fc-consent-root');
                if (consentPopup) {
                    consentPopup.parentNode.removeChild(consentPopup);
                    console.log('Consent pop-up removed successfully.');
                }
            """)
            print(Fore.GREEN + "[+] Consent pop-up removed successfully.")
        except TimeoutException:
            print(Fore.YELLOW + "[~] Consent pop-up not found or already removed.")
        except Exception as e:
            print(Fore.RED + f"[!] An error occurred while removing consent pop-up: {e}")

    def handle_generic_popups(self):
        """
        Detect and close generic pop-ups or overlays.
        """
        try:
            # Example: Close buttons with 'Close' text or 'X' icon
            close_buttons = self.driver.find_elements(By.XPATH, "//button[text()='Close'] | //button[contains(@class, 'close')] | //button[contains(@aria-label, 'Close')]")
            for btn in close_buttons:
                if btn.is_displayed() and btn.is_enabled():
                    self.driver.execute_script("arguments[0].click();", btn)
                    print(Fore.GREEN + "[+] A generic pop-up was closed.")
                    time.sleep(1)  # Allow time for the pop-up to close
        except Exception as e:
            print(Fore.YELLOW + f"[~] No generic pop-ups detected or an error occurred: {e}")

if __name__ == "__main__":
    bot = Bot()
    bot.start()
    
# Made by github.com/zebbern
