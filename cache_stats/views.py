import datetime
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.core.cache import cache
from django.shortcuts import render
from django.template import RequestContext
from .util import get_stats

def server_list(request):
    context = {"stats": get_stats()}
    return render(
        request, "memcached/server_list.html", context)

if getattr(settings, 'DJANGO_MEMCACHED_REQUIRE_STAFF', False):
    server_list = user_passes_test(lambda u: u.is_staff)(server_list)
