"""Health check utilities for zefoy.com."""
import urllib.request
import urllib.error
from typing import Tuple


def check_site_status(url: str = "https://zefoy.com", timeout: int = 10) -> Tuple[bool, str]:
    """
    Check if zefoy.com is accessible.
    
    Args:
        url: The URL to check
        timeout: Request timeout in seconds
    
    Returns:
        Tuple of (is_up: bool, status_message: str)
    """
    try:
        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        )
        response = urllib.request.urlopen(request, timeout=timeout)
        status_code = response.getcode()
        
        if status_code == 200:
            return True, f"✅ zefoy.com is UP (HTTP {status_code})"
        else:
            return False, f"⚠️ zefoy.com returned HTTP {status_code}"
            
    except urllib.error.HTTPError as e:
        if e.code == 502:
            return False, f"❌ zefoy.com is DOWN (502 Bad Gateway - Server Error)"
        elif e.code == 503:
            return False, f"❌ zefoy.com is DOWN (503 Service Unavailable)"
        elif e.code == 520:
            return False, f"❌ zefoy.com is DOWN (520 Cloudflare Error)"
        else:
            return False, f"❌ zefoy.com returned HTTP {e.code}: {e.reason}"
            
    except urllib.error.URLError as e:
        return False, f"❌ Cannot reach zefoy.com: {e.reason}"
        
    except TimeoutError:
        return False, f"❌ zefoy.com timed out after {timeout}s"
        
    except Exception as e:
        return False, f"❌ Error checking zefoy.com: {str(e)}"


def print_status():
    """Print the current status of zefoy.com."""
    is_up, message = check_site_status()
    print(message)
    return is_up
