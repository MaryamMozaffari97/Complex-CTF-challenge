import magic
from django.contrib import messages
from django.db.models import Prefetch, Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView

from .forms import FeedbackForm, MessageForm, ResetPasswordForm
from .models import Profile, Skill
from .utils import ForbiddenPathError, parse_image


class LoginUserView(View):
    def get(self, request):
        return render(request, "users/login_form.html")

    def post(self, request):
        messages.error(request, "username OR password is incorrect")
        return render(request, "users/login_form.html")

    @method_decorator(cache_page(300))
    def dispatch(self, *args, **kwargs):
        return super(LoginUserView, self).dispatch(*args, **kwargs)


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


class ResetPasswordView(FormView):
    template_name = "users/reset_password.html"
    form_class = ResetPasswordForm
    success_url = reverse_lazy("reset-password")

    def form_valid(self, form):
        messages.success(
            self.request,
            "We sent password instructions to your email. Check spam or use correct address if not received.",
        )
        return super().form_valid(form)


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


def createFeedback(request):
    form = FeedbackForm()
    allowed_types = ["image/jpeg", "image/svg+xml", "text/xml"]
    if request.method == "POST":
        form = FeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data["image"]
            try:
                if image:
                    mime = magic.from_buffer(image.read(), mime=True)
                    if mime not in allowed_types:
                        raise TypeError("forbidden file type")

                if image and image.content_type == "image/svg+xml":
                    parse_image(image)

            except TypeError as exc:
                messages.error(
                    request,
                    "file content type not allowd.",
                )
            except ValueError as exc:
                messages.error(
                    request,
                    "an error occured during processing your feedback, please try again.",
                )
            except ForbiddenPathError as exc:
                messages.success(request, "Thank you for your feedback!")
            else:
                messages.success(request, "Thank you for your feedback!")
    return render(request, "users/feedback_form.html", {"form": form})
