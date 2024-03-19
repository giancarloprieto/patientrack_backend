from django.urls import re_path

from pwa.views import manifest, service_worker, offline

urlpatterns = [
    re_path(r'^serviceworker\.js$', service_worker, name='serviceworker'),
    re_path(r'^manifest\.json$', manifest, name='manifest'),
    re_path('^offline/$', offline, name='offline')
]
