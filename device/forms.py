from django import forms

from main.forms import BaseModelForm
from .models import Variable, Sensor, Device, DeviceType


class VariableForm(BaseModelForm):
    class Meta:
        model = Variable
        fields = ['unit', 'name', 'identifier', 'icon', 'css_class_suffix', 'color']


class SensorForm(BaseModelForm):
    class Meta:
        model = Sensor
        fields = ['name', 'manufacturer', 'variable']


class DeviceTypeForm(BaseModelForm):
    class Meta:
        model = DeviceType
        fields = ['name', 'manufacturer', 'sensors']


class DeviceForm(BaseModelForm):
    class Meta:
        model = Device
        fields = ['identifier', 'device_type', 'patient']
