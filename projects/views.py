from django.contrib import messages
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from .forms import ReviewForm
from .models import Project
from .utils import paginateProjects, searchProjects


def projects(request):
    projects, search_query = searchProjects(request)
    custom_range, projects = paginateProjects(request, projects, 6)

    context = {
        "projects": projects,
        "search_query": search_query,
        "custom_range": custom_range,
    }
    return render(request, "projects/projects.html", context)


@cache_page(300)
def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            messages.success(request, "Your review was successfully submitted!")

    return render(
        request, "projects/single-project.html", {"project": projectObj, "form": form}
    )
