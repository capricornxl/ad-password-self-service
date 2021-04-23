"""
Created by auto_sdk on 2019.08.23
"""
from api.base import RestApi


class OapiEduCardTaskTodayListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.card_type = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.card.task.today.list'
