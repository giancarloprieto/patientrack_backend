from django.db.models import Prefetch
from django.utils import timezone

from device.models import Variable
from main.views import StaffListView
from monitoring.models import Record
from patient.models import Patient


# Create your views here.

class MonitoringView(StaffListView):
    template_name = 'monitoring/list.html'
    permission_required = 'patient.list'
    paginate_by = 100
    model = Patient
    search_fields = ['first_name', 'last_name', 'identification']

    def get_queryset(self):
        datetime_48_hours_ago = timezone.now() - timezone.timedelta(hours=48)
        prefetch_list = [Prefetch(
            'patient_record_set',
            queryset=Record.objects.filter(alarm_name__isnull=False,
                                           datetime_server__gte=datetime_48_hours_ago).order_by('-datetime_server')[:1],
            to_attr='alarms'
        )]

        variables = Variable.objects.only('id')
        for variable in variables:
            prefetch_list.append(
                Prefetch(
                    'patient_record_set',
                    queryset=Record.objects.filter(variable=variable).order_by('-datetime_server')[:1],
                    to_attr=f'latest_{variable.id}_record'
                )
            )

        self.queryset = Patient.objects.prefetch_related(*prefetch_list).all()

        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['variables'] = Variable.objects.all()
        return context
