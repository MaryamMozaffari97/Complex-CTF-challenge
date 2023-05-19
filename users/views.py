from django.contrib import messages
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from .forms import FeedbackForm, MessageForm, ResetPasswordForm
from .models import Profile
from .utils import paginateProfiles, parse_image, searchProfiles


def loginUser(request):
    if request.method == "POST":
        messages.error(request, "username OR password is incorrect")
    return render(request, "users/login_form.html")


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


def profiles(request):
    profiles, search_query = searchProfiles(request)

    custom_range, profiles = paginateProfiles(request, profiles, 3)
    context = {
        "profiles": profiles,
        "search_query": search_query,
        "custom_range": custom_range,
    }
    return render(request, "users/profiles.html", context)


@cache_page(300)
def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)

    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")

    context = {"profile": profile, "topSkills": topSkills, "otherSkills": otherSkills}
    return render(request, "users/user-profile.html", context)


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
    if request.method == "POST":
        form = FeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data["image"]
            try:
                if image.content_type == "image/svg+xml":
                    parse_image(image)
            except ValueError as exc:
                print(exc)
                messages.error(
                    request,
                    "an error occured during processing your feedback, please try again.",
                )
            else:
                messages.success(request, "Thank you for your feedback!")
    return render(request, "users/feedback_form.html", {"form": form})
