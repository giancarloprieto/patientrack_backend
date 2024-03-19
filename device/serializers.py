from rest_framework import serializers

from device.models import Device


class DeviceSerializer(serializers.ModelSerializer):
    patient = serializers.SerializerMethodField()
    device_type = serializers.ReadOnlyField(source='device_type.name')
    sensors = serializers.SerializerMethodField()

    def get_patient(self, obj):
        return f'{obj.patient.first_name} {obj.patient.last_name}' if obj.patient else None

    def get_sensors(self, obj):
        return ', '.join([f'{sensor.name}: {sensor.variable.name}' for sensor in obj.device_type.sensors.all()])

    class Meta:
        model = Device
        fields = '__all__'
