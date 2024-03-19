from rest_framework import serializers

from report.models import RecordReport


class RecordReportSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()
    status = serializers.CharField(source='get_status_display')
    variables = serializers.SerializerMethodField()
    patient = serializers.SerializerMethodField()

    class Meta:
        model = RecordReport
        fields = [
            'patient', 'file',  'variables', 'start_datetime',
            'end_datetime', 'status', 'error', 'created_by', 'created_at'
        ]

    def get_file(self, obj):
        if obj.file:
            return obj.file.url
        return None

    def get_variables(self, obj):
        return ', '.join(obj.variables.all().values_list('name', flat=True))

    def get_patient(self, obj):
        return f'{obj.patient.first_name} {obj.patient.last_name}' if obj.patient else None
