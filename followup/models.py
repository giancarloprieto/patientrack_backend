from django.db import models
from django.utils.translation import gettext_lazy as _

from main.models import AbstractAuditModel


# Create your models here.


class FollowUp(AbstractAuditModel):
    patient = models.ForeignKey('patient.Patient', related_name='patient_followup_set',
                                verbose_name=_('patient'), null=True,
                                on_delete=models.SET_NULL)
    comment = models.TextField(_('comment'))
