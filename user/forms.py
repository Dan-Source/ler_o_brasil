# myapp/forms.py
from django import forms
from django.utils.translation import gettext_lazy as _
from wagtail.users.forms import UserCreationForm, UserEditForm


class CustomUserEditForm(UserEditForm):
    # Use ModelForm's automatic form fields generation for the model's `country` field,
    class Meta(UserEditForm.Meta):
        fields = UserEditForm.Meta.fields | {"country"}


class CustomUserCreationForm(UserCreationForm):
    # Use ModelForm's automatic form fields generation for the model's `country` field,
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields | {"country"}
