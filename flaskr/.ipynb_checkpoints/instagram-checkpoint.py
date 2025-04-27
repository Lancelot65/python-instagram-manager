import json
import httpx
from datetime import datetime
import os
import random

USER_AGENTS = [
    # Chrome - Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.86 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.94 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.140 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.224 Safari/537.36",
    
    # Firefox - Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
    
    # Chrome - macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.86 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_7_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.85 Safari/537.36",

    # Safari - macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Safari/605.1.15",

    # Chrome - Android
    "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.86 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.94 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Redmi Note 10 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.85 Mobile Safari/537.36",
    
    # Firefox - Android
    "Mozilla/5.0 (Android 13; Mobile; rv:124.0) Gecko/124.0 Firefox/124.0",
    "Mozilla/5.0 (Android 12; Mobile; rv:123.0) Gecko/123.0 Firefox/123.0",
    
    # Safari - iOS
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
]


class Instagram:
    def __init__(self, username):
        self.username = username
        self.client = httpx.Client(
            headers={
                "x-ig-app-id": "936619743392459",
                "User-Agent": random.choice(USER_AGENTS),
                "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept": "*/*",
            }
        )

    def add_user(self):
        if os.path.exists(os.path.join(os.path.dirname(__file__), f"static/profiles/{self.username}.json")):
            raise Exception("Profile already exists")
        else:
            self.data = None
            self.scrape_user()
            self.save_user()

    def update_user(self):
        if not os.path.exists(os.path.join(os.path.dirname(__file__), f"static/profiles/{self.username}.json")):
            raise Exception("Profile does not exist")
        else:
            self.data = None
            self.scrape_user()
            self.save_user()

    def scrape_user(self):
        try:
            result = self.client.get(
                f"https://i.instagram.com/api/v1/users/web_profile_info/?username={self.username}",
            )
            if result.status_code == 200:
                data = json.loads(result.content)
                if "data" in data and "user" in data["data"]:
                    self.data = data["data"]["user"]
                else:
                    raise KeyError("The expected keys 'data' or 'user' are missing in the API response.")
            else:
                raise ValueError(f"Instagram API request failed with status code {result.status_code}")
        except (json.JSONDecodeError, KeyError) as e:
            raise ValueError("Failed to parse Instagram API response") from e

    def save_user(self):
        """Save Instagram user's data to a file"""
        if self.data:
            creator_folder = os.path.join(os.path.dirname(__file__), "static/profiles/")
            os.makedirs(creator_folder, exist_ok=True)
            file_path = os.path.join(creator_folder, f"{self.username}.json")

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(self.profiles_data(self.data), f, ensure_ascii=False, indent=4)
            self.update_database()
        else:
            raise ValueError("No user data available to save.")

    def update_database(self):
        if self.data:
            creator_folder = os.path.join(os.path.dirname(__file__), "static/data/")
            os.makedirs(creator_folder, exist_ok=True)
            file_path = os.path.join(creator_folder, f"{self.username}.json")
            old_data = []
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    old_data = json.load(f)

            # Append new data to old data
            old_data.append(self.chart_data(self.data))

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(old_data, f, ensure_ascii=False, indent=4)
        else:
            raise ValueError("No user data available to save.")

    @staticmethod
    def profiles_data(data):
        temp = {
            "biography": data.get("biography", ""),
            "follow": data.get("edge_follow", {}).get("count", 0),
            "follower": data.get("edge_followed_by").get("count", 0),
            "username": data.get("username", ""),
            "profile_picture": data.get("profile_pic_url", ""),
            "profile_picture_hd": data.get("profile_pic_url_hd", ""),
            "total_media": data.get("edge_owner_to_timeline_media", {}).get("count", 0),
            "last_download" : datetime.now().strftime("%y.%m.%d %H:%M:%S"),
        }
        return temp

    @staticmethod
    def chart_data(data):
        temp = {
            "follow":  data.get("edge_follow", {}).get("count", 0),
            "follower": data.get("edge_followed_by", {}).get("count", 0),
            "reel": [
            {
                "view": reel["node"].get("video_view_count", 0),
                "comment": reel["node"].get("edge_media_to_comment", {}).get("count", 0),
                "like": reel["node"].get("edge_media_preview_like", {}).get("count", 0),
                "quality": {
                "is_eligible": reel["node"].get("dash_info", {}).get("is_dash_eligible", False),
                "number_of_qualities": reel["node"].get("dash_info", {}).get("number_of_qualities", 0),
                },
            }
            for reel in data.get("edge_owner_to_timeline_media", {}).get("edges", [])
            ],
            "time": datetime.now().strftime("%y.%m.%d %H:%M:%S"),

        }
        return temp