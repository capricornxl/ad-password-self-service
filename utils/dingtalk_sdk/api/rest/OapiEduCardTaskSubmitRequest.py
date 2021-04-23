"""
Created by auto_sdk on 2019.08.23
"""
from api.base import RestApi


class OapiEduCardTaskSubmitRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.card_type = None
        self.content = None
        self.metering_number = None
        self.user_card_task_id = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.card.task.submit'
