from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from staff.models import Staff


class StaffSerializer(serializers.ModelSerializer):
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    patients_in_charge = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()

    def get_patients_in_charge(self, obj):
        return ', '.join([f'{pat.first_name} {pat.last_name}' for pat in obj.staff_patient_set.all()])

    def get_is_active(self, obj):
        return _('yes') if obj.is_active else _('no')

    class Meta:
        model = Staff
        fields = '__all__'
