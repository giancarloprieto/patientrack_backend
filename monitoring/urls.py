from django.urls import path

from monitoring.views import MonitoringView, PatientMonitoringView

app_name = 'monitoring'

urlpatterns = [
    path('', MonitoringView.as_view(), name='list'),
    path('detail/<pk>', PatientMonitoringView.as_view(), name='detail')
]