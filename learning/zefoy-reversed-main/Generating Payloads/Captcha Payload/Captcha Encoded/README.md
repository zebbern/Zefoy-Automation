`captcha_encoded` Generation
---
In this module, we generate our own `captcha_encoded` value that validates on Zefoy's backend. Using this Python function, you can generate the exact fingerprint that Zefoy encodes to generate the JSON object. **Below this block of code I will show you how to encode it.**
```py
def generate_random_fingerprint():
    cpu_cores_options = [2, 4, 6, 8, 12, 16]
    cpu_load = random.randint(1, 100)
    device_memory_gb = random.choice([4, 6, 8, 12, 16, 32])
    platforms = ['Win32', 'MacIntel', 'Linux x86_64', 'Android', 'iPhone']
    gpu_vendors = ['Intel', 'NVIDIA', 'AMD', 'Google Inc. (Intel)', 'Apple']
    gpu_renderers = [
        "ANGLE (Intel, Intel(R) UHD Graphics 630 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (NVIDIA GeForce GTX 1060 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (AMD Radeon RX 580 Direct3D11 vs_5_0 ps_5_0)",
        "Apple A13 GPU",
        "Google SwiftShader"
    ]
    battery_charging = random.choice([True, False])
    battery_level = round(random.uniform(0, 1), 2)
    stylus_detection = random.choice(['Yes', 'No'])
    touch_support = random.choice(['Yes', 'No'])
    timezone = random.choice(['Africa/Cairo', 'America/New_York', 'Europe/London', 'Asia/Tokyo'])
    languages = ['en-US', 'fr-FR', 'es-ES', 'de-DE', 'zh-CN']
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
        "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
    ]
    screen_widths = [1280, 1366, 1440, 1536, 1600, 1920, 2560]
    screen_heights = [720, 768, 900, 1024, 1080, 1440, 1600]
    color_depth = random.choice([24, 30, 32])
    device_pixel_ratio = random.choice([1, 1.25, 1.5, 2, 3])

    fingerprint = {
        "deviceInfo": {
            "cpuCores": random.choice(cpu_cores_options),
            "cpuLoad": cpu_load,
            "deviceMemoryGB": device_memory_gb,
            "platform": random.choice(platforms),
            "maxTouchPoints": 0 if touch_support == 'No' else random.choice([1, 5, 10]),
            "msMaxTouchPoints": 'Not Supported',
            "gpu": {
                "vendor": random.choice(gpu_vendors),
                "renderer": random.choice(gpu_renderers)
            },
            "battery": {
                "charging": battery_charging,
                "level": battery_level,
                "chargingTime": 0 if battery_charging else random.randint(1000, 5000),
                "dischargingTime": None if battery_charging else random.randint(10000, 20000)
            },
            "stylusDetection": stylus_detection,
            "touchSupport": touch_support
        },
        "browserInfo": {
            "userAgent": random.choice(user_agents),
            "timezone": timezone,
            "timezoneOffset": -180 if timezone == 'Africa/Cairo' else random.choice([-300, 0, 540]),
            "localeDateTime": time.strftime("%m/%d/%Y, %I:%M:%S %p"),
            "localUnixTime": int(time.time()),
            "calendar": "gregory",
            "day": "numeric",
            "locale": "en-US",
            "month": "numeric",
            "numberingSystem": "latn",
            "year": "numeric",
            "appName": "Netscape",
            "appVersion": "5.0 (Windows NT 10.0; Win64; x64)",
            "vendor": "Google Inc.",
            "language": random.choice(languages),
            "languages": languages,
            "cookieEnabled": True,
            "onlineStatus": "Online",
            "javaEnabled": False,
            "doNotTrack": None,
            "referrerHeader": "https://www.google.com/",
            "httpsConnection": "Yes",
            "historyLength": random.randint(1, 10),
            "mimeTypes": random.randint(5, 20),
            "plugins": random.randint(1, 10),
            "webdriver": False,
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
            "width": random.choice(screen_widths),
            "height": random.choice(screen_heights),
            "colorDepth": color_depth,
            "pixelDepth": color_depth,
            "devicePixelRatio": device_pixel_ratio,
            "orientation": "landscape-primary",
            "screenOrientationAngle": 0,
            "availableWidth": random.choice(screen_widths),
            "availableHeight": random.choice(screen_heights),
            "screenLeft": 0,
            "screenTop": 0,
            "outerWidth": random.choice(screen_widths),
            "outerHeight": random.choice(screen_heights),
            "innerWidth": random.choice(screen_widths),
            "innerHeight": random.choice(screen_heights)
        },
        "otherData": {
            "mouseAvailable": "Yes",
            "keyboardAvailable": "Yes",
            "bluetoothSupport": "Yes",
            "usb exacerbate": "Yes",
            "gamepadSupport": "Yes",
            "incognitoMode": False
        },
        "storageInfo": {
            "localStorage": 1,
            "sessionStorage": 1,
            "indexedDB": "Available",
            "cacheStorage": "Available",
            "storageEstimate": {
                "quota": random.randint(500000000, 2000000000),
                "usage": random.randint(1000000, 100000000),
                "usageDetails": {}
            }
        }
    }

    return json.dumps(fingerprint, indent=2)
```

```py
PASS = "43fdda1192dde7f8ffff7161e13580d7"  

def evp_bytes_to_key(password: bytes, salt: bytes, key_len: int, iv_len: int):
    dt = b""
    prev = b""
    while len(dt) < (key_len + iv_len):
        prev = md5(prev + password + salt).digest()
        dt += prev
    key = dt[:key_len]
    iv = dt[key_len:key_len + iv_len]
    return key, iv

def pkcs7_pad(b: bytes, block_size: int = 16) -> bytes:
    pad_len = block_size - (len(b) % block_size)
    return b + bytes([pad_len]) * pad_len

def cryptojs_aes_encrypt_json(plaintext: str, passphrase: str) -> str:

    salt = get_random_bytes(8)         
    key_len = 16                          
    iv_len = 16
    key, iv = evp_bytes_to_key(passphrase.encode('utf-8'), salt, key_len, iv_len)

    data = plaintext.encode('utf-8')
    data_padded = pkcs7_pad(data, AES.block_size)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct_bytes = cipher.encrypt(data_padded)

    ct_b64 = base64.b64encode(ct_bytes).decode('utf-8')
    iv_hex = iv.hex()
    salt_hex = salt.hex()
    json_obj = {"ct": ct_b64, "iv": iv_hex, "s": salt_hex}
    return json.dumps(json_obj)
```
# Example Usage:
```py
if __name__ == "__main__":
    plaintext_json = json.dumps(generate_random_fingerprint(), separators=(",", ":"))  
    captchaencoded_value = cryptojs_aes_encrypt_json(plaintext_json, PASS)
    print(captchaencoded_value)

# Output: {"ct": "fqfo5cApbAnb6/Cg6b+nl.........", "iv": "3ce4c8792dc85cf023bc087bfdcca9fe", "s": "e19d0f2d421ac181"}
```
The returned JSON object will validate on Zefoy's backend as a legitimate fingerprint.

