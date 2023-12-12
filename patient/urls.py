from django.urls import include, path

from patient.views import PatientListView, PatientCreateView

app_name = 'patient'


urlpatterns = [
    path('', PatientListView.as_view(), name='list'),
    path('create', PatientCreateView.as_view(), name='create'),
]
