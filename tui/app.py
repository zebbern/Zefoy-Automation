"""
Zefoy-CLI Automation - TUI Application
========================================

Beautiful Terminal User Interface for Zefoy automation.

Author: zebbern (https://github.com/zebbern)
Repository: https://github.com/zebbern/Zefoy-Automation
License: MIT
Copyright (c) 2024 zebbern
"""
from __future__ import annotations

import asyncio
import warnings
from typing import TYPE_CHECKING

# Suppress asyncio unclosed transport warnings on exit
warnings.filterwarnings("ignore", category=ResourceWarning, message=".*unclosed transport.*")

from textual import on, work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import (
    Button,
    Footer,
    Input,
    Label,
    ListItem,
    ListView,
    Rule,
    Static,
    RichLog,
)

if TYPE_CHECKING:
    from browser.automation import ZefoyAutomation


class ServiceItem(ListItem):
    """A compact service option."""
    
    def __init__(self, key: str, display_name: str) -> None:
        super().__init__()
        self.service_key = key
        self.display_name = display_name
    
    def compose(self) -> ComposeResult:
        yield Label(f"  {self.display_name}")


class WelcomeScreen(Screen):
    """Welcome screen with video URL input."""
    
    CSS = """
    #welcome-container {
        align: center middle;
    }
    
    #welcome-box {
        width: 70;
        height: auto;
        border: round $primary;
        padding: 1 2;
    }
    
    #title {
        text-align: center;
        text-style: bold;
    }
    
    #subtitle {
        text-align: center;
        color: $text-muted;
    }
    
    #author {
        text-align: center;
        color: $primary-lighten-2;
        margin-bottom: 1;
    }
    
    #url-input {
        margin: 1 0;
    }
    
    .error-message {
        color: $error;
        text-align: center;
    }
    
    #button-row {
        height: 3;
        margin-top: 1;
    }
    
    #start-btn {
        width: 1fr;
    }
    
    #settings-btn {
        width: auto;
        min-width: 12;
    }
    """
    
    BINDINGS = [
        Binding("escape", "quit", "Quit"),
        Binding("s", "open_settings", "Settings"),
    ]
    
    def compose(self) -> ComposeResult:
        from utils.credits import get_author, get_version
        
        yield Container(
            Vertical(
                Static("ZEFOY TUI", id="title"),
                Static(f"TikTok Automation v{get_version()}", id="subtitle"),
                Static(f"by @{get_author()}", id="author"),
                Rule(),
                Label("Enter TikTok Video URL:"),
                Input(placeholder="https://www.tiktok.com/@user/video/123...", id="url-input"),
                Static("", id="error-message", classes="error-message"),
                Horizontal(
                    Button("▶ Start", id="start-btn", variant="primary"),
                    Button("Settings", id="settings-btn", variant="default"),
                    id="button-row",
                ),
                id="welcome-box",
            ),
            id="welcome-container",
        )
    
    def action_quit(self) -> None:
        self.app.exit()
    
    def action_open_settings(self) -> None:
        self.app.push_screen("settings")
    
    @on(Button.Pressed, "#settings-btn")
    def on_settings(self) -> None:
        self.app.push_screen("settings")
    
    @on(Button.Pressed, "#start-btn")
    @on(Input.Submitted, "#url-input")
    def on_start(self) -> None:
        url_input = self.query_one("#url-input", Input)
        url = url_input.value.strip()
        
        error_label = self.query_one("#error-message", Static)
        
        if not url:
            error_label.update("Please enter a video URL")
            return
        
        if "tiktok.com" not in url.lower():
            error_label.update("Invalid TikTok URL")
            return
        
        self.app.video_url = url
        self.app.push_screen("service")


class SettingsScreen(Screen):
    """Settings configuration screen."""
    
    CSS = """
    #settings-container {
        align: center middle;
    }
    
    #settings-box {
        width: 90;
        height: 100%;
        max-height: 95%;
        border: round $primary;
        padding: 1 2;
        overflow-y: auto;
    }
    
    #settings-title {
        text-align: center;
        text-style: bold;
        color: $primary;
        margin-bottom: 1;
    }
    
    .section-title {
        text-style: bold;
        color: $secondary;
        margin-top: 1;
        margin-bottom: 0;
    }
    
    .setting-row {
        height: 3;
        align: left middle;
    }
    
    .setting-label {
        width: 30;
        height: 3;
        content-align: left middle;
    }
    
    .setting-input {
        width: 1fr;
        height: 3;
    }
    
    #test-webhook-btn {
        width: 12;
        height: 3;
        margin-left: 1;
    }
    
    #webhook-status {
        height: 1;
        color: $secondary;
        margin-left: 30;
    }
    
    .toggle-row {
        height: 3;
        align: left middle;
    }
    
    .toggle-label {
        width: 30;
        height: 3;
        content-align: left middle;
    }
    
    Switch {
        height: 3;
    }
    
    .hint-text {
        color: $warning;
        text-style: italic;
        height: 1;
        margin-left: 2;
    }
    
    #button-row {
        height: 3;
        margin-top: 1;
    }
    
    #save-btn {
        width: 1fr;
    }
    
    #back-btn {
        width: 12;
    }
    
    #save-status {
        text-align: center;
        color: $success;
        height: 1;
    }
    """
    
    BINDINGS = [
        Binding("escape", "go_back", "Back"),
        Binding("s", "save_settings", "Save"),
    ]
    
    def compose(self) -> ComposeResult:
        from utils.config import get_config
        from textual.widgets import Switch
        from textual.containers import VerticalScroll
        
        config = get_config()
        
        yield Container(
            VerticalScroll(
                Static("Settings", id="settings-title"),
                Rule(),
                
                # Notifications Section
                Static("[Notifications]", classes="section-title"),
                Horizontal(
                    Label("Discord Webhook:", classes="setting-label"),
                    Input(
                        value=config.notification.webhook_url,
                        placeholder="https://discord.com/api/webhooks/...",
                        id="webhook-input",
                        classes="setting-input",
                    ),
                    Button("Test", id="test-webhook-btn", variant="warning"),
                    classes="setting-row",
                ),
                Static("", id="webhook-status"),
                Horizontal(
                    Label("Notify on Errors:", classes="toggle-label"),
                    Switch(value=config.notification.notify_on_errors, id="notify-errors-switch"),
                    classes="toggle-row",
                ),
                Horizontal(
                    Label("Notify on Ban Detection:", classes="toggle-label"),
                    Switch(value=config.notification.notify_on_ban, id="notify-ban-switch"),
                    classes="toggle-row",
                ),
                Horizontal(
                    Label("Session Summary:", classes="toggle-label"),
                    Switch(value=config.notification.send_session_summary, id="session-summary-switch"),
                    classes="toggle-row",
                ),
                
                Rule(),
                
                # Automation Section
                Static("[Automation]", classes="section-title"),
                Horizontal(
                    Label("CAPTCHA Max Attempts:", classes="setting-label"),
                    Input(
                        value=str(config.automation.captcha_max_attempts),
                        placeholder="25",
                        id="captcha-attempts-input",
                        classes="setting-input",
                    ),
                    classes="setting-row",
                ),
                Horizontal(
                    Label("Browser Timeout (sec):", classes="setting-label"),
                    Input(
                        value=str(config.automation.browser_timeout),
                        placeholder="30",
                        id="browser-timeout-input",
                        classes="setting-input",
                    ),
                    classes="setting-row",
                ),
                Horizontal(
                    Label("Retry Delay (sec):", classes="setting-label"),
                    Input(
                        value=str(config.automation.auto_retry_delay),
                        placeholder="3",
                        id="retry-delay-input",
                        classes="setting-input",
                    ),
                    classes="setting-row",
                ),
                Horizontal(
                    Label("Max Consecutive Errors:", classes="setting-label"),
                    Input(
                        value=str(config.automation.max_consecutive_errors),
                        placeholder="5",
                        id="max-errors-input",
                        classes="setting-input",
                    ),
                    classes="setting-row",
                ),
                Horizontal(
                    Label("Auto Solve CAPTCHA:", classes="toggle-label"),
                    Switch(value=config.automation.auto_solve_captcha, id="auto-captcha-switch"),
                    classes="toggle-row",
                ),
                Horizontal(
                    Label("Headless Mode:", classes="toggle-label"),
                    Switch(value=config.automation.headless_mode, id="headless-switch"),
                    classes="toggle-row",
                ),
                Horizontal(
                    Label("Stop on Ban:", classes="toggle-label"),
                    Switch(value=config.automation.stop_on_ban, id="stop-ban-switch"),
                    classes="toggle-row",
                ),
                Horizontal(
                    Label("Debug Mode:", classes="toggle-label"),
                    Switch(value=config.automation.debug_mode, id="debug-switch"),
                    classes="toggle-row",
                ),
                
                Rule(),
                
                # Rate Limiting Section
                Static("[Rate Limiting]", classes="section-title"),
                Static("Recommended: max 5 sends/hour to avoid rate-limits", classes="hint-text"),
                Horizontal(
                    Label("Safe Mode (4/hour):", classes="toggle-label"),
                    Switch(value=config.automation.safe_mode, id="safe-mode-switch"),
                    classes="toggle-row",
                ),
                Horizontal(
                    Label("Safe Mode Delay (sec):", classes="setting-label"),
                    Input(
                        value=str(config.automation.safe_mode_delay),
                        placeholder="900 (15 min)",
                        id="safe-mode-delay-input",
                        classes="setting-input",
                    ),
                    classes="setting-row",
                ),
                
                Rule(),
                
                # Network Section
                Static("[Network]", classes="section-title"),
                Horizontal(
                    Label("Proxy URL:", classes="setting-label"),
                    Input(
                        value=config.automation.proxy_url,
                        placeholder="http://user:pass@host:port (optional)",
                        id="proxy-input",
                        classes="setting-input",
                    ),
                    classes="setting-row",
                ),
                
                Rule(),
                Static("", id="save-status"),
                
                Horizontal(
                    Button("Save Settings", id="save-btn", variant="primary"),
                    Button("Back", id="back-btn", variant="default"),
                    id="button-row",
                ),
                
                id="settings-box",
            ),
            id="settings-container",
        )
    
    def action_go_back(self) -> None:
        self.app.pop_screen()
    
    def action_save_settings(self) -> None:
        self.on_save()
    
    @on(Button.Pressed, "#back-btn")
    def on_back(self) -> None:
        self.app.pop_screen()
    
    @on(Button.Pressed, "#save-btn")
    def on_save(self) -> None:
        from utils.config import update_config
        from textual.widgets import Switch
        
        # Get input values
        webhook = self.query_one("#webhook-input", Input).value.strip()
        captcha_attempts_str = self.query_one("#captcha-attempts-input", Input).value.strip()
        browser_timeout_str = self.query_one("#browser-timeout-input", Input).value.strip()
        retry_delay_str = self.query_one("#retry-delay-input", Input).value.strip()
        max_errors_str = self.query_one("#max-errors-input", Input).value.strip()
        proxy = self.query_one("#proxy-input", Input).value.strip()
        
        # Get toggle values
        notify_errors = self.query_one("#notify-errors-switch", Switch).value
        notify_ban = self.query_one("#notify-ban-switch", Switch).value
        session_summary = self.query_one("#session-summary-switch", Switch).value
        auto_captcha = self.query_one("#auto-captcha-switch", Switch).value
        headless = self.query_one("#headless-switch", Switch).value
        stop_ban = self.query_one("#stop-ban-switch", Switch).value
        debug = self.query_one("#debug-switch", Switch).value
        safe_mode = self.query_one("#safe-mode-switch", Switch).value
        
        # Parse integers with defaults
        def parse_int(val: str, default: int, min_val: int, max_val: int) -> int:
            try:
                return max(min_val, min(max_val, int(val))) if val else default
            except ValueError:
                return default
        
        captcha_attempts = parse_int(captcha_attempts_str, 25, 1, 100)
        browser_timeout = parse_int(browser_timeout_str, 30, 5, 120)
        retry_delay = parse_int(retry_delay_str, 3, 0, 60)
        max_errors = parse_int(max_errors_str, 5, 1, 50)
        safe_mode_delay = parse_int(
            self.query_one("#safe-mode-delay-input", Input).value.strip(),
            900, 60, 3600
        )
        
        # Save all settings
        update_config(
            webhook_url=webhook,
            captcha_max_attempts=captcha_attempts,
            browser_timeout=browser_timeout,
            auto_retry_delay=retry_delay,
            max_consecutive_errors=max_errors,
            proxy_url=proxy,
            notify_on_errors=notify_errors,
            notify_on_ban=notify_ban,
            send_session_summary=session_summary,
            auto_solve_captcha=auto_captcha,
            headless_mode=headless,
            stop_on_ban=stop_ban,
            debug_mode=debug,
            safe_mode=safe_mode,
            safe_mode_delay=safe_mode_delay,
        )
        
        self.query_one("#save-status", Static).update("Settings saved to ~/.zefoy/config.json")
    
    @on(Button.Pressed, "#test-webhook-btn")
    async def on_test_webhook(self) -> None:
        """Send a test notification to the configured webhook."""
        from utils.notifications import send_webhook
        
        webhook_url = self.query_one("#webhook-input", Input).value.strip()
        status_widget = self.query_one("#webhook-status", Static)
        
        if not webhook_url:
            status_widget.update("⚠️ Enter a webhook URL first")
            return
        
        if not webhook_url.startswith("https://discord.com/api/webhooks/"):
            status_widget.update("⚠️ Invalid Discord webhook URL format")
            return
        
        status_widget.update("🔄 Testing webhook...")
        
        success = await send_webhook(
            title="🔔 Webhook Test",
            description="Your Discord webhook is configured correctly!",
            color=0x00FF00,
            fields=[
                {"name": "Status", "value": "✅ Connection successful", "inline": True},
                {"name": "Source", "value": "Zefoy Automation", "inline": True},
            ],
            webhook_url=webhook_url,
        )
        
        if success:
            status_widget.update("✅ Test sent! Check your Discord channel")
        else:
            status_widget.update("❌ Failed to send - check webhook URL")


class ServiceScreen(Screen):
    """Quick service selection - auto-starts on select."""
    
    CSS = """
    #service-container {
        align: center middle;
    }
    
    #service-box {
        width: 50;
        height: auto;
        border: round $primary;
        padding: 1 2;
    }
    
    #service-title {
        text-align: center;
        text-style: bold;
        margin-bottom: 1;
    }
    
    ListView {
        height: 5;
        margin: 1 0;
    }
    
    ListItem {
        height: 1;
    }
    """
    
    BINDINGS = [
        Binding("escape", "go_back", "Back"),
    ]
    
    def compose(self) -> ComposeResult:
        yield Container(
            Vertical(
                Static("Select Service", id="service-title"),
                Rule(),
                ListView(
                    ServiceItem("hearts", "Hearts"),
                    ServiceItem("favorites", "Favorites"),
                    ServiceItem("chearts", "Comment Hearts"),
                    id="service-list",
                ),
                id="service-box",
            ),
            id="service-container",
        )
    
    def action_go_back(self) -> None:
        self.app.pop_screen()
    
    @on(ListView.Selected)
    def on_service_selected(self, event: ListView.Selected) -> None:
        if isinstance(event.item, ServiceItem):
            self.app.selected_service = event.item.service_key
            # Go directly to running screen - auto-start
            self.app.push_screen("running")


class RunningScreen(Screen):
    """Minimal running screen - just shows progress."""
    
    CSS = """
    #running-container {
        align: center middle;
    }
    
    #running-box {
        width: 80;
        height: 100%;
        border: round $primary;
        padding: 1 2;
    }
    
    #run-title {
        text-style: bold;
        margin-bottom: 1;
    }
    
    #status-info {
        height: auto;
        margin-bottom: 1;
    }
    
    .info-row {
        height: 1;
    }
    
    .label {
        width: 12;
        color: $text-muted;
    }
    
    .value {
        width: 1fr;
    }
    
    #timer-value {
        color: $warning;
        text-style: bold;
    }
    
    #state-value {
        color: $success;
    }
    
    #progress-bar {
        height: 1;
        margin: 0 0 1 0;
    }
    
    RichLog {
        height: 1fr;
        border: round $primary-darken-2;
        background: $surface-darken-1;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit_automation", "Quit"),
    ]
    
    def __init__(self) -> None:
        super().__init__()
        self._running = False
        self._successful = 0
        self._should_exit = False
        self._total_attempts = 0
        self._start_time = None
        self._banned = False
    
    def compose(self) -> ComposeResult:
        yield Container(
            Vertical(
                Static("Running Automation", id="run-title"),
                Vertical(
                    Horizontal(
                        Label("Service:", classes="label"),
                        Label("...", id="service-val", classes="value"),
                        classes="info-row",
                    ),
                    Horizontal(
                        Label("Timer:", classes="label"),
                        Label("--", id="timer-value", classes="value"),
                        classes="info-row",
                    ),
                    Horizontal(
                        Label("State:", classes="label"),
                        Label("Starting...", id="state-value", classes="value"),
                        classes="info-row",
                    ),
                    Horizontal(
                        Label("Sent:", classes="label"),
                        Label("0", id="sent-value", classes="value"),
                        classes="info-row",
                    ),
                    Horizontal(
                        Label("Attempts:", classes="label"),
                        Label("0", id="attempts-value", classes="value"),
                        classes="info-row",
                    ),
                    Horizontal(
                        Label("Elapsed:", classes="label"),
                        Label("0:00", id="elapsed-value", classes="value"),
                        classes="info-row",
                    ),
                    id="status-info",
                ),
                RichLog(id="output-log", auto_scroll=True, markup=True),
                id="running-box",
            ),
            id="running-container",
        )
        yield Footer()
    
    def on_mount(self) -> None:
        # Update service name now that we're mounted
        self.query_one("#service-val", Label).update(self.app.selected_service.capitalize())
        # Start elapsed time updater
        import time
        self._start_time = time.time()
        self.set_interval(1.0, self._update_elapsed_time)
        # Auto-start automation when screen mounts
        self.run_automation()
    
    def _update_elapsed_time(self) -> None:
        """Update elapsed time display every second."""
        if self._start_time is None:
            return
        import time
        elapsed = int(time.time() - self._start_time)
        mins, secs = divmod(elapsed, 60)
        hours, mins = divmod(mins, 60)
        if hours:
            text = f"{hours}:{mins:02d}:{secs:02d}"
        else:
            text = f"{mins}:{secs:02d}"
        try:
            self.query_one("#elapsed-value", Label).update(text)
        except Exception:
            pass
    
    def action_quit_automation(self) -> None:
        self._running = False
        self._should_exit = True
        try:
            self.write_log("[yellow]Stopping...[/]")
        except Exception:
            pass
    
    async def _send_session_summary(self, reason: str) -> None:
        """Send session summary to Discord webhook."""
        from utils.notifications import notify_session_end, is_notifications_enabled
        if not is_notifications_enabled():
            return
        
        elapsed_text = "Unknown"
        if self._start_time:
            import time
            elapsed = int(time.time() - self._start_time)
            mins, secs = divmod(elapsed, 60)
            hours, mins = divmod(mins, 60)
            elapsed_text = f"{hours}h {mins}m {secs}s" if hours else f"{mins}m {secs}s"
        
        await notify_session_end(
            service=self.app.selected_service,
            sent_count=self._successful,
            attempts=self._total_attempts,
            elapsed_time=elapsed_text,
            reason=reason,
        )
    
    def write_log(self, message: str) -> None:
        self.query_one("#output-log", RichLog).write(message)
    
    def set_state(self, state: str) -> None:
        self.query_one("#state-value", Label).update(state)
    
    def update_timer_display(self, seconds: int) -> None:
        if seconds > 0:
            mins, secs = divmod(seconds, 60)
            text = f"{mins}m {secs}s" if mins else f"{secs}s"
        else:
            text = "--"
        self.query_one("#timer-value", Label).update(text)
    
    def update_sent(self) -> None:
        self.query_one("#sent-value", Label).update(str(self._successful))
    
    def update_attempts(self) -> None:
        self.query_one("#attempts-value", Label).update(str(self._total_attempts))
    
    @work(exclusive=True)
    async def run_automation(self) -> None:
        """Run the full automation workflow."""
        from browser.automation import create_automation
        from utils.health_check import check_site_status
        from utils.config import get_config
        
        # Load config
        config = get_config()
        
        self._running = True
        self._successful = 0
        self._total_attempts = 0
        
        try:
            # Check site
            self.write_log("[cyan]Checking zefoy.com status...[/]")
            is_up, message = check_site_status()
            if not is_up:
                self.write_log(f"[red]{message}[/]")
                self.set_state("Site Down")
                return
            self.write_log("[green]zefoy.com is UP[/]")
            
            # Launch browser
            self.set_state("Launching browser...")
            self.write_log("[cyan]Starting browser...[/]")
            
            # Use config settings
            proxy = config.automation.proxy_url if config.automation.proxy_url else None
            
            async with create_automation(
                headless=config.automation.headless_mode,
                verbose=config.automation.debug_mode,
                proxy=proxy,
            ) as automation:
                # Start the browser and navigate
                await automation.start()
                
                # Handle popups
                self.set_state("Handling popups...")
                self.write_log("[cyan]Dismissing popups...[/]")
                await automation.popup_handlers.handle_all_popups()
                
                # CAPTCHA - check if we're NOT on main page (meaning CAPTCHA is present)
                if not await automation.is_on_main_page():
                    captcha_attempts = config.automation.captcha_max_attempts
                    self.set_state("CAPTCHA detected")
                    self.write_log(f"[yellow]CAPTCHA detected - auto-solving (up to {captcha_attempts} tries)...[/]")
                    
                    # Create progress callback for CAPTCHA attempts
                    async def captcha_progress(attempt: int, max_attempts: int, status: str):
                        self.set_state(f"CAPTCHA try {attempt}/{max_attempts}")
                        if status == "trying":
                            self.write_log(f"[dim]CAPTCHA attempt {attempt}/{max_attempts}...[/]")
                    
                    result = await automation.solve_captcha_auto(
                        max_attempts=captcha_attempts, 
                        progress_callback=captcha_progress
                    )
                    if result == "solved":
                        self.write_log("[green]CAPTCHA solved![/]")
                    else:
                        self.write_log("[yellow]Auto-solve failed - solve manually[/]")
                        self.set_state("Waiting for CAPTCHA...")
                        await automation.solve_captcha_manual()
                        self.write_log("[green]CAPTCHA solved![/]")
                
                # Detect services
                self.set_state("Detecting services...")
                await automation.detect_available_services()
                
                # Check service availability
                service_key = self.app.selected_service
                if not automation._available_services.get(service_key, False):
                    self.write_log(f"[red]{service_key} unavailable[/]")
                    self.set_state("Service unavailable")
                    return
                
                self.write_log(f"[green]Using {service_key.capitalize()}[/]")
                
                # Run loop - continuous until user quits
                video_url = self.app.video_url
                
                # Import ban detection and notifications
                from utils.timer import is_likely_ban
                from utils.notifications import (
                    notify_milestone, notify_ban_detected, is_notifications_enabled
                )
                
                while self._running:
                    self._total_attempts += 1
                    self.update_attempts()
                    self.write_log(f"[cyan]--- Attempt {self._total_attempts} ---[/]")
                    self.set_state(f"Attempt {self._total_attempts}")
                    
                    result = await automation.send_service(service_key, video_url)
                    
                    if result["success"]:
                        self._successful += 1
                        self.update_sent()
                        self.write_log(f"[green]✓ Sent! Total: {self._successful}[/]")
                        
                        # Check for milestone notifications
                        if is_notifications_enabled():
                            await notify_milestone(self._successful, service_key, video_url)
                        
                        # Calculate wait time
                        retry_delay = config.automation.auto_retry_delay
                        base_wait = result.get("wait_time", 180) + retry_delay
                        
                        # Safe mode: enforce minimum 15 min between sends
                        if config.automation.safe_mode:
                            safe_delay = config.automation.safe_mode_delay
                            if base_wait < safe_delay:
                                self.write_log(f"[cyan]Safe mode: waiting {safe_delay}s (15 min)[/]")
                                wait_time = safe_delay
                            else:
                                wait_time = base_wait
                        else:
                            wait_time = base_wait
                        
                        self.write_log(f"[dim]Waiting {wait_time}s...[/]")
                        self.set_state("Waiting")
                        for remaining in range(wait_time, 0, -1):
                            if not self._running:
                                break
                            self.update_timer_display(remaining)
                            await asyncio.sleep(1)
                        self.update_timer_display(0)
                    elif result["wait_time"] > 0:
                        wait_time = result["wait_time"]
                        
                        # Check for ban (24h+ rate limit)
                        if is_likely_ban(wait_time):
                            hours = wait_time // 3600
                            self._banned = True
                            self._running = False
                            self.write_log(f"[red bold]⚠️ BAN DETECTED: {hours}h+ rate limit![/]")
                            self.write_log("[red]This indicates a likely IP/account ban.[/]")
                            self.set_state("BANNED")
                            
                            # Send ban notification
                            if is_notifications_enabled():
                                await notify_ban_detected(wait_time, service_key)
                            
                            # Send session summary with ban reason
                            await self._send_session_summary("Ban detected")
                            break
                        
                        retry_delay = config.automation.auto_retry_delay
                        wait_time += retry_delay
                        self.write_log(f"[yellow]Rate limited: {wait_time}s[/]")
                        self.set_state("Rate limited")
                        
                        for remaining in range(wait_time, 0, -1):
                            if not self._running:
                                break
                            self.update_timer_display(remaining)
                            await asyncio.sleep(1)
                        self.update_timer_display(0)
                    else:
                        self.write_log(f"[red]{result['message']}[/]")
                
                if not self._banned:
                    self.write_log("[yellow]Stopped[/]")
                    self.set_state("Stopped")
                    # Send session summary for normal stop
                    await self._send_session_summary("User stopped")
        
        except Exception as e:
            try:
                self.write_log(f"[red]Error: {e}[/]")
                self.set_state("Error")
                # Send error notification
                from utils.notifications import notify_error, is_notifications_enabled
                if is_notifications_enabled():
                    await notify_error(str(e), self.app.selected_service)
                await self._send_session_summary(f"Error: {str(e)[:50]}")
            except Exception:
                pass  # App is exiting
        
        finally:
            self._running = False
            if self._should_exit:
                # Give a small delay for cleanup messages
                await asyncio.sleep(0.1)
                self.app.exit()
            else:
                try:
                    self.write_log("[dim]Press Q to quit[/]")
                except Exception:
                    pass  # App is exiting


class ZefoyTUI(App):
    """Zefoy TUI Application."""
    
    TITLE = "Zefoy TUI"
    ENABLE_COMMAND_PALETTE = False
    
    CSS = """
    Screen {
        background: $surface;
    }
    """
    
    SCREENS = {
        "welcome": WelcomeScreen,
        "settings": SettingsScreen,
        "service": ServiceScreen,
        "running": RunningScreen,
    }
    
    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit", show=False),
    ]
    
    def __init__(self) -> None:
        super().__init__()
        self.video_url: str = ""
        self.selected_service: str = ""
    
    def on_mount(self) -> None:
        self.push_screen("welcome")


def run_tui() -> None:
    """Run the TUI."""
    app = ZefoyTUI()
    app.run()


if __name__ == "__main__":
    run_tui()
