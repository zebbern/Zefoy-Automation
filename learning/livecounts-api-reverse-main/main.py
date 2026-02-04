import hashlib
import time
import requests

class Tiktok:
    VIDEOID = 'tiktok.video'
    USERID = 'tiktok.user'

class Twitter:
    USERNAME = 'twitter.user'

def get_sha1_hash(t):
    sha1 = hashlib.sha1()
    sha1.update(t.encode('utf-8'))
    return sha1.hexdigest()

def get_sha384_hash(t):
    sha384 = hashlib.sha384()
    sha384.update(t.encode('utf-8'))
    return sha384.hexdigest()

def generate_headers():
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'
    
    headers = {
        'User-Agent': ua,
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9',
        'Origin': 'https://livecounts.io',
        'Referer': 'https://livecounts.io/',
        'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site'
    }
       
    timestamp = int(time.time() * 1000)
    x_catto = str(timestamp)
    x_ajay = get_sha1_hash(x_catto)
    x_midas = get_sha384_hash(x_ajay + x_catto)
        
    headers['x-ajay'] = x_ajay
    headers['x-catto'] = x_catto
    headers['x-midas'] = x_midas
    
    return headers

def get_stats(type, identifier):
    if type == 'tiktok.video':
        url = f'https://tiktok.livecounts.io/video/stats/{identifier}'
        headers = generate_headers()     
    elif type == 'tiktok.user':
        url = f'https://tiktok.livecounts.io/user/stats/{identifier}'
        headers = generate_headers()  
    elif type in ['twitter.user', 'x.user']:
        url = f'https://api.livecounts.io/twitter-live-follower-counter/stats/{identifier}'
        headers = generate_headers()
    else:
        return {'error': 'invalid type'}

    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            data = r.json()
            return parse_response(type, data)
        elif r.status_code == 429:
            return {'error': 'rate limited', 'retry_after': r.headers.get('Retry-After', '60')}
        else:
            return {'error': f'status {r.status_code}', 'text': r.text}
    except requests.exceptions.Timeout:
        return {'error': 'timeout'}
    except requests.exceptions.ConnectionError:
        return {'error': 'connection failed'}
    except Exception as e:
        return {'error': str(e)}

def parse_response(type, data):
    result = {'raw': data}
    print(data)
    
    if type == 'tiktok.video':
        if data.get('success'):
            result['views'] = data.get('viewCount', 0)
            result['likes'] = data.get('likeCount', 0)
            result['comments'] = data.get('commentCount', 0)
            result['shares'] = data.get('shareCount', 0)
            result['favorites'] = data.get('collectCount', 0)
            
    elif type == 'tiktok.user':
        if data.get('success'):
            result['followers'] = data.get('followerCount', 0)
            result['following'] = data.get('followingCount', 0)
            result['likes'] = data.get('heartCount', 0)
            result['videos'] = data.get('videoCount', 0)
            
    elif type == 'twitter.user':
        if data.get('success'):
            result['followers'] = data.get('followerCount', 0)
            bottom = data.get('bottomOdos', [])
            if len(bottom) >= 3:
                result['tweets'] = bottom[0]
                result['following'] = bottom[1]
                result['goal'] = bottom[2]
    
    return result

if __name__ == '__main__':
    print("https://discord.gg/tcnksFMCR9\n")
    
    print('TikTok Video:')
    video = get_stats(Tiktok.VIDEOID, '7389894188692704544')
    print(f"Views: {video.get('views')}, Likes: {video.get('likes')}")
    print()

    print('TikTok User:')
    user = get_stats(Tiktok.USERID, '7388534953741927456')
    print(f"Followers: {user.get('followers')}, Videos: {user.get('videos')}")
    print()
    
    print('Twitter/X:')
    twitter = get_stats(Twitter.USERNAME, 'darkg3n')
    print(f"Followers: {twitter.get('followers')}, Tweets: {twitter.get('tweets')}")
    print()
    
    # you can add other it easy anyway if you want
    #
    # just for 130 lines xD
