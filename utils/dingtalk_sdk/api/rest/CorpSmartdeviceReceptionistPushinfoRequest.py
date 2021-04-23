"""
Created by auto_sdk on 2019.07.03
"""
from api.base import RestApi


class CorpSmartdeviceReceptionistPushinfoRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.desc_content = None
        self.desc_template = None
        self.microapp_agent_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.corp.smartdevice.receptionist.pushinfo'
