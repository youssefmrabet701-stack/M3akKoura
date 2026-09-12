import requests
import os
from dotenv import load_dotenv

def search_videos(query):
    url = "https://www.googleapis.com/youtube/v3/search"
    load_dotenv()
    key = os.getenv('YOUTUBE_API_KEY')
    response = requests.get(url, params={"key": key ,"part": "snippet","type":"video","q":query})
    data = response.json()
    return data
def get_video_ids(data):
    video_ids = []
    for item in data["items"]:
        x = item["id"]["kind"]
        if x =="youtube#video":
            video_ids.append(item["id"]["videoId"]) 
    return video_ids

def get_view_counts(video_ids):
    load_dotenv()
    id = ",".join(video_ids)
    key = os.getenv('YOUTUBE_API_KEY')
    part = "statistics"
    url = "https://www.googleapis.com/youtube/v3/videos"
    response = requests.get(url, params={"key": key ,"part": part,"id":id})
    return response.json()

def get_most_popular(data):
    scores={}
    for i in data["items"]:
        scores[i["id"]] = int(i["statistics"]["viewCount"])
    return sort_by_views(scores)

def sort_by_views(data):
    return sorted(data.items(),key = lambda x: x[1],reverse=True)
    
def get_ranked_videos(player):
    data = search_videos(player)
    video_ids = get_video_ids(data)
    view_data = get_view_counts(video_ids)
    return get_most_popular(view_data)