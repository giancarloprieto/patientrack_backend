
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView

from authentication.urls import authentication_patterns


urlpatterns = [
    path('sitemap.xml', sitemap, name='sitemap-xml'),
]


urlpatterns += i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')),
    path('', RedirectView.as_view(url=reverse_lazy('monitoring:detail'), permanent=False), name='home'),
    path('admin/', admin.site.urls),
    path('authentication/', include(authentication_patterns, namespace='authentication')),
    path('monitoring/', include('monitoring.urls')),
    path('patient/', include('patient.urls')),
    path('staff/', include('staff.urls')),
    path('follow-up/', include('followup.urls')),
    path('report/', include('report.urls')),
    path('device/', include('device.urls'))

)