
CAPTCHA Solving
---

The payload that was sent during CAPTCHA submission is below. It looks overwhelming and complex, in reality it's just low-level encoding.
<img width="2051" height="670" alt="image" src="https://github.com/user-attachments/assets/bbe5bad9-7e5e-46ce-992c-59b4efeba934" /><br><br>

Payload Keys (Form Names)
---- 
The keys in the POST Request are present on your first GET request to `zefoy.com`. They are dynamic and can be extracted like this:
```py
# Extract the first key in the payload  (9467f3d825ca70a18c1e)
text_input = soup.select_one("input#captchatoken")
text_input_name = text_input["name"]

# Extract the second key in the payload  (9c1ce27f08b16479d2e17743062b28ed)
hidden_input = soup.select_one("input[type='hidden'][class='input']")
hidden_name = hidden_input["name"]

# The captcha_encoded key is static and it's name will not change
```
<br>

1. The value for the first key is the plain text of solution submitted. Simple and easy.
2. The value for the second key is an encoded string.
3. The value for the third key is a ciphered JSON
   - This includes `ct`, `iv` and `s`, which is Ciphertext, Initialisation Vector and the Salt.
   - In order to decode this, you need the logic used to encode it.

<br>

`captcha_encoded` Logic (Cipher) (Third Key)
---- 

**I looked into [Zefoy's Javascript.](https://zefoy.com/assets/53fbc84b11a13a7942a850361e5d7b49.js?v=1754384581) Deobfuscating using [obf.io](https://obf-io.deobfuscate.io/) to make it readable. This is what I noted down:**<br>
- **A single object `_0x39f21f` is created to gather all client info.**
   - deviceInfo – CPU cores, CPU load, GPU info, device memory, touch/stylus support, battery info.
   -  browserInfo – User agent, language, timezone, local time, locale, bot detection, feature detection, etc.
   -   screenInfo – Screen width, height, color depth, pixel depth, device pixel ratio, orientation, inner/outer size, available width/height.
   -   otherData – Mouse, keyboard, USB, Bluetooth, gamepad, and incognito mode support.
   -    storageInfo – localStorage, sessionStorage, indexedDB, Cache API, storage estimate.

**Once `_0x39f21f` is populated, it is converted to a JSON string**
```js
var _0x1eee13 = JSON.stringify(_0x39f21f);
```

**The AES encryption format configuration is held on the variable `_0x1fb2fd`**
```js
var _0x1fb2fd = {format: CryptoJSAesJson};
```

**The JSON string is then encrypted using AES with a static key ("43fdda1192dde7f8ffff7161e13580d7") and the configuration in `_0x1fb2fd`**
```js
var _0x475601 = CryptoJS.AES.encrypt(_0x1eee13, "43fdda1192dde7f8ffff7161e13580d7", _0x1fb2fd).toString();
```

**The encrypted string is placed into the hidden HTML input field `captchaencoded` and used in the CAPTCHA submit request**
```js
document.getElementById("captchaencoded").value = _0x475601;
```

<br><br>

Second Key Logic (Encoding + XOR)
----

- **The _0x5d0ea3() function collects mouse movement data & makes an object like `x=672&y=880&d=0.88&g=False`**
   - "x": 0x0,  (X Coordinate)
   - "y": 0x0,  (Y Coordinate)
   - "d": 0x0,  (Direction)
   - "g": false,  (Dragging Boolean)


**Then `_0x2d89df` XORs each character of the input string with a key `(index % 5 + 77)` to obfuscate it.**
```js
const _0x2d89df = function (_0x2d8981) {
    let _0x3605c2 = '';
    for (let _0x3fd4aa = 0; _0x3fd4aa < _0x2d8981.length; _0x3fd4aa++) {
        _0x3605c2 += String.fromCharCode(_0x2d8981.charCodeAt(_0x3fd4aa) ^ _0x3fd4aa % 5 + 77);
    }
    ...
}
```


**The obfuscated string is wrapped with K9x! on both ends of the string for further obfuscation & confusion.**
```js
const wrapped = "K9x!" + _0x3605c2 + "K9x!";
```

**Encodes the wrapped string in Base64 and then reverses the result to obfuscate even further.**
```js
  return (function (input) {
    let out = '';
    let i = 0;
    while (i < input.length) {
      const c1 = input.charCodeAt(i++);
      const c2 = input.charCodeAt(i++);
      const c3 = input.charCodeAt(i++);

      const enc1 = c1 >> 2;
      const enc2 = ((c1 & 3) << 4) | (c2 >> 4);
      const enc3 = ((c2 & 15) << 2) | (c3 >> 6);
      const enc4 = c3 & 63;

      const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
      out += chars.charAt(enc1)
           + chars.charAt(enc2)
           + (isNaN(c2) ? '=' : chars.charAt(enc3))
           + (isNaN(c3) ? '=' : chars.charAt(enc4));
    }
    return out;
  })(wrapped).split('').reverse().join('');
};
```

**The reversed string is then inserted into the input element.**
```js
const _0x457738 = document.getElementById("input");
if (_0x457738) {
  _0x457738.value = _0x2d89df;
}
```

