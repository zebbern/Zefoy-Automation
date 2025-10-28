#!/usr/bin/env python3
"""
Zefoy Automation Bot - Main Launcher
Auto-setup and run the bot with one command

Usage: python main.py
"""

import sys
import subprocess
import os
import venv
from pathlib import Path

# ANSI color codes
class Color:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def clear_screen():
    """Clear console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner():
    """Display welcome banner"""
    banner = f"""
{Color.CYAN}{'='*60}
{Color.BOLD}{Color.MAGENTA}  ⚡ ZEFOY AUTOMATION BOT v2.0.0 ⚡{Color.RESET}
{Color.CYAN}{'='*60}{Color.RESET}

{Color.YELLOW}  🤖 Automated TikTok engagement via Zefoy.com{Color.RESET}
{Color.YELLOW}  📦 Clean Architecture Edition{Color.RESET}
{Color.YELLOW}  👨‍💻 Made by github.com/zebbern{Color.RESET}

{Color.CYAN}{'='*60}{Color.RESET}
"""
    print(banner)


def check_python_version():
    """Check if Python version is compatible"""
    print(f"{Color.YELLOW}[~] Checking Python version...{Color.RESET}")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 6):
        print(f"{Color.RED}[!] Python 3.6 or higher is required!{Color.RESET}")
        print(f"{Color.RED}[!] Current version: {sys.version}{Color.RESET}")
        return False
    
    print(f"{Color.GREEN}[✓] Python {version.major}.{version.minor}.{version.micro} detected{Color.RESET}")
    return True


def setup_virtual_environment():
    """Create and setup virtual environment if it doesn't exist"""
    venv_path = Path(__file__).parent / "venv"
    
    if venv_path.exists():
        print(f"{Color.GREEN}[✓] Virtual environment already exists{Color.RESET}")
        return venv_path
    
    print(f"\n{Color.CYAN}{'='*60}{Color.RESET}")
    print(f"{Color.YELLOW}[~] Creating virtual environment...{Color.RESET}")
    print(f"{Color.YELLOW}[~] This is a one-time setup{Color.RESET}")
    print(f"{Color.CYAN}{'='*60}{Color.RESET}\n")
    
    try:
        # Create virtual environment
        venv.create(venv_path, with_pip=True)
        print(f"{Color.GREEN}[✓] Virtual environment created at: {venv_path}{Color.RESET}")
        return venv_path
    except Exception as e:
        print(f"{Color.RED}[!] Failed to create virtual environment: {e}{Color.RESET}")
        return None


def get_venv_python(venv_path):
    """Get the Python executable path from virtual environment"""
    if os.name == 'nt':  # Windows
        return venv_path / "Scripts" / "python.exe"
    else:  # Unix/macOS
        return venv_path / "bin" / "python"


def check_requirements(python_exe):
    """Check if required packages are installed in venv"""
    print(f"\n{Color.YELLOW}[~] Checking dependencies...{Color.RESET}")
    
    # Map package names to their import names
    required_packages = {
        'selenium': 'selenium',
        'colorama': 'colorama',
        'webdriver-manager': 'webdriver_manager',
        'requests': 'requests',
        'python-dotenv': 'dotenv',
        'rich': 'rich'
    }
    
    missing_packages = []
    
    for package_name, import_name in required_packages.items():
        try:
            # Check if package is installed in venv
            result = subprocess.run(
                [str(python_exe), "-c", f"import {import_name}"],
                capture_output=True,
                timeout=5
            )
            if result.returncode != 0:
                missing_packages.append(package_name)
        except:
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"{Color.YELLOW}[!] Missing packages detected: {', '.join(missing_packages)}{Color.RESET}")
        return False
    
    print(f"{Color.GREEN}[✓] All dependencies installed{Color.RESET}")
    return True


def install_requirements(python_exe):
    """Install required packages from requirements.txt into venv"""
    print(f"\n{Color.CYAN}{'='*60}{Color.RESET}")
    print(f"{Color.YELLOW}[~] Installing dependencies into virtual environment...{Color.RESET}")
    print(f"{Color.YELLOW}[~] This may take a minute (one-time setup)...{Color.RESET}")
    print(f"{Color.CYAN}{'='*60}{Color.RESET}\n")
    
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if not requirements_file.exists():
        print(f"{Color.RED}[!] requirements.txt not found!{Color.RESET}")
        return False
    
    try:
        subprocess.check_call([
            str(python_exe),
            "-m",
            "pip",
            "install",
            "-r",
            str(requirements_file),
            "--quiet"
        ])
        print(f"\n{Color.GREEN}[✓] Dependencies installed successfully!{Color.RESET}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n{Color.RED}[!] Failed to install dependencies: {e}{Color.RESET}")
        return False


def run_bot(python_exe=None):
    """Run the main bot"""
    print(f"\n{Color.CYAN}{'='*60}{Color.RESET}")
    print(f"{Color.GREEN}[✓] Starting bot...{Color.RESET}")
    print(f"{Color.CYAN}{'='*60}{Color.RESET}\n")
    
    try:
        # If python_exe provided, run in venv context
        if python_exe:
            result = subprocess.run(
                [str(python_exe), "-c", "from src.bot import main; main()"],
                cwd=Path(__file__).parent
            )
            sys.exit(result.returncode)
        else:
            from src.bot import main
            main()
    except Exception as e:
        error_str = str(e)
        
        # Check if it's a ChromeDriver error
        if 'chromedriver' in error_str.lower() or 'driver' in error_str.lower():
            print(f"\n{Color.RED}[!] ChromeDriver not found or incompatible{Color.RESET}")
            print(f"\n{Color.YELLOW}[?] Would you like to auto-install ChromeDriver? (y/n): {Color.RESET}", end='')
            choice = input().strip().lower()
            
            if choice in ['y', 'yes']:
                print(f"\n{Color.CYAN}{'='*60}{Color.RESET}")
                print(f"{Color.YELLOW}[~] Installing ChromeDriver...{Color.RESET}")
                print(f"{Color.CYAN}{'='*60}{Color.RESET}\n")
                
                try:
                    # Run the installer
                    result = subprocess.run([sys.executable, "install_chromedriver.py"], 
                                          capture_output=False)
                    
                    if result.returncode == 0:
                        print(f"\n{Color.GREEN}[✓] ChromeDriver installed! Please run the script again.{Color.RESET}")
                    else:
                        print(f"\n{Color.RED}[!] ChromeDriver installation failed.{Color.RESET}")
                        print(f"{Color.YELLOW}[!] Please install manually or run: chromedriveinstall.bat{Color.RESET}")
                except Exception as install_error:
                    print(f"\n{Color.RED}[!] Installation error: {install_error}{Color.RESET}")
            else:
                print(f"\n{Color.YELLOW}[!] Please install ChromeDriver manually:{Color.RESET}")
                print(f"{Color.YELLOW}    - Run: python install_chromedriver.py{Color.RESET}")
                print(f"{Color.YELLOW}    - Or: chromedriveinstall.bat (Windows){Color.RESET}")
        else:
            print(f"\n{Color.RED}[!] Error running bot: {e}{Color.RESET}")
            print(f"{Color.YELLOW}[!] Check zefoy_bot.log for details{Color.RESET}")
        
        sys.exit(1)


def main():
    """Main entry point with auto-setup"""
    try:
        clear_screen()
        print_banner()
        
        # Step 1: Check Python version
        if not check_python_version():
            input(f"\n{Color.YELLOW}Press Enter to exit...{Color.RESET}")
            sys.exit(1)
        
        # Step 2: Setup virtual environment
        venv_path = setup_virtual_environment()
        if not venv_path:
            print(f"\n{Color.RED}[!] Failed to setup virtual environment{Color.RESET}")
            input(f"\n{Color.YELLOW}Press Enter to exit...{Color.RESET}")
            sys.exit(1)
        
        # Get venv Python executable
        python_exe = get_venv_python(venv_path)
        if not python_exe.exists():
            print(f"{Color.RED}[!] Virtual environment Python not found{Color.RESET}")
            sys.exit(1)
        
        # Step 3: Check dependencies in venv
        deps_installed = check_requirements(python_exe)
        
        if not deps_installed:
            print(f"\n{Color.YELLOW}[?] Would you like to install missing dependencies? (y/n): {Color.RESET}", end='')
            choice = input().strip().lower()
            
            if choice in ['y', 'yes']:
                if not install_requirements(python_exe):
                    print(f"\n{Color.RED}[!] Setup failed. Please install dependencies manually:{Color.RESET}")
                    print(f"{Color.YELLOW}    .\\venv\\Scripts\\activate  # Windows{Color.RESET}")
                    print(f"{Color.YELLOW}    pip install -r requirements.txt{Color.RESET}")
                    input(f"\n{Color.YELLOW}Press Enter to exit...{Color.RESET}")
                    sys.exit(1)
            else:
                print(f"\n{Color.RED}[!] Cannot run without dependencies installed.{Color.RESET}")
                print(f"{Color.YELLOW}[!] Activate venv and install manually{Color.RESET}")
                input(f"\n{Color.YELLOW}Press Enter to exit...{Color.RESET}")
                sys.exit(1)
        
        # Step 4: Run the bot using venv Python
        run_bot(python_exe)
    
    except KeyboardInterrupt:
        print(f"\n\n{Color.YELLOW}[!] Interrupted by user{Color.RESET}")
        sys.exit(0)


if __name__ == "__main__":
    main()
