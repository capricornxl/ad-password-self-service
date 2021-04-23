"""
Created by auto_sdk on 2019.07.03
"""
from api.base import RestApi


class OapiSmartdeviceVisitorAddvisitorRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.visitor_vo = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.smartdevice.visitor.addvisitor'
