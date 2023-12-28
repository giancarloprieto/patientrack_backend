from django.urls import path

from followup.views import FollowUpCreateView, FollowUpUpdateView, FollowUpListView

app_name = 'followup'

urlpatterns = [
    path('<patient_id>', FollowUpListView.as_view(), name='list'),
    path('<patient_id>/create', FollowUpCreateView.as_view(), name='create'),
    path('<patient_id>/update/<pk>', FollowUpUpdateView.as_view(), name='update'),
]
