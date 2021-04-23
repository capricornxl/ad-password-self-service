"""
Created by auto_sdk on 2021.03.10
"""
from api.base import RestApi


class OapiV2UserUpdateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.dept_id_list = None
        self.dept_order_list = None
        self.dept_title_list = None
        self.email = None
        self.extension = None
        self.hide_mobile = None
        self.hired_date = None
        self.init_password = None
        self.job_number = None
        self.language = None
        self.mobile = None
        self.name = None
        self.org_email = None
        self.remark = None
        self.senior_mode = None
        self.telephone = None
        self.title = None
        self.userid = None
        self.work_place = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.v2.user.update'
