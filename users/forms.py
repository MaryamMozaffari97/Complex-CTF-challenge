from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
    FileExtensionValidator,
)
from .models import Profile, Skill, Message


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "email", "username", "password1", "password2"]
        labels = {
            "first_name": "Name",
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
            "name",
            "email",
            "username",
            "location",
            "bio",
            "short_intro",
            "profile_image",
            "social_github",
            "social_linkedin",
            "social_twitter",
            "social_youtube",
            "social_website",
        ]

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = "__all__"
        exclude = ["owner"]

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})


class MessageForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "input", "maxlength": 100, "minlength": 5, "required": True}
        )
    )
    subject = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "input", "maxlength": 100, "minlength": 5, "required": True}
        )
    )
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "input input--textarea",
                "maxlength": 1000,
                "minlength": 10,
                "required": True,
            }
        )
    )


class FeedbackForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "input", "maxlength": 100, "minlength": 5, "required": True}
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "input", "maxlength": 100, "minlength": 5, "required": True}
        )
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "input input--textarea",
                "maxlength": 1000,
                "minlength": 10,
                "required": True,
            }
        )
    )


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "input", "maxlength": 100, "minlength": 5, "required": True}
        )
    )
