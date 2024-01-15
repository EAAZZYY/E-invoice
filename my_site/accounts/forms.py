from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ["username","email","password1","password2"]
        

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name","last_name"]
        labels = {
            "first_name":"Name",
            "last_name":"Surname"
        }

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["phone_number","profile_pix"]
        labels = {"profile_pix":"Picture"}