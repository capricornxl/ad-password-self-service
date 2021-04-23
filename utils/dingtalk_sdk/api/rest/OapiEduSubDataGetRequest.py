"""
Created by auto_sdk on 2021.01.29
"""
from api.base import RestApi


class OapiEduSubDataGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.orders = None
        self.page_num = None
        self.page_size = None
        self.stat_date = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.sub.data.get'
