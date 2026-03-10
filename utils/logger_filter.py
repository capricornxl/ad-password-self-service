#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from functools import wraps
from traceback import format_exc


def decorator_request_logger(logger):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            try:
                rsp = func(request, *args, **kwargs)
                logger.info(
                    f'Request Arguments: {args} {kwargs}')
                # logger.info(
                #     f'Request: {request.META["REMOTE_ADDR"]} {request.method} "{request.META["PATH_INFO"]}'
                #     f'{request.META["QUERY_STRING"]} {request.META["SERVER_PROTOCOL"]}" {rsp.status_code} {rsp.content}')
                logger.info(rsp)
                return rsp
            except Exception as e:
                logger.error(format_exc())
                raise e

        return wrapper

    return decorator


def decorator_default_logger(logger):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f'{args}, {kwargs}')
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(format_exc())
                raise e

        return wrapper

    return decorator
