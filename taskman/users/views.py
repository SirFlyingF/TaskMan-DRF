from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from .forms import UserRegisterForm 

# Create your views here.

def register(request):
    match request.method:
        case 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f"Successfully created {username}")
                return redirect('task-home')
        case 'GET':
            form = UserRegisterForm()
            return render(request, "users/register.html", {"form":form})