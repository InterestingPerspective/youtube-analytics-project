from src.channel import Channel


class Video(Channel):
    def __init__(self, video_id: str):
        self.__video_id = video_id
        self.video_response = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                               id=self.__video_id
                                                               ).execute()
        super().__init__(channel_id=self.video_response['items'][0]['snippet']['channelId'])
        self.video_title: str = self.video_response['items'][0]['snippet']['title']
        self.video_url: str = f"https://www.youtube.com/watch?v={self.__video_id}"
        self.view_count: int = self.video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = self.video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return self.video_title


class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        self.__playlist_id = playlist_id

    def __str__(self):
        return self.video_title
