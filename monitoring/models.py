from django.db import models
from django.utils.translation import gettext_lazy as _

from main.models import AbstractAuditModel
from main.utils import get_model_choices


class AlarmSettings(AbstractAuditModel):
    class Operator:
        E = 'E'
        GT = 'GT'
        GTE = 'GTE'
        LT = 'LT'
        LTE = 'LTE'

    variable = models.ForeignKey('device.Variable', related_name='variable_alarm_settings_set',
                                 verbose_name=_('variable'), on_delete=models.CASCADE)
    reference_value = models.FloatField(_("reference value"))
    name = models.CharField(_("name"), max_length=100)
    operator = models.CharField(_('operator'), choices=get_model_choices(Operator))

    def __str__(self):
        return self.name


class Record(AbstractAuditModel):
    datetime_server = models.DateTimeField(_('date and time of server'))
    datetime_device = models.DateTimeField(_('date and time of device'))
    patient = models.ForeignKey('patient.Patient', related_name='patient_record_set',
                                verbose_name=_('patient'), null=True,
                                on_delete=models.SET_NULL)
    patient_identification = models.CharField(_("patient's identification"), max_length=100)
    device = models.ForeignKey('device.Device', related_name='device_record_set',
                               verbose_name=_('device'), null=True,
                               on_delete=models.SET_NULL)
    device_identifier = models.CharField(_("device's identifier"), max_length=100)
    variable = models.ForeignKey('device.Variable', related_name='variable_record_set',
                                 verbose_name=_('variable'), null=True,
                                 on_delete=models.SET_NULL)
    variable_name = models.CharField(_("variable's name"), max_length=100)
    value = models.FloatField(_("value"))
    payload = models.TextField(_("payload"))
    alarm_settings_fk = models.ForeignKey(AlarmSettings, related_name='alarm_settings_record_set',
                                          verbose_name=_('alarm settings'), null=True,
                                          on_delete=models.SET_NULL)
    alarm_name = models.CharField(_("alarm's name"), default="")
    alarm_operator = models.CharField(_("alarm's operator"), default="",
                                      choices=get_model_choices(AlarmSettings.Operator))
    alarm_ref_value = models.FloatField(_("reference value"), null=True)
