from django.contrib import messages
from django.db.models import Prefetch, Q
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, ListView

from .forms import FeedbackForm, MessageForm, ResetPasswordForm
from .models import Profile, Skill
from .utils import parse_image


@cache_page(900)
def loginUser(request):
    if request.method == "POST":
        messages.error(request, "username OR password is incorrect")
    return render(request, "users/login_form.html")


class ProfileListView(ListView):
    model = Profile
    template_name = "users/profiles.html"
    paginate_by = 6
    context_object_name = "profiles"

    def get_queryset(self):
        search_query = self.request.GET.get("search_query", "")
        profiles = Profile.objects.filter(
            Q(name__icontains=search_query) | Q(short_intro__icontains=search_query)
        ).distinct()

        return profiles

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("search_query", "")
        return context

    @method_decorator(cache_page(300))
    def dispatch(self, *args, **kwargs):
        return super(ProfileListView, self).dispatch(*args, **kwargs)


class ProfileDetailView(DetailView):
    model = Profile
    template_name = "users/user-profile.html"

    def get_queryset(self):
        return Profile.objects.prefetch_related(
            Prefetch(
                "skill_set",
                queryset=Skill.objects.exclude(description__exact=""),
                to_attr="top_skills",
            ),
            Prefetch(
                "skill_set",
                queryset=Skill.objects.filter(description=""),
                to_attr="other_skills",
            ),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["topSkills"] = self.object.top_skills
        context["otherSkills"] = self.object.other_skills
        return context

    @method_decorator(cache_page(300))
    def dispatch(self, *args, **kwargs):
        return super(ProfileDetailView, self).dispatch(*args, **kwargs)


@cache_page(900)
def resetPassword(request):
    form = ResetPasswordForm()
    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            messages.success(
                request,
                "We sent password instructions to your email. Check spam or use correct address if not received.",
            )
    return render(request, "users/reset_password.html", context={"form": form})


@cache_page(900)
def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            messages.success(request, "Your message was successfully sent!")

    return render(
        request,
        "users/message_form.html",
        context={"recipient": recipient, "form": form},
    )


@cache_page(900)
def createFeedback(request):
    form = FeedbackForm()
    if request.method == "POST":
        form = FeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data["image"]
            try:
                if image and image.content_type == "image/svg+xml":
                    parse_image(image)
            except ValueError as exc:
                messages.error(
                    request,
                    "an error occured during processing your feedback, please try again.",
                )
            else:
                messages.success(request, "Thank you for your feedback!")
    return render(request, "users/feedback_form.html", {"form": form})
