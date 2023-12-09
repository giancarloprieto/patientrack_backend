from django import forms
from django.forms import ModelForm, ClearableFileInput
from django.utils.translation import gettext_lazy as _

from authentication.models import User


class RegisterForm(ModelForm):
    password1 = forms.CharField(
        label=_('Password'),
        required=True
    )

    password2 = forms.CharField(
        label=_('Password confirmation'),
        required=True
    )

    def clean_email(self):
        return self.cleaned_data['email'].lower()

    def clean_first_name(self):
        return self.cleaned_data['first_name'].capitalize()

    def clean_last_name(self):
        return self.cleaned_data['last_name'].capitalize()

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password1', True) != cleaned_data.get('password2', False):
            self.add_error('password1', _("The two password fields didn't match."))

    def save(self, commit=True):
        username = self.instance.email.split('@')[0]
        if not User.objects.filter(username=username).exists():
            self.instance.username = username
        else:
            self.instance.username = self.instance.email
        instance = super().save(commit)
        instance.set_password(self.cleaned_data["password1"])
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")


class ProfileForm(ModelForm):
    picture = forms.ImageField(
        label=_('Picture'),
        required=False,
        widget=ClearableFileInput(),
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "picture")
