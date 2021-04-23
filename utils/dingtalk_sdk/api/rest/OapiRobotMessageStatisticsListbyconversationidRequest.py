"""
Created by auto_sdk on 2019.07.01
"""
from api.base import RestApi


class OapiRobotMessageStatisticsListbyconversationidRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.conversation_ids = None
        self.page = None
        self.page_size = None
        self.push_id = None
        self.read_status = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.robot.message.statistics.listbyconversationid'
