from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^iotshm/', include('iotshm_dashboard.urls', namespace="iotshm_dashboard")),
    url(r'^admin/', include(admin.site.urls)),
)