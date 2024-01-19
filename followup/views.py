from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse

from followup.forms import FollowUpForm
from followup.models import FollowUp
from main.views import StaffListView, StaffCreateView, StaffUpdateView
from patient.models import Patient


class FollowUpListView(StaffListView):
    model = FollowUp
    template_name = 'monitoring/follow_up/list.html'
    permission_required = 'followup.view_followup'
    search_fields = ['created_by', 'comment']
    ordering = '-created_at'
    active_tab = 'monitoring'
    open_menu = 'monitoring'

    def get_queryset(self):
        # if self.request.user.is_staff:
        #     queryset = self.model.objects.filter(attending_staff__user=self.request.user)
        # else:
        #     queryset = self.model.objects.all()
        self.queryset = self.model.objects.filter(patient=self.kwargs.get('patient_id'))
        return super().get_queryset()


class FollowUpCreateView(StaffCreateView):
    model = FollowUp
    template_name = 'monitoring/follow_up/form.html'
    permission_required = 'followup.add_followup'
    form_class = FollowUpForm
    active_tab = 'monitoring'
    open_menu = 'monitoring'

    def form_valid(self, form):
        patient_id = self.kwargs['patient_id']
        patient = get_object_or_404(Patient, pk=patient_id)
        form.instance.patient = patient
        form.instance.created_by = self.request.user.email
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        patient_id = self.kwargs['patient_id']
        return reverse('monitoring:detail', kwargs={'pk': patient_id})


class FollowUpUpdateView(StaffUpdateView):
    model = FollowUp
    template_name = 'monitoring/follow_up/form.html'
    permission_required = 'followup.change_followup'
    form_class = FollowUpForm
    success_url = reverse_lazy('patient:list')
    active_tab = 'monitoring'
    open_menu = 'monitoring'

    def get_queryset(self):
        self.queryset = self.model.objects.filter(patient_id=self.kwargs['patient_id'],
                                                  created_by=self.request.user.email)
        return super().get_queryset()

    def get_success_url(self):
        patient_id = self.kwargs['patient_id']
        return reverse('monitoring:detail', kwargs={'pk': patient_id})
