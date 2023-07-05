import os
from dotenv import dotenv_values
from googleapiclient.discovery import build
import googleapiclient.errors


def connect_yt(env_secrets):
    api_service_name = "youtube"
    api_version = "v3"

    youtube = build(
        api_service_name, api_version, developerKey=env_secrets["API_KEY"])
    return youtube


def get_video_id(url):
    id = url.rsplit("/")
    return id


def parse_yt_data(youtube, video):
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=video
    )
    response = request.execute()

    all_video_info = {}

    for video in response['items']:
        stats_to_keep = {'snippet': ['channelTitle', 'title', 'description', 'tags', 'publishedAt'],
                         'statistics': ['viewCount', 'likeCount', 'favouriteCount', 'commentCount'],
                         'contentDetails': ['duration', 'definition', 'caption']
                         }
        video_info = {'video_id': video['id']}

        for k in stats_to_keep.keys():
            for v in stats_to_keep[k]:
                try:
                    video_info[v] = video[k][v]
                except:
                    video_info[v] = None

        return video_info


def get_video_info():
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
    secrets = dotenv_values(".env")
    yt = connect_yt(secrets)
    video_url = "https://youtu.be/fPJVkF_9jmI"
    video = get_video_id(video_url)
    parse_yt_data(yt, video)
