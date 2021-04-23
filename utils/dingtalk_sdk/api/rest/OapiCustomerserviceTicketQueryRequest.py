"""
Created by auto_sdk on 2021.03.29
"""
from api.base import RestApi


class OapiCustomerserviceTicketQueryRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.ticket_page_query_dto = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.customerservice.ticket.query'
