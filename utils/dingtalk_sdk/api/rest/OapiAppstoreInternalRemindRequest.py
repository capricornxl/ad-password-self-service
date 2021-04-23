"""
Created by auto_sdk on 2020.04.09
"""
from api.base import RestApi


class OapiAppstoreInternalRemindRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.goods_code = None
        self.process_instance_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.appstore.internal.remind'
