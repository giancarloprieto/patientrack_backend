from django.urls import reverse_lazy

from main.views import StaffListView, StaffCreateView, StaffUpdateView, StaffDetailView
from patient.forms import PatientForm
from patient.models import Patient
from patient.serializers import PatientSerializer


# Create your views here.

class PatientListView(StaffListView):
    model = Patient
    template_name = 'patient/list.html'
    permission_required = 'patient.view_patient'
    search_fields = ['first_name', 'last_name', 'identification']

    def get_queryset(self):
        # if self.request.user.is_staff:
        #     queryset = self.model.objects.filter(attending_staff__user=self.request.user)
        # else:
        #     queryset = self.model.objects.all()
        self.queryset = self.model.objects.all().prefetch_related('attending_staff')
        return super().get_queryset()


class PatientCreateView(StaffCreateView):
    model = Patient
    template_name = 'patient/form.html'
    permission_required = 'patient.add_patient'
    form_class = PatientForm
    success_url = reverse_lazy('patient:list')


class PatientUpdateView(StaffUpdateView):
    model = Patient
    template_name = 'patient/form.html'
    permission_required = 'patient.change_patient'
    form_class = PatientForm
    success_url = reverse_lazy('patient:list')


class PatientDetailView(StaffDetailView):
    model = Patient
    template_name = 'patient/detail.html'
    permission_required = 'patient.view_patient'
    serializer_class = PatientSerializer
    sections = {'personal information': ['first_name', 'last_name', 'identification', 'gender', 'address', 'city'],
                'contact information': ['contact_number', 'emergency_contact_name', 'emergency_contact_number'],
                'medical information': ['admission_date', 'discharge_date', 'status', 'facility', 'attending_staff',
                                        'alarm_settings']}
