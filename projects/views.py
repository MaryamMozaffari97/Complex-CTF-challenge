from django.contrib import messages
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, ListView

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

    @method_decorator(cache_page(300))
    def dispatch(self, *args, **kwargs):
        return super(ProjectListView, self).dispatch(*args, **kwargs)


class ProjectDetailView(DetailView):
    model = Project
    template_name = "projects/single-project.html"
    context_object_name = "project"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ReviewForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ReviewForm(request.POST)
        if form.is_valid():
            messages.success(request, "Your review was successfully submitted!")
        return self.render_to_response(self.get_context_data(form=form))

    @method_decorator(cache_page(300))
    def dispatch(self, *args, **kwargs):
        return super(ProjectDetailView, self).dispatch(*args, **kwargs)
