from django.shortcuts import redirect, render, HttpResponse, Http404
from django.http import FileResponse
import os
from django.conf import settings

def landing_view(request):
    if not request.user or not request.user.is_authenticated:
        return redirect('login')
    else:
        return redirect('task-home')
    

# def serve_media(request, path):
#     file_path = os.path.join(settings.MEDIA_ROOT, path)
#     if os.path.exists(file_path):
#         with open(file_path, 'rb') as file:
#             return HttpResponse(file.read(), content_type="image/jpeg")
#     else:
#         raise Http404("Image does not exist")