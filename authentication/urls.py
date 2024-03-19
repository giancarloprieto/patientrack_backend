import django.contrib.auth.views as auth_views
from django.urls import path, reverse_lazy
from django.views.generic import TemplateView

from authentication.views import RegisterView, EmailConfirmView, ProfileView, UserListView, UserUpdateView

authentication_patterns = (
    [
        path('logout/', auth_views.LogoutView.as_view(), name='logout'),

        path('login/', auth_views.LoginView.as_view(template_name='authentication/login_final.html'),
             name='login'),

        path('password-change/', auth_views.PasswordChangeView.as_view(
            template_name='authentication/password/password_change.html',
            success_url=reverse_lazy('authentication:password_change_done')),
             name='password_change'),

        path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(
            template_name='authentication/password/password_change_done.html'),
             name='password_change_done'),

        path('password-reset/', auth_views.PasswordResetView.as_view(
            template_name='authentication/password/password_reset.html',
            email_template_name="authentication/password/password_reset_email.html",
            html_email_template_name="authentication/password/password_reset_email.html",
            subject_template_name="authentication/password/password_reset_subject.txt",
            success_url=reverse_lazy('authentication:password_reset_done')),
            name='password_reset'),

        path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
            template_name='authentication/password/password_reset_done.html'),
             name='password_reset_done'),

        path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
            template_name='authentication/password/password_reset_confirm.html',
            success_url=reverse_lazy('authentication:password_reset_complete')),
             name='password_reset_confirm'),

        path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
            template_name='authentication/password/password_reset_complete.html', ),
             name='password_reset_complete'),

        path('register/', RegisterView.as_view(),
             name='register'),

        path('register/done/', TemplateView.as_view(
            template_name='authentication/register/register_done.html'),
             name='register_done'),

        path('register/email/<uidb64>/<token>/', EmailConfirmView.as_view(),
             name='register_email_confirm'),
        # path('register/email/resend/<pk>', ResendVerificationMailView.as_view(), name='register_email_resend'),
        path('profile', ProfileView.as_view(), name='profile'),
        path('user', UserListView.as_view(), name='user_list'),
        path('user/update/<pk>', UserUpdateView.as_view(), name='user_update'),

    ], 'authentication')
