"""
Created by auto_sdk on 2020.08.24
"""
from api.base import RestApi


class OapiEduCourseParticipantRemoveRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.course_code = None
        self.op_userid = None
        self.participant_corpid = None
        self.participant_id = None
        self.participant_type = None
        self.role = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.course.participant.remove'
