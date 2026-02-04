"""
Zefoy-CLI Automation - CLI Entry Point
=======================================

Automate TikTok interactions via Zefoy with ease.

Author: zebbern (https://github.com/zebbern)
Repository: https://github.com/zebbern/Zefoy-Automation
License: MIT
Copyright (c) 2024 zebbern
"""
import argparse
import asyncio
import sys
import warnings
from browser.automation import ZefoyAutomation, SERVICES, create_automation
from utils.timer import wait_with_progress
from utils.health_check import check_site_status
from utils.colors import success, error, warning, info, dim, bold, Colors
from utils.livecounts import LivecountsAPI, VideoStats

# Suppress asyncio cleanup warnings
warnings.filterwarnings("ignore", category=ResourceWarning)
warnings.filterwarnings("ignore", message=".*unclosed transport.*")


def print_header_box(service: str, url: str, count: int, auto_wait: bool, stats: VideoStats | None = None) -> None:
    """Print a nice header with optional video stats."""
    print()
    print(f"{Colors.BRIGHT_CYAN}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.BRIGHT_CYAN}|{Colors.RESET}{'ZEFOY CLI AUTOMATION':^58}{Colors.BRIGHT_CYAN}|{Colors.RESET}")
    print(f"{Colors.BRIGHT_CYAN}{'=' * 60}{Colors.RESET}")
    print(f"  {dim('Service:')}   {bold(service.capitalize())}")
    print(f"  {dim('Target:')}    {bold(str(count))} successful send(s)")
    print(f"  {dim('Auto-wait:')} {success('Yes') if auto_wait else error('No')}")
    print(f"{Colors.BRIGHT_CYAN}{'-' * 60}{Colors.RESET}")
    print(f"  {dim('Video:')} {info(url)}")
    
    # Show video stats if available
    if stats and stats.success:
        print(f"{Colors.BRIGHT_CYAN}{'-' * 60}{Colors.RESET}")
        print(f"  {bold('📊 Current Stats:')}")
        print(f"    👁️  Views:    {Colors.BRIGHT_WHITE}{stats.views:,}{Colors.RESET}")
        print(f"    ❤️  Likes:    {Colors.BRIGHT_WHITE}{stats.likes:,}{Colors.RESET}")
        print(f"    💬 Comments: {Colors.BRIGHT_WHITE}{stats.comments:,}{Colors.RESET}")
        print(f"    🔁 Shares:   {Colors.BRIGHT_WHITE}{stats.shares:,}{Colors.RESET}")
    elif stats and not stats.success:
        print(f"{Colors.BRIGHT_CYAN}{'-' * 60}{Colors.RESET}")
        print(f"  {dim('Stats:')} {warning(f'Could not fetch ({stats.error})')}")
    
    print(f"{Colors.BRIGHT_CYAN}{'=' * 60}{Colors.RESET}")
    print()


def print_section(title: str) -> None:
    """Print a section header."""
    print(f"\n{Colors.BRIGHT_CYAN}> {Colors.BOLD}{title}{Colors.RESET}")


def print_attempt_header(attempt: int, successful: int, total: int) -> None:
    """Print attempt header."""
    progress = f"{successful}/{total}"
    print(f"\n{Colors.BRIGHT_BLUE}{'-' * 50}{Colors.RESET}")
    print(f"  {bold('Attempt')} {attempt}  |  {dim('Progress:')} {info(progress)}")
    print(f"{Colors.BRIGHT_BLUE}{'-' * 50}{Colors.RESET}")


def format_time(seconds: int) -> str:
    """Format seconds as Xm Ys."""
    mins = seconds // 60
    secs = seconds % 60
    if mins > 0:
        return f"{mins}m {secs}s"
    return f"{secs}s"


def print_stats_comparison(before: VideoStats, after: VideoStats) -> None:
    """Print before/after stats comparison."""
    if not before.success or not after.success:
        return
    
    views_delta = after.views - before.views
    likes_delta = after.likes - before.likes
    comments_delta = after.comments - before.comments
    shares_delta = after.shares - before.shares
    
    def format_delta(value: int) -> str:
        if value > 0:
            return f"{Colors.BRIGHT_GREEN}+{value:,}{Colors.RESET}"
        elif value < 0:
            return f"{Colors.BRIGHT_RED}{value:,}{Colors.RESET}"
        return f"{Colors.DIM}0{Colors.RESET}"
    
    print(f"\n{Colors.BRIGHT_MAGENTA}{'=' * 50}{Colors.RESET}")
    print(f"  {bold('📊 STATS COMPARISON')}")
    print(f"{Colors.BRIGHT_MAGENTA}{'-' * 50}{Colors.RESET}")
    print(f"               {'Before':>12}  →  {'After':>12}   {'Change':>10}")
    print(f"  👁️  Views:   {before.views:>12,}  →  {after.views:>12,}   {format_delta(views_delta)}")
    print(f"  ❤️  Likes:   {before.likes:>12,}  →  {after.likes:>12,}   {format_delta(likes_delta)}")
    print(f"  💬 Comments:{before.comments:>12,}  →  {after.comments:>12,}   {format_delta(comments_delta)}")
    print(f"  🔁 Shares:  {before.shares:>12,}  →  {after.shares:>12,}   {format_delta(shares_delta)}")
    print(f"{Colors.BRIGHT_MAGENTA}{'=' * 50}{Colors.RESET}")


def fetch_video_stats(url: str) -> VideoStats | None:
    """Fetch video stats from livecounts.io."""
    try:
        api = LivecountsAPI()
        return api.get_video_stats(url)
    except Exception:
        return None


async def clear_cookies_standalone() -> None:
    """Clear Playwright browser cookies for zefoy.com."""
    from playwright.async_api import async_playwright
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        # Navigate to set up cookies
        page = await context.new_page()
        try:
            await page.goto("https://zefoy.com", timeout=10000)
        except Exception:
            pass
        # Clear all cookies
        await context.clear_cookies()
        await browser.close()


async def select_service_interactive(automation: ZefoyAutomation) -> str | None:
    """Let user select from available services.
    
    Shows service status with numbers inline, user picks by number.
    """
    # Detect and display services with inline selection
    print_section("Service Status")
    await automation.detect_available_services()
    automation.print_service_status_with_selection()
    
    count = automation.get_selection_count()
    
    if count == 0:
        print(f"\n  {error('No services are currently available!')}")
        return None
    
    while True:
        try:
            prompt = f"\n  {dim(f'Select service (1-{count}):')} "
            choice = input(prompt).strip()
            if not choice:
                continue
            idx = int(choice)
            service = automation.get_service_by_selection(idx)
            if service:
                service_name = SERVICES[service]["name"]
                print(f"  {success(f'Selected: {service_name}')}")
                return service
            print(f"  {error('Invalid choice. Try again.')}")
        except ValueError:
            print(f"  {error('Please enter a number.')}")
        except KeyboardInterrupt:
            return None


async def run_automation(
    video_url: str,
    service: str | None = None,
    headless: bool = False,
    loop_count: int = 1,
    auto_wait: bool = True,
    verbose: bool = False,
    interactive: bool = False,
    auto_captcha: bool = False,
    proxy: str | None = None,
    initial_stats: VideoStats | None = None
) -> None:
    """Run automation for the specified service."""
    # Use provided initial stats or fetch new ones
    before_stats = initial_stats
    if before_stats is None:
        print_section("Fetching Video Stats")
        before_stats = fetch_video_stats(video_url)
        if before_stats and before_stats.success:
            print(f"  {success('Stats retrieved from livecounts.io')}")
        else:
            print(f"  {warning('Could not fetch stats (will skip comparison)')}")
    
    # Check if site is up first
    print_section("Checking Site Status")
    is_up, message = check_site_status()
    
    if is_up:
        print(f"  {success('zefoy.com is UP')}")
    else:
        print(f"  {error(message)}")
        print(f"\n  {warning('Site is down. Please try again later.')}")
        return
    
    # Use context manager for proper cleanup
    async with create_automation(headless=headless, verbose=verbose, proxy=proxy) as automation:
        print_section("Starting Browser")
        if proxy:
            print(f"  {info('Using proxy:')} {dim(proxy)}")
        await automation.start()
        
        print(f"  {dim('Handling popups...')}")
        await automation.handle_initial_setup()
        
        # CAPTCHA handling
        print(f"\n{Colors.BRIGHT_YELLOW}{'=' * 50}{Colors.RESET}")
        print(f"  {warning('CAPTCHA REQUIRED')}")
        print(f"{Colors.BRIGHT_YELLOW}{'=' * 50}{Colors.RESET}")
        
        if auto_captcha:
            print(f"  {info('Attempting auto-solve using OCR...')}")
            print(f"{Colors.BRIGHT_YELLOW}{'=' * 50}{Colors.RESET}")
            captcha_result = await automation.solve_captcha_auto(max_attempts=5)
        else:
            print(f"  {dim('Solve the CAPTCHA in the browser window.')}")
            print(f"  {dim('The script will continue automatically.')}")
            print(f"{Colors.BRIGHT_YELLOW}{'=' * 50}{Colors.RESET}")
            captcha_result = await automation.solve_captcha_manual()
        if captcha_result == "timeout":
            print(f"\n  {error('CAPTCHA timeout. Exiting...')}")
            return
        
        print(f"\n  {success('CAPTCHA solved!')}")
        
        # Service selection
        if interactive or service is None:
            service = await select_service_interactive(automation)
            if service is None:
                print(f"\n  {warning('No service selected. Exiting...')}")
                return
        else:
            # Detect and verify requested service is available
            print_section("Service Status")
            await automation.detect_available_services()
            automation.print_service_status_with_selection()
            
            if not automation._available_services.get(service, False):
                print(f"\n  {error(f'Service \"{service}\" is not available!')}")
                return
        
        service_name = SERVICES[service]["name"]
        print_section(f"Starting {service_name} Automation")
        
        successful_sends = 0
        attempt = 0
        
        while successful_sends < loop_count:
            attempt += 1
            print_attempt_header(attempt, successful_sends, loop_count)
            
            print(f"  {dim('Opening service panel...')}")
            result = await automation.send_service(service, video_url)
            
            if result["success"]:
                successful_sends += 1
                print(f"\n  {success('SUCCESS!')} {result['message']}")
                print(f"  {info(f'Progress: {successful_sends}/{loop_count}')}")
                
                if successful_sends < loop_count:
                    wait_time = result.get("wait_time", 0)
                    if result.get("wait_time", 0) == 0:
                        wait_time = 180
                    wait_time += 3
                    
                    print(f"\n  {dim(f'Waiting {format_time(wait_time)} before next attempt...')}")
                    
                    async def progress(remaining: int) -> None:
                        print(f"\r  {dim(format_time(remaining) + ' remaining...')}   ", end="", flush=True)
                    
                    await wait_with_progress(wait_time, progress)
                    print()
            else:
                if result["wait_time"] > 0 and auto_wait:
                    wait_time = result["wait_time"] + 3
                    
                    # Check for massive ban (>24 hours / 86400 seconds)
                    if wait_time > 86400:
                        hours = wait_time // 3600
                        days = hours // 24
                        print(f"\n  {error(f'BANNED! Server returned a {days} day ({hours} hour) rate limit!')}")
                        print(f"  {warning('This usually means the video URL or IP is blocked.')}")
                        print(f"  {info('Try: 1) Different video URL  2) VPN/different IP  3) Wait it out')}")
                        return
                    
                    print(f"\n  {warning(f'Rate limited. Waiting {format_time(wait_time)}...')}")
                    
                    async def progress(remaining: int) -> None:
                        print(f"\r  {dim(format_time(remaining) + ' remaining...')}   ", end="", flush=True)
                    
                    await wait_with_progress(wait_time, progress)
                    print(f"\n  {info('Retrying...')}")
                else:
                    print(f"\n  {error(result['message'])}")
        
        print(f"\n{Colors.BRIGHT_GREEN}{'=' * 50}{Colors.RESET}")
        print(f"  {success(f'COMPLETE! {loop_count} successful send(s)')}")
        print(f"{Colors.BRIGHT_GREEN}{'=' * 50}{Colors.RESET}")
        
        # Fetch after stats and show comparison
        if before_stats and before_stats.success:
            print_section("Verifying Results")
            print(f"  {dim('Fetching updated stats...')}")
            # Small delay to let TikTok update their counts
            await asyncio.sleep(3)
            after_stats = fetch_video_stats(video_url)
            if after_stats and after_stats.success:
                print_stats_comparison(before_stats, after_stats)
            else:
                print(f"  {warning('Could not fetch updated stats')}")
        
        print()


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Zefoy CLI - Automate TikTok engagement services",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "https://vm.tiktok.com/..." -n 5      Send 5 times
  %(prog)s "https://vm.tiktok.com/..." -s hearts Use hearts service
  %(prog)s --check                                Check site status
        """
    )
    
    parser.add_argument(
        "url",
        nargs="?",
        help="TikTok video URL"
    )
    
    parser.add_argument(
        "-s", "--service",
        choices=["hearts", "favorites", "chearts"],
        default=None,
        help="Service to use (default: interactive selection)"
    )
    
    parser.add_argument(
        "-n", "--count",
        type=int,
        default=1,
        help="Number of successful sends (default: 1)"
    )
    
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run browser in headless mode"
    )
    
    parser.add_argument(
        "--auto-captcha",
        action="store_true",
        help="Attempt to auto-solve CAPTCHA using OCR"
    )
    
    parser.add_argument(
        "--no-wait",
        action="store_true",
        help="Don't auto-wait on rate limits"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show debug output"
    )
    
    parser.add_argument(
        "--check",
        action="store_true",
        help="Only check if zefoy.com is up"
    )
    
    parser.add_argument(
        "--clear-cookies",
        action="store_true",
        help="Clear Playwright browser cookies and exit"
    )
    
    parser.add_argument(
        "--proxy",
        type=str,
        default=None,
        help="Proxy server URL (e.g., http://user:pass@host:port)"
    )
    
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show version and exit"
    )
    
    parser.add_argument(
        "--about",
        action="store_true",
        help="Show credits and project info"
    )
    
    args = parser.parse_args()
    
    # Handle --about flag
    if args.about:
        from utils.credits import get_credits_full
        print(get_credits_full())
        sys.exit(0)
    
    # Handle --version flag
    if args.version:
        from utils.credits import get_version, get_author
        print(f"zefoy-cli v{get_version()} by @{get_author()}")
        sys.exit(0)
    
    # Handle --check flag
    if args.check:
        print(f"\n{dim('Checking zefoy.com status...')}")
        is_up, message = check_site_status()
        if is_up:
            print(f"  {success('zefoy.com is UP')}")
        else:
            print(f"  {error(message)}")
        sys.exit(0 if is_up else 1)
    
    # Handle --clear-cookies flag
    if args.clear_cookies:
        print(f"\n{dim('Clearing Playwright cookies...')}")
        asyncio.run(clear_cookies_standalone())
        print(f"  {success('Cookies cleared!')}")
        sys.exit(0)
    
    # URL is required if not using --check
    if not args.url:
        parser.error("URL is required (unless using --check or --version)")
    
    # Determine if interactive mode
    interactive = args.service is None
    service_display = args.service or "interactive"
    
    # Fetch initial stats for header display
    initial_stats = fetch_video_stats(args.url)
    
    print_header_box(service_display, args.url, args.count, not args.no_wait, initial_stats)
    
    try:
        asyncio.run(run_automation(
            args.url,
            service=args.service,
            headless=args.headless,
            loop_count=args.count,
            auto_wait=not args.no_wait,
            verbose=args.verbose,
            interactive=interactive,
            auto_captcha=args.auto_captcha,
            proxy=args.proxy,
            initial_stats=initial_stats
        ))
    except Exception as e:
        import traceback
        print(f"\n  {error('Error:')} {e}")
        if args.verbose:
            traceback.print_exc()


if __name__ == "__main__":
    main()
