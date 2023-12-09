from django.contrib import messages
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect

from django.utils.translation import gettext_lazy as _


class SuccessMessageMixin:
    success_message = ''

    def form_valid(self, form):
        response = super(SuccessMessageMixin, self).form_valid(form)
        success_message = self.get_success_message(form)
        if success_message:
            messages.success(self.request, success_message)
        return response

    def get_success_message(self, form):
        return self.success_message % form.cleaned_data


class DeleteSuccessMessageMixin:
    success_message = _("Successfully deleted")
    error_message = _("Element cannot be deleted. There are relationships with other elements.")
    success = True

    def delete(self, request, *args, **kwargs):
        try:
            response = super(DeleteSuccessMessageMixin, self).delete(request, *args, **kwargs)
        except ProtectedError:
            self.success = False
            response = HttpResponseRedirect(self.success_url)
        if self.success:
            messages.success(request, self.success_message)
        else:
            messages.error(request, self.error_message)
        return response
