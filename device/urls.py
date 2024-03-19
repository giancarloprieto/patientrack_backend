from django.urls import path

from device.views import DeviceCreateView, DeviceListView, DeviceUpdateView, DeviceDetailView, \
    DeviceTypeCreateView, DeviceTypeListView, DeviceTypeUpdateView, \
    SensorCreateView, SensorListView, SensorUpdateView, \
    VariableListView, VariableCreateView, VariableUpdateView

app_name = 'device'

urlpatterns = [
    path('', DeviceListView.as_view(), name='list'),
    path('create', DeviceCreateView.as_view(), name='create'),
    path('update/<pk>', DeviceUpdateView.as_view(), name='update'),
    path('detail/<pk>', DeviceDetailView.as_view(), name='detail'),
    path('type/', DeviceTypeListView.as_view(), name='type_list'),
    path('type/create', DeviceTypeCreateView.as_view(), name='type_create'),
    path('type/update/<pk>', DeviceTypeUpdateView.as_view(), name='type_update'),
    path('sensor/', SensorListView.as_view(), name='sensor_list'),
    path('sensor/create', SensorCreateView.as_view(), name='sensor_create'),
    path('sensor/update/<pk>', SensorUpdateView.as_view(), name='sensor_update'),
    path('variable/', VariableListView.as_view(), name='variable_list'),
    path('variable/create', VariableCreateView.as_view(), name='variable_create'),
    path('variable/update/<pk>', VariableUpdateView.as_view(), name='variable_update'),
]
