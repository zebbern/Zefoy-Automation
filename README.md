<div align="center">
  <a href="https://github.com/zebbern/Zefoy-Automation">
    <img src="https://www.edigitalagency.com.au/wp-content/uploads/TikTok-icon-glyph.png" alt="Logo" width="120" height="121">
  </a>

## Automate Zefoy Interactions With No Effort

**v3.3.0 - Ban Detection & Discord Notifications**

---

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Playwright](https://img.shields.io/badge/Playwright-Powered-orange.svg)](https://playwright.dev/)
[![Stars](https://img.shields.io/github/stars/zebbern/Zefoy-Automation?style=social)](https://github.com/zebbern/Zefoy-Automation/stargazers)

**A powerful, fully automated TikTok engagement tool using Zefoy.com**

[Features](#features) • [Quick Start](#quick-start) • [TUI](#terminal-ui) • [Documentation](#documentation) • [Contributing](#contributing)

</div>

---

## Features

<table>
<tr>
<td width="50%">

### Core Features
- **Terminal UI (TUI)** - Beautiful interactive interface
- **Headless Mode** - Run completely in background
- **Auto-CAPTCHA** - EasyOCR + spell correction
- **Multi-Service** - Hearts, Favorites, Comment Hearts

</td>
<td width="50%">

### Safety & Monitoring
- **Ban Detection** - Auto-stops on 24h+ rate limits
- **Discord Alerts** - Real-time webhook notifications
- **Live Stats** - Track views, likes, and deltas
- **Session Stats** - Sent count, attempts, elapsed time

</td>
</tr>
<tr>
<td>

### Performance
- **Smart Rate Limiting** - Intelligent auto-wait
- **Error Recovery** - Automatic retry handling
- **Proxy Support** - Route through HTTP proxies
- **Cookie Management** - Clear on demand

</td>
<td>

### Developer Experience
- **Clean Architecture** - Modular & maintainable
- **One-Click Install** - Auto venv + dependencies
- **Verbose Logging** - Detailed debug output
- **Comprehensive Tests** - pytest coverage

</td>
</tr>
</table>

---

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/zebbern/Zefoy-Automation.git
cd Zefoy-Automation

# Auto-install (creates venv, installs deps, playwright)
python install.py
```

### Usage

```bash
# Terminal UI (Recommended)
python tui_main.py

# Fully automated CLI
python main.py --headless --auto-captcha --service hearts "YOUR_TIKTOK_URL"

# Interactive CLI
python main.py --auto-captcha "YOUR_TIKTOK_URL"
```

---

## Terminal UI

<div align="center">
  
*A beautiful interactive terminal interface for easier automation*

</div>

```bash
python tui_main.py
```

### Features

| Feature | Description |
|---------|-------------|
| **URL Input** | Paste your TikTok video URL |
| **Service Selection** | Choose Hearts, Favorites, or Comment Hearts |
| **Live Timer** | Watch rate limit countdown in real-time |
| **Live Stats** | Views, Likes, Comments, Shares + deltas |
| **Headless Mode** | Runs completely in background |

### Controls

| Key | Action |
|-----|--------|
| `Enter` | Confirm |
| `Escape` | Back |
| `Q` | Quit |
| `Ctrl+C` | Shows quit hint (press twice to force) |

---

## Documentation

<details>
<summary><b>Discord Notifications</b></summary>

Get real-time alerts to your Discord server.

**Setup:**
```bash
# Windows
set ZEFOY_DISCORD_WEBHOOK=https://discord.com/api/webhooks/...

# Linux/macOS
export ZEFOY_DISCORD_WEBHOOK=https://discord.com/api/webhooks/...
```

**Events:**
| Event | Description |
|-------|-------------|
| Milestones | At 10, 25, 50, 100, 250, 500, 1000 sends |
| Ban Detected | Rate limit exceeds 24 hours |
| Session Summary | Stats when session ends |
| Errors | When automation fails |

</details>

<details>
<summary><b>CLI Reference</b></summary>

```bash
python main.py [SERVICE] [OPTIONS] VIDEO_URL
```

**Arguments:**
| Argument | Description | Default |
|----------|-------------|---------|
| `VIDEO_URL` | TikTok video URL | Required |
| `--service` | hearts, favorites, chearts | Interactive |
| `--headless` | No browser window | Disabled |
| `--auto-captcha` | Enable OCR solving | Disabled |
| `--verbose` | Debug output | Disabled |
| `--proxy URL` | HTTP proxy | None |
| `--count N` | Number of sends | 1 |
| `--clear-cookies` | Clear cookies first | Disabled |

**Examples:**
```bash
# Hearts with auto-CAPTCHA
python main.py hearts --auto-captcha "URL"

# Headless favorites
python main.py favorites --headless --auto-captcha "URL"

# With proxy
python main.py --proxy http://user:pass@host:8080 "URL"

# Verbose debug
python main.py --verbose --auto-captcha "URL"
```

</details>

<details>
<summary><b>Ban Detection</b></summary>

When rate-limited for 24+ hours (indicating IP/account ban):

- **Auto-stops** automation immediately
- **Alerts** you in TUI with red warning
- **Sends** Discord notification (if configured)
- **Suggests** trying again later or using different network

</details>

<details>
<summary><b>Manual Installation</b></summary>

```bash
# Create virtual environment
python -m venv .venv

# Activate
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install browser
playwright install chromium
```

</details>

<details>
<summary><b>Troubleshooting</b></summary>

**CAPTCHA solving fails:**
- Upgrade EasyOCR: `pip install easyocr --upgrade`
- Use `--verbose` to see OCR output
- Some CAPTCHAs need manual solving

**Browser not installed:**
```bash
playwright install chromium
```

**Rate limited immediately:**
- Clear cookies: `--clear-cookies`
- Try a proxy: `--proxy http://...`
- Wait a few minutes

**pyenchant fails on Windows:**
- Download from [pyenchant wiki](https://github.com/pyenchant/pyenchant/wiki/Download-The-Enchant-Library)
- Or: `pip install pyenchant --no-build-isolation`

</details>

---

## Project Structure

```
Zefoy-Automation/
├── main.py              # CLI entry point
├── tui_main.py          # TUI entry point
├── install.py           # Auto-installer
├── requirements.txt     # Dependencies
│
├── browser/
│   ├── automation.py    # Browser control
│   ├── captcha_solver.py # OCR + spell correction
│   ├── popup_handlers.py # Popup handling
│   └── js_injections.py  # JS helpers
│
├── services/
│   ├── base_service.py   # Base class
│   ├── hearts.py         # Hearts service
│   ├── favorites.py      # Favorites service
│   └── comment_hearts.py # Comment Hearts
│
├── tui/
│   └── app.py            # Textual TUI app
│
└── utils/
    ├── timer.py          # Countdown timer
    ├── colors.py         # Console colors
    ├── livecounts.py     # TikTok stats API
    └── health_check.py   # Site availability
```

---

## Contributing

Contributions are welcome! Please read our contributing guidelines.

1. **Fork** the repository
2. **Create** feature branch: `git checkout -b feature/amazing`
3. **Commit** changes: `git commit -m 'Add amazing feature'`
4. **Push** branch: `git push origin feature/amazing`
5. **Open** Pull Request

### Development

```bash
git clone https://github.com/yourusername/Zefoy-Automation.git
cd Zefoy-Automation
python install.py
pytest  # Run tests
```

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `playwright` | Browser automation |
| `textual` | Terminal UI framework |
| `easyocr` | OCR for CAPTCHA |
| `pyenchant` | Spell correction |
| `requests` | HTTP requests |
| `Pillow` | Image processing |

---

## Disclaimer

<details>
<summary><b>Read Full Disclaimer</b></summary>

**This tool is for educational and research purposes only.**

- Not affiliated with or endorsed by zefoy.com or TikTok
- Automated interactions may violate Terms of Service
- Use entirely at your own risk

**Prohibited Uses:**
- Spam or malicious activities
- Harassment or abuse
- Commercial purposes without authorization

**By using this software, you agree to:**
1. Understand the risks (account bans, etc.)
2. Verify compliance with ToS
3. Use responsibly
4. Accept full liability

</details>

---

<div align="center">

**Star this repo if you find it useful!**

Made by [@zebbern](https://github.com/zebbern)

</div>
