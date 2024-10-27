from django.shortcuts import render
from tracer import settings

def index(request):
    index_video_url = f"{settings.MEDIA_URL}AAA_index/range_index.mp4"
    return render(request, 'index.html', {'index_video_url': index_video_url})