from django.urls import reverse

from main.views import StaffCreateView, StaffListView, StaffDetailView
from report.excel_generator import generate_excel_report
from report.forms import RecordReportForm
from report.models import RecordReport
from report.serializers import RecordReportSerializer


# Create your views here.

class RecordReportCreateView(StaffCreateView):
    model = RecordReport
    template_name = 'report/form.html'
    permission_required = 'report.add'
    form_class = RecordReportForm

    def get_success_url(self):
        return reverse('report:detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.created_by = self.request.user.email
        response = super().form_valid(form)
        generate_excel_report(self.object.id)  # Assuming the function accepts a RecordReport instance
        return response


class RecordReportListView(StaffListView):
    model = RecordReport
    template_name = 'report/list.html'
    permission_required = 'report.list'
    search_fields = ['created_by', 'patient__first_name', 'patient__last_name']


class RecordReportDetailView(StaffDetailView):
    model = RecordReport
    template_name = 'report/detail.html'
    permission_required = 'report.view'
    serializer_class = RecordReportSerializer
    sections = {'Report Status': ['created_by', 'created_at', 'patient', 'variables', 'status', 'file', 'error']}
