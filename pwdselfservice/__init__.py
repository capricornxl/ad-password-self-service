import datetime
import sys
import traceback
import logging
from django_redis import get_redis_connection
from utils.storage.kvstorage import KvStorage

logger = logging.getLogger(__name__)

try:
    redis_conn = get_redis_connection()
    cache_storage = KvStorage(redis_conn)
    cache_storage.set('test_redis_connection', str(datetime.datetime))
    cache_storage.get('test_redis_connection')
    cache_storage.delete('test_redis_connection')
    logger.info("Redis连接成功，set/get/delete测试通过...")
except Exception as e:
    cache_storage = None
    logger.error("Redis无法连接，请排查Redis配置...")
    logger.error("{}".format(traceback.format_exc()))
    sys.exit(1)

