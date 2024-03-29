from django.db import models
from django.utils.translation import gettext_lazy as _

from main.models import AbstractAuditModel
from main.utils import get_model_choices


class AlarmSettings(AbstractAuditModel):
    class Operator:
        E = '='
        GT = '>'
        GTE = '>='
        LT = '<'
        LTE = '<='

    variable = models.ForeignKey('device.Variable', related_name='variable_alarm_settings_set',
                                 verbose_name=_('variable'), on_delete=models.CASCADE)
    reference_value = models.FloatField(_("valor de referencia"))
    name = models.CharField(_("nombre"), max_length=100)
    operator = models.CharField(_('operador'), choices=get_model_choices(Operator))

    def __str__(self):
        return self.name


class Record(AbstractAuditModel):
    datetime_server = models.DateTimeField(_('fecha y hora del servidor'))
    datetime_device = models.DateTimeField(_('fecha y hora del equipo'))
    patient = models.ForeignKey('patient.Patient', related_name='patient_record_set',
                                verbose_name=_('paciente'), null=True,
                                on_delete=models.SET_NULL)
    patient_identification = models.CharField(_("identificación de paciente"), max_length=100)
    device = models.ForeignKey('device.Device', related_name='device_record_set',
                               verbose_name=_('equipo'), null=True,
                               on_delete=models.SET_NULL)
    device_identifier = models.CharField(_("identificador del equipo"), max_length=100)
    variable = models.ForeignKey('device.Variable', related_name='variable_record_set',
                                 verbose_name=_('variable'), null=True,
                                 on_delete=models.SET_NULL)
    variable_name = models.CharField(_("nombre de variable"), max_length=100)
    value = models.FloatField(_("valor"))
    payload = models.TextField(_("trama"))
    alarm_settings_fk = models.ForeignKey(AlarmSettings, related_name='alarm_settings_record_set',
                                          verbose_name=_('config alarmas'), null=True, blank=True,
                                          on_delete=models.SET_NULL)
    alarm_name = models.CharField(_("nombre de alarma"), default="", blank=True)
    alarm_operator = models.CharField(_("operador de alarma"), default="", blank=True,
                                      choices=get_model_choices(AlarmSettings.Operator))
    alarm_ref_value = models.FloatField(_("valor de referencia"), null=True, blank=True)

    def __str__(self):
        return f'{self.patient_identification} {self.variable_name} {self.datetime_device.strftime("%Y:%m:%d,%H:%M:%S")}'
