from django.urls import include, path

from patient.views import PatientListView

app_name = 'patient'


urlpatterns = [
    path('', PatientListView.as_view(), name='list'),
]
