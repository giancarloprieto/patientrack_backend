from django.shortcuts import render

from main.views import StaffListView
from patient.models import Patient


# Create your views here.

class PatientListView(StaffListView):
    model = Patient
    paginate_by = 100
    template_name = 'patient/list.html'
    permission_required = 'patient.list'


