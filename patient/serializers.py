from rest_framework import serializers

from patient.models import Patient


class PatientSerializer(serializers.ModelSerializer):
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    attending_staff = serializers.StringRelatedField(many=True)
    alarm_settings = serializers.StringRelatedField(many=True)

    class Meta:
        model = Patient
        fields = '__all__'
