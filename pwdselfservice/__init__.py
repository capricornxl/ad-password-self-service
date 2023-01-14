import sys

import datetime
from utils.storage.memorystorage import MemoryStorage
from traceback import format_exc


try:
    cache_storage = MemoryStorage()
    cache_storage.set('MemoryStorage', str(datetime.datetime.now()))
    redis_get = cache_storage.get('MemoryStorage')
except Exception as e:
    print("MemoryStorage Exception: {}".format(format_exc()))
    sys.exit(1)
