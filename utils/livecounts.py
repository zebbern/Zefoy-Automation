"""
Livecounts.io API Client for TikTok Statistics
===============================================

Retrieves real-time stats from TikTok videos and users via livecounts.io.
Based on reverse engineering by 5k-omar (https://github.com/5k-omar/livecounts-api-reverse)

Usage:
    from utils.livecounts import LivecountsAPI
    
    api = LivecountsAPI()
    stats = api.get_video_stats("https://www.tiktok.com/@user/video/1234567890")
    print(f"Views: {stats['views']}, Likes: {stats['likes']}")
"""
from __future__ import annotations

import hashlib
import json
import re
import time
from dataclasses import dataclass
from typing import Optional

import requests


@dataclass
class VideoStats:
    """TikTok video statistics."""
    video_id: str
    views: int
    likes: int
    comments: int
    shares: int
    favorites: int = 0
    success: bool = True
    error: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'video_id': self.video_id,
            'views': self.views,
            'likes': self.likes,
            'comments': self.comments,
            'shares': self.shares,
            'favorites': self.favorites,
            'success': self.success,
            'error': self.error
        }
    
    def format_display(self) -> str:
        """Format stats for TUI display."""
        if not self.success:
            return f"  ❌ Error: {self.error}"
        
        return (
            f"  👁️  Views:    {self.views:,}\n"
            f"  ❤️  Likes:    {self.likes:,}\n"
            f"  💬 Comments: {self.comments:,}\n"
            f"  🔁 Shares:   {self.shares:,}"
        )


@dataclass 
class UserStats:
    """TikTok user statistics."""
    user_id: str
    followers: int
    following: int
    likes: int
    videos: int
    success: bool = True
    error: Optional[str] = None


class LivecountsAPI:
    """Client for livecounts.io API to get TikTok statistics."""
    
    BASE_URL_VIDEO = "https://tiktok.livecounts.io/video/stats"
    BASE_URL_USER = "https://tiktok.livecounts.io/user/stats"
    
    # Regex patterns for extracting IDs from TikTok URLs
    VIDEO_ID_PATTERNS = [
        r'video/(\d+)',  # https://tiktok.com/@user/video/1234567890
        r'/v/(\d+)',     # https://vm.tiktok.com/v/1234567890
        r'/(\d{19})/?',  # Direct video ID (19 digits)
    ]
    
    USER_ID_PATTERNS = [
        r'@([a-zA-Z0-9_.]+)',  # https://tiktok.com/@username
    ]
    
    def __init__(self, timeout: int = 15):
        """Initialize the API client.
        
        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.session = requests.Session()
    
    def _generate_auth_headers(self) -> dict:
        """Generate authentication headers for livecounts.io API.
        
        Algorithm:
            x-catto = timestamp (milliseconds)
            x-ajay = SHA1(x-catto)
            x-midas = SHA384(x-ajay + x-catto)
        """
        timestamp = int(time.time() * 1000)
        x_catto = str(timestamp)
        x_ajay = hashlib.sha1(x_catto.encode()).hexdigest()
        x_midas = hashlib.sha384((x_ajay + x_catto).encode()).hexdigest()
        
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9',
            'Origin': 'https://livecounts.io',
            'Referer': 'https://livecounts.io/',
            'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'x-ajay': x_ajay,
            'x-catto': x_catto,
            'x-midas': x_midas,
        }
    
    def extract_video_id(self, url_or_id: str) -> Optional[str]:
        """Extract video ID from TikTok URL or return as-is if already an ID.
        
        Args:
            url_or_id: TikTok video URL or video ID
            
        Returns:
            Video ID string or None if not found
        """
        # If it's already a numeric ID (19 digits), return as-is
        if url_or_id.isdigit() and len(url_or_id) >= 17:
            return url_or_id
        
        # Try each pattern
        for pattern in self.VIDEO_ID_PATTERNS:
            match = re.search(pattern, url_or_id)
            if match:
                return match.group(1)
        
        return None
    
    def extract_username(self, url: str) -> Optional[str]:
        """Extract username from TikTok URL.
        
        Args:
            url: TikTok profile URL
            
        Returns:
            Username string or None if not found
        """
        for pattern in self.USER_ID_PATTERNS:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def get_video_stats(self, url_or_id: str) -> VideoStats:
        """Get statistics for a TikTok video.
        
        Args:
            url_or_id: TikTok video URL or video ID
            
        Returns:
            VideoStats dataclass with views, likes, comments, shares
        """
        video_id = self.extract_video_id(url_or_id)
        if not video_id:
            return VideoStats(
                video_id=url_or_id,
                views=0, likes=0, comments=0, shares=0,
                success=False,
                error="Could not extract video ID from URL"
            )
        
        try:
            url = f"{self.BASE_URL_VIDEO}/{video_id}"
            headers = self._generate_auth_headers()
            
            response = self.session.get(url, headers=headers, timeout=self.timeout)
            
            if response.status_code == 429:
                return VideoStats(
                    video_id=video_id,
                    views=0, likes=0, comments=0, shares=0,
                    success=False,
                    error="Rate limited - try again later"
                )
            
            if response.status_code != 200:
                return VideoStats(
                    video_id=video_id,
                    views=0, likes=0, comments=0, shares=0,
                    success=False,
                    error=f"HTTP {response.status_code}"
                )
            
            data = response.json()
            
            if not data.get('success'):
                return VideoStats(
                    video_id=video_id,
                    views=0, likes=0, comments=0, shares=0,
                    success=False,
                    error="Video not found or API error"
                )
            
            return VideoStats(
                video_id=video_id,
                views=data.get('viewCount', 0),
                likes=data.get('likeCount', 0),
                comments=data.get('commentCount', 0),
                shares=data.get('shareCount', 0),
                favorites=data.get('collectCount', 0),
                success=True
            )
            
        except requests.exceptions.Timeout:
            return VideoStats(
                video_id=video_id,
                views=0, likes=0, comments=0, shares=0,
                success=False,
                error="Request timeout"
            )
        except requests.exceptions.ConnectionError:
            return VideoStats(
                video_id=video_id,
                views=0, likes=0, comments=0, shares=0,
                success=False,
                error="Connection failed"
            )
        except json.JSONDecodeError:
            return VideoStats(
                video_id=video_id,
                views=0, likes=0, comments=0, shares=0,
                success=False,
                error="Invalid API response"
            )
        except Exception as e:
            return VideoStats(
                video_id=video_id,
                views=0, likes=0, comments=0, shares=0,
                success=False,
                error=str(e)
            )
    
    def get_user_stats(self, url_or_id: str) -> UserStats:
        """Get statistics for a TikTok user.
        
        Args:
            url_or_id: TikTok profile URL or user ID
            
        Returns:
            UserStats dataclass with followers, following, likes, videos
        """
        # If it looks like a URL, try to resolve to user ID
        # Note: This is more complex as we need the numeric user ID, not username
        user_id = url_or_id
        
        if not user_id.isdigit():
            return UserStats(
                user_id=url_or_id,
                followers=0, following=0, likes=0, videos=0,
                success=False,
                error="User stats require numeric user ID (not username)"
            )
        
        try:
            url = f"{self.BASE_URL_USER}/{user_id}"
            headers = self._generate_auth_headers()
            
            response = self.session.get(url, headers=headers, timeout=self.timeout)
            
            if response.status_code != 200:
                return UserStats(
                    user_id=user_id,
                    followers=0, following=0, likes=0, videos=0,
                    success=False,
                    error=f"HTTP {response.status_code}"
                )
            
            data = response.json()
            
            if not data.get('success'):
                return UserStats(
                    user_id=user_id,
                    followers=0, following=0, likes=0, videos=0,
                    success=False,
                    error="User not found or API error"
                )
            
            return UserStats(
                user_id=user_id,
                followers=data.get('followerCount', 0),
                following=data.get('followingCount', 0),
                likes=data.get('heartCount', 0),
                videos=data.get('videoCount', 0),
                success=True
            )
            
        except Exception as e:
            return UserStats(
                user_id=user_id,
                followers=0, following=0, likes=0, videos=0,
                success=False,
                error=str(e)
            )
    
    def compare_stats(self, before: VideoStats, after: VideoStats) -> dict:
        """Compare two VideoStats and return the difference.
        
        Args:
            before: Stats before automation
            after: Stats after automation
            
        Returns:
            Dictionary with deltas for each stat
        """
        return {
            'views_delta': after.views - before.views,
            'likes_delta': after.likes - before.likes,
            'comments_delta': after.comments - before.comments,
            'shares_delta': after.shares - before.shares,
            'favorites_delta': after.favorites - before.favorites,
        }
    
    def format_comparison(self, before: VideoStats, after: VideoStats) -> str:
        """Format a before/after comparison for display.
        
        Args:
            before: Stats before automation
            after: Stats after automation
            
        Returns:
            Formatted string showing changes
        """
        delta = self.compare_stats(before, after)
        
        def format_delta(value: int) -> str:
            if value > 0:
                return f"+{value:,}"
            elif value < 0:
                return f"{value:,}"
            return "0"
        
        lines = [
            "  ╔════════════════════════════════════════╗",
            "  ║       📊 STATS COMPARISON              ║",
            "  ╠════════════════════════════════════════╣",
            f"  ║  👁️  Views:    {before.views:>10,} → {after.views:>10,}  ({format_delta(delta['views_delta']):>8})",
            f"  ║  ❤️  Likes:    {before.likes:>10,} → {after.likes:>10,}  ({format_delta(delta['likes_delta']):>8})",
            f"  ║  💬 Comments: {before.comments:>10,} → {after.comments:>10,}  ({format_delta(delta['comments_delta']):>8})",
            f"  ║  🔁 Shares:   {before.shares:>10,} → {after.shares:>10,}  ({format_delta(delta['shares_delta']):>8})",
            "  ╚════════════════════════════════════════╝",
        ]
        
        return "\n".join(lines)


# Convenience functions
def get_video_stats(url_or_id: str) -> VideoStats:
    """Get video stats (convenience function)."""
    return LivecountsAPI().get_video_stats(url_or_id)


def get_user_stats(url_or_id: str) -> UserStats:
    """Get user stats (convenience function)."""
    return LivecountsAPI().get_user_stats(url_or_id)


if __name__ == "__main__":
    # Test the module
    print("=" * 50)
    print("Livecounts API Test")
    print("=" * 50)
    
    api = LivecountsAPI()
    
    # Test with known video
    test_url = "https://www.tiktok.com/@cc_pz/video/7593834518168063254"
    print(f"\nTesting: {test_url}")
    
    stats = api.get_video_stats(test_url)
    print(f"\n{stats.format_display()}")
    
    if stats.success:
        print(f"\n✅ API working!")
    else:
        print(f"\n❌ API failed: {stats.error}")
