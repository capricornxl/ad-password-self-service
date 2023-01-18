#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json

import requests

DEBUG = False


class ApiException(Exception):
    def __init__(self, errCode, errMsg):
        self.errCode = errCode
        self.errMsg = errMsg


class AbstractApi(object):
    def __init__(self):
        return

    def access_token(self):
        raise NotImplementedError

    def http_call(self, url_type, args=None):
        short_url = url_type[0]
        method = url_type[1]
        response = {}
        for retryCnt in range(0, 3):
            if 'POST' == method:
                url = self.__make_url(short_url)
                response = self.__http_post(url, args)
            elif 'GET' == method:
                url = self.__make_url(short_url)
                url = self.__append_args(url, args)
                response = self.__http_get(url)
            else:
                raise ApiException(-1, "unknown method type")

            # check if token expired
            if self.__token_expired(response.get('errcode')):
                self.__refresh_token(short_url)
                retryCnt += 1
                continue
            else:
                break

        return self.__check_response(response)

    @staticmethod
    def __append_args(url, args):
        if args is None:
            return url

        for key, value in args.items():
            if '?' in url:
                url += ('&' + key + '=' + value)
            else:
                url += ('?' + key + '=' + value)
        return url

    @staticmethod
    def __make_url(short_url):
        base = "https://qyapi.weixin.qq.com"
        if short_url[0] == '/':
            return base + short_url
        else:
            return base + '/' + short_url

    def __append_token(self, url):
        if 'ACCESS_TOKEN' in url:
            return url.replace('ACCESS_TOKEN', self.access_token())
        else:
            return url

    def __http_post(self, url, args):
        real_url = self.__append_token(url)

        if DEBUG is True:
            print(real_url, args)

        return requests.post(real_url, data=json.dumps(args, ensure_ascii=False).encode('utf-8')).json()

    def __http_get(self, url):
        real_url = self.__append_token(url)

        if DEBUG is True:
            print(real_url)

        return requests.get(real_url).json()

    def __post_file(self, url, media_file):
        return requests.post(url, file=media_file).json()

    @staticmethod
    def __check_response(response):
        errCode = response.get('errcode')
        errMsg = response.get('errmsg')

        if errCode == 0:
            return response
        else:
            raise ApiException(errCode, errMsg)

    @staticmethod
    def __token_expired(errCode):
        if errCode == 40014 or errCode == 42001 or errCode == 42007 or errCode == 42009:
            return True
        else:
            return False

    def __refresh_token(self, url):
        if 'ACCESS_TOKEN' in url:
            self.access_token()
