from django.urls import path

from patient.views import PatientListView, PatientCreateView, PatientUpdateView, PatientDetailView

app_name = 'patient'

urlpatterns = [
    path('', PatientListView.as_view(), name='list'),
    path('create', PatientCreateView.as_view(), name='create'),
    path('update/<pk>', PatientUpdateView.as_view(), name='update'),
    path('detail/<pk>', PatientDetailView.as_view(), name='detail'),
]
