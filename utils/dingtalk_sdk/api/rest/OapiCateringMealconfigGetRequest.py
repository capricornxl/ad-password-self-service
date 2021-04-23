"""
Created by auto_sdk on 2021.03.10
"""
from api.base import RestApi


class OapiCateringMealconfigGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.meal_day_offset = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.catering.mealconfig.get'
