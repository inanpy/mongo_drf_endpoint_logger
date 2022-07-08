import re

from django.conf import settings

# Default sensitive keys
PRIVATE_VALUE_KEYS = ['password', 'token', 'access', 'refresh']

if hasattr(settings, 'MONGO_DRF_ENDPOINT_LOGGER_EXCLUDE_KEYS'):
    value_attr = getattr(settings, 'MONGO_DRF_ENDPOINT_LOGGER_EXCLUDE_KEYS')
    if type(value_attr) is (list, tuple):
        PRIVATE_VALUE_KEYS.extend(settings.MONGO_DRF_ENDPOINT_LOGGER_EXCLUDE_KEYS)


# Compile to header items.
def get_compiled_headers(request=None):
    regex = re.compile('^HTTP_')
    return dict(
        (regex.sub('', header), value) for (header, value) in request.META.items() if header.startswith('HTTP_')
    )


def get_request_ip(request):
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    except ValueError:
        return ''


# Check private data
def check_private_data(data):
    if type(data) != dict:
        return data
    for key, value in data.items():
        if key in PRIVATE_VALUE_KEYS:
            data[key] = "***PRIVATE VALUE***"
        if type(value) == dict:
            data[key] = check_private_data(data[key])
        if type(value) == list:
            data[key] = [check_private_data(item) for item in data[key]]
    return data
