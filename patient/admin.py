from django.contrib import admin

from patient.models import Patient


class PatientAdmin(admin.ModelAdmin):
    pass


admin.site.register(Patient, PatientAdmin)

