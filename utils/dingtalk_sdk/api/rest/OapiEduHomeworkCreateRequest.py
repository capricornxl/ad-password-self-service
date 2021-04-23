"""
Created by auto_sdk on 2020.12.04
"""
from api.base import RestApi


class OapiEduHomeworkCreateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.attributes = None
        self.biz_code = None
        self.course_name = None
        self.hw_content = None
        self.hw_deadline = None
        self.hw_deadline_open = None
        self.hw_media = None
        self.hw_photo = None
        self.hw_title = None
        self.hw_type = None
        self.hw_video = None
        self.identifier = None
        self.scheduled_release = None
        self.scheduled_time = None
        self.select_class = None
        self.select_stu = None
        self.status = None
        self.target_role = None
        self.teacher_name = None
        self.teacher_userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.homework.create'
