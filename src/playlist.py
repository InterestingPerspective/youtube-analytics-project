from src.channel import Channel
import isodate
import datetime


class PlayList(Channel):
    def __init__(self, playlist_id: str):
        self.__playlist_id = playlist_id
        self.playlists = self.get_service().playlists().list(channelId="UC-OVMPlMA3-YCIeg4z5z23A",
                                                             part='contentDetails,snippet',
                                                             maxResults=50,
                                                             ).execute()
        for playlist in self.playlists['items']:
            if playlist['id'] == self.__playlist_id:
                self.title = playlist['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.__playlist_id}"
        super().__init__("UC-OVMPlMA3-YCIeg4z5z23A")

    @property
    def total_duration(self):
        total_dur = datetime.timedelta()
        playlist_videos = self.get_service().playlistItems().list(playlistId=self.__playlist_id,
                                                                  part='contentDetails',
                                                                  maxResults=50,
                                                                  ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                          id=','.join(video_ids)
                                                          ).execute()

        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_dur += duration

        return total_dur

    def show_best_video(self):
        like_count = 0
        video_id = ""
        playlist_videos = self.get_service().playlistItems().list(playlistId=self.__playlist_id,
                                                                  part='contentDetails',
                                                                  maxResults=50,
                                                                  ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                          id=','.join(video_ids)
                                                          ).execute()

        for video in video_response['items']:
            if int(video['statistics']['likeCount']) > like_count:
                like_count = int(video['statistics']['likeCount'])
                video_id = video['id']

        return f"https://youtu.be/{video_id}"
