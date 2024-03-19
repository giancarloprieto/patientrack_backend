from rest_framework import serializers

from patient.models import Patient


class PatientSerializer(serializers.ModelSerializer):
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    admission_date = serializers.DateTimeField(format="%Y-%m-%d")
    staff_a_cargo = serializers.SerializerMethodField()
    config_alarmas = serializers.SerializerMethodField()

    def get_staff_a_cargo(self, obj):
        return ', '.join([f'{staff.first_name} {staff.last_name}' for staff in obj.attending_staff.all()])

    def get_config_alarmas(self, obj):
        return ', '.join([f'{al_set.name}' for al_set in obj.alarm_settings.all()])

    class Meta:
        model = Patient
        fields = '__all__'
