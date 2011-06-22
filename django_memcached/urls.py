from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'django_memcached.views.server_list'),
)
