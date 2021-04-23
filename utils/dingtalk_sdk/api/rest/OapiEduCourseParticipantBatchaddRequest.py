"""
Created by auto_sdk on 2021.04.20
"""
from api.base import RestApi


class OapiEduCourseParticipantBatchaddRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.course_code = None
        self.course_participants = None
        self.op_userid = None
        self.participant_corpid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.course.participant.batchadd'
