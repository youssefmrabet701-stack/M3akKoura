from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from pipeline.research.topic import get_player
from pipeline.research.football_api import get_player_teams
from pipeline.research.popularity import get_ranked_videos
from pipeline.research.downloader import download_video
from pipeline.research.vision import analyze_video as analyze_video_pipeline

# Create your views here.
def pick_topic(request):
    return JsonResponse({"topic" : get_player()})

def get_teams(request):
    player = request.GET.get('topic',None)
    return JsonResponse(get_player_teams(player), safe=False)

def search_videos(request):
    player = request.GET.get('topic',None)
    teams = request.GET.get('teams',"").split(",")
    return JsonResponse(get_ranked_videos(player,teams), safe=False)

def download_videos(request):
    id=request.GET.get('video_id',None)
    result = download_video(id)
    if result:
        return JsonResponse({"path": result},status=200)
    else:
        return JsonResponse({"error": "nothing"}, status=500)

def analyze_video(request):
    path = request.GET.get('path',None)
    return JsonResponse(analyze_video_pipeline(path), safe=False)