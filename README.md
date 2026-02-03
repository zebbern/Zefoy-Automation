<div align="center">
  <a href="https://github.com/zebbern/Zefoy-Automation">
    <img src="https://www.edigitalagency.com.au/wp-content/uploads/TikTok-icon-glyph.png" alt="Logo" width="120" height="121">
  </a>

## Automate Zefoy Interactions With No Effort

**v3.2.0 - Ban Detection & Discord Notifications**

---

| **Features** | **Description** |
|-------------|-----------------|
| **🆕 Terminal UI (TUI)** | Beautiful interactive terminal interface with live timer. |
| **🚫 Ban Detection** | Auto-stops when 24h+ rate limit detected (likely IP/account ban). |
| **📣 Discord Notifications** | Webhook alerts for milestones, bans, and session summaries. |
| **Session Statistics** | Track Sent count, Attempts, and Elapsed time in real-time. |
| **Virtual Environment Setup** | Automatic venv creation and dependency management. |
| **One-Click Launch** | Auto-setup and run with a single command. |
| **Smart Popup Handling** | Auto-dismisses alerts, clicks close buttons, removes overlays. |
| **Auto-CAPTCHA Solving** | Uses EasyOCR + spell correction for accurate text recognition. |
| **Hearts Automation** | Perform automated hearts on specified videos. |
| **Favorites Automation** | Add videos to favorites automatically. |
| **Comment Hearts** | Boost engagement by automating comment hearts. |
| **Dynamic Service Detection** | Automatically detects available services on page load. |
| **Continuous Execution** | Automatically loops tasks until stopped by the user. |
| **Rate Limit Handling** | Intelligent auto-wait when rate limited. |
| **Proxy Support** | Route traffic through HTTP proxies. |
| **Error Recovery** | Robust error handling and automatic retries. |
| **Clean Architecture** | Modular, maintainable, and easy to extend. |

---

</div>

## Overview

The **Zefoy-CLI Automation** leverages Python and Playwright to automate TikTok interactions via [Zefoy](https://zefoy.com/). Completely refactored with clean architecture and robust popup handling.

### Fully Automated (Headless Mode)

Run completely in the background with no browser window:

```bash
python main.py --headless --auto-captcha --service hearts "https://www.tiktok.com/@user/video/123456789"
```

This command runs 100% automated - no user interaction needed!

### Standard Mode (With Browser Window)

```bash
python main.py --auto-captcha "https://www.tiktok.com/@user/video/123456789"
```

---

## Quick Start

```bash
# Clone and install
git clone https://github.com/zebbern/Zefoy-Automation.git
cd Zefoy-Automation
python install.py

# Run fully automated (headless)
python main.py --headless --auto-captcha "https://www.tiktok.com/@user/video/123456789"
```

---

## 🆕 Terminal UI (TUI)

A beautiful interactive terminal interface for easier automation:

```bash
python tui_main.py
```

### TUI Features

- **Interactive URL input** - Paste your TikTok video URL
- **Service selection** - Choose Hearts, Favorites, or Comment Hearts
- **Live countdown timer** - Watch the rate limit countdown in real-time
- **Progress tracking** - See your progress at a glance
- **Headless mode** - Runs completely in the background (no browser window)

### TUI Controls

| Key | Action |
|-----|--------|
| `Enter` | Confirm selection |
| `Escape` | Go back |
| `Q` | Quit |

---

## 📣 Discord Notifications

Get real-time alerts sent to your Discord server!

### Setup

1. Create a Discord webhook in your server (Server Settings → Integrations → Webhooks)
2. Set the environment variable:

```bash
# Windows
set ZEFOY_DISCORD_WEBHOOK=https://discord.com/api/webhooks/...

# Linux/Mac
export ZEFOY_DISCORD_WEBHOOK=https://discord.com/api/webhooks/...
```

### Notification Types

| Event | Description |
|-------|-------------|
| 🎉 **Milestones** | Sent at 10, 25, 50, 100, 250, 500, 1000 successful sends |
| 🚫 **Ban Detected** | When rate limit exceeds 24 hours (likely IP ban) |
| 📊 **Session Summary** | Statistics when session ends |
| ❌ **Errors** | When automation encounters errors |

---

## 🚫 Ban Detection

The automation automatically detects when you've been rate-limited for 24+ hours, which typically indicates an IP or account ban:

- **Auto-stops** the automation immediately
- **Alerts** you in the TUI with red warning
- **Sends** Discord notification (if configured)
- **Suggests** trying again later or using a different network

---

## Installation

### Method 1: Auto-Install Script (Recommended)

The automated installer handles everything for you:

```bash
python install.py
```

This will:
- Create a virtual environment (`.venv`)
- Install all Python dependencies
- Install Playwright Chromium browser

### Method 2: Manual Installation

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browser
playwright install chromium
```

### System Requirements

- **Python**: 3.10 or higher
- **OS**: Windows, macOS, or Linux
- **RAM**: 4GB minimum (8GB recommended for OCR)

---

## Usage

### Interactive Mode

Launch without specifying a service to choose interactively:

```bash
python main.py --auto-captcha "https://www.tiktok.com/@user/video/123456789"
```

### Command Line Examples

```bash
# Hearts service with auto-CAPTCHA
python main.py hearts --auto-captcha "https://www.tiktok.com/@user/video/123456789"

# Favorites with specific count
python main.py favorites --count 5 --auto-captcha "https://www.tiktok.com/@user/video/123456789"

# Comment Hearts service
python main.py comment-hearts --auto-captcha "https://www.tiktok.com/@user/video/123456789"

# With HTTP proxy
python main.py --proxy http://user:pass@proxy.example.com:8080 "https://www.tiktok.com/@user/video/123456789"

# Verbose mode for debugging
python main.py --verbose --auto-captcha "https://www.tiktok.com/@user/video/123456789"

# Clear cookies before starting
python main.py --clear-cookies --auto-captcha "https://www.tiktok.com/@user/video/123456789"

# Combined options
python main.py hearts --count 10 --auto-captcha --verbose "https://www.tiktok.com/@user/video/123456789"
```

---

## Command Line Reference

| Argument | Description | Default |
|----------|-------------|---------|
| `VIDEO_URL` | TikTok video URL (required) | - |
| `--service SERVICE` | Service: `hearts`, `favorites`, `chearts` | Interactive |
| `--headless` | Run browser invisibly (no window) | Disabled |
| `--auto-captcha` | Enable automatic CAPTCHA solving with OCR | Disabled |
| `--verbose` | Show detailed debug output | Disabled |
| `--proxy URL` | HTTP proxy URL (e.g., `http://user:pass@host:port`) | None |
| `--count N` | Number of sends to perform | 1 |
| `--clear-cookies` | Clear browser cookies on start | Disabled |

### Recommended Command (Fully Automated)

```bash
python main.py --headless --auto-captcha --service hearts "YOUR_VIDEO_URL"
```

### Services

| Service | Command | Description |
|---------|---------|-------------|
| Hearts | `hearts` | Send hearts/likes to the video |
| Favorites | `favorites` | Add video to favorites |
| Comment Hearts | `comment-hearts` | Send hearts to video comments |

---

## Project Structure

```
Zefoy-Automation/
├── main.py                    # CLI entry point & argument parsing
├── install.py                 # Auto-installer script
├── requirements.txt           # Python dependencies
├── pyproject.toml             # Project configuration
│
├── browser/
│   ├── automation.py          # Browser control & navigation
│   ├── captcha_solver.py      # OCR + spell correction logic
│   ├── popup_handlers.py      # Handle popups & modals
│   └── js_injections.py       # JavaScript helper functions
│
├── services/
│   ├── base_service.py        # Abstract service base class
│   ├── hearts.py              # Hearts service implementation
│   ├── favorites.py           # Favorites service implementation
│   └── comment_hearts.py      # Comment Hearts service implementation
│
└── utils/
    ├── timer.py               # Wait time parsing & countdown
    ├── colors.py              # Console color formatting
    └── health_check.py        # Site availability checking
```

---

## How It Works

### CAPTCHA Solving Pipeline

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Screenshot     │ --> │  EasyOCR        │ --> │  Spell          │
│  CAPTCHA Image  │     │  Text Extract   │     │  Correction     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                                                        v
                                               ┌─────────────────┐
                                               │  Submit         │
                                               │  Solution       │
                                               └─────────────────┘
```

1. **Screenshot Capture**: The browser takes a screenshot of the CAPTCHA region
2. **OCR Processing**: EasyOCR extracts text from the image
3. **Spell Correction**: pyenchant corrects common OCR errors (e.g., "l" -> "I", "0" -> "O")
4. **Submission**: The corrected text is entered and submitted

### Rate Limit Handling

When Zefoy rate-limits requests, the automation:
1. Detects the wait time from the page
2. Displays a countdown timer
3. Automatically retries after the wait period

---

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `playwright` | >=1.40.0 | Browser automation |
| `easyocr` | >=1.7.0 | Optical Character Recognition |
| `numpy` | >=1.24.0 | Array processing for OCR |
| `Pillow` | >=10.0.0 | Image processing |
| `pyenchant` | >=3.2.0 | Spell checking/correction |
| `pytest` | >=7.0.0 | Testing framework |
| `pytest-asyncio` | >=0.21.0 | Async test support |

---

## Troubleshooting

### Common Issues

<details>
<summary><b>CAPTCHA solving fails repeatedly</b></summary>

- Ensure EasyOCR is properly installed: `pip install easyocr --upgrade`
- Try running with `--verbose` to see OCR output
- The CAPTCHA image might be too distorted; manual solving may be needed

</details>

<details>
<summary><b>"Browser not installed" error</b></summary>

Run the Playwright installer:
```bash
playwright install chromium
```

</details>

<details>
<summary><b>Rate limited immediately</b></summary>

- Clear cookies: `python main.py --clear-cookies ...`
- Try using a proxy: `--proxy http://...`
- Wait a few minutes before retrying

</details>

<details>
<summary><b>pyenchant installation fails on Windows</b></summary>

1. Download the enchant library from [here](https://github.com/pyenchant/pyenchant/wiki/Download-The-Enchant-Library)
2. Or use: `pip install pyenchant --no-build-isolation`

</details>

<details>
<summary><b>Service shows "Not Available"</b></summary>

Zefoy occasionally disables services. Check the site manually or try a different service.

</details>

### Debug Mode

For detailed logging, always use the `--verbose` flag:

```bash
python main.py --verbose --auto-captcha "https://www.tiktok.com/@user/video/123"
```

---

## Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/Zefoy-Automation.git
cd Zefoy-Automation

# Install in development mode
python install.py

# Run tests
pytest
```

---

## ⚠️ Disclaimer

**This tool is provided for educational and research purposes only.**

### Important Notices

- This project is an independent automation tool and is **not affiliated with or endorsed by** zefoy.com or TikTok
- The author has no control over third-party service availability or functionality
- Automated interactions may violate TikTok's and/or Zefoy's Terms of Service
- **Use of this tool is entirely at your own risk**

### Prohibited Uses

This tool must **NOT** be used for:
- Spam or malicious activities
- Harassment or abuse
- Any activities that violate platform Terms of Service
- Commercial purposes without proper authorization

### Your Responsibilities

By using this software, you acknowledge and agree that:

1. **You understand the risks** - Including potential account restrictions or bans
2. **You will verify compliance** - Check TikTok's and Zefoy's Terms of Service before use
3. **You will use responsibly** - Respect rate limits and ethical guidelines
4. **You accept full liability** - The author assumes no responsibility for:
   - Consequences arising from your use of this tool
   - Violations of any Terms of Service
   - Account suspensions, bans, or other penalties
   - Any damages or losses incurred

---

**By installing, or using this software, you agree to this disclaimer and accept sole responsibility for your actions.**

---

<div align="center">

**Made with love for automation enthusiasts**

Star this repo if you find it useful!

</div>
