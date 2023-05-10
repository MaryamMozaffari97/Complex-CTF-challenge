from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.loginUser, name="login"),
    path("reset_password/", views.resetPassword, name="reset_password"),
    path("", views.profiles, name="profiles"),
    path("profile/<str:pk>/", views.userProfile, name="user-profile"),
    path("account/", views.userAccount, name="account"),
    path("edit-account/", views.editAccount, name="edit-account"),
    path("create-skill/", views.createSkill, name="create-skill"),
    path("update-skill/<str:pk>/", views.updateSkill, name="update-skill"),
    path("create-message/<str:pk>/", views.createMessage, name="create-message"),
    path("feedback/", views.createFeedback, name="feedback"),
]
