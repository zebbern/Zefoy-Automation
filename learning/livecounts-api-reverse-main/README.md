<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=180&section=header&text=livecounts.io%20Reverse&fontSize=60&fontAlignY=58&animation=fadeIn&fontColor=ffffff"/>

# 🚀 livecounts.io API

[![GitHub Stars](https://img.shields.io/github/stars/5k-omar/livecounts-api-reverse?style=for-the-badge&logo=github&color=FFD700)](https://github.com/5k-omar/Zefoy-Bot/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/5k-omar/livecounts-api-reverse?style=for-the-badge&logo=github&color=28a745)](https://github.com/5k-omar/Zefoy-Bot/network/members)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)

**100% working as of (1/22/2026)**

[Star this repo](https://github.com/5k-omar/livecounts-api-reverse) • [Join Discord](https://discord.gg/tcnksFMCR9)

</div>

---

# livecounts.io API

unofficial python wrapper for livecounts.io stats api

## what it does

gets live stats from livecounts.io without rate limits or browser overhead

supports:
- tiktok videos (views, likes, comments, shares)
- tiktok users (followers, following, total likes)
- twitter/x users (followers, tweets, following)

## how it works

livecounts.io protects their api with custom auth headers that change every request:

```
x-ajay: f8e227969316d0adf670c7c08a7d185a5be8b215
x-catto: 1769090337041
x-midas: 9d59b34634cce7838fc19894ecf6514b5df26dbf017c36d5536e81fdfee68ae47a5261a1507dec2f64ad80481e7834c7
```

### reverse engineering process

**step 1: find the api endpoints**

opened livecounts.io and went to any counter (tiktok video for example)

opened chrome devtools (F12) -> network tab -> filter by XHR/Fetch

saw requests going to:
```
https://tiktok.livecounts.io/video/stats/VIDEO_ID
https://tiktok.livecounts.io/user/stats/USER_ID
https://api.livecounts.io/twitter-live-follower-counter/stats/USERNAME
```

noticed three custom headers that change every request:
```
x-ajay: f8e227969316d0adf670c7c08a7d185a5be8b215
x-catto: 1769090337041
x-midas: 9d59b34634cce7838fc19894ecf6514b5df26dbf017c36d5536e81fdfee68ae47a5261a1507dec2f64ad80481e7834c7
```

**step 2: find the header generation code**

in devtools sources tab, searched for "x-ajay" in all files (ctrl+shift+f)

found it in a webpack bundle file named something like `1769092987149_48387aa08817f3f4.js`

inside found this code:
```javascript
t.exports=()=>{
    let e=Date.now().toString();
    return{
        "x-midas":i(o(e+64)),
        "x-ajay":n(e),
        "x-catto":e
    }
}
```

**step 3: identify the hash functions**

looked at the imports at top of file:
```javascript
let i=e.r(90642),  // this is SHA384
    o=e.r(35521),  // this is SHA256
    n=e.r(88114);  // this is RIPEMD160
```

searched these module IDs in the file and found:
- module 90642 = SHA384
- module 35521 = SHA256  
- module 88114 = RIPEMD160

**step 4: found OLD algorithm in code (doesn't work)**

from the bundled code found this:
```javascript
"x-midas":i(o(e+64)),
"x-ajay":n(e),
"x-catto":e
```

where:
- e = timestamp
- o(e+64) = SHA256(timestamp + 64)
- i(o(e+64)) = SHA384(SHA256(timestamp + 64))
- n(e) = RIPEMD160(timestamp)

so OLD algorithm was:
```
x-catto = timestamp
x-ajay = RIPEMD160(timestamp)
x-midas = SHA384(SHA256(timestamp + 64))
```

**step 5: OLD ALGORITHM DOESN'T WORK**

tested this in browser console and headers didn't match

actual headers from network tab:
```
x-ajay: f8e227969316d0adf670c7c08a7d185a5be8b215 (40 chars)
```

RIPEMD160 would also be 40 chars but hash was completely different

they changed the algorithm but old code is still in the bundle

**step 6: reverse from actual headers**

analyzed the actual header values:
```
x-catto: 1769090337041  -> timestamp
x-ajay: f8e227...       -> 40 chars = SHA1
x-midas: 9d59b3...      -> 96 chars = SHA384
```

tested in console:
```javascript
timestamp = Date.now()
ajay = CryptoJS.SHA1(timestamp.toString())
midas = CryptoJS.SHA384(ajay + timestamp)
```

both matched perfectly

**step 7: current algorithm**

```
timestamp = Date.now()
x-catto = timestamp (string)
x-ajay = SHA1(x-catto)
x-midas = SHA384(x-ajay + x-catto)
```

found the actual implementation in the js file at line with module 90165:
```javascript
t.exports=()=>{
    let e=Date.now().toString();
    return{
        "x-midas":i(o(e+64)),  // old code still there but not used
        "x-ajay":n(e),         // this is the real one
        "x-catto":e
    }
}
```

but when i checked the network requests, they were using different values

the REAL current code (found by testing) is:
```javascript
timestamp = Date.now().toString()
x_catto = timestamp
x_ajay = SHA1(timestamp)
x_midas = SHA384(x_ajay + timestamp)
```

**algorithm discovered:**
```
timestamp = current_time_milliseconds
x-catto = timestamp (string)
x-ajay = SHA1(x-catto)
x-midas = SHA384(x-ajay + x-catto)
```

### code breakdown

the algorithm is simple once deobfuscated:

```python
timestamp = int(time.time() * 1000)
x_catto = str(timestamp)
x_ajay = sha1_hash(x_catto)
x_midas = sha384_hash(x_ajay + x_catto)
```

then these headers get sent with every request to bypass the challenge

## responses

### tiktok video
```json
{
  "views": 1234567,
  "likes": 98765,
  "comments": 4321,
  "shares": 567,
  "favorites": 890
}
```

### tiktok user
```json
{
  "followers": 123456,
  "following": 789,
  "likes": 9876543,
  "videos": 234
}
```

### twitter user
```json
{
  "followers": 12345,
  "tweets": 678,
  "following": 123,
  "goal": 5
}
```

## notes

- no api key needed
- algorithm might change if they update their challenge
- headers must be regenerated for each request (timestamp-based)
## why this exists

livecounts.io has public data but makes you load their entire frontend. this skips that and gives you raw json xD.

## legal

this is educational. respect rate limits. don't abuse their servers.

## 🤝 Community & Support

<div align="center">

### Love this project? Show your support!

[![Star History](https://img.shields.io/github/stars/5k-omar/livecounts-api-reverse?style=social&label=Star%20This%20Repo)](https://github.com/5k-omar/livecounts-api-reverse)

**Join our Discord community for:**
- 🔔 Real-time updates
- 💬 Support & troubleshooting
- 🎉 Feature announcements
- 🤝 Connect with other users

[![Discord](https://img.shields.io/badge/Join-Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/tcnksFMCR9)

---

**Made with ❤️ by [@5k-omar](https://github.com/5k-omar)**

</div>
