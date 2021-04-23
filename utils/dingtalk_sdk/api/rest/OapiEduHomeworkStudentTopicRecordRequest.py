"""
Created by auto_sdk on 2020.04.29
"""
from api.base import RestApi


class OapiEduHomeworkStudentTopicRecordRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.student_answer_details = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.homework.student.topic.record'
