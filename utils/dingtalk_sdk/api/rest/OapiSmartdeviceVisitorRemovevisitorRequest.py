"""
Created by auto_sdk on 2018.07.25
"""
from api.base import RestApi


class OapiSmartdeviceVisitorRemovevisitorRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.reservation_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.smartdevice.visitor.removevisitor'
