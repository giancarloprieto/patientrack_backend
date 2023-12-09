import os


def upload_to(instance, filename):
    ext = os.path.splitext(filename)[1]
    return 'users/{id}/profile{ext}'.format(id=instance.id, ext=ext)


from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from django.contrib.auth.tokens import PasswordResetTokenGenerator


def send_mail(subject_template_name, email_template_name,
              context, to_email, from_email=None, html_email_template_name=None):

    subject = loader.render_to_string(subject_template_name, context)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    body = loader.render_to_string(email_template_name, context)

    email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
    if html_email_template_name is not None:
        html_email = loader.render_to_string(html_email_template_name, context)
        email_message.attach_alternative(html_email, 'text/html')
    email_message.send()


def send_verification_mail(user, request, extra_email_context=None):
    """
    Generate a one-use only link for resetting password and send it to the
    user.
    """

    subject_template_name = 'authentication/register/register_subject.txt',
    email_template_name = 'authentication/register/register_email.html',
    use_https = request.is_secure()
    token_generator = PasswordResetTokenGenerator()
    current_site = get_current_site(request)
    site_name = current_site.name
    domain = current_site.domain

    context = {
        'email': user.email,
        'domain': domain,
        'site_name': site_name,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'user': user,
        'token': token_generator.make_token(user),
        'protocol': 'https' if use_https else 'http',
    }
    if extra_email_context is not None:
        context.update(extra_email_context)
    send_mail(subject_template_name, email_template_name, context, user.email,
              html_email_template_name=email_template_name)
