from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.LoginUserView.as_view(), name="login"),
    path("reset_password/", views.ResetPasswordView.as_view(), name="reset-password"),
    path("", views.ProfileListView.as_view(), name="profiles"),
    path("profiles/<str:pk>/", views.ProfileDetailView.as_view(), name="user-profile"),
    path(
        "create-message/<str:pk>/",
        views.createMessage,
        name="create-message",
    ),
    path("feedback/", views.createFeedback, name="create-feedback"),
]
