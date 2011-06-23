from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'cache_stats.views.server_list'),
)
