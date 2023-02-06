# -*- coding: utf-8 -*-
import os.path
import re
import sys
from copy import deepcopy as dcopy
from functools import wraps
from traceback import format_exc
from pwdselfservice.settings import BASE_DIR
from pprint import pformat as cformat


NOT_CHECK_CALL_FUNC_NAME = []

DEBUG_FLAG_FILE_PATH = os.path.join(BASE_DIR, '/log')


class TraceFuncContext:
    def __init__(self, func_name, logger, log_head='Run function', debug_flag_name=None, verbose=1,
                 pretty=False, indent=0, check_calls=None):
        self.name = func_name
        self.logger = logger
        self.debug_flag_name = debug_flag_name
        self.log_head = log_head
        self.verbose = verbose
        self.pretty = pretty
        self.indent = indent
        self.check_calls = check_calls
        self.copied_verbose = dcopy(verbose)
        self.is_exit = False
        self.debug_flag_suffix = '.debug.flag'
        if self.verbose is not None:
            self.check_calls = None

    def __enter__(self):
        sys.settrace(self.get_callbacks)

    def check_debug_flag(self):
        if self.debug_flag_name:
            if os.path.isfile(os.path.join(DEBUG_FLAG_FILE_PATH, '{}{}'.format(
                    self.debug_flag_name, self.debug_flag_suffix))):
                self.verbose = 2
            else:
                self.verbose = self.copied_verbose

    @staticmethod
    def check_in_excludes(func_name):
        if len(NOT_CHECK_CALL_FUNC_NAME) > 0:
            regex_gen = r'{0}'.format('|'.join(NOT_CHECK_CALL_FUNC_NAME))
            re_c = re.compile(regex_gen, flags=re.IGNORECASE)
            return re_c.search(func_name)
        return False

    def get_callbacks(self, frame, event, arg=None):
        self.check_debug_flag()
        __co_name = frame.f_code.co_name
        if event != 'call':    # Only trace call
            return
        if self.verbose:
            if self.verbose == 1 or self.verbose == 'v':
                self.check_calls = [self.name]
                if __co_name not in self.check_calls:
                    return
            elif self.verbose == 2 or self.verbose == 'vv':
                if self.check_calls is None:
                    self.check_calls = list(set(frame.f_code.co_names))
                    self.check_calls.append(self.name)
                if __co_name not in self.check_calls or self.check_in_excludes(__co_name):
                    return
            else:
                raise ValueError("UNKNOWN VERBOSE VALUE: support verbose is 1/2 or v/vv...")
        else:
            if self.check_calls is None:
                self.check_calls = [self.name]
            else:
                if isinstance(self.check_calls, list):
                    self.check_calls.append(self.name)
                else:
                    raise ValueError("CHECK CALLS TYPE ERROR: check_calls need a list or tuple with function name.")
            if __co_name not in self.check_calls:
                return
        return self.get_code_line

    def get_code_line(self, frame, event, agr=None):
        # 正常情况下只有line或return事件才做记录
        if event not in ['line', 'return']:
            return
        __code = frame.f_code
        __func_name = __code.co_name
        __line_num = frame.f_lineno
        __locals = frame.f_locals
        if __func_name == self.name:
            self.logger.info(
                "{4} [{0}] trace detail "
                "--- {1} {2}, locals as following: {5}{3}{5}".format(__func_name,
                                                                     event,
                                                                     __line_num,
                                                                     cformat(__locals, indent=self.indent)
                                                                     if self.pretty else __locals,
                                                                     self.log_head,
                                                                     '\n' if self.pretty else ''
                                                                     ))
        else:
            self.logger.info(
                "{5} [{0}] call [{1}] trace detail "
                "--- {2} {3}, locals as following: {6}{4}{6}".format(self.name,
                                                                     __func_name,
                                                                     event,
                                                                     __line_num,
                                                                     cformat(__locals, indent=self.indent)
                                                                     if self.pretty else __locals,
                                                                     self.log_head,
                                                                     '\n' if self.pretty else ''
                                                                     ))

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.settrace(None)


def decorator_logger(logger, log_head='Run function', debug_flag_name=None, verbose=1, check_calls=None,
                     pretty=False, indent=0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_consts = func.__code__.co_consts
            logger.debug("{4} [{0}] entering trace with --- consts-{3}, args-{1}, kwargs-{2}...".format(
                func.__name__, args, kwargs, func_consts, log_head))

            with TraceFuncContext(func.__name__, logger,
                                  log_head=log_head,
                                  debug_flag_name=debug_flag_name,
                                  verbose=verbose,
                                  check_calls=check_calls,
                                  pretty=pretty,
                                  indent=indent
                                  ):
                try:
                    func_res = func(*args, **kwargs)
                    logger.debug("{4} [{0}] exiting trace with --- consts-{3}, args-{1}, kwargs-{2}...".format(
                        func.__name__, args, kwargs, func_consts, log_head))
                    return func_res
                except Exception as e:
                    logger.error(
                        "{4} [{0}] has exception, trace with --- consts-{3}, args-{1}, kwargs-{2}. Trackback as "
                        "following: ".format(
                            func.__name__, args, kwargs, func_consts, log_head))
                    logger.error(format_exc())
                    raise e
        return wrapper
    return decorator
