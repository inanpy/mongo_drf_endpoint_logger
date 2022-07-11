import json

from mongo_drf_endpoint_logger.threads import LOGGER_THREAD
from mongo_drf_endpoint_logger.serializers import LogInsertSerializer

"""
    url: CharField,
    headers: JsonField,
    body: JsonField,
    method: CharField,
    ip: CharField,
    response: JsonField,
    status_code: CharField",
    execution_time: string,
    created_date: DateTimeField
"""


def insert_log(data):
    serializer = LogInsertSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    if LOGGER_THREAD:
        d = data.copy()
        d['headers'] = json.dumps(d['headers'])
        d['body'] = json.dumps(d['body'])
        d['response'] = json.dumps(d['response'])
        LOGGER_THREAD.put_log_data(data=d)
