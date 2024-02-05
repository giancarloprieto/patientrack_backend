from django.urls import reverse_lazy

from device.forms import VariableForm, SensorForm, DeviceTypeForm, DeviceForm
from device.models import Variable, Sensor, DeviceType, Device
from device.serializers import DeviceSerializer
from main.views import StaffListView, StaffCreateView, StaffUpdateView, StaffDetailView


class VariableListView(StaffListView):
    model = Variable
    template_name = 'variable/list.html'
    permission_required = 'device.view_variable'
    search_fields = ['name', 'identifier']


class VariableCreateView(StaffCreateView):
    model = Variable
    template_name = 'variable/form.html'
    permission_required = 'device.add_variable'
    form_class = VariableForm
    success_url = reverse_lazy('device:variable_list')


class VariableUpdateView(StaffUpdateView):
    model = Variable
    template_name = 'variable/form.html'
    permission_required = 'device.change_variable'
    form_class = VariableForm
    success_url = reverse_lazy('device:variable_list')


class SensorListView(StaffListView):
    model = Sensor
    template_name = 'sensor/list.html'
    permission_required = 'device.view_sensor'
    search_fields = ['name']

    def get_queryset(self):
        self.queryset = self.model.objects.select_related('variable')
        return super().get_queryset()


class SensorCreateView(StaffCreateView):
    model = Sensor
    template_name = 'sensor/form.html'
    permission_required = 'device.add_sensor'
    form_class = SensorForm
    success_url = reverse_lazy('device:sensor_list')


class SensorUpdateView(StaffUpdateView):
    model = Sensor
    template_name = 'sensor/form.html'
    permission_required = 'device.change_sensor'
    form_class = SensorForm
    success_url = reverse_lazy('device:sensor_list')


class DeviceTypeListView(StaffListView):
    model = DeviceType
    template_name = 'device_type/list.html'
    permission_required = 'device.view_devicetype'
    search_fields = ['name']

    def get_queryset(self):
        self.queryset = self.model.objects.prefetch_related('sensors')
        return super().get_queryset()


class DeviceTypeCreateView(StaffCreateView):
    model = DeviceType
    template_name = 'device_type/form.html'
    permission_required = 'device.add_devicetype'
    form_class = DeviceTypeForm
    success_url = reverse_lazy('device:type_list')


class DeviceTypeUpdateView(StaffUpdateView):
    model = DeviceType
    template_name = 'device_type/form.html'
    permission_required = 'device.change_devicetype'
    form_class = DeviceTypeForm
    success_url = reverse_lazy('device:type_list')


class DeviceListView(StaffListView):
    model = Device
    template_name = 'device/list.html'
    permission_required = 'device.view_device'
    search_fields = ['name']

    def get_queryset(self):
        self.queryset = self.model.objects.select_related('patient', 'device_type')
        return super().get_queryset()


class DeviceCreateView(StaffCreateView):
    model = Device
    template_name = 'device/form.html'
    permission_required = 'device.add_device'
    form_class = DeviceForm
    success_url = reverse_lazy('device:list')


class DeviceUpdateView(StaffUpdateView):
    model = Device
    template_name = 'device/form.html'
    permission_required = 'device.change_device'
    form_class = DeviceForm
    success_url = reverse_lazy('device:list')


class DeviceDetailView(StaffDetailView):
    model = Device
    template_name = 'device/detail.html'
    permission_required = 'device.view_device'
    serializer_class = DeviceSerializer
    sections = {'Device information': ['identifier', 'patient', 'device_type', 'sensors']}

    def get_queryset(self):
        self.queryset = self.model.objects.select_related('patient', 'device_type').\
            prefetch_related('device_type__sensors__variable')
        return super().get_queryset()
