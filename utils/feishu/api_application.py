# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

from typing import TYPE_CHECKING, List

from utils.feishu.dt_application import App
from utils.feishu.dt_code import SimpleUser
from utils.feishu.dt_enum import I18NType
from utils.feishu.dt_help import make_datatype
from utils.feishu.exception import LarkInvalidArguments
from utils.feishu.helper import converter_enum

if TYPE_CHECKING:
    from utils.feishu.api import OpenLark


class APIApplicationMixin(object):
    def is_user_admin(self, open_id=None, employee_id=None):
        """获取应用管理权限

        :type self: OpenLark
        :param open_id: 用户 open_id
        :type open_id: str
        :param employee_id: 用户租户 ID
        :type employee_id: str
        :return: 是否是应用管理员
        :rtype: bool

        该接口用于查询用户是否为应用管理员。

        https://open.feishu.cn/document/ukTMukTMukTM/uITN1EjLyUTNx4iM1UTM
        """
        if open_id:
            url = '/open-apis/application/v3/is_user_admin?open_id={}'.format(open_id)
        elif employee_id:
            url = '/open-apis/application/v3/is_user_admin?employee_id={}'.format(employee_id)
        else:
            raise LarkInvalidArguments(msg='[is_user_admin] empty open_id and employee_id')

        url = self._gen_request_url(url)
        res = self._get(url, with_tenant_token=True)

        data = res['data']
        return data['is_app_admin']  # type: bool

    def get_app_visibility(self, app_id, user_page_token='', user_page_size=20):
        """获取应用在企业内的可用范围

        :type self: OpenLark
        :param app_id: 	目标应用的 ID
        :type app_id: str
        :param user_page_token: 分页拉取用户列表起始位置标示，不填表示从头开始
        :type user_page_token: str
        :param user_page_size: 本次拉取用户列表最大个数(最大值 1000 ，0 自动最大个数 )
        :type user_page_size: int
        :return: (部门列表, 可见的用户列表，是否全员可见，是否还有更多用户，用户翻页token，
                    所有可见用户数量（仅包含单独设置的用户，可用部门中的用户不计算在内)
        :rtype: (list[str], list[SimpleUser], bool, bool, str, int)

        该接口用于查询应用在该企业内可以被使用的范围，只能被企业自建应用调用且需要“获取应用信息”权限。

        https://open.feishu.cn/document/ukTMukTMukTM/uIjM3UjLyIzN14iMycTN
        """
        url = self._gen_request_url('/open-apis/application/v1/app/visibility?app_id={}'.format(app_id))
        if user_page_token:
            url = '{}&user_page_token={}'.format(url, user_page_token)
        if user_page_size:
            url = '{}&user_page_size={}'.format(url, user_page_size)
        res = self._get(url, with_tenant_token=True)

        data = res['data']
        department_ids = [i.get('id') for i in data.get('departments', [])]  # type: List[str]
        users = [make_datatype(SimpleUser, i) for i in data.get('users', [])]  # type: List[SimpleUser]
        is_visible_to_all = bool(data.get('is_visible_to_all', False))  # type: bool
        has_more_users = bool(data.get('has_more_users', False))  # type: bool
        user_page_token = data.get('user_page_token')  # type: str
        total_user_count = data.get('total_user_count')  # type: int

        return department_ids, users, is_visible_to_all, has_more_users, user_page_token, total_user_count

    def get_visible_apps(self, user_id=None, open_id=None, page_size=20, page_token='', lang=I18NType.zh_cn):
        """获取应用在企业内的可用范围

        :type self: OpenLark
        :param user_id: 目标用户 user_id，与 open_id 至少给其中之一，user_id 优先于 open_id
        :type user_id: str
        :param open_id: 目标用户 open_id
        :type open_id: str
        :param page_size: 本次拉取用户列表最大个数(最大值 1000 ，0 自动最大个数 )
        :type page_size: int
        :param page_token: 分页拉取用户列表起始位置标示，不填表示从头开始
        :type page_token: str
        :param lang: 优先展示的应用信息的语言版本（zh_cn：中文，en_us：英文，ja_jp：日文）
        :type lang: I18NType
        :return: 是否还有更多, page_token, page_size, 总数, 语言, 应用列表
        :rtype: (bool, str, int, int, I18NType, list[App])

        该接口用于查询应用在该企业内可以被使用的范围，只能被企业自建应用调用且需要“获取应用信息”权限。

        https://open.feishu.cn/document/ukTMukTMukTM/uIjM3UjLyIzN14iMycTN
        """
        url = self._gen_request_url('/open-apis/application/v1/user/visible_apps?')
        if user_id:
            url = '{}&user_id={}'.format(url, user_id)
        elif open_id:
            url = '{}&open_id={}'.format(url, open_id)
        else:
            raise LarkInvalidArguments(msg='empty user_id and open_id')
        if page_token:
            url = '{}&page_token={}'.format(url, page_token)
        if page_size:
            url = '{}&page_size={}'.format(url, page_size)
        if lang:
            url = '{}&lang={}'.format(url, converter_enum(lang))

        res = self._get(url, with_tenant_token=True)
        data = res['data']

        apps = [make_datatype(App, i) for i in data.get('app_list', [])]  # type: List[App]

        has_more = bool(data.get('has_more', False))  # type: bool
        lang = I18NType(data.get('lang', 'zh_cn'))  # type: I18NType
        page_size = data.get('page_size')  # type: int
        page_token = data.get('page_token')  # type: str
        total_count = data.get('total_count')  # type: int
        return has_more, page_token, page_size, total_count, lang, apps

    def get_installed_apps(self, page_size=20, page_token='', lang=I18NType.zh_cn, status=-1):
        """获取企业安装的应用

        :type self: OpenLark
        :param page_size: 本次拉取用户列表最大个数(最大值 1000 ，0 自动最大个数 )
        :type page_size: int
        :param page_token: 分页拉取用户列表起始位置标示，不填表示从头开始
        :type page_token: str
        :param lang: 优先展示的应用信息的语言版本（zh_cn：中文，en_us：英文，ja_jp：日文）
        :type lang: I18NType
        :param status: 要返回的应用的状态，0:停用；1:启用；-1:全部
        :type status: int
        :return: 是否还有更多, page_token, page_size, 总数, 语言, 应用列表
        :rtype: (bool, str, int, int, I18NType, list[App])

        该接口用于查询企业安装的应用列表，只能被企业自建应用调用且需要“获取应用信息”权限。

        https://open.feishu.cn/document/ukTMukTMukTM/uYDN3UjL2QzN14iN0cTN
        """
        url = self._gen_request_url('/open-apis/application/v3/app/list?')
        if page_token:
            url = '{}&page_token={}'.format(url, page_token)
        if page_size:
            url = '{}&page_size={}'.format(url, page_size)
        if lang:
            url = '{}&lang={}'.format(url, converter_enum(lang))
        if status in [0, 1, -1]:
            url = '{}&status={}'.format(url, status)

        res = self._get(url, with_tenant_token=True)
        data = res['data']

        apps = [make_datatype(App, i) for i in data.get('app_list', [])]  # type: List[App]

        has_more = bool(data.get('has_more', False))  # type: bool
        lang = I18NType(data.get('lang', 'zh_cn'))  # type: I18NType
        page_size = data.get('page_size')  # type: int
        page_token = data.get('page_token')  # type: str
        total_count = data.get('total_count')  # type: int
        return has_more, page_token, page_size, total_count, lang, apps

    def update_app_visibility(self, app_id, add_users=None, del_users=None, add_departments=None, del_departments=None,
                              is_visiable_to_all=None):
        """更新应用可用范围

        :type self: OpenLark
        :param app_id: 应用 ID
        :type app_id: str
        :param add_users: 增加的用户列表，元素个数不超过500，先增加后删除
        :type add_users: list[SimpleUser]
        :param del_users: 删除的用户列表，元素个数不超过 500，先增加后删除
        :type del_users: list[SimpleUser]
        :param add_departments: 添加的部门列表，元素个数不超过 500，先增加后删除
        :type add_departments: list[str]
        :param del_departments: 删除的部门列表，元素个数不超过 500，先增加后删除
        :type del_departments: list[str]
        :param is_visiable_to_all: 是否全员可见，不填：继续当前状态不改变
        :type is_visiable_to_all: bool

        该接口用于增加或者删除指定应用被哪些人可用，只能被企业自建应用调用且需要“管理应用”权限。

        https://open.feishu.cn/document/ukTMukTMukTM/ucDN3UjL3QzN14yN0cTN
        """
        url = self._gen_request_url('/open-apis/application/v3/app/update_visibility')

        _add_users = []
        for i in (add_users or []):
            if i.user_id:
                _add_users.append({'user_id': i.user_id})
            elif i.open_id:
                _add_users.append({'open_id': i.open_id})
            else:
                raise LarkInvalidArguments(msg='empty user_id and open_id')

        _del_users = []
        for i in (del_users or []):
            if i.user_id:
                _del_users.append({'user_id': i.user_id})
            elif i.open_id:
                _del_users.append({'open_id': i.open_id})
            else:
                raise LarkInvalidArguments(msg='empty user_id and open_id')

        body = {
            'app_id': app_id,
            'add_users': _add_users,
            'del_users': _del_users,
            'add_departments': add_departments or [],
            'del_departments': del_departments or []
        }

        if is_visiable_to_all is not None:
            body['is_visiable_to_all'] = int(is_visiable_to_all)
        self._post(url, body=body, with_tenant_token=True)
