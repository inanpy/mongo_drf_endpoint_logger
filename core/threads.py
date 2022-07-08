from core.utils import check_logger_active

LOGGER_THREAD = None

if check_logger_active():
    from core.operations import InsertLogIntoDatabase
    import threading

    LOG_THREAD_NAME = 'insert_log_into_database'
    already_exists = False

    for t in threading.enumerate():
        if t.getName() == LOG_THREAD_NAME:
            already_exists = True

    if not already_exists:
        t = InsertLogIntoDatabase()
        t.daemon = True
        t.setName(LOG_THREAD_NAME)
        t.start()
        LOGGER_THREAD = t
