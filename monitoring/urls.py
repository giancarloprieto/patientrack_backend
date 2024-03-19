from django.urls import path

from monitoring.views import MonitoringView, PatientMonitoringView, AlarmSettingsListView, AlarmSettingsUpdateView, \
    AlarmSettingsCreateView

app_name = 'monitoring'

urlpatterns = [
    path('', MonitoringView.as_view(), name='list'),
    path('detail/<pk>', PatientMonitoringView.as_view(), name='detail'),
    path('alarm-settings', AlarmSettingsListView.as_view(), name='alarm_settings_list'),
    path('alarm-settings/create', AlarmSettingsCreateView.as_view(), name='alarm_settings_create'),
    path('alarm-settings/update/<pk>', AlarmSettingsUpdateView.as_view(), name='alarm_settings_update'),
]