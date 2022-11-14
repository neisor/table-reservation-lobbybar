from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("change_password/", change_password, name="change_password"),
    # path("register/", register_user, name="register"),
    
    # Password reset paths:
    path(
        "reset_password/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset.html",
            subject_template_name="accounts/password_reset_subject.txt",
            email_template_name="accounts/password_reset_email.html",
        ),
        name="reset_password",
    ),
    path(
        "reset_password_sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_sent.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_form.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset_done.html"
        ),
        name="password_reset_complete",
    ),
]

"""
1 - Submit email form  //PasswordResetView.as_view()
2 - Email sent success message  //PasswordResetDoneView.as_view()
3 - Link to password reset form in email  //PasswordResetConfirmView.as_view()
4 - Password successfully changed message  //PasswordResetCompleteView.as_view()
"""
