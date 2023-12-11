from django.contrib import admin
from facility.models import Facility
class FacilityAdmin(admin.ModelAdmin):
    pass


admin.site.register(Facility, FacilityAdmin)