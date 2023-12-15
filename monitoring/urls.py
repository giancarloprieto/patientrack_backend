from django.urls import path

from monitoring.views import MonitoringView

app_name = 'monitoring'

urlpatterns = [
    path('', MonitoringView.as_view(), name='list')
]