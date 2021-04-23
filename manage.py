#!/usr/bin/env python
import os
import sys
from utils.ad_ops import AdOps

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pwdselfservice.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    try:
        AdOps()
    except Exception as e:
        print(str(e))
        print("未能连接到AD，先决条件未满足，Django不会运行..")
        sys.exit(1)
    execute_from_command_line(sys.argv)
