from django import forms

from monitoring.models import AlarmSettings


class AlarmSettingsForm(forms.ModelForm):
    class Meta:
        model = AlarmSettings
        fields = ['variable', 'name', 'reference_value', 'operator']
