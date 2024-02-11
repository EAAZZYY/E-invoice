from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth.models import User
from .forms import UserEditForm, ProfileEditForm

# Create your views here.

@login_required
def profile(request):
    """
    The page user is redirected to on login,
    does not use any context as all context on template is
    gotten from the globally available request.user context
    """
    return render(request, "accounts/profile.html")

def signup(request):
    """
    Logic to handle new user registration
    """
    if request.method == "POST":
        username=request.POST["username"]
        email=request.POST["email"]
        password=request.POST["password"]
        password2=request.POST["password2"]
        user = User.objects.create_user(username=username,email=email,password=password)
        user.save()        
        
        #message to use for successful reqgistration
        messages.success(request, f"Welcome in {username}")
            
        return redirect("login")

        
    return render(request, "accounts/signup.html", )


@login_required
def editprofile(request):
    """
    Logic to update user profile, user automatically has a profile via post save in signals.py
    """
    user = request.user
    if request.method == "POST":
        """
        passing both Userform and ProfileForm to the same template if method is POST
        """
        user_form = UserEditForm(instance=user, data=request.POST, files=request.FILES)
        profile_form = ProfileEditForm(data=request.POST, files=request.FILES, instance=user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect("profile")
    else:
        user_form = UserEditForm(instance=user)
        profile_form = ProfileEditForm(instance=user.profile)
        context = {
            "user_form":user_form,
            "profile_form":profile_form
        }
        return render(request, "accounts/edit_profile.html", context)