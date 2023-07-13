import os
from googleapiclient.discovery import build


class Video:
    def __init__(self, video_id: str):
        self.__video_id = video_id
        try:
            self.video_response = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                                   id=video_id
                                                                   ).execute()
            if not self.video_response["items"]:
                raise VideoNotFoundError
        except VideoNotFoundError:
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None
        else:
            self.title: str = self.video_response['items'][0]['snippet']['title']
            self.url: str = f"https://www.youtube.com/watch?v={self.__video_id}"
            self.view_count: int = self.video_response['items'][0]['statistics']['viewCount']
            self.like_count: int = self.video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return self.title

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с Youtube API"""
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube


class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        self.__playlist_id = playlist_id

    def __str__(self):
        return self.title


class VideoNotFoundError(Exception):
    pass
