from pipeline.research.topic import get_player
from pipeline.research.football_api import get_player_teams
from pipeline.research.popularity import get_ranked_videos
from pipeline.research.downloader import download_video
from pipeline.research.vision import analyze_video
import os

if __name__ == "__main__":
    player = get_player()
    print("PLAYER:", player)

    teams = get_player_teams(player)
    print("TEAMS:", teams)

    vids = get_ranked_videos(player, teams)
    print("RANKED VIDEOS:", vids)

    size = 0
    l = []
    for video_id, views in vids:
        path = download_video(video_id)
        print("DOWNLOADED:", video_id, "->", path)
        if path is not None:
            size += os.path.getsize(path)
            l.append(path)
        print("RUNNING SIZE:", size)
        if size > 1_073_741_824:
            break

    print("FINAL DOWNLOADED PATHS:", l)

    vids_moments = {}
    for i in l:
        print("ANALYZING:", i)
        vids_moments[i] = analyze_video(i)
        print("MOMENTS:", vids_moments[i])