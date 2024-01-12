from django import forms

from .models import Staff


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        exclude = ('created_at', 'created_by', 'last_updated_at', 'last_updated_by',)
