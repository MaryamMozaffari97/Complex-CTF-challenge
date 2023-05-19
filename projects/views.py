from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.generic import ListView

from .forms import ReviewForm
from .models import Project

CACHE_TTL = 300


class ProjectListView(ListView):
    model = Project
    template_name = "projects/projects.html"
    paginate_by = 6
    context_object_name = "projects"

    def get_queryset(self):
        search_query = self.request.GET.get("search_query", "")
        projects = Project.objects.filter(
            Q(title__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(owner__name__icontains=search_query)
            | Q(tags__name__icontains=search_query)
        ).distinct()
        return projects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("search_query", "")
        return context

    def dispatch(self, *args, **kwargs):
        return cache_page(CACHE_TTL)(super(ProjectListView, self).dispatch)(
            *args, **kwargs
        )


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
