import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id

    @property
    def channel_id(self):
        return self.__channel_id

    @property
    def title(self):
        return self.channel["items"][0]["snippet"]["title"]

    @property
    def description(self):
        return self.channel["items"][0]["snippet"]["description"]

    @property
    def url(self):
        return f"https://www.youtube.com/channel/{self.__channel_id}"

    @property
    def sub_count(self):
        return self.channel["items"][0]["statistics"]["subscriberCount"]

    @property
    def video_count(self):
        return self.channel["items"][0]["statistics"]["videoCount"]

    @property
    def view_count(self):
        return self.channel["items"][0]["statistics"]["viewCount"]

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с Youtube API"""
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    @property
    def channel(self):
        """Возвращает данные о канале по ID"""
        return self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()

    def to_json(self, filename):
        """Сохраняет в файл значения атрибутов экземпляра Channel"""
        with open(filename, "w", encoding="utf-8") as file:
            json.dump({"id": self.__channel_id, "title": self.title, "description": self.description, "url": self.url,
                       "sub_count": self.sub_count, "video_count": self.video_count, "view_count": self.view_count},
                      file, indent=4, ensure_ascii=False)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()

        print(json.dumps(channel, indent=2, ensure_ascii=False))
