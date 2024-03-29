from django.db import models
from django.utils.translation import gettext_lazy as _

from main.models import AbstractAuditModel


class Variable(AbstractAuditModel):
    name = models.CharField(_('nombre'), max_length=100)
    unit = models.CharField(_('unidades'), max_length=100)
    identifier = models.CharField(_('identificador'), unique=True, max_length=100)
    icon = models.CharField(_('icono'), max_length=100)
    css_class_suffix = models.CharField(_('sufijo css'), max_length=100)
    color = models.CharField(_('color'), max_length=100)

    def __str__(self):
        return self.name


class Sensor(AbstractAuditModel):
    name = models.CharField(_('nombre'), max_length=100)
    manufacturer = models.CharField(_('fabricante'), max_length=100)
    variable = models.ForeignKey('device.Variable', related_name='variable_sensor_set', verbose_name=_('variable'),
                                 on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class DeviceType(AbstractAuditModel):
    name = models.CharField(_('nombre'), max_length=100)
    manufacturer = models.CharField(_('fabricante'), max_length=100)
    sensors = models.ManyToManyField('device.Sensor', related_name='sensor_device_type_set',
                                     verbose_name=_('sensores'))

    def __str__(self):
        return self.name


class Device(AbstractAuditModel):
    identifier = models.CharField(_('identificador'), max_length=100)
    device_type = models.ForeignKey('device.DeviceType', related_name='type_device_set',
                                    verbose_name=_('tipo de equipo'),
                                    on_delete=models.CASCADE)
    patient = models.ForeignKey('patient.Patient', related_name='patient_device_set',
                                verbose_name=_('paciente'), null=True,
                                on_delete=models.SET_NULL)

    def __str__(self):
        return self.identifier
