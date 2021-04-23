"""
Created by auto_sdk on 2021.03.17
"""
from api.base import RestApi


class OapiKacOpenliveWhiteUsersListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.live_id = None
        self.page_size = None
        self.page_start = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.kac.openlive.white_users.list'
