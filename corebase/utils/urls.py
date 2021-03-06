from django.urls import URLPattern, URLResolver, get_resolver


def collect_urls(urls=None, namespace=None, prefix=None):
    if urls is None:
        urls = get_resolver()
    _collected = []
    prefix = prefix or []

    for url_pattern in urls.url_patterns:

        if isinstance(url_pattern, URLResolver):
            _collected += collect_urls(
                url_pattern, 
                namespace=url_pattern.namespace or namespace,
                prefix=prefix + [url_pattern.pattern.regex.pattern],
            )

        elif isinstance(url_pattern, URLPattern):
            _collected.append(
                {'namespace': namespace or '',
                 'name': url_pattern.name or '',
                 'pattern': prefix + [url_pattern.pattern.regex.pattern],
                 'lookup_str': url_pattern.lookup_str,
                 'default_args': dict(url_pattern.default_args)})
        else:
            raise NotImplementedError(repr(url_pattern))

    return _collected


def app_urls():
    all_urls = collect_urls()
    all_urls.sort(key=lambda x: (x['namespace'], x['name']))

    max_lengths = {}
    for u in all_urls:
        for k in ['pattern', 'default_args']:
            u[k] = str(u[k])
        for k, v in list(u.items())[:-1]:
            # Skip app_list due to length (contains all app names)
            if (u['namespace'], u['name'], k) == \
                    ('admin', 'app_list', 'pattern'):
                continue
            max_lengths[k] = max(len(v), max_lengths.get(k, 0))

    return all_urls
