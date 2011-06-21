from django.http import Http404
from django.shortcuts import render_to_response
from django.conf import settings
from django.template import RequestContext
from django.core.exceptions import ImproperlyConfigured
from django.core.cache import (
    parse_backend_uri, parse_backend_conf, DEFAULT_CACHE_ALIAS)

from django_memcached.util import get_memcached_stats
from django.contrib.auth.decorators import user_passes_test

def get_cache_server_list():
    """Returns a list of active memcached servers.

    Compatible with both 1.2 and 1.3 style cache configuration.

    """
    # If settings.CACHES isn't defined, we're using Django <= 1.2.x
    if getattr(settings, 'CACHES', None) is None:
        scheme, hosts, params  = parse_backend_uri(settings.CACHE_BACKEND)
        if not 'memcached' in scheme:
            raise ImproperlyConfigured("Must use memcached.  Currently using '%s'" % scheme)

    # Django >= 1.3
    #
    # Django silently converts old-style CACHE_* arguments into the new-style
    # CACHES dictionary.  So we're safe to use this.
    else:
        engine, hosts, params = parse_backend_conf(DEFAULT_CACHE_ALIAS)
        if 'memcached' not in engine:
            raise ImproperlyConfigured("Must use memcached.  Currently using '%s'" % engine)

    return hosts if isinstance(hosts, list) else hosts.split(';')

def server_list(request):
    servers = get_cache_server_list()
    statuses = []
    for idx, server in enumerate(servers):
        statuses.append((idx, server, get_memcached_stats(server)))

    context = {
        'statuses': statuses,
    }
    return render_to_response(
        'memcached/server_list.html',
        context,
        context_instance=RequestContext(request)
    )

def server_status(request, index):
    servers = get_cache_server_list()
    try:
        index = int(index)
    except ValueError:
        raise Http404
    try:
        server = servers[index]
    except IndexError:
        raise Http404
    stats = get_memcached_stats(server)
    if not stats:
        raise Http404
    context = {
        'server': server,
        'stats': stats.items(),
    }
    return render_to_response(
        'memcached/server_status.html',
        context,
        context_instance=RequestContext(request)
    )

if getattr(settings, 'DJANGO_MEMCACHED_REQUIRE_STAFF', False):
    server_list = user_passes_test(lambda u: u.is_staff)(server_list)
    server_status = user_passes_test(lambda u: u.is_staff)(server_status)
