import datetime
from src.channel import Channel


class PlayList(Channel):
    """
    Получить данные по видеороликам в плейлисте
    """

    def __init__(self, playlist_id):
        self.__playlist_id = playlist_id
        self.title = str(self.get_service_playlist()['items'][0]['snippet']['title'].split(".")[0])
        self.url = f"https://www.youtube.com/playlist?list={self.__playlist_id}"

    @property
    def playlist_id(self):
        return self.__playlist_id

    def get_service_playlist(self):
        playlist = self.get_service().playlistItems().list(playlistId=self.__playlist_id, part='contentDetails', maxResults=50).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist['items']]
        video_response = self.get_service().videos().list(part='snippet,contentDetails,statistics', id=','.join(video_ids)).execute()
        return video_response

    @property
    def total_duration(self):
        sum_duration = datetime.timedelta(minutes=0, seconds=0)
        for video in self.get_service_playlist()['items']:
            duration = video['contentDetails']['duration']
            try:
                seconds = int(duration[2:duration.index('M')])*60 + int(duration[duration.index('M')+1:-1])
                delta = datetime.timedelta(seconds=seconds)
                sum_duration += delta
            except ValueError:
                seconds = int(duration[2:duration.index('M')])*60
                delta = datetime.timedelta(seconds=seconds)
                sum_duration += delta

        return sum_duration

    @property
    def show_best_video(self):
        max_likes = 0
        for video in self.get_service_playlist()["items"]:
            if int(video["statistics"]["likeCount"]) > int(max_likes):
                max_likes = video["statistics"]["likeCount"]
                video_id = video["id"]
        return f"https://youtu.be/{video_id}"