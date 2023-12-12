from django import forms

from .models import Patient


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        exclude = ('created_at', 'created_by', 'last_updated_at', 'last_updated_by',)
