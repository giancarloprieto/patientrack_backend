from django.urls import path

from monitoring.views import DashboardView

app_name = 'monitoring'

urlpatterns = [
    path('', DashboardView.as_view(), name='detail')
]