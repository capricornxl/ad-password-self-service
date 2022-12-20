import sys

from django_redis import get_redis_connection
from utils.storage.kvstorage import KvStorage
import datetime
from traceback import format_exc


try:
    redis_conn = get_redis_connection()
    cache_storage = KvStorage(redis_conn)
    cache_storage.set('redis_connection', str(datetime.datetime.now()))
    redis_get = cache_storage.get('redis_connection')
except Exception as e:
    print("请排查Redis配置，错误信息如下：")
    print("Redis Exception: {}".format(format_exc()))
    sys.exit(1)
