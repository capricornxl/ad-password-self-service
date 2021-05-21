import datetime
from cryptography.fernet import Fernet
from django_redis import get_redis_connection
from utils.storage.kvstorage import KvStorage
from utils.storage.memorystorage import MemoryStorage

try:
    redis_conn = get_redis_connection()
    cache_storage = KvStorage(redis_conn)
    cache_storage.set('redis_connection', str(datetime.datetime.now()))
    redis_get = cache_storage.get('redis_connection')
    # print("Redis连接成功，set/get测试通过--{}，Token缓存将使用Redis处理".format(redis_get))
except Exception as e:
    cache_storage = MemoryStorage()
    print("Redis无法连接，Token缓存将使用MemoryStorage处理")
    print("如果确定需要使用Redis作为缓存，请排查Redis配置，错误信息如下：")
    print("Redis Exception: {}".format(e))

crypto_key = Fernet.generate_key()
