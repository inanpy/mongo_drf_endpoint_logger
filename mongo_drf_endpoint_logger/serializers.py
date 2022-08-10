from rest_framework import serializers
from rest_framework.fields import empty
from mongo_drf_endpoint_logger.utils import check_private_data


class LogInsertSerializer(serializers.Serializer):
    url = serializers.CharField(max_length=99999)
    headers = serializers.DictField()
    body = serializers.DictField()
    method = serializers.CharField(min_length=3, max_length=10)
    ip = serializers.CharField(min_length=5, max_length=20)
    response = serializers.DictField()
    status_code = serializers.IntegerField()
    execution_time = serializers.CharField()
    created_date = serializers.DateTimeField()

    def run_validation(self, data=empty):
        validated_data = super().run_validation(data=data)
        validated_data['body'] = check_private_data(validated_data['body'])
        validated_data['headers'] = check_private_data(validated_data['headers'])
        validated_data['response'] = check_private_data(validated_data['response'])
        return validated_data
