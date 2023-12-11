from django.contrib import admin
from followup.models import FollowUp
class FollowUpAdmin(admin.ModelAdmin):
    pass


admin.site.register(FollowUp, FollowUpAdmin)