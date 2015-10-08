from django.conf.urls import patterns, url
from iotshm_dashboard import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^change_password/complete/$', views.change_password_complete, name='change_password_complete'),
    url(r'^aboutiotshm/$', views.about, name='about'),
    url(r'^contact/$', views.contact, name='contactus'),
    url(r'^contact/thanks/$', views.contact_thanks, name='contactus'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^dashboard/(?P<building_num>\d+)/real_time/$', views.real_time, name='real_time'),
    url(r'^dashboard/(?P<building_num>\d+)/$', views.building_info, name='building_info'),
    url(r'^dashboard/(?P<building_num>\d+)/long_term/$', views.long_term, name='long_term'),
    url(r'^dashboard/(?P<building_num>\d+)/sensors/$', views.sensors, name='sensors'),
    url(r'^dashboard/my_buildings/$', views.my_buildings, name='my_buildings'),
    url(r'^health/(?P<building_num>\d+)/$', views.health, name='health'),
    url(r'^real_time_ajax_x/(?P<building_num>\d+)/$', views.real_time_ajax_x, name='real_time_ajax_x'),
    url(r'^real_time_ajax_y/(?P<building_num>\d+)/$', views.real_time_ajax_y, name='real_time_ajax_y'),
    url(r'^real_time_ajax_z/(?P<building_num>\d+)/$', views.real_time_ajax_z, name='real_time_ajax_z'),
)