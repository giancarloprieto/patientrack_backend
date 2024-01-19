from django.urls import reverse

from main.views import StaffCreateView, StaffListView, StaffDetailView
from monitoring.utils import get_patient_qs_filter
from report.excel_generator import generate_excel_report
from report.forms import RecordReportForm
from report.models import RecordReport
from report.serializers import RecordReportSerializer


class PatientQuerysetMixin:
    def get_queryset(self):
        qs_filter = get_patient_qs_filter(self.request.user, patient_prefix=True)
        if qs_filter:
            self.queryset = self.model.objects.filter(**qs_filter).select_related('patient')
        else:
            self.queryset = self.model.objects.select_related('patient')
        return super().get_queryset()


class RecordReportCreateView(StaffCreateView):
    model = RecordReport
    template_name = 'report/form.html'
    permission_required = 'report.add_recordreport'
    form_class = RecordReportForm

    def get_success_url(self):
        return reverse('report:detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.created_by = self.request.user.email
        response = super().form_valid(form)
        generate_excel_report(self.object.id)
        return response


class RecordReportListView(PatientQuerysetMixin, StaffListView):
    model = RecordReport
    template_name = 'report/list.html'
    permission_required = 'report.view_recordreport'
    search_fields = ['created_by', 'patient__first_name', 'patient__last_name']


class RecordReportDetailView(PatientQuerysetMixin, StaffDetailView):
    model = RecordReport
    template_name = 'report/detail.html'
    permission_required = 'report.view_recordreport'
    serializer_class = RecordReportSerializer
    sections = {'Report Status': ['created_by', 'created_at', 'patient', 'variables', 'status', 'file', 'error']}
