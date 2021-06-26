# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

import time
from collections import OrderedDict
from threading import RLock

_NOTSET = object()


class _Cache(object):
    """
    An in-memory, FIFO cache object that supports:
    - Maximum number of cache entries
    - Global TTL default
    - Per cache entry TTL
    - TTL first/non-TTL FIFO cache eviction policy
    Cache entries are stored in an ``OrderedDict`` so that key ordering based
    on the cache type can be maintained without the need for additional
    list(s). Essentially, the key order of the ``OrderedDict`` is treated as an
    "eviction queue" with the convention that entries at the beginning of the
    queue are "newer" while the entries at the end are "older" (the exact
    meaning of "newer" and "older" will vary between different cache types).
    When cache entries need to be evicted, expired entries are removed first
    followed by the "older" entries (i.e. the ones at the end of the queue).
    Attributes:
        maxsize (int, optional): Maximum size of cache dictionary. Defaults to ``256``.
        ttl (int, optional): Default TTL for all cache entries. Defaults to ``0`` which
            means that entries do not expire.
        timer (callable, optional): Timer function to use to calculate TTL expiration.
            Defaults to ``time.time``.
        default (mixed, optional): Default value or function to use in :meth:`get` when
            key is not found. If callable, it will be passed a single argument, ``key``,
            and its return value will be set for that cache key.
    """

    def __init__(self, maxsize=None, ttl=None, timer=None, default=None):
        if maxsize is None:
            maxsize = 256

        if ttl is None:
            ttl = 0

        if timer is None:
            timer = time.time

        self.setup()
        self.configure(maxsize=maxsize, ttl=ttl, timer=timer, default=default)

    def setup(self):
        self._cache = OrderedDict()
        self._expire_times = {}
        self._lock = RLock()

    def configure(self, maxsize=None, ttl=None, timer=None, default=None):
        """
        Configure cache settings. This method is meant to support runtime level
        configurations for global level cache objects.
        """
        if maxsize is not None:
            if not isinstance(maxsize, int):
                raise TypeError("maxsize must be an integer")

            if not maxsize >= 0:
                raise ValueError("maxsize must be greater than or equal to 0")

            self.maxsize = maxsize

        if ttl is not None:
            if not isinstance(ttl, (int, float)):
                raise TypeError("ttl must be a number")

            if not ttl >= 0:
                raise ValueError("ttl must be greater than or equal to 0")

            self.ttl = ttl

        if timer is not None:
            if not callable(timer):
                raise TypeError("timer must be a callable")

            self.timer = timer

        self.default = default

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, list(self.copy().items()))

    def __len__(self):
        with self._lock:
            return len(self._cache)

    def __contains__(self, key):
        with self._lock:
            return key in self._cache

    def __iter__(self):
        for i in self.keys():
            yield i

    def __next__(self):
        return next(iter(self._cache))

    def next(self):
        return next(iter(self._cache))

    def copy(self):
        """
        Return a copy of the cache.
        Returns:
            OrderedDict
        """
        with self._lock:
            return self._cache.copy()

    def keys(self):
        """
        Return ``dict_keys`` view of all cache keys.
        Note:
            Cache is copied from the underlying cache storage before returning.
        Returns:
            dict_keys
        """
        return self.copy().keys()

    def _has(self, key):
        # Use get method since it will take care of evicting expired keys.
        return self._get(key, default=_NOTSET) is not _NOTSET

    def size(self):
        """Return number of cache entries."""
        return len(self)

    def full(self):
        """
        Return whether the cache is full or not.
        Returns:
            bool
        """
        if self.maxsize == 0:
            return False
        return len(self) >= self.maxsize

    def get(self, key, default=None):
        """
        Return the cache value for `key` or `default` or ``missing(key)`` if it doesn't
        exist or has expired.
        Args:
            key (mixed): Cache key.
            default (mixed, optional): Value to return if `key` doesn't exist. If any
                value other than ``None``, then it will take precendence over
                :attr:`missing` and be used as the return value. If `default` is
                callable, it will function like :attr:`missing` and its return value
                will be set for the cache `key`. Defaults to ``None``.
        Returns:
            mixed: The cached value.
        """
        with self._lock:
            return self._get(key, default=default)

    def _get(self, key, default=None):
        try:
            value = self._cache[key]

            if self.expired(key):
                self._delete(key)
                raise KeyError
        except KeyError:
            if default is None:
                default = self.default

            if callable(default):
                value = default(key)
                self._set(key, value)
            else:
                value = default

        return value

    def add(self, key, value, ttl=None):
        """
        Add cache key/value if it doesn't already exist. Essentially, this method
        ignores keys that exist which leaves the original TTL in tact.
        Note:
            Cache key must be hashable.
        Args:
            key (mixed): Cache key to add.
            value (mixed): Cache value.
            ttl (int, optional): TTL value. Defaults to ``None`` which uses :attr:`ttl`.
        """
        with self._lock:
            self._add(key, value, ttl=ttl)

    def _add(self, key, value, ttl=None):
        if self._has(key):
            return
        self._set(key, value, ttl=ttl)

    def set(self, key, value, ttl=None):
        """
        Set cache key/value and replace any previously set cache key. If the cache key
        previous existed, setting it will move it to the end of the cache stack which
        means it would be evicted last.
        Note:
            Cache key must be hashable.
        Args:
            key (mixed): Cache key to set.
            value (mixed): Cache value.
            ttl (int, optional): TTL value. Defaults to ``None`` which uses :attr:`ttl`.
        """
        with self._lock:
            self._set(key, value, ttl=ttl)

    def _set(self, key, value, ttl=None):
        if ttl is None:
            ttl = self.ttl

        if key not in self:
            self.evict()

        self._delete(key)
        self._cache[key] = value

        if ttl and ttl > 0:
            self._expire_times[key] = self.timer() + ttl

    def _delete(self, key):
        count = 0

        try:
            del self._cache[key]
            count = 1
        except KeyError:
            pass

        try:
            del self._expire_times[key]
        except KeyError:
            pass

        return count

    def delete_expired(self):
        """
        Delete expired cache keys and return number of entries deleted.
        Returns:
            int: Number of entries deleted.
        """
        with self._lock:
            return self._delete_expired()

    def _delete_expired(self):
        count = 0

        if not self._expire_times:
            return count

        # Use a static expiration time for each key for better consistency as opposed to
        # a newly computed timestamp on each iteration.
        expires_on = self.timer()
        expire_times = self._expire_times.copy()

        for key, expiration in expire_times.items():
            if expiration <= expires_on:
                count += self._delete(key)

        return count

    def expired(self, key, expires_on=None):
        """
        Return whether cache key is expired or not.
        Args:
            key (mixed): Cache key.
            expires_on (float, optional): Timestamp of when the key is considered
                expired. Defaults to ``None`` which uses the current value returned from
                :meth:`timer`.
        Returns:
            bool
        """
        if not expires_on:
            expires_on = self.timer()

        try:
            return self._expire_times[key] <= expires_on
        except KeyError:
            return key not in self

    def evict(self):
        """
        Perform cache eviction per the cache replacement policy:
        - First, remove **all** expired entries.
        - Then, remove non-TTL entries using the cache replacement policy.
        When removing non-TTL entries, this method will only remove the minimum number
        of entries to reduce the number of entries below :attr:`maxsize`. If
        :attr:`maxsize` is ``0``, then only expired entries will be removed.
        Returns:
            int: Number of cache entries evicted.
        """
        count = self.delete_expired()

        if not self.full():
            return count

        with self._lock:
            while self.full():
                try:
                    self._popitem()
                except KeyError:  # pragma: no cover
                    break
                count += 1

        return count

    def _popitem(self):
        try:
            key = next(self)
        except StopIteration:
            raise KeyError("popitem(): cache is empty")

        value = self._cache[key]

        self._delete(key)

        return (key, value)
