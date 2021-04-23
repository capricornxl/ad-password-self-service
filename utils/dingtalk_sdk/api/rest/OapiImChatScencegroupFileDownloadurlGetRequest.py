"""
Created by auto_sdk on 2021.04.01
"""
from api.base import RestApi


class OapiImChatScencegroupFileDownloadurlGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.download_code = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.im.chat.scencegroup.file.downloadurl.get'
