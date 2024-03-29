from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from main.models import AbstractAuditModel
from main.utils import get_model_choices


class Staff(AbstractAuditModel):
    class Gender:
        MALE = 'M'
        FEMALE = 'F'
        OTHER = 'O'

    first_name = models.CharField(_('nombres'), max_length=100)
    last_name = models.CharField(_('apellidos'), max_length=100)
    date_of_birth = models.DateField(_('fecha de nacimiento'))
    gender = models.CharField(_('género'), choices=get_model_choices(Gender), default=Gender.OTHER)
    contact_number = models.CharField(_('número de contacto'), max_length=100, default="")
    email = models.EmailField(_("correo electrónico"))
    address = models.CharField(_('dirección'), max_length=100)
    city = models.CharField(_('ciudad'), max_length=100)
    hire_date = models.DateField(_('fecha de contratación'))
    specialization = models.CharField(_('especialización'), max_length=100)
    identification = models.CharField(_('identificación'), max_length=100)
    is_active = models.BooleanField(_('activo'), default=True)
    facility = models.ForeignKey('facility.Facility', related_name='facility_staff_set', verbose_name=_('facility'),
                                 on_delete=models.CASCADE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_('usuario'), null=True, blank=True,
                                related_name='staff_user_set', on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
