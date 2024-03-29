# Create your models here.


from django.db import models
from django.utils.translation import gettext_lazy as _

from main.models import AbstractAuditModel
from main.utils import get_model_choices
from report.utils import upload_to


class RecordReport(AbstractAuditModel):

    class Status:
        PENDING = 'Pending'
        FAILED = 'Failed'
        SUCCESSFUL = 'Successful'

    patient = models.ForeignKey('patient.Patient', related_name='patient_record_report_set',
                                verbose_name=_('paciente'), null=True,
                                on_delete=models.SET_NULL)
    file = models.FileField(_('archivo'), null=True, blank=True, upload_to=upload_to)
    variables = models.ManyToManyField('device.Variable', related_name='variable_record_report_set',
                                       verbose_name=_('variables'))
    start_datetime = models.DateTimeField(_('fecha de inicio'))
    end_datetime = models.DateTimeField(_('fecha de fin'))
    status = models.CharField(_('estado'), choices=get_model_choices(Status), default=Status.PENDING)
    error = models.TextField(_('error'), default="", blank=True)
