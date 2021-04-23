"""
Created by auto_sdk on 2021.03.29
"""
from api.base import RestApi


class OapiCustomerserviceActionQueryRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.ticket_action_page_query = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.customerservice.action.query'
