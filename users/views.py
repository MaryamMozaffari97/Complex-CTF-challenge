from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Prefetch
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from .forms import FeedbackForm, MessageForm, ResetPasswordForm
from .models import Profile, Skill
from .utils import parse_image, searchProfiles


@cache_page(900)
def loginUser(request):
    if request.method == "POST":
        messages.error(request, "username OR password is incorrect")
    return render(request, "users/login_form.html")


def profiles(request):
    profiles, search_query = searchProfiles(request)

    paginator = Paginator(profiles, 3)
    page = request.GET.get("page")

    try:
        paginated_profiles = paginator.page(page)
    except PageNotAnInteger:
        paginated_profiles = paginator.page(1)
    except EmptyPage:
        paginated_profiles = paginator.page(paginator.num_pages)

    context = {
        "profiles": paginated_profiles,
        "search_query": search_query,
    }
    return render(request, "users/profiles.html", context)


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
def userProfile(request, pk):
    profile = Profile.objects.prefetch_related(
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
    ).get(id=pk)

    topSkills = profile.top_skills
    otherSkills = profile.other_skills

    context = {"profile": profile, "topSkills": topSkills, "otherSkills": otherSkills}
    return render(request, "users/user-profile.html", context)


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
