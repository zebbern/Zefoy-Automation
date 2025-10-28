
<div align="center">
   <a href="https://github.com/zebbern/Zefoy-Automator-2025">
      <img src="https://www.edigitalagency.com.au/wp-content/uploads/TikTok-icon-glyph.png" alt="Logo" width="120" height="121">
   </a>

## Automate Zefoy Interactions With No Effort

**v2.0.0 - Clean Architecture Edition**

---

| **Features**                      | **Description**                                                              |
|-----------------------------------|------------------------------------------------------------------------------|
| **Virtual Environment Setup**     | Automatic venv creation and dependency management.                           |
| **One-Click Launch**              | Auto-setup and run with a single command.                                    |
| **Smart Popup Handling**          | Auto-dismisses alerts, clicks close buttons, removes overlays.               |
| **Automated Views**               | Automate video views on TikTok seamlessly.                                   |
| **Likes Automation**              | Perform automated likes on specified videos or profiles.                     |
| **Comment Likes**                 | Boost engagement by automating comment likes.                                |
| **Dynamic Service Detection**     | Automatically detects available services on page load.                       |
| **Continuous Execution**          | Automatically loops tasks until stopped by the user.                         |
| **Professional Logging**          | File and console logging with automatic rotation.                            |
| **Error Recovery**                | Robust error handling and automatic retries.                                 |
| **Clean Architecture**            | Modular, maintainable, and easy to extend.                                   |

---
</div>

## **Overview**

The **TikTok Automation Bot** leverages Python and Selenium WebDriver to automate TikTok interactions via [Zefoy](https://zefoy.com/). Completely refactored with clean architecture and robust popup handling.

### **How It Works**

1. **Run the Script:** Execute `python main.py` to start the bot with auto-setup and virtual environment.
2. **Auto-Install:** Virtual environment is created on first run, dependencies automatically installed.
3. **Solve the CAPTCHA:** Manually complete the CAPTCHA on Zefoy.
4. **Auto Popup Removal:** Bot automatically dismisses alerts and removes all consent/monetization dialogs.
5. **Select a Service:** Choose from detected available services in the console.
6. **Enter Details:** Provide video URL or username depending on service chosen.
7. **Relax:** The script runs continuously until manually stopped.  

---

## ⚡ Quick Start

1. **Run the bot** (automatic setup):
   ```bash
   python main.py
   ```
   - First run: Creates `venv/` folder and installs all dependencies (~1 minute)
   - Subsequent runs: Instant startup using existing virtual environment

2. **Complete CAPTCHA**: 
   - Solve the CAPTCHA on the website
   - Press Enter in the terminal when done
   - Bot automatically dismisses notification alerts
   - Bot clicks close buttons on consent dialogs  
   - Bot removes any remaining popups/overlays via JavaScript

3. **Select service**: 
   - View automatically detected available services
   - Choose from: followers, hearts, views, shares, favorites, comment_hearts

4. **Provide input**: 
   - Enter TikTok URL(s) or username as requested
   - Bot will continuously execute until you press Ctrl+C

---

## **Prerequisites**

- Python 3.6 or newer
- Google Chrome or Chromium browser
- ChromeDriver (compatible with your browser version)

---

## **Installation**

### 1. Clone the Repository

```bash
git clone https://github.com/zebbern/Zefoy-Automation.git
cd Zefoy-Automation
```

### 2. Run the Bot

```bash
python main.py
```

The launcher handles everything else automatically!

### 3. Manual Installation (Optional)

If you prefer to install dependencies manually:

```bash
pip install -r requirements.txt
```

---

## **Project Structure**

```
Zefoy-Automation/
├── main.py                # ← Run this file (auto-setup with venv)
├── venv/                  # Virtual environment (auto-created)
├── src/                   # Python modules
│   ├── bot.py            # Main bot logic & popup handling
│   ├── config.py         # All settings & configuration
│   ├── services.py       # Service detection & operations
│   ├── driver_manager.py # WebDriver management & anti-detection
│   ├── actions.py        # Reusable Selenium actions
│   ├── logger.py         # Logging system with rotation
│   ├── validators.py     # Input validation & sanitization
│   └── exceptions.py     # Custom exception hierarchy
├── script.js              # JavaScript utilities
├── requirements.txt       # Python dependencies
├── install_chromedriver.py # ChromeDriver auto-installer
└── README.md             # This file
```

---

## **Usage**

### **Basic Usage**

```bash
python main.py
```

### **What Happens:**

1. **Auto-Setup Check**
   - Verifies Python version (3.6+)
   - Creates virtual environment (`venv/`) on first run
   - Checks if dependencies are installed in venv
   - Offers to auto-install if missing

2. **Browser Opens**
   - Chrome opens and navigates to Zefoy.com
   - Initial consent popup is handled (alert dismissal + close button click)
   - You solve the CAPTCHA manually and press Enter

3. **Post-CAPTCHA Cleanup**
   - Bot automatically dismisses browser notification alerts
   - Clicks close buttons on consent/monetization dialogs
   - Removes any remaining overlay popups via JavaScript
   - Waits for page to stabilize

4. **Service Detection**
   - Bot checks which services are currently available
   - Console shows detected services with status:
     - [1] followers - [✓ WORKING] or [✗ OFFLINE]
     - [2] hearts (likes)
     - [3] comment_hearts
     - [4] views
     - [5] shares
     - [6] favorites

5. **Provide Input**
   - For most services: Enter TikTok video URLs (space-separated)
   - For comment hearts: Enter username and target URL

6. **Automation Runs**
   - Bot performs the selected action continuously
   - Press Ctrl+C to stop

---

## Features

### Virtual Environment Management
- Automatic venv creation on first run
- Isolated dependency management
- No reinstallation needed on subsequent runs
- One-time setup (~1 minute)

### Smart Popup Handling
- Browser alert dismissal (notification requests)
- Automatic close button clicking on consent dialogs
- JavaScript-based removal for stubborn popups
- Handles consent, monetization, and message overlays
- Multi-layer approach for maximum reliability

### Dynamic Service Detection
- Automatically checks service availability on page load
- Real-time status display (✓ WORKING / ✗ OFFLINE)
- Updated XPath detection for accurate button location
- No hardcoded assumptions about page structure

### Clean Architecture
- Modular design with separation of concerns
- 8 specialized modules for different responsibilities
- Easy to maintain and extend
- Professional code quality with type hints

### Logging System
- Console output with color coding (colorama)
- File logging: `zefoy_bot.log`
- Automatic log rotation (10MB max, 5 backups)
- Multiple log levels (DEBUG, INFO, WARNING, ERROR)

### Error Handling
- Custom exception types for specific errors
- Automatic retry logic for failed operations (3 retries with 2s delay)
- Graceful degradation on failures
- Detailed error messages with stack traces

### Input Validation
- URL format validation
- Username format checking (@username)
- Input sanitization for security
- Clear error messages for invalid inputs

### Centralized Configuration
All settings in one place (`src/config.py`):
- Service wait times (randomized delays)
- XPath locators (auto-updated)
- CSS selectors for popups
- Timeout settings
- Retry configurations
- ChromeDriver options

---

## **Configuration**

### **Changing Wait Times**

Edit `src/config.py`:

```python
SERVICE_WAIT_TIMES = {
    "views": (125, 135),      # Random wait between 125-135 seconds
    "hearts": (125, 135),
    "comment_hearts": (70, 70),
    # ... modify as needed
}
```

### **Adding New Services**

Edit `src/config.py`:

```python
SERVICES = {
    "new_service": ("/xpath/to/button", 13)
}

SERVICE_WAIT_TIMES = {
    "new_service": (100, 120)
}
```

No code changes needed - it's automatically detected!

---

## **Troubleshooting**

### **Dependencies Not Installing?**

Install manually:
```bash
pip install -r requirements.txt
```

### **ChromeDriver Issues?**

Run the installer:
```bash
chromedriveinstall.bat  # Windows
```

Or install manually from [ChromeDriver Downloads](https://chromedriver.chromium.org/)

### **Bot Crashing?**

Check the log file:
```bash
cat zefoy_bot.log  # Linux/Mac
type zefoy_bot.log # Windows
```

### **Service Offline?**

Some services may be temporarily unavailable on Zefoy. Try:
- Refreshing the page
- Selecting a different service
- Waiting a few minutes and trying again

---

## **Advanced Usage**

### **Running in Background (Linux/Mac)**

```bash
nohup python main.py > output.log 2>&1 &
```

### **Debug Mode**

Check `zefoy_bot.log` for detailed debug information.

---

## **Changelog**

### **v2.0.0 - Clean Architecture Edition**
- ✅ Complete refactor with modular architecture
- ✅ Auto-setup launcher (`main.py`)
- ✅ Professional logging system
- ✅ Input validation and sanitization
- ✅ Custom exception handling
- ✅ Retry logic for robustness
- ✅ Organized code structure (`src/` folder)
- ✅ Type hints throughout
- ✅ Comprehensive documentation

### **v1.0.0 - Initial Release**
- Basic automation functionality
- Manual setup required

---

## **Contributing**

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## **License**

This project is for educational purposes only. Use responsibly and at your own risk.

---

## **Author**

**Made with ♥️ by [github.com/zebbern](https://github.com/zebbern)**

⭐ Star this repo if you find it useful!

---

## **Disclaimer**

This bot automates interactions with third-party services. Use at your own risk. The author is not responsible for any consequences of using this software.

---

## **Acknowledgments**

A special thanks to [Zefoy](https://zefoy.com/) for providing the platform for automation.  

---

## **Disclaimer**

> [!WARNING] 
This project is for **educational purposes only** and is not affiliated with TikTok or Zefoy. Users are responsible for ensuring compliance with TikTok's terms of service. Use responsibly and ethically.

---
