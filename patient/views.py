from django.urls import reverse_lazy

from main.views import StaffListView, StaffCreateView
from patient.forms import PatientForm
from patient.models import Patient


# Create your views here.

class PatientListView(StaffListView):
    model = Patient
    template_name = 'patient/list.html'
    permission_required = 'patient.list'
    search_fields = ['first_name', 'last_name', 'identification']

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = self.model.objects.all()
        elif self.request.user.is_staff:
            queryset = self.model.objects.filter(attending_staff__user=self.request.user)
        elif self.request.user.is_patient:
            queryset = self.model.objects.filter(user=self.request.user)

        self.queryset = queryset.prefetch_related('attending_staff')
        return super().get_queryset()


class PatientCreateView(StaffCreateView):
    model = Patient
    template_name = 'patient/create.html'
    permission_required = 'patient.add'
    form_class = PatientForm
    success_url = reverse_lazy('patient:list')

