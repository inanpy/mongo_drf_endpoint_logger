import time
from queue import Queue
from threading import Thread

from django.conf import settings
from django.db.utils import OperationalError

from mongo_drf_endpoint_logger.models import ApiLog


class InsertLogIntoDatabase(Thread):
    def __init__(self):
        super().__init__()

        self.MONGO_DRF_ENDPOINT_LOGGER_QUEUE_MAX_SIZE = 50  # Default
        if hasattr(settings, 'MONGO_DRF_ENDPOINT_LOGGER_QUEUE_MAX_SIZE'):
            self.MONGO_DRF_ENDPOINT_LOGGER_QUEUE_MAX_SIZE = settings.MONGO_DRF_ENDPOINT_LOGGER_QUEUE_MAX_SIZE

        if self.MONGO_DRF_ENDPOINT_LOGGER_QUEUE_MAX_SIZE < 1:
            raise Exception("""
            Value of MONGO_DRF_ENDPOINT_LOGGER_QUEUE_MAX_SIZE must be greater than 0
            """)

        self.MONGO_DRF_ENDPOINT_LOGGER_INTERVAL = 10  # Default DB insertion interval is 10 seconds.
        if hasattr(settings, 'DRF_LOGGER_INTERVAL'):
            self.MONGO_DRF_ENDPOINT_LOGGER_INTERVAL = settings.MONGO_DRF_ENDPOINT_LOGGER_INTERVAL

            if self.MONGO_DRF_ENDPOINT_LOGGER_INTERVAL < 1:
                raise Exception("""
                Value of MONGO_DRF_ENDPOINT_LOGGER_INTERVAL must be greater than 0
                """)
        self._queue = Queue(maxsize=self.MONGO_DRF_ENDPOINT_LOGGER_INTERVAL)

    def put_log_data(self, data):
        self._queue.put(ApiLog(**data))
        if self._queue.qsize() >= self.MONGO_DRF_ENDPOINT_LOGGER_QUEUE_MAX_SIZE:
            self._start_bulk_insertion()

    @staticmethod
    def _insert_into_data_base(bulk_item):
        try:
            # Mongo Bulk Insert
            ApiLog.objects.insert(bulk_item, load_bulk=False)
        except OperationalError:
            raise Exception("""
            ApiLog model does not exists.
            """)
        except Exception as e:
            print('Mongo DRF Endpoint Logger Exception:', e)

    def _start_bulk_insertion(self):
        bulk_item = []
        while not self._queue.empty():
            bulk_item.append(self._queue.get())
        if bulk_item:
            self._insert_into_data_base(bulk_item)

    def start_queue_process(self):
        while True:
            time.sleep(self.MONGO_DRF_ENDPOINT_LOGGER_INTERVAL)
            self._start_bulk_insertion()

    def run(self) -> None:
        self.start_queue_process()
