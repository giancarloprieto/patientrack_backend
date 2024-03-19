from main.forms import BaseModelForm
from .models import Staff


class StaffForm(BaseModelForm):
    class Meta:
        model = Staff
        exclude = ('created_at', 'created_by', 'last_updated_at', 'last_updated_by',)
