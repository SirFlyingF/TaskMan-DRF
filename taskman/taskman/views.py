from django.shortcuts import redirect

def landing_view(request):
    if not request.user or not request.user.is_authenticated:
        return redirect('login')
    else:
        return redirect('task-home')