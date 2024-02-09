from django.urls import path

# Django inbuilt views
from django.contrib.auth import views as auth_views

# custom views
from . import views



urlpatterns = [
    # Signup, Login and Logout Urls
    path("signup/", views.signup,name="signup"),

    # Django inbuilt views were used for Login and Logout
    path("login/",auth_views.LoginView.as_view(template_name="accounts/login.html"),name="login"),
    path("logout/",auth_views.LogoutView.as_view(template_name="accounts/logout.html"), name="logout"),
    
    # Password change views are from django inbuilt auth views
    path("password_change/",auth_views.PasswordChangeView.as_view(template_name="accounts/password_change.html"), name="password_change"),
    path("password_change/done/",auth_views.PasswordChangeDoneView.as_view(template_name="accounts/password_change_done.html"), name="password_change_done"),
    
    # Password reset views are from django inbuilt auth views
    path("password_reset",auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),name="password_reset"),
    path("password_reset/done/",auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"),name="password_reset_done"),
    path("reset_confirm/<uidb64>/<token>",auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"),name="password_reset_confirm"),
    path("password_reset_complete/",auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"),name="password_reset_complete"),
    
    # Profile and Edit Profile urls
    path("profile/",views.profile, name="profile"),
    path("edit_profile/", views.editprofile,name="edit_profile"),
]