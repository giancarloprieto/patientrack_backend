from main.forms import BaseModelForm
from .models import Patient


class PatientForm(BaseModelForm):
    class Meta:
        model = Patient
        exclude = ('created_at', 'created_by', 'last_updated_at', 'last_updated_by',)
