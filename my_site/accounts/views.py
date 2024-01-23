from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserEditForm, ProfileEditForm

# Create your views here.

@login_required
def profile(request):
    
    return render(request, "accounts/profile.html")

def signup(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            messages.success(request, f"Welcome in {username}")
            form.save()
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "accounts/signup.html", {"form":form})

def editprofile(request):
    user = request.user
    if request.method == "POST":
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