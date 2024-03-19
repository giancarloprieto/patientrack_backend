from main.forms import BaseModelForm
from .models import RecordReport


class RecordReportForm(BaseModelForm):
    class Meta:
        model = RecordReport
        fields = ('patient', 'variables', 'start_datetime', 'end_datetime')
