"""
Created by auto_sdk on 2021.03.29
"""
from api.base import RestApi


class OapiCustomerserviceTicketCreateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.ticket_create = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.customerservice.ticket.create'
