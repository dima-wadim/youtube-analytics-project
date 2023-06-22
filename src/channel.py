import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб - канала"""

    def __init__(self, channel_id: str) -> None:
        """
        Экземпляр инициализируется id канала.
        Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        channel_info = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = channel_info["items"][0]["snippet"]["title"]
        self.description = channel_info["items"][0]["snippet"]["description"]
        self.url = f"https://www.youtube.com/channel/{self.__channel_id}"
        self.subs_count = int(channel_info["items"][0]["statistics"]["subscriberCount"])
        self.video_count = channel_info["items"][0]["statistics"]["videoCount"]
        self.view_count = channel_info["items"][0]["statistics"]["viewCount"]

    def __str__(self):
        return f"{self.title} {self.url}"

    def __add__(self, other):
        return self.subs_count + other.subs_count

    def __sub__(self, other):
        return self.subs_count - other.subs_count

    def __lt__(self, other):
        if self.subs_count < other.subs_count:
            return True

    def __le__(self, other):
        if self.subs_count <= other.subs_count:
            return True

    def __gt__(self, other):
        if self.subs_count > other.subs_count:
            return False

    def __ge__(self, other):
        if self.subs_count >= other.subs_count:
            return False

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        api_key: str = os.getenv('API_KEY_YT')
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = youtube.channels()
        channel = channel.list(id=self.__channel_id, part='snippet,statistics')
        channel = channel.execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('API_KEY_YT')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def to_json(self, filename):
        file = f"../src/{filename}"
        with open(file, "w") as f:
            data = {"id": self.__channel_id,
                    "title": self.title,
                    "description": self.description,
                    "url": self.url,
                    "subs_count": self.subs_count,
                    "video_count": self.video_count,
                    "view_count": self.view_count,
                    }
            json.dump(data, f)

    @property
    def channel_id(self):
        return self.__channel_id