import time
import json
from django.conf import settings
from django.urls import resolve
from django.utils import timezone

from mongo_drf_endpoint_logger.utils import (
    get_compiled_headers,
    check_private_data,
    get_request_ip
)

from mongo_drf_endpoint_logger.threads import LOGGER_THREAD


class EndpointLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.MONGO_DRF_ENDPOINT_LOGGER_LOG_TO_DB = False
        self.MONGO_DRF_ENDPOINT_LOGGER_SIGNAL = False
        self.MONGO_DRF_ENDPOINT_LOGGER_PATH_TYPE = 'ABSOLUTE'
        self.MONGO_DRF_ENDPOINT_LOGGER_SKIP_URL_NAME = []
        self.MONGO_DRF_ENDPOINT_LOGGER_SKIP_NAMESPACE = []
        self.MONGO_DRF_ENDPOINT_LOGGER_METHODS = []
        self.MONGO_DRF_ENDPOINT_LOGGER_STATUS_CODES = []
        self.MONGO_DRF_ENDPOINT_LOGGER_EXCLUDE_KEYS = []

        check_key_type_in_settings = {
            'MONGO_DRF_ENDPOINT_LOGGER_LOG_TO_DB': [bool],
            'MONGO_DRF_ENDPOINT_LOGGER_PATH_TYPE': [str],
            'MONGO_DRF_ENDPOINT_LOGGER_SKIP_URL_NAME': [list, tuple],
            'MONGO_DRF_ENDPOINT_LOGGER_SKIP_NAMESPACE': [list, tuple],
            'MONGO_DRF_ENDPOINT_LOGGER_METHODS': [list, tuple],
            'MONGO_DRF_ENDPOINT_LOGGER_STATUS_CODES': [list, tuple],
            'MONGO_DRF_ENDPOINT_LOGGER_EXCLUDE_KEYS': [list, tuple]
        }

        # Check settings attr with value type
        for key, key_type in check_key_type_in_settings.items():
            if hasattr(settings, key):
                value_attr = getattr(settings, key)
                if type(value_attr) in key_type:
                    setattr(self, key, value_attr)

        # TODO: i must add signal for other DB system.

    def __call__(self, request):
        if self.MONGO_DRF_ENDPOINT_LOGGER_LOG_TO_DB:
            request_url_name = resolve(request.path).url_name
            request_namespace = resolve(request.path).namespace
            if (
                    request_namespace == 'admin'
                    or request_namespace in self.MONGO_DRF_ENDPOINT_LOGGER_SKIP_NAMESPACE
                    or request_url_name in self.MONGO_DRF_ENDPOINT_LOGGER_SKIP_URL_NAME
            ):
                return self.get_response(request)
            request_start_time = time.time()

            try:
                request_data = json.loads(request.body) if request.body else ''
            except ValueError as e:
                request_data = ''

            response = self.get_response(request)

            if (
                    self.MONGO_DRF_ENDPOINT_LOGGER_STATUS_CODES
                    and response.status_code not in self.MONGO_DRF_ENDPOINT_LOGGER_STATUS_CODES
            ):
                return response

            request_method = request.method
            if (
                    len(self.MONGO_DRF_ENDPOINT_LOGGER_METHODS) > 0
                    and request_method not in self.MONGO_DRF_ENDPOINT_LOGGER_METHODS
            ):
                return response

            request_headers = get_compiled_headers(request=request)
            content_type_json_values = (
                'application/json',
                'application/vnd.api+json'
            )
            # Check response content type.
            if response.get('content-type') in content_type_json_values:
                # Check response streaming value.
                if getattr(response, 'streaming', False):
                    response_body = '***Response Is Streaming***'
                else:
                    res_content = response.content.decode() if type(response.content) == bytes else response.content
                    response_body = json.loads(res_content)

                # Check request url.
                if self.MONGO_DRF_ENDPOINT_LOGGER_PATH_TYPE == 'ABSOLUTE_URI':
                    request_url = request.build_absolute_uri()
                elif self.MONGO_DRF_ENDPOINT_LOGGER_PATH_TYPE == 'FULL_PATH_URI':
                    request_url = request.get_full_path()
                elif self.MONGO_DRF_ENDPOINT_LOGGER_PATH_TYPE == 'RAW_URI':
                    request_url = request.get_raw_uri()
                else:
                    request_url = request.build_absolute_uri()

                data = dict(
                    url=request_url,
                    headers=check_private_data(request_headers),
                    body=check_private_data(request_data),
                    method=request_method,
                    ip=get_request_ip(request),
                    response=check_private_data(response_body),
                    status_code=response.status_code,
                    execution_time=time.time() - request_start_time,
                    created_date=timezone.now()
                )
                if self.MONGO_DRF_ENDPOINT_LOGGER_LOG_TO_DB:
                    if LOGGER_THREAD:
                        d = data.copy()
                        d['headers'] = json.dumps(d['headers'], indent=4)
                        if request_data:
                            d['body'] = json.dumps(d['body'], indent=4)
                        d['response'] = json.dumps(d['response'], indent=4)
                        LOGGER_THREAD.put_log_data(data=d)
            else:
                return response
        else:
            response = self.get_response(request)
        return response
