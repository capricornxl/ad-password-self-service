# -*- coding: utf-8 -*-
from django.apps import AppConfig
import sys


class PasswordManagerConfig(AppConfig):
    name = 'apps.password_manager'
    verbose_name = "Password Manager Application"
    
    def ready(self):
        """
        应用启动时执行的初始化操作
        
        包括：
        1. 自动创建Database Cache表（如果使用database缓存）
        """
        # 导入必须在ready()内部，避免AppRegistryNotReady错误
        from django.conf import settings
        
        # 检查是否需要自动创建缓存表
        if getattr(settings, 'CACHE_AUTO_CREATE_TABLE', False):
            self._auto_create_cache_table()
    
    def _auto_create_cache_table(self):
        """
        自动检测并创建Database Cache表
        
        失败则终止启动（符合Fail-Fast原则）
        """
        from django.conf import settings
        from django.core.management import call_command
        from django.db import connection
        
        cache_table_name = getattr(settings, 'CACHE_TABLE_NAME', 'rate_limit_cache')
        
        try:
            # 检查表是否存在
            with connection.cursor() as cursor:
                table_list = connection.introspection.table_names()
                
                if cache_table_name not in table_list:
                    print(f"检测到缓存表 '{cache_table_name}' 不存在，正在自动创建...")
                    
                    # 调用Django管理命令创建缓存表
                    call_command('createcachetable', verbosity=0)
                    
                    print(f"缓存表 '{cache_table_name}' 创建成功")
                else:
                    print(f"缓存表 '{cache_table_name}' 已存在")
                    
        except Exception as e:
            error_msg = f"""
{'='*70}
致命错误：Database Cache表创建失败
{'='*70}
表名: {cache_table_name}
错误详情: {e}

可能原因：
  1. 数据库连接失败
  2. 数据库权限不足（无法创建表）
  3. 数据库配置错误

解决方法：
  1. 检查数据库配置（DATABASES in settings.py）
  2. 确保数据库用户有CREATE TABLE权限
  3. 手动运行: python manage.py createcachetable
  4. 或切换到memory/file缓存: cache.backend: memory

{'='*70}
"""
            print(error_msg)
            sys.exit(1)  # 终止启动
