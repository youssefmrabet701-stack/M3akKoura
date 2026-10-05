from django.urls import path
from api.views import pick_topic,get_teams,search_videos,download_videos,analyze_video

urlpatterns = [
    path("pick-topic", pick_topic),
    path("get-teams", get_teams),
    path("search-videos", search_videos),
    path("download-videos", download_videos),
    path("analyze-video", analyze_video)
]