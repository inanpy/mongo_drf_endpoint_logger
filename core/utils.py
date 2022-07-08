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
