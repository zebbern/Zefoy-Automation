Second Key Generation
----
In this module, we generate our own mouse data and encode it using Zefoy's exact logic. Ensuring that when checked by their backend, the request is validated.

```py
def encode_state_string() -> str:
    s = f"x={random.randint(0,1000)}&y={random.randint(0,1000)}&d={random.random():.2f}&g=False"
    print("State:", s)
    xored = ''.join(chr(ord(c) ^ ((i % 5) + 77)) for i, c in enumerate(s))
    encoded = base64.b64encode(("K9x!" + xored + "K9x!").encode()).decode()[::-1]
    return encoded
```

This would return something like the following. The `encoded` variable would be the value sent in the CAPTCHA submission request, alongside the raw text and the `captcha_encoded` value.
```
State: x=732&y=532&d=0.94&g=False
==QI4lzSoICPugAc2Y3e3NWYttCa/JWZydzajNGezVTI4lzS
```
