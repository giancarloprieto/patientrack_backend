from django.contrib.auth.mixins import PermissionRequiredMixin as OriginalPermissionRequiredMixin, LoginRequiredMixin, \
    AccessMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import DeleteView, FormView, CreateView, UpdateView, DetailView, ListView

from main.messages import DeleteSuccessMessageMixin, SuccessMessageMixin


class StaffRequiredMixin(AccessMixin):
    """ Verifica si el usuario es Staff"""
    staff_required = True
    permission_denied_message = 'User is not staff'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class PermissionRequiredMixin(OriginalPermissionRequiredMixin):
    def has_permission(self):
        perms = self.get_permission_required()
        for perm in perms:
            if '|' in perm:
                perms_or = perm.split('|')
                if not self.request.user.has_at_least_perms(perms_or):
                    return False
            elif not self.request.user.has_perms(perms):
                return False
        return True


class LoggedFormView(SuccessMessageMixin, LoginRequiredMixin, FormView):
    success_message = None


class StaffFormView(SuccessMessageMixin, LoginRequiredMixin, StaffRequiredMixin,
                    PermissionRequiredMixin, FormView):
    success_message = None


class StaffCreateView(SuccessMessageMixin, LoginRequiredMixin, StaffRequiredMixin,
                      PermissionRequiredMixin, CreateView):
    success_message = _("Successfully created")


class StaffUpdateView(SuccessMessageMixin, LoginRequiredMixin, StaffRequiredMixin,
                      PermissionRequiredMixin, UpdateView):
    success_message = _("Successfully updated")


class StaffDetailView(LoginRequiredMixin, StaffRequiredMixin,
                      PermissionRequiredMixin, DetailView):
    pass


class StaffListView(LoginRequiredMixin, StaffRequiredMixin,
                    PermissionRequiredMixin, ListView):
    pass


class StaffDeleteView(DeleteSuccessMessageMixin, LoginRequiredMixin, StaffRequiredMixin,
                      PermissionRequiredMixin, DeleteView):
    pass
