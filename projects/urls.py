from django.urls import path

from . import views

urlpatterns = [
    path("", views.ProjectListView.as_view(), name="projects"),
    path("<str:pk>/", views.project, name="project"),
]
