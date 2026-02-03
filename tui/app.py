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
    Header,
    Input,
    Label,
    ListItem,
    ListView,
    ProgressBar,
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
    """
    
    BINDINGS = [
        Binding("escape", "quit", "Quit"),
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
                Button("Continue", id="start-btn", variant="primary"),
                id="welcome-box",
            ),
            id="welcome-container",
        )
    
    def action_quit(self) -> None:
        self.app.exit()
    
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
            
            async with create_automation(headless=True, verbose=False) as automation:
                # Start the browser and navigate
                await automation.start()
                
                # Handle popups
                self.set_state("Handling popups...")
                self.write_log("[cyan]Dismissing popups...[/]")
                await automation.popup_handlers.handle_all_popups()
                
                # CAPTCHA - check if we're NOT on main page (meaning CAPTCHA is present)
                if not await automation.is_on_main_page():
                    self.set_state("CAPTCHA detected")
                    self.write_log("[yellow]CAPTCHA detected - auto-solving...[/]")
                    
                    result = await automation.solve_captcha_auto()
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
                        
                        # Wait after success before next attempt
                        wait_time = result.get("wait_time", 180) + 3
                        self.write_log(f"[dim]Waiting {wait_time}s...[/]")
                        self.set_state("Waiting")
                        for remaining in range(wait_time, 0, -1):
                            if not self._running:
                                break
                            self.update_timer_display(remaining)
                            await asyncio.sleep(1)
                        self.update_timer_display(0)
                    elif result["wait_time"] > 0:
                        wait_time = result["wait_time"] + 3
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
                
                self.write_log("[yellow]Stopped[/]")
                self.set_state("Stopped")
        
        except Exception as e:
            try:
                self.write_log(f"[red]Error: {e}[/]")
                self.set_state("Error")
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
