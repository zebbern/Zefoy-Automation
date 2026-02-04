Zefoy Signatures
---
Zefoy has 2 security headers called `ltj` and `PHPSESSID`. They are checked by Zefoy to authenticate & secure API requests. <br> As you can see below, their headers are quite simple. It seems that **their priority in security is their dynamic Javascript.** <br><br>


LTJ
----
The `ltj` header is simple, it is a Unix Timestamp that can be generated with the function below.

```py
def update_ltj_cookie():
    return math.floor(time.time())
```
This function would count the total amount of seconds since **January 1, 1970, 00:00:00 UTC**, as of making this, it is `1758403678`<br><br>


PHPSESSID
----
The **PHPSESSID** header is used to identify a session. It is globally used by PHP sites to link a client to server side data. Once generated, it must be reused for all requests moving forward. It is generated when you make an initial GET Request to [Zefoy](zefoy.com)

```py
def get_phpsessid()
    response = requests.get('https://zefoy.com/')
    return response.headers.get('Set-Cookie')
```
This would return this: `PHPSESSID=gb2lm6ov8ogk34r04jb8dl72h1`. Ensure to reuse this cookie on all your next requests. It's static but necessary.
