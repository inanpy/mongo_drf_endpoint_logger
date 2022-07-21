import json
from datetime import datetime
from mongo_drf_endpoint_logger.models import ApiLog
from mongo_drf_endpoint_logger.threads import LOGGER_THREAD
from mongo_drf_endpoint_logger.serializers import LogInsertSerializer

"""
    url: CharField,
    headers: DictField,
    body: DictField,
    method: CharField,
    response: DictField,
    status_code: CharField: 200,
    execution_time: string: 0,
    ip: CharField: 0.0.0.0,
    created_date: DateTimeField: datetime.now()
"""


class LogData:
    def __init__(self, url, headers, body, method, response, status_code, execution_time, ip, created_date):
        self.url = url
        self.headers = headers
        self.body = body
        self.method = method
        self.ip = ip
        self.response = response
        self.status_code = status_code
        self.execution_time = execution_time
        self.created_date = created_date


def dumps_validated_dict(data):
    data['headers'] = json.dumps(data['headers'])
    data['body'] = json.dumps(data['body'])
    data['response'] = json.dumps(data['response'])
    return data


def async_insert_log(url, headers, body, method, response, status_code="200", execution_time="0", ip="0.0.0.0",
                     created_date=datetime.now()
                     ):
    log_object = LogData(url, headers, body, method, response, status_code, execution_time, ip, created_date)
    serializer = LogInsertSerializer(log_object)
    data = serializer.run_validation(serializer.data)
    if LOGGER_THREAD:
        d = data.copy()
        d = dumps_validated_dict(d)
        LOGGER_THREAD.put_log_data(data=d)


def sync_insert_log(url, headers, body, method, response, status_code="200", execution_time="0", ip="0.0.0.0",
                    created_date=datetime.now()
                    ):
    log_object = LogData(url, headers, body, method, response, status_code, execution_time, ip, created_date)
    serializer = LogInsertSerializer(log_object)
    data = serializer.run_validation(serializer.data)
    log = ApiLog(**data)
    log.save()
