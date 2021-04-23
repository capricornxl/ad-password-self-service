"""
Created by auto_sdk on 2021.01.06
"""
from api.base import RestApi


class OapiConnectorTriggerSendV2Request(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.trigger_msg_request = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.connector.trigger.send_v2'
