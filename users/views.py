from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .forms import ProfileForm, SkillForm, MessageForm, FeedbackForm, ResetPasswordForm
from .utils import searchProfiles, paginateProfiles


def loginUser(request):
    if request.method == "POST":
        messages.error(request, "username OR password is incorrect")
    return render(request, "users/login_register.html")


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


@login_required(login_url="login")
def userAccount(request):
    profile = request.user.profile

    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {"profile": profile, "skills": skills, "projects": projects}
    return render(request, "users/account.html", context)


@login_required(login_url="login")
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect("account")

    context = {"form": form}
    return render(request, "users/profile_form.html", context)


@login_required(login_url="login")
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, "Skill was added successfully!")
            return redirect("account")

    context = {"form": form}
    return render(request, "users/skill_form.html", context)


@login_required(login_url="login")
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill was updated successfully!")
            return redirect("account")

    context = {"form": form}
    return render(request, "users/skill_form.html", context)


@login_required(login_url="login")
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill was deleted successfully!")
        return redirect("account")

    context = {"object": skill}
    return render(request, "delete_template.html", context)


@login_required(login_url="login")
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {"messageRequests": messageRequests, "unreadCount": unreadCount}
    return render(request, "users/inbox.html", context)


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
            messages.error(request, "failed to process your data, please try again")
    else:
        form = FeedbackForm()
    return render(request, "users/feedback_form.html", {"form": form})
