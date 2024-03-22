from django.shortcuts import redirect, render, HttpResponse
from django.http import FileResponse
import os

def landing_view(request):
    if not request.user or not request.user.is_authenticated:
        return redirect('login')
    else:
        return redirect('task-home')
    

def serve_media(request, path):
    try:
        with open(path, 'rb') as f:
            respons = FileResponse(f, content_type='application/octet-stream')
            respons['Content-Disposition'] = f'attachment; filename="{os.path.basename(path)}"'
        return respons
    except Exception as e:
        print(e)
