from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from main.models import AbstractAuditModel
from main.utils import get_model_choices


class Patient(AbstractAuditModel):
    class Gender:
        MALE = 'M'
        FEMALE = 'F'
        OTHER = 'O'

    class Status:
        ADMITTED = 'Admitted'
        DISCHARGED = 'Discharged'
        TRANSFERRED = 'Transferred'
        DECEASED = 'Deceased'

    first_name = models.CharField(_('first name'), max_length=100)
    last_name = models.CharField(_('last name'), max_length=100)
    identification = models.CharField(_('identification'), max_length=100)
    admission_date = models.DateTimeField(_('admission date'))
    discharge_date = models.DateTimeField(_('discharge date'), null=True, blank=True)
    gender = models.CharField(_('gender'), choices=get_model_choices(Gender), default=Gender.OTHER)
    status = models.CharField(_('status'), choices=get_model_choices(Status), default=Status.ADMITTED)
    address = models.CharField(_('address'), max_length=100)
    city = models.CharField(_('city'), max_length=100)
    contact_number = models.CharField(_('contact number'), max_length=100, default="")
    emergency_contact_name = models.CharField(_('emergency contact name'), max_length=100, default="")
    emergency_contact_number = models.CharField(_('emergency contact number'), max_length=100, default="")
    facility = models.ForeignKey('facility.Facility', related_name='facility_patient_set', verbose_name=_('facility'),
                                 on_delete=models.CASCADE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_('user'), null=True, blank=True,
                                related_name='patient_user_set', on_delete=models.SET_NULL)

    attending_staff = models.ManyToManyField('staff.Staff', related_name='staff_patient_set',
                                             verbose_name=_('attending staff'), blank=True)
    alarm_settings = models.ManyToManyField('monitoring.AlarmSettings', related_name='alarm_settings_patient_set',
                                            verbose_name=_('alarm settings'), blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
