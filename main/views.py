from django.contrib.auth.mixins import PermissionRequiredMixin as OriginalPermissionRequiredMixin, LoginRequiredMixin, \
    AccessMixin
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.views.generic import DeleteView, FormView, CreateView, UpdateView, DetailView, ListView

from main.forms import SearchForm
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


class MenuActiveMixin:
    active_tab = None
    open_menu = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tab = {'active': self.active_tab, 'open': self.open_menu}
        tabs_map = {'monitoring': ['monitoring', 'alarm_settings'],
                    'administration': ['patient', 'staff', 'device', 'user'],
                    'report': ['report'],
                    'reference': ['device_type', 'sensor', 'variable']}
        if not self.active_tab:
            module = self.template_name.split('/'[0])
            for open, active_list in tabs_map.items():
                for active in active_list:
                    if active in module:
                        tab = {'active': active, 'open': open}
                        break
                else:
                    continue
                break
        context['tab'] = tab
        return context


class BaseDetailView(MenuActiveMixin, DetailView):
    serializer_class = None
    sections = None
    special_labels = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if getattr(self, 'serializer_class'):
            context['object_data'] = self.serializer_class(self.object).data
        if getattr(self, 'sections'):
            context['sections'] = self.sections
        if getattr(self, 'special_labels'):
            context['special_labels'] = self.special_labels
        return context


class LoggedFormView(SuccessMessageMixin, LoginRequiredMixin, MenuActiveMixin, FormView):
    success_message = None


class LoggedDetailView(LoginRequiredMixin, BaseDetailView):
    success_message = None


class StaffFormView(SuccessMessageMixin, LoginRequiredMixin, StaffRequiredMixin,
                    PermissionRequiredMixin, MenuActiveMixin, FormView):
    success_message = None


class StaffCreateView(SuccessMessageMixin, LoginRequiredMixin, StaffRequiredMixin,
                      PermissionRequiredMixin, MenuActiveMixin, CreateView):
    success_message = _("Successfully created")


class StaffUpdateView(SuccessMessageMixin, LoginRequiredMixin, StaffRequiredMixin,
                      PermissionRequiredMixin, MenuActiveMixin, UpdateView):
    success_message = _("Successfully updated")


class StaffDetailView(LoginRequiredMixin, StaffRequiredMixin,
                      PermissionRequiredMixin, BaseDetailView):
    pass


class StaffListView(LoginRequiredMixin, StaffRequiredMixin,
                    PermissionRequiredMixin, MenuActiveMixin, ListView):
    search_fields = []
    paginate_by = 100

    def get_queryset(self):
        self.queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        if search_query:
            or_conditions = [Q(**{f'{field}__icontains': search_query}) for field in self.search_fields]
            query = or_conditions.pop()
            for condition in or_conditions:
                query |= condition

            self.queryset = self.queryset.filter(query)

        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm(self.request.GET)
        return context


class StaffDeleteView(DeleteSuccessMessageMixin, LoginRequiredMixin, StaffRequiredMixin,
                      PermissionRequiredMixin, MenuActiveMixin, DeleteView):
    pass
