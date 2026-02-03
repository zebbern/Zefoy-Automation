#!/usr/bin/env python3
"""
Zefoy-CLI Auto-Installer

This script sets up everything needed to run the Zefoy automation tool:
1. Creates a virtual environment
2. Installs Python dependencies
3. Installs Playwright browsers
4. Sets up enchant dictionary (Windows)

Usage: python install.py
"""

import os
import platform
import subprocess
import sys
from pathlib import Path


# Minimum Python version required
MIN_PYTHON_VERSION = (3, 10)


def print_header(text: str) -> None:
    """Print a styled header."""
    print(f"\n{'=' * 60}")
    print(f"  {text}")
    print(f"{'=' * 60}")


def print_step(step: int, total: int, text: str) -> None:
    """Print a step indicator."""
    print(f"\n[{step}/{total}] {text}")
    print("-" * 40)


def print_success(text: str) -> None:
    """Print success message in green."""
    print(f"  ✓ {text}")


def print_error(text: str) -> None:
    """Print error message in red."""
    print(f"  ✗ {text}")


def print_warning(text: str) -> None:
    """Print warning message in yellow."""
    print(f"  ⚠ {text}")


def check_python_version() -> bool:
    """Check if Python version meets minimum requirements."""
    current = sys.version_info[:2]
    if current < MIN_PYTHON_VERSION:
        print_error(f"Python {MIN_PYTHON_VERSION[0]}.{MIN_PYTHON_VERSION[1]}+ required.")
        print_error(f"Current version: {current[0]}.{current[1]}")
        return False
    print_success(f"Python {current[0]}.{current[1]} detected")
    return True


def get_venv_path() -> Path:
    """Get the virtual environment path."""
    return Path(__file__).parent / ".venv"


def get_python_executable() -> Path:
    """Get the Python executable path in the venv."""
    venv = get_venv_path()
    if platform.system() == "Windows":
        return venv / "Scripts" / "python.exe"
    return venv / "bin" / "python"


def get_pip_executable() -> Path:
    """Get the pip executable path in the venv."""
    venv = get_venv_path()
    if platform.system() == "Windows":
        return venv / "Scripts" / "pip.exe"
    return venv / "bin" / "pip"


def create_virtual_environment() -> bool:
    """Create virtual environment if it doesn't exist."""
    venv_path = get_venv_path()
    
    if venv_path.exists():
        print_success(f"Virtual environment already exists at: {venv_path}")
        return True
    
    print(f"  Creating virtual environment at: {venv_path}")
    try:
        subprocess.run(
            [sys.executable, "-m", "venv", str(venv_path)],
            check=True,
            capture_output=True,
            text=True
        )
        print_success("Virtual environment created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to create virtual environment: {e.stderr}")
        return False


def upgrade_pip() -> bool:
    """Upgrade pip to latest version."""
    pip_exe = get_pip_executable()
    python_exe = get_python_executable()
    
    try:
        subprocess.run(
            [str(python_exe), "-m", "pip", "install", "--upgrade", "pip"],
            check=True,
            capture_output=True,
            text=True
        )
        print_success("pip upgraded to latest version")
        return True
    except subprocess.CalledProcessError as e:
        print_warning(f"Failed to upgrade pip (continuing anyway): {e.stderr}")
        return True  # Non-fatal


def install_requirements() -> bool:
    """Install requirements from requirements.txt."""
    pip_exe = get_pip_executable()
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if not requirements_file.exists():
        print_error(f"requirements.txt not found at: {requirements_file}")
        return False
    
    print(f"  Installing dependencies from: requirements.txt")
    try:
        result = subprocess.run(
            [str(pip_exe), "install", "-r", str(requirements_file)],
            check=True,
            capture_output=True,
            text=True
        )
        print_success("All Python dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to install dependencies")
        print(f"    stderr: {e.stderr}")
        return False


def install_playwright_browsers() -> bool:
    """Install Playwright Chromium browser."""
    python_exe = get_python_executable()
    
    print("  Installing Playwright Chromium browser...")
    print("  (This may take a few minutes on first run)")
    
    try:
        result = subprocess.run(
            [str(python_exe), "-m", "playwright", "install", "chromium"],
            check=True,
            capture_output=True,
            text=True
        )
        print_success("Playwright Chromium browser installed")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to install Playwright browser: {e.stderr}")
        return False


def install_enchant_windows() -> bool:
    """Install enchant dictionary on Windows."""
    if platform.system() != "Windows":
        print_success("Enchant: No additional setup needed on Linux/macOS")
        return True
    
    print("  Checking enchant dictionary for Windows...")
    
    # pyenchant on Windows needs the enchant library
    # It's typically bundled, but we'll verify it works
    python_exe = get_python_executable()
    
    test_code = '''
import sys
try:
    import enchant
    d = enchant.Dict("en_US")
    print("OK")
    sys.exit(0)
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
'''
    
    try:
        result = subprocess.run(
            [str(python_exe), "-c", test_code],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print_success("Enchant dictionary is working")
            return True
        else:
            print_warning(f"Enchant test failed: {result.stdout.strip()}")
            print_warning("Spell correction may not work, but the tool will still function")
            print_warning("To fix on Windows, try: pip install pyenchant")
            return True  # Non-fatal
    except Exception as e:
        print_warning(f"Could not verify enchant: {e}")
        return True  # Non-fatal


def print_usage_instructions() -> None:
    """Print usage instructions after successful installation."""
    venv = get_venv_path()
    
    print_header("Installation Complete!")
    
    print("\n📋 USAGE INSTRUCTIONS:")
    print("=" * 40)
    
    if platform.system() == "Windows":
        activate_cmd = f".venv\\Scripts\\activate"
        python_cmd = f".venv\\Scripts\\python.exe"
    else:
        activate_cmd = f"source .venv/bin/activate"
        python_cmd = f".venv/bin/python"
    
    print(f"""
1. Activate the virtual environment:
   {activate_cmd}

2. Run the automation:
   python main.py --help

3. Example usage:
   python main.py hearts --count 10 "https://tiktok.com/..."
   python main.py hearts --auto-captcha "https://tiktok.com/..."

Alternatively, run without activating:
   {python_cmd} main.py --help
""")
    
    print("=" * 40)
    print("✅ Setup complete! Happy automating!")
    print("=" * 40)


def main() -> int:
    """Main installation routine."""
    print_header("Zefoy-CLI Auto-Installer")
    print(f"Platform: {platform.system()} {platform.machine()}")
    print(f"Python: {sys.version}")
    
    total_steps = 6
    current_step = 0
    
    # Step 1: Check Python version
    current_step += 1
    print_step(current_step, total_steps, "Checking Python version...")
    if not check_python_version():
        return 1
    
    # Step 2: Create virtual environment
    current_step += 1
    print_step(current_step, total_steps, "Setting up virtual environment...")
    if not create_virtual_environment():
        return 1
    
    # Step 3: Upgrade pip
    current_step += 1
    print_step(current_step, total_steps, "Upgrading pip...")
    upgrade_pip()  # Non-fatal if fails
    
    # Step 4: Install requirements
    current_step += 1
    print_step(current_step, total_steps, "Installing Python dependencies...")
    if not install_requirements():
        return 1
    
    # Step 5: Install Playwright browsers
    current_step += 1
    print_step(current_step, total_steps, "Installing Playwright browser...")
    if not install_playwright_browsers():
        return 1
    
    # Step 6: Setup enchant (Windows)
    current_step += 1
    print_step(current_step, total_steps, "Configuring spell-check dictionary...")
    install_enchant_windows()  # Non-fatal if fails
    
    # Success!
    print_usage_instructions()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nInstallation cancelled by user.")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)
