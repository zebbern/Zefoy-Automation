"""
Automatic ChromeDriver installer
Downloads and installs the correct ChromeDriver for your Chrome version
"""

import os
import sys
import zipfile
import requests
import platform
import subprocess
from pathlib import Path


def get_chrome_version():
    """Get installed Chrome version"""
    try:
        if platform.system() == "Windows":
            # Try Chrome stable
            cmd = r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version'
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                version = result.stdout.split()[-1]
                return version
        elif platform.system() == "Darwin":  # macOS
            cmd = "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version"
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            return result.stdout.split()[-1]
        else:  # Linux
            cmd = "google-chrome --version"
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            return result.stdout.split()[-1]
    except:
        return None


def download_chromedriver(version, dest_dir):
    """Download ChromeDriver for the specified version"""
    major_version = version.split('.')[0]
    system = platform.system()
    
    if system == "Windows":
        platform_name = "win64" if platform.machine().endswith('64') else "win32"
        ext = ".zip"
    elif system == "Darwin":
        platform_name = "mac-x64" if platform.machine() == "x86_64" else "mac-arm64"
        ext = ".zip"
    else:
        platform_name = "linux64"
        ext = ".zip"
    
    # Chrome for Testing JSON API
    url = f"https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_{major_version}"
    
    try:
        response = requests.get(url)
        exact_version = response.text.strip()
        
        download_url = f"https://storage.googleapis.com/chrome-for-testing-public/{exact_version}/{platform_name}/chromedriver-{platform_name}.zip"
        
        print(f"Downloading ChromeDriver {exact_version} for {platform_name}...")
        response = requests.get(download_url, stream=True)
        response.raise_for_status()
        
        zip_path = dest_dir / f"chromedriver{ext}"
        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Extracting...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(dest_dir)
        
        os.remove(zip_path)
        
        # Find the chromedriver executable
        for root, dirs, files in os.walk(dest_dir):
            for file in files:
                if file.startswith('chromedriver'):
                    driver_path = Path(root) / file
                    if system != "Windows":
                        os.chmod(driver_path, 0o755)
                    return driver_path
        
        return None
    except Exception as e:
        print(f"Error downloading ChromeDriver: {e}")
        return None


def main():
    print("="*60)
    print("  ChromeDriver Auto-Installer")
    print("="*60)
    
    chrome_version = get_chrome_version()
    if not chrome_version:
        print("\n❌ Could not detect Chrome version.")
        print("Please install Google Chrome first:")
        print("  https://www.google.com/chrome/")
        return False
    
    print(f"\n✓ Detected Chrome version: {chrome_version}")
    
    # Create drivers directory
    drivers_dir = Path.home() / ".zefoy_drivers"
    drivers_dir.mkdir(exist_ok=True)
    
    driver_path = download_chromedriver(chrome_version, drivers_dir)
    
    if driver_path and driver_path.exists():
        print(f"\n✓ ChromeDriver installed successfully!")
        print(f"  Location: {driver_path}")
        
        # Add to PATH temporarily
        os.environ['PATH'] = str(drivers_dir) + os.pathsep + os.environ['PATH']
        
        print(f"\n✓ Added to PATH for this session")
        print(f"\nTo make it permanent, add this to your PATH:")
        print(f"  {drivers_dir}")
        
        return True
    else:
        print(f"\n❌ Failed to install ChromeDriver")
        print(f"\nPlease install manually:")
        print(f"  1. Go to: https://googlechromelabs.github.io/chrome-for-testing/")
        print(f"  2. Download ChromeDriver for your Chrome version")
        print(f"  3. Extract and add to your PATH")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
