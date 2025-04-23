import json
import httpx
from datetime import datetime
import os


class Instagram:
    def __init__(self, username):
        self.username = username
        self.client = httpx.Client(
            headers={
                # This is the internal ID of an Instagram backend app. It doesn't change often.
                "x-ig-app-id": "936619743392459",
                # Use browser-like features
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept": "*/*",
            }
        )
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
                    self.data = self.clean_data(data["data"]["user"])
                else:
                    raise KeyError("The expected keys 'data' or 'user' are missing in the API response.")
            else:
                raise ValueError(f"Instagram API request failed with status code {result.status_code}")
        except (json.JSONDecodeError, KeyError) as e:
            raise ValueError("Failed to parse Instagram API response") from e

    def save_user(self):
        """Save Instagram user's data to a file"""
        if self.data:
            creator_folder = os.path.join(os.path.dirname(__file__), f"static/data/{self.data['username']}")
            os.makedirs(creator_folder, exist_ok=True)
            with open(f"{creator_folder}/{self.data['username']}.json", "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
        else:
            raise ValueError("No user data available to save.")

    @staticmethod
    def clean_data(data):
        with open('tets.json', 'w') as file:
            json.dump(data, file)
        temp = {
            "biography": data.get("biography", ""),
            "follow": data.get("edge_follow", {}).get("count", 0),
            "followed": data.get("edge_followed_by").get("count", 0),
            "username": data.get("username", ""),
            "profile_picture": data.get("profile_pic_url", ""),
            "profile_picture_hd": data.get("profile_pic_url_hd", ""),
            "total_media": data.get("edge_owner_to_timeline_media", {}).get("count", 0),
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
            "request_at": datetime.now().strftime("%y.%m.%d"),
        }
        return temp