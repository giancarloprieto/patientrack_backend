from django.db.models import Prefetch
from django.utils import timezone

from device.models import Variable
from followup.models import FollowUp
from main.views import StaffListView, LoggedDetailView
from monitoring.models import Record
from monitoring.utils import get_records_data_for_chart
from patient.models import Patient
from patient.serializers import PatientSerializer
from staff.models import Staff


# Create your views here.

class MonitoringView(StaffListView):
    template_name = 'monitoring/list.html'
    permission_required = 'patient.view_patient'
    paginate_by = 100
    model = Patient
    search_fields = ['first_name', 'last_name', 'identification']

    def get_queryset(self):
        datetime_48_hours_ago = timezone.now() - timezone.timedelta(days=365)
        prefetch_list = [Prefetch(
            'patient_record_set',
            queryset=Record.objects.filter(datetime_device__gte=datetime_48_hours_ago).exclude(alarm_name="").order_by(
                '-datetime_device'),
            to_attr='alarms'
        )]

        variables = Variable.objects.only('id')
        for variable in variables:
            prefetch_list.append(
                Prefetch(
                    'patient_record_set',
                    queryset=Record.objects.filter(variable=variable).order_by('-datetime_device')[:1],
                    to_attr=f'latest_{variable.id}_record'
                )
            )

        self.queryset = self.model.objects.prefetch_related(*prefetch_list).all()

        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['variables'] = Variable.objects.all()
        return context


class PatientMonitoringView(LoggedDetailView):
    model = Patient
    template_name = 'monitoring/detail.html'
    permission_required = 'patient.view_patient'
    serializer_class = PatientSerializer
    sections = {'patient information': ['first_name', 'last_name', 'identification', 'gender', 'address', 'city',
                                        'admission_date', 'discharge_date', 'status', 'facility', 'attending_staff',
                                        'alarm_settings']}
    datetime_48_hours_ago = timezone.now() - timezone.timedelta(days=365)

    def get_variables_data(self):
        variables = Variable.objects.all()
        variables_data = {}
        for variable in variables:
            records = Record.objects.filter(variable=variable, patient=self.object,
                                            datetime_device__gte=self.datetime_48_hours_ago)
            if records:
                variables_data[variable.id] = {
                    'name': variable.name,
                    'unit': variable.unit,
                    'data': get_records_data_for_chart(records)
                }
        return variables_data

    def get_follow_up_data(self):
        entries = FollowUp.objects.filter(patient=self.object).order_by('-created_at')[:50]
        staff = Staff.objects.filter(user__email__in=entries.values('created_by')).select_related('user')
        staff_dict = {st.user.email: {'name': str(st), 'picture_url': st.user.picture.url if st.user.picture else None}
                      for st in staff}
        entries_data = []
        for entry in entries:
            if entry.created_by in staff_dict:
                staff_name = staff_dict[entry.created_by]['name']
                staff_picture = staff_dict[entry.created_by]['picture_url']
            else:
                staff_name = entry.created_by
                staff_picture = None
            entries_data.append(
                {'id': entry.id,
                 'comment': entry.comment,
                 'created_at': entry.created_at,
                 'staff_name': staff_name,
                 'staff_picture': staff_picture,
                 'edit': entry.created_by == self.request.user.email}
            )
        return entries_data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['variables_data'] = self.get_variables_data()
        context['alarms'] = Record.objects.filter(patient=self.object,
                                                  datetime_device__gte=self.datetime_48_hours_ago). \
            exclude(alarm_name="").order_by('-datetime_device')
        context['follow_up'] = self.get_follow_up_data()
        return context
