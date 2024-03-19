from django.urls import path

from staff.views import MedicalStaffListView, MedicalStaffCreateView, MedicalStaffUpdateView, MedicalStaffDetailView

app_name = 'staff'

urlpatterns = [
    path('', MedicalStaffListView.as_view(), name='list'),
    path('create', MedicalStaffCreateView.as_view(), name='create'),
    path('update/<pk>', MedicalStaffUpdateView.as_view(), name='update'),
    path('detail/<pk>', MedicalStaffDetailView.as_view(), name='detail'),
]
