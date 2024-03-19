from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.views import INTERNAL_RESET_SESSION_TOKEN, UserModel
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, TemplateView

from authentication.forms import RegisterForm, ProfileForm, UserForm
from authentication.models import User
from authentication.utils import send_verification_mail
from main.views import LoggedFormView, StaffListView, StaffUpdateView

INTERNAL_RESET_URL_TOKEN = 'set-password'


# Create your views here.

class RegisterView(FormView):
    template_name = 'authentication/register/register_final.html'
    form_class = RegisterForm
    success_url = reverse_lazy('authentication:register_done')

    def form_valid(self, form):
        user = form.save()
        send_verification_mail(user, self.request)
        return super().form_valid(form)


class EmailConfirmView(TemplateView):
    template_name = 'authentication/register/register_email_done.html'
    token_generator = PasswordResetTokenGenerator()
    user = None

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        assert 'uidb64' in kwargs and 'token' in kwargs

        self.validlink = False
        self.user = self.get_user(kwargs['uidb64'])

        if self.user is not None:
            token = kwargs['token']
            if token == INTERNAL_RESET_URL_TOKEN:
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    # If the token is valid, display the password reset form.
                    self.validlink = True
                    return super().dispatch(*args, **kwargs)
            else:
                if self.token_generator.check_token(self.user, token):
                    # Store the token in the session and redirect to the
                    # password reset form at a URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(token, INTERNAL_RESET_URL_TOKEN)
                    return HttpResponseRedirect(redirect_url)

        # Display the "Password reset unsuccessful" page.
        return self.render_to_response(self.get_context_data())

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist, ValidationError):
            user = None
        return user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.validlink:
            context['validlink'] = True
            self.user.email_checked = True
            self.user.save()
        return context


class ProfileView(LoggedFormView):
    template_name = 'authentication/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('authentication:profile')
    success_message = _("Successfully updated")
    instance = None

    def get_object(self):
        if self.instance is None:
            self.instance = get_object_or_404(User, **{'pk': self.request.user.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.get_object()
        context['object'] = self.instance
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.get_object()
        kwargs.update({'instance': self.instance})
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class UserListView(StaffListView):
    model = User
    template_name = 'user/list.html'
    permission_required = 'auth.view_user'
    search_fields = ['name']


class UserUpdateView(StaffUpdateView):
    model = User
    template_name = 'user/form.html'
    permission_required = 'auth.change_user'
    form_class = UserForm
    success_url = reverse_lazy('device:list')
