from src.channel import Channel


class Video(Channel):

    def __init__(self, video_id):
        self.__video_id = video_id
        video_response = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails', id=video_id).execute()
        self.title = str(video_response['items'][0]['snippet']['title'])
        self.url = f"https://youtu.be/{self.__video_id}"
        self.view_count = int(video_response['items'][0]['statistics']['viewCount'])
        self.like_count = int(video_response['items'][0]['statistics']['likeCount'])

    def __str__(self):
        return f"{self.title}"

    @property
    def channel_id(self):
        return self.__video_id


class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
        self.get_service().playlistItems().list(playlistId=playlist_id, part='contentDetails', maxResults=50).execute()