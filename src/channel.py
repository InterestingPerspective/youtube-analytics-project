import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self._title = self.channel["items"][0]["snippet"]["title"]
        self.description = self.channel["items"][0]["snippet"]["description"]
        self._url = f"https://www.youtube.com/channel/{self.__channel_id}"
        self.sub_count = int(self.channel["items"][0]["statistics"]["subscriberCount"])
        self.video_count = int(self.channel["items"][0]["statistics"]["videoCount"])
        self.view_count = int(self.channel["items"][0]["statistics"]["viewCount"])

    def __str__(self):
        return f"{self._title} ({self._url})"

    def __add__(self, other):
        return self.sub_count + other.sub_count

    def __sub__(self, other):
        return self.sub_count - other.sub_count

    def __lt__(self, other):
        return self.sub_count < other.sub_count

    def __le__(self, other):
        return self.sub_count <= other.sub_count

    def __gt__(self, other):
        return self.sub_count > other.sub_count

    def __ge__(self, other):
        return self.sub_count >= other.sub_count

    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с Youtube API"""
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def to_json(self, filename):
        """Сохраняет в файл значения атрибутов экземпляра Channel"""
        with open(filename, "w", encoding="utf-8") as file:
            json.dump({"id": self.__channel_id, "title": self._title, "description": self.description, "url": self._url,
                       "sub_count": self.sub_count, "video_count": self.video_count, "view_count": self.view_count},
                      file, indent=4, ensure_ascii=False)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()

        print(json.dumps(channel, indent=2, ensure_ascii=False))
