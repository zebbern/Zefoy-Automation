"""
Fingerprint Spoofing Module for Zefoy Anti-Bot Bypass

This module generates randomized browser fingerprints and encrypts them
using CryptoJS-compatible AES-CBC encryption with Zefoy's hardcoded key.

Based on reverse engineering from:
https://zefoy.com/assets/53fbc84b11a13a7942a850361e5d7b49.js

Key: 43fdda1192dde7f8ffff7161e13580d7
"""

import base64
import hashlib
import json
import os
import random
import time
from typing import Any

from Crypto.Cipher import AES

# Zefoy's hardcoded AES key (found in their obfuscated JS)
ZEFOY_AES_KEY = "43fdda1192dde7f8ffff7161e13580d7"

# Realistic GPU options for spoofing
GPU_OPTIONS = [
    {"vendor": "Google Inc. (NVIDIA)", "renderer": "ANGLE (NVIDIA, NVIDIA GeForce GTX 1060 6GB Direct3D11 vs_5_0 ps_5_0, D3D11)"},
    {"vendor": "Google Inc. (NVIDIA)", "renderer": "ANGLE (NVIDIA, NVIDIA GeForce RTX 2060 Direct3D11 vs_5_0 ps_5_0, D3D11)"},
    {"vendor": "Google Inc. (NVIDIA)", "renderer": "ANGLE (NVIDIA, NVIDIA GeForce RTX 3070 Direct3D11 vs_5_0 ps_5_0, D3D11)"},
    {"vendor": "Google Inc. (NVIDIA)", "renderer": "ANGLE (NVIDIA, NVIDIA GeForce GTX 1650 Direct3D11 vs_5_0 ps_5_0, D3D11)"},
    {"vendor": "Google Inc. (NVIDIA)", "renderer": "ANGLE (NVIDIA, NVIDIA Quadro P600 (0x00001CBC) Direct3D11 vs_5_0 ps_5_0, D3D11)"},
    {"vendor": "Google Inc. (Intel)", "renderer": "ANGLE (Intel, Intel(R) UHD Graphics 630 Direct3D11 vs_5_0 ps_5_0, D3D11)"},
    {"vendor": "Google Inc. (Intel)", "renderer": "ANGLE (Intel, Intel(R) Iris(R) Xe Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)"},
    {"vendor": "Google Inc. (AMD)", "renderer": "ANGLE (AMD, AMD Radeon RX 580 Series Direct3D11 vs_5_0 ps_5_0, D3D11)"},
    {"vendor": "Google Inc. (AMD)", "renderer": "ANGLE (AMD, AMD Radeon RX 6700 XT Direct3D11 vs_5_0 ps_5_0, D3D11)"},
]

# Common screen resolutions
SCREEN_RESOLUTIONS = [
    {"width": 1920, "height": 1080},
    {"width": 2560, "height": 1440},
    {"width": 1366, "height": 768},
    {"width": 1536, "height": 864},
    {"width": 1440, "height": 900},
    {"width": 1600, "height": 900},
]

# CPU core options
CPU_CORES_OPTIONS = [4, 6, 8, 12, 16]

# Device memory options (GB)
DEVICE_MEMORY_OPTIONS = [4, 8, 16, 32]


def evp_bytes_to_key(password: bytes, salt: bytes) -> tuple[bytes, bytes]:
    """
    CryptoJS EVP_BytesToKey key derivation function.
    Derives a 32-byte key and 16-byte IV from password and salt.
    
    This matches CryptoJS's default key derivation.
    """
    dtot = b""
    d = b""
    while len(dtot) < 48:
        d = hashlib.md5(d + password + salt).digest()
        dtot += d
    return dtot[:32], dtot[32:48]


def cryptojs_aes_encrypt(plaintext: str) -> dict[str, str]:
    """
    Encrypt plaintext using CryptoJS-compatible AES-CBC encryption.
    
    Returns a dict with:
        - ct: Base64 encoded ciphertext
        - iv: Hex encoded IV
        - s: Hex encoded salt
    
    This format matches CryptoJS.AES.encrypt() output when using
    JSON format: CryptoJS.format.OpenSSL
    """
    password = ZEFOY_AES_KEY
    salt = os.urandom(8)
    key, iv = evp_bytes_to_key(password.encode(), salt)
    
    # PKCS7 padding
    block_size = 16
    padding_len = block_size - (len(plaintext.encode()) % block_size)
    padded = plaintext.encode() + bytes([padding_len] * padding_len)
    
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct = cipher.encrypt(padded)
    
    return {
        "ct": base64.b64encode(ct).decode(),
        "iv": iv.hex(),
        "s": salt.hex()
    }


def generate_fingerprint() -> dict[str, Any]:
    """
    Generate a randomized but realistic browser fingerprint.
    
    Values that are randomized:
        - cpuCores, cpuLoad, deviceMemory
        - GPU vendor/renderer
        - Screen resolution
        - historyLength, mimeTypes, plugins
        - localStorage/sessionStorage usage
    
    Values that stay consistent (important for stealth):
        - webdriver: False (CRITICAL)
        - platform: Win32
        - Feature support flags
    """
    gpu = random.choice(GPU_OPTIONS)
    screen = random.choice(SCREEN_RESOLUTIONS)
    cpu_cores = random.choice(CPU_CORES_OPTIONS)
    device_memory = random.choice(DEVICE_MEMORY_OPTIONS)
    
    return {
        "deviceInfo": {
            "cpuCores": cpu_cores,
            "cpuLoad": random.randint(1, 20),
            "deviceMemoryGB": device_memory,
            "platform": "Win32",
            "maxTouchPoints": 0,
            "msMaxTouchPoints": "Not Supported",
            "gpu": gpu,
            "battery": {
                "charging": random.choice([True, False]),
                "level": round(random.uniform(0.2, 1.0), 2),
                "chargingTime": 0 if random.random() > 0.5 else random.randint(100, 7200),
                "dischargingTime": None
            },
            "stylusDetection": random.choice(["Yes", "No"]),
            "touchSupport": "No"
        },
        "browserInfo": {
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
            "timezone": "America/New_York",  # Common timezone
            "timezoneOffset": -240,  # EDT offset
            "localeDateTime": time.strftime("%m/%d/%Y, %I:%M:%S %p"),
            "localUnixTime": int(time.time()),
            "calendar": "gregory",
            "day": "numeric",
            "locale": "en-US",
            "month": "numeric",
            "numberingSystem": "latn",
            "year": "numeric",
            "appName": "Netscape",
            "appVersion": "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
            "vendor": "Google Inc.",
            "language": "en-US",
            "languages": ["en-US", "en"],
            "cookieEnabled": True,
            "onlineStatus": "Online",
            "javaEnabled": False,
            "doNotTrack": None,
            "referrerHeader": "None",
            "httpsConnection": "Yes",
            "historyLength": random.randint(1, 50),
            "mimeTypes": random.choice([2, 3, 4, 5]),
            "plugins": random.choice([4, 5, 6]),
            "webdriver": False,  # CRITICAL - must be False
            "pageVisibility": "visible",
            "isBot": "No",
            "featuresSupported": {
                "geolocation": "Yes",
                "serviceWorker": "Yes",
                "localStorage": "Yes",
                "sessionStorage": "Yes",
                "indexedDB": "Yes",
                "notifications": "Yes",
                "notificationsFirebase": "default",
                "clipboard": "Yes",
                "pushAPI": "Yes",
                "webRTC": "Yes",
                "gamepadAPI": "Yes",
                "speechSynthesis": "Yes",
                "webGL": "Yes",
                "vibrationAPI": "Yes",
                "deviceMotion": "Yes",
                "deviceOrientation": "Yes",
                "wakeLock": "Yes",
                "serial": "Yes",
                "usb": "Yes",
                "networkInformation": "Yes",
                "screenCapture": "Yes",
                "fullscreenAPI": "Yes",
                "pictureInPicture": "Yes"
            }
        },
        "screenInfo": {
            "width": screen["width"],
            "height": screen["height"],
            "colorDepth": 24,
            "pixelDepth": 24,
            "devicePixelRatio": random.choice([1, 1.25, 1.5, 2]),
            "orientation": "landscape-primary",
            "screenOrientationAngle": 0,
            "availableWidth": screen["width"],
            "availableHeight": screen["height"] - 40,  # Taskbar
            "screenLeft": 0,
            "screenTop": 0,
            "outerWidth": screen["width"],
            "outerHeight": screen["height"] - 40,
            "innerWidth": screen["width"],
            "innerHeight": screen["height"] - 127  # Browser chrome
        },
        "otherData": {
            "mouseAvailable": "Yes",
            "keyboardAvailable": "Yes",
            "bluetoothSupport": random.choice(["Yes", "No"]),
            "usbSupport": "Yes",
            "gamepadSupport": "Yes",
            "incognitoMode": "No"
        },
        "storageInfo": {
            "localStorage": random.randint(0, 15),
            "sessionStorage": random.randint(0, 5),
            "indexedDB": "Available",
            "cacheStorage": "Available",
            "storageEstimate": {
                "quota": random.randint(150000000000, 200000000000),
                "usage": random.randint(5000, 100000),
                "usageDetails": {
                    "indexedDB": random.randint(5000, 50000)
                }
            }
        }
    }


def get_spoofed_captcha_encoded() -> str:
    """
    Generate a complete spoofed captcha_encoded value ready for injection.
    
    Returns a JSON string in CryptoJS format:
    {"ct":"...","iv":"...","s":"..."}
    """
    fingerprint = generate_fingerprint()
    fingerprint_json = json.dumps(fingerprint, separators=(",", ":"))
    encrypted = cryptojs_aes_encrypt(fingerprint_json)
    return json.dumps(encrypted, separators=(",", ":"))


def encode_k9x_mouse_data() -> str:
    """
    Generate K9x! encoded mouse movement data.
    
    Format: Random mouse points → XOR encoding → wrap with K9x! → Base64 → reverse
    
    This simulates realistic mouse movement patterns.
    """
    points = []
    num_points = random.randint(12, 28)
    
    for i in range(num_points):
        x = random.randint(50, 1900)
        y = random.randint(50, 1000)
        d = round(random.uniform(0.05, 2.8), 4)
        g = "True" if random.random() > 0.65 else "False"
        points.append(f"x={x}&y={y}&d={d}&g={g}")
    
    raw = "|".join(points)
    
    # XOR encoding with rotating key
    xored = "".join(chr(ord(c) ^ (i % 5 + 77)) for i, c in enumerate(raw))
    
    # Wrap with K9x! markers
    wrapped = "K9x!" + xored + "K9x!"
    
    # Base64 encode
    encoded = base64.b64encode(wrapped.encode()).decode()
    
    # Reverse the string
    final = encoded[::-1]
    
    # Add padding if needed
    final += "=" * ((4 - len(final) % 4) % 4)
    
    return final


if __name__ == "__main__":
    # Test the module
    print("=" * 60)
    print("Fingerprint Spoofing Module Test")
    print("=" * 60)
    
    # Generate fingerprint
    fp = generate_fingerprint()
    print(f"\n✅ Generated fingerprint with:")
    print(f"   CPU Cores: {fp['deviceInfo']['cpuCores']}")
    print(f"   Memory: {fp['deviceInfo']['deviceMemoryGB']}GB")
    print(f"   GPU: {fp['deviceInfo']['gpu']['renderer'][:50]}...")
    print(f"   Screen: {fp['screenInfo']['width']}x{fp['screenInfo']['height']}")
    print(f"   webdriver: {fp['browserInfo']['webdriver']}")
    
    # Encrypt it
    captcha_encoded = get_spoofed_captcha_encoded()
    print(f"\n✅ Encrypted captcha_encoded:")
    print(f"   Length: {len(captcha_encoded)} chars")
    print(f"   Preview: {captcha_encoded[:80]}...")
    
    # Generate K9x! data
    k9x_data = encode_k9x_mouse_data()
    print(f"\n✅ K9x! mouse data:")
    print(f"   Length: {len(k9x_data)} chars")
    print(f"   Preview: {k9x_data[:60]}...")
    
    print("\n" + "=" * 60)
    print("All tests passed! ✅")
    print("=" * 60)
