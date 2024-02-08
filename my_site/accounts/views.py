from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import RegisterForm
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
    Logic to handle new user registration if request is POST
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            #getting username from submitted form to use for messages
            username = form.cleaned_data.get("username")
            messages.success(request, f"Welcome in {username}")
            form.save()
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "accounts/signup.html", {"form":form})


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