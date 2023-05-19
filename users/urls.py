from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.loginUser, name="login"),
    path("reset_password/", views.resetPassword, name="reset_password"),
    path("", views.profiles, name="profiles"),
    path("profiles/<str:pk>/", views.userProfile, name="user-profile"),
    path("create-message/<str:pk>/", views.createMessage, name="create-message"),
    path("feedback/", views.createFeedback, name="feedback"),
]
