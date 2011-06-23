import datetime
from django.core.cache import cache

def get_stats():
    stats = cache._cache.get_stats()
    new_stats = {}

    for server, server_stats in stats:
        info = server_stats.copy()
        new_stats[server] = info
        for memcached_key, memcached_value in server_stats.iteritems():
            if memcached_key == "uptime":
                info["uptime"] = datetime.timedelta(seconds=int(memcached_value))
            elif memcached_key == "time":
                info["time"] = datetime.datetime.fromtimestamp(int(memcached_value))
            else:
                try:
                    info[memcached_key] = int(memcached_value)
                except ValueError:
                    pass

        try:
            info["hit_rate"] = 100. * info["get_hits"] / float(info["cmd_get"])
        except ZeroDivisionError:
            info["hit_rate"] = info["get_hits"]

        info["started_at"] = info["time"] - info["uptime"]

        info["cmd_get_per_second"] = info["cmd_get"] / float(info["uptime"].seconds)
        info["cmd_set_per_second"] = info["cmd_set"] / float(info["uptime"].seconds)

    return new_stats
