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


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ["name", "email", "subject", "body"]

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})


class FeedbackForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2, message="Name must be at least 2 characters long."),
            MaxLengthValidator(30, message="Name cannot exceed 100 characters."),
        ],
    )
    email = forms.EmailField(
        validators=[
            MinLengthValidator(5, message="Email must be at least 5 characters long."),
            MaxLengthValidator(254, message="Email cannot exceed 254 characters."),
        ]
    )
    message = forms.CharField(
        widget=forms.Textarea,
        validators=[
            MinLengthValidator(
                10, message="Message must be at least 10 characters long."
            ),
            MaxLengthValidator(5000, message="Message cannot exceed 5000 characters."),
        ],
    )
    image = forms.FileField(
        validators=[
            FileExtensionValidator(
                allowed_extensions=["svg"], message="Only 'svg' file format is allowed."
            )
        ],
        help_text="You can upload an SVG image file along with your feedback. This is useful for providing a screenshot or diagram to help explain your issue.",
    )


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(
        validators=[
            MinLengthValidator(5, message="Email must be at least 5 characters long."),
            MaxLengthValidator(254, message="Email cannot exceed 254 characters."),
        ]
    )
