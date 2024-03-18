from django.urls import reverse_lazy

from main.views import StaffListView, StaffCreateView, StaffUpdateView, StaffDetailView
from monitoring.utils import get_patient_qs_filter
from patient.forms import PatientForm
from patient.models import Patient
from patient.serializers import PatientSerializer


class PatientQuerysetMixin:
    def get_queryset(self):
        qs_filter = get_patient_qs_filter(self.request.user)
        if qs_filter:
            self.queryset = self.model.objects.filter(**qs_filter).prefetch_related('attending_staff')
        else:
            self.queryset = self.model.objects.prefetch_related('attending_staff')
        return super().get_queryset()


class PatientListView(PatientQuerysetMixin, StaffListView):
    model = Patient
    template_name = 'patient/list.html'
    permission_required = 'patient.view_patient'
    search_fields = ['first_name', 'last_name', 'identification']


class PatientCreateView(StaffCreateView):
    model = Patient
    template_name = 'patient/form.html'
    permission_required = 'patient.add_patient'
    form_class = PatientForm
    success_url = reverse_lazy('patient:list')


class PatientUpdateView(PatientQuerysetMixin, StaffUpdateView):
    model = Patient
    template_name = 'patient/form.html'
    permission_required = 'patient.change_patient'
    form_class = PatientForm
    success_url = reverse_lazy('patient:list')


class PatientDetailView(PatientQuerysetMixin, StaffDetailView):
    model = Patient
    template_name = 'patient/detail.html'
    permission_required = 'patient.view_patient'
    serializer_class = PatientSerializer
    sections = {
        'Información personal': ['first_name', 'last_name', 'age', 'identification', 'gender', 'address', 'city'],
        'Información de contacto': ['contact_number', 'emergency_contact_name', 'emergency_contact_number'],
        'Información médica': ['admission_date', 'discharge_date', 'status', 'facility', 'attending_staff',
                                'alarm_settings']}
