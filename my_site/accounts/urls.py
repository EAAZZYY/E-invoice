from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path("signup/", views.signup,name="signup"),
    path("profile/",views.profile, name="profile"),
    path("edit_profile/", views.editprofile,name="edit_profile"),
    path("login/",auth_views.LoginView.as_view(template_name="accounts/login.html"),name="login"),
    path("logout/",auth_views.LogoutView.as_view(template_name="accounts/logout.html"), name="logout"),
    path("password_change/",auth_views.PasswordChangeView.as_view(template_name="accounts/password_change.html"), name="password_change"),
    path("password_change/done/",auth_views.PasswordChangeDoneView.as_view(template_name="accounts/password_change_done.html"), name="password_change_done"),
    path("password_reset",auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),name="password_reset"),
    path("password_reset/done/",auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"),name="password_reset_done"),
    path("reset_confirm/<uidb64>/<token>",auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"),name="password_reset_confirm"),
    path("password_reset_complete/",auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"),name="password_reset_complete")
]