import mongoengine

from core.utils import check_logger_active


if check_logger_active():
    class ApiLog(mongoengine.Document):
        url = mongoengine.StringField(required=True, max_length=512)
        headers = mongoengine.DictField()
        body = mongoengine.DictField()
        method = mongoengine.StringField(max_length=10)
        ip = mongoengine.StringField(max_length=50)
        response = mongoengine.DictField()
        status_code = mongoengine.StringField()
        execution_time = mongoengine.StringField(max_value=8)
        created_date = mongoengine.DateTimeField()
