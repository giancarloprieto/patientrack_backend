from django.urls import path

from report.views import RecordReportListView, RecordReportCreateView, RecordReportDetailView

app_name = 'report'

urlpatterns = [
    path('', RecordReportListView.as_view(), name='list'),
    path('create', RecordReportCreateView.as_view(), name='create'),
    path('detail/<pk>', RecordReportDetailView.as_view(), name='detail'),
]
