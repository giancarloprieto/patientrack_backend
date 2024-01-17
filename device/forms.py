from django import forms

from .models import Variable, Sensor, Device, DeviceType


class VariableForm(forms.ModelForm):
    class Meta:
        model = Variable
        fields = ['unit', 'name']


class SensorForm(forms.ModelForm):
    class Meta:
        model = Sensor
        fields = ['name', 'manufacturer', 'variable']


class DeviceTypeForm(forms.ModelForm):
    class Meta:
        model = DeviceType
        fields = ['name', 'manufacturer', 'sensors']


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['identifier', 'device_type', 'patient']
