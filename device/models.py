from django.db import models
from django.utils.translation import gettext_lazy as _

from main.models import AbstractAuditModel


class Variable(AbstractAuditModel):
    name = models.CharField(_('name'), max_length=100)
    unit = models.CharField(_('unit'), max_length=100)

    def __str__(self):
        return self.name


class Sensor(AbstractAuditModel):
    name = models.CharField(_('name'), max_length=100)
    manufacturer = models.CharField(_('manufacturer'), max_length=100)
    variable = models.ForeignKey('device.Variable', related_name='variable_sensor_set', verbose_name=_('variable'),
                                 on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class DeviceType(AbstractAuditModel):
    name = models.CharField(_('name'), max_length=100)
    manufacturer = models.CharField(_('manufacturer'), max_length=100)
    sensors = models.ManyToManyField('device.Sensor', related_name='sensor_device_type_set',
                                     verbose_name=_('sensors'))

    def __str__(self):
        return self.name


class Device(AbstractAuditModel):
    identifier = models.CharField(_('identifier'), max_length=100)
    device_type = models.ForeignKey('device.DeviceType', related_name='type_device_set',
                                    verbose_name=_('type of device'),
                                    on_delete=models.CASCADE)
    patient = models.ForeignKey('patient.Patient', related_name='patient_device_set',
                                verbose_name=_('patient'), null=True,
                                on_delete=models.SET_NULL)

    def __str__(self):
        return self.identifier
