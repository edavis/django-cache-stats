import datetime
from decimal import Decimal
from django.core.cache import cache

def get_stats():
    c = cache._cache
    stats = dict(c.get_stats())
    servers = stats.keys()

    conversion_map = {
        "uptime": lambda n: datetime.timedelta(seconds=int(n)),
        "rusage_system": Decimal,
        "rusage_user": Decimal,
        "time": lambda n: datetime.datetime.fromtimestamp(int(n)),
    }

    cache_hosts = {}

    for server in servers:
        cache_hosts[server] = {}
        info = stats[server].copy()

        for k, v in info.items():
            func = conversion_map.get(k)

            if func is not None:
                info[k] = func(v)

            elif v.isdigit():
                info[k] = int(v)

        info["hit_rate"] = 100.0 * info["get_hits"] / float(info["cmd_get"])
        info["gets_per_second"] = info["cmd_get"] / float(info["uptime"].seconds)
        info["sets_per_second"] = info["cmd_set"] / float(info["uptime"].seconds)
        info["started_at"] = datetime.datetime.now() - info["uptime"]

        cache_hosts[server].update(info)

    return cache_hosts
