from django.conf import settings


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

        check_key_type_in_settings = {
            'MONGO_DRF_ENDPOINT_LOGGER_LOG_TO_DB': bool,
            'MONGO_DRF_ENDPOINT_LOGGER_SIGNAL': bool,
            'MONGO_DRF_ENDPOINT_LOGGER_PATH_TYPE': str,
            'MONGO_DRF_ENDPOINT_LOGGER_SKIP_URL_NAME': list or tuple,
            'MONGO_DRF_ENDPOINT_LOGGER_SKIP_NAMESPACE': list or tuple,
            'MONGO_DRF_ENDPOINT_LOGGER_METHODS': list or tuple,
            'MONGO_DRF_ENDPOINT_LOGGER_STATUS_CODES': list or tuple
        }

        # Check settings attr with value type
        for key, key_type in check_key_type_in_settings:
            if hasattr(settings, key):
                value_attr = getattr(settings, key)
                if type(value_attr) is key_type:
                    setattr(self, key, value_attr)

    def __call__(self, request):
        pass
