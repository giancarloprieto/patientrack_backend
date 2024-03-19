from django import forms

from main.forms import BaseModelForm
from .models import FollowUp


class FollowUpForm(BaseModelForm):
    class Meta:
        model = FollowUp
        fields = ('comment',)
