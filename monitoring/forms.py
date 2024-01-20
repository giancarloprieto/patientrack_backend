from main.forms import BaseModelForm
from monitoring.models import AlarmSettings


class AlarmSettingsForm(BaseModelForm):
    class Meta:
        model = AlarmSettings
        fields = ['variable', 'name', 'reference_value', 'operator']
