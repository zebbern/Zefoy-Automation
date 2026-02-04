
CAPTCHA Payloads
---

#### Table of Contents 
- [Reverse Engineering the Values/Encoding](https://github.com/AdamBankz/zefoy-reversed/tree/main/Generating%20Payloads/Captcha%20Payload)
- [Second Key Generation Code](https://github.com/AdamBankz/zefoy-reversed/blob/main/Generating%20Payloads/Captcha%20Payload/Second%20Key%20Generation/README.md)
- [captcha_encoded Generation Code](https://github.com/AdamBankz/zefoy-reversed/blob/main/Generating%20Payloads/Captcha%20Payload/Captcha%20Encoded/README.md)


Final Request Payloads
---

The final request made to their endpoint to send the views/likes is quite simple.

```
name="79d49db9535a68" → 7552231885657607446
name="130e92e5e9eba6dfd91ed0ad1" → https://www.tiktok.com/@matfromni/video/7552231885657607446
name="e5f1eca2787f" → ==QI4lzSoICPugCc2YXf4NWYttCa6JmYydzalNGfzVTI4lzS
```
```
name="79d49db9535a68" → 7552231885657607446
name="130e92e5e9eba6dfd91ed0ad1" → https://www.tiktok.com/@matfromni/video/7552231885657607446
name="e5f1eca2787f" → ==QI4lzSoICPugCc2YXe5NWYttCa4VmYydzapVWfzVTI4lzS
```
In these 2 seperate requests made off the same session, the `e5f1eca2787f` value is the one one that changes. It uses the exact same logic to encode as the [Second Key Generation Code](https://github.com/AdamBankz/zefoy-reversed/blob/main/Generating%20Payloads/Captcha%20Payload/Second%20Key%20Generation/README.md), wrapping the string with K9x!, XORing and Base64. The `name=""` keys are just same the keys used in CAPTCHA submission, they wont change when on the same session, meaning you can reuse the keys from the CAPTCHA submission for the final request.<br><br>

**The WebKitFormBoundary in the final request isn't checked on their backend, it can be recreated with the following code:**
```py
boundary = '----WebKitFormBoundary' + ''.join(random.sample(string.ascii_letters + string.digits, 16))
````


