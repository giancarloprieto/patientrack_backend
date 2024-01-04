from django import forms

from .models import RecordReport


class RecordReportForm(forms.ModelForm):
    class Meta:
        model = RecordReport
        fields = ('patient', 'variables', 'start_datetime', 'end_datetime')
