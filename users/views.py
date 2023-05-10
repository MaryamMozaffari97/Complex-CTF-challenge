from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .forms import ProfileForm, MessageForm, FeedbackForm, ResetPasswordForm
from .utils import searchProfiles, paginateProfiles


def loginUser(request):
    if request.method == "POST":
        messages.error(request, "username OR password is incorrect")
    return render(request, "users/login_form.html")


def resetPassword(request):
    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            messages.success(
                request,
                "We sent password instructions to your email. Check spam or use correct address if not received.",
            )
    else:
        form = ResetPasswordForm()
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


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)

    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")

    context = {"profile": profile, "topSkills": topSkills, "otherSkills": otherSkills}
    return render(request, "users/user-profile.html", context)


def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            messages.success(request, "Your message was successfully sent!")
    else:
        form = MessageForm()

    return render(
        request,
        "users/message_form.html",
        context={"recipient": recipient, "form": form},
    )


def createFeedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            # svg_file = request.FILES["image"]
            # parsing the image
            messages.success(request, "Thank you for your feedback!")
    else:
        form = FeedbackForm()
    return render(request, "users/feedback_form.html", {"form": form})
