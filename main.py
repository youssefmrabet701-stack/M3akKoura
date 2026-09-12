from pipeline.research.topic import get_player
from pipeline.research.football_api import get_confirmed_teams
from pipeline.research.popularity import get_ranked_videos
from pipeline.research.downloader import download_video
from pipeline.research.vision import analyze_video
import os

if __name__ == "__main__":
    player = get_player()
    teams = get_confirmed_teams(player)
    vids = get_ranked_videos(player)
    size = 0
    l=[]
    for video_id, views in vids:
        path = download_video(video_id)
        if path is not None:
            size +=os.path.getsize(path)
            l.append(path)
        if size > 1_073_741_824:
            break
    vids_moments = {}
    for i in l:
        vids_moments[i]=analyze_video(i)