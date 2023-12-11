from django.contrib import admin

from monitoring.models import Record, AlarmSettings


class RecordAdmin(admin.ModelAdmin):
    pass


admin.site.register(Record, RecordAdmin)


class AlarmSettingsAdmin(admin.ModelAdmin):
    pass


admin.site.register(AlarmSettings, AlarmSettingsAdmin)
