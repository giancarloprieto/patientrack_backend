from django.db.models import Prefetch, F
from django.urls import reverse_lazy
from django.utils import timezone

from device.models import Variable
from followup.models import FollowUp
from main.views import StaffListView, LoggedDetailView, StaffCreateView, StaffUpdateView
from monitoring.forms import AlarmSettingsForm
from monitoring.models import Record, AlarmSettings
from monitoring.utils import get_records_data_for_chart, get_patient_qs_filter
from patient.models import Patient
from patient.serializers import PatientSerializer
from staff.models import Staff


# Create your views here.

class MonitoringView(StaffListView):
    template_name = 'monitoring/list.html'
    permission_required = 'monitoring.view_record'
    paginate_by = 100
    model = Patient
    search_fields = ['first_name', 'last_name', 'identification']

    def get_queryset(self):
        datetime_48_hours_ago = timezone.now() - timezone.timedelta(days=2)
        prefetch_list = [Prefetch(
            'patient_record_set',
            queryset=Record.objects.filter(datetime_device__gte=datetime_48_hours_ago).exclude(alarm_name="").
            annotate(css_class_suffix=F('variable__css_class_suffix')).order_by(
                '-datetime_device')[:20],
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

        qs_filter = get_patient_qs_filter(self.request.user)
        if qs_filter:
            self.queryset = self.model.objects.filter(**qs_filter).prefetch_related(*prefetch_list).all()
        else:
            self.queryset = self.model.objects.prefetch_related(*prefetch_list).all()
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['variables'] = Variable.objects.all()
        return context


class PatientMonitoringView(LoggedDetailView):
    model = Patient
    template_name = 'monitoring/detail_final.html'
    permission_required = 'monitoring.view_record'
    serializer_class = PatientSerializer
    sections = {'first': ['first_name', 'last_name', 'identification', 'gender'],
                'second': ['address', 'city', 'age', 'staff_a_cargo'],
                'third': ['admission_date', 'status', 'contact_number']}
    datetime_48_hours_ago = timezone.now() - timezone.timedelta(days=2)

    def get_variables_data(self):
        variables = Variable.objects.all()
        variables_data = {}
        for variable in variables:
            records = Record.objects.filter(variable=variable, patient=self.object,
                                            datetime_device__gte=self.datetime_48_hours_ago).order_by('datetime_device')[0:500]
            if records:
                variables_data[variable.id] = {
                    'name': variable.name,
                    'unit': variable.unit,
                    'color': variable.color,
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
            exclude(alarm_name="").select_related('variable').order_by('-datetime_device')[0:50]
        context['follow_up'] = self.get_follow_up_data()
        return context

    def get_queryset(self):
        qs_filter = get_patient_qs_filter(self.request.user)
        if qs_filter:
            self.queryset = self.model.objects.filter(**qs_filter).all()
        else:
            self.queryset = self.model.objects.all()
        return super().get_queryset()


class AlarmSettingsListView(StaffListView):
    model = AlarmSettings
    template_name = 'monitoring/alarm_settings/list.html'
    permission_required = 'monitoring.view_alarmsettings'
    search_fields = ['name']
    active_tab = 'alarm_settings'
    open_menu = 'monitoring'


class AlarmSettingsCreateView(StaffCreateView):
    model = AlarmSettings
    template_name = 'monitoring/alarm_settings/form.html'
    permission_required = 'monitoring.add_alarmsettings'
    form_class = AlarmSettingsForm
    success_url = reverse_lazy('monitoring:alarm_settings_list')
    active_tab = 'alarm_settings'
    open_menu = 'monitoring'


class AlarmSettingsUpdateView(StaffUpdateView):
    model = AlarmSettings
    template_name = 'monitoring/alarm_settings/form.html'
    permission_required = 'monitoring.add_alarmsettings'
    form_class = AlarmSettingsForm
    success_url = reverse_lazy('monitoring:alarm_settings_list')
    active_tab = 'alarm_settings'
    open_menu = 'monitoring'
