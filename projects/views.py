from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Project
from .forms import ReviewForm
from .utils import searchProjects, paginateProjects


def projects(request):
    projects, search_query = searchProjects(request)
    custom_range, projects = paginateProjects(request, projects, 6)

    context = {
        "projects": projects,
        "search_query": search_query,
        "custom_range": custom_range,
    }
    return render(request, "projects/projects.html", context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()

        projectObj.getVoteCount

        messages.success(request, "Your review was successfully submitted!")
        return redirect("project", pk=projectObj.id)

    return render(
        request, "projects/single-project.html", {"project": projectObj, "form": form}
    )
