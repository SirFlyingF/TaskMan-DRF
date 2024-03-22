from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, UserProfileUpdateForm



# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Successfully Registered! You can now Login")
            return redirect('login')
        else:
            messages.error(request, f'Something went wrong!')
    else: # GET
        form = UserRegisterForm()
    
    return render(request, "users/register.html", {"form":form})


@login_required
def logout_view(request):
    # LogoutView class has been deprecated in django5.
    # Hence used a logout function view
    auth.logout(request)
    return render(request, 'users/logout.html', {})
       

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Saved Successfully')
            return redirect('profile')
        else:
            messages.error(request, f'Something went wrong')
    else: # GET
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileUpdateForm(instance=request.user.userprofile)
    
    context = {
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request, 'users/profile.html', context)

        