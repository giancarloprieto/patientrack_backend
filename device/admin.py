from django.contrib import admin

from device.models import Device, Sensor, Variable, DeviceType


class DeviceAdmin(admin.ModelAdmin):
    pass


admin.site.register(Device, DeviceAdmin)


class SensorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Sensor, SensorAdmin)


class VariableAdmin(admin.ModelAdmin):
    pass


admin.site.register(Variable, VariableAdmin)


class DeviceTypeAdmin(admin.ModelAdmin):
    pass


admin.site.register(DeviceType, DeviceTypeAdmin)
