from django.urls import reverse_lazy

from main.views import StaffListView, StaffCreateView, StaffUpdateView, StaffDetailView
from staff.forms import StaffForm
from staff.models import Staff
from staff.serializers import StaffSerializer


# Create your views here.

class MedicalStaffListView(StaffListView):
    model = Staff
    template_name = 'staff/list.html'
    permission_required = 'staff.view_staff'
    search_fields = ['first_name', 'last_name', 'identification', 'email']

    def get_queryset(self):
        # if self.request.user.is_staff:
        #     queryset = self.model.objects.filter(attending_staff__user=self.request.user)
        # else:
        #     queryset = self.model.objects.all()
        self.queryset = self.model.objects.prefetch_related('staff_patient_set')
        return super().get_queryset()


class MedicalStaffCreateView(StaffCreateView):
    model = Staff
    template_name = 'staff/form.html'
    permission_required = 'staff.add_staff'
    form_class = StaffForm
    success_url = reverse_lazy('staff:list')


class MedicalStaffUpdateView(StaffUpdateView):
    model = Staff
    template_name = 'staff/form.html'
    permission_required = 'staff.change_staff'
    form_class = StaffForm
    success_url = reverse_lazy('staff:list')


class MedicalStaffDetailView(StaffDetailView):
    model = Staff
    template_name = 'staff/detail.html'
    permission_required = 'staff.view_staff'
    serializer_class = StaffSerializer
    sections = {'personal information': ['first_name', 'last_name', 'identification', 'gender', 'address', 'city',
                                         'contact_number', 'date_of_birth', 'email'],
                'employee information': ['hire_date', 'specialization', 'is_active', 'facility', 'user',
                                         'patients_in_charge']}

    def get_queryset(self):
        # if self.request.user.is_staff:
        #     queryset = self.model.objects.filter(attending_staff__user=self.request.user)
        # else:
        #     queryset = self.model.objects.all()
        self.queryset = self.model.objects.prefetch_related('staff_patient_set')
        return super().get_queryset()
