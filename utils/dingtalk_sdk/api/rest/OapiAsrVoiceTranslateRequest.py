"""
Created by auto_sdk on 2020.09.11
"""
from api.base import RestApi


class OapiAsrVoiceTranslateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.media_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.asr.voice.translate'
