import datetime

from django_redis import get_redis_connection

from utils.storage.memorystorage import MemoryStorage
from utils.storage.kvstorage import KvStorage

try:
    redis_conn = get_redis_connection()
    cache_storage = KvStorage(redis_conn)
    cache_storage.set('redis_connection', str(datetime.datetime))
    cache_storage.get('redis_connection')
    print("Redis连接成功，set/get测试通过，Token缓存将使用Redis处理")
except Exception as e:
    cache_storage = MemoryStorage()
    print("Redis无法连接，Token缓存将使用MemoryStorage处理")
    print("如果确定需要使用Redis作为缓存，请排查Redis配置")
    print("Exception: {}".format(e))
