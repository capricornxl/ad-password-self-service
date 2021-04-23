"""
Created by auto_sdk on 2020.03.10
"""
from api.base import RestApi


class OapiKacDatavVideoliveGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.param_video_live_summary_request = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.kac.datav.videolive.get'
