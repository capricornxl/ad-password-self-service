# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

from six import PY2

if PY2:
    def implements_to_string(cls):
        cls.__unicode__ = cls.__str__
        cls.__str__ = lambda x: x.__unicode__().encode('utf-8')
        return cls
else:
    def implements_to_string(x):
        return x


@implements_to_string
class OpenLarkException(Exception):
    def __init__(self, *args, **kwargs):
        """基本 Exception
        """
        self.code = kwargs.pop('code', None) or getattr(self, 'code', None) or 0
        self.msg = kwargs.pop('msg', None) or getattr(self, 'msg', None)
        self.url = kwargs.pop('url', None) or getattr(self, 'url', None)

    def __str__(self):
        if PY2:
            if self.url:
                return u'<{} code={} msg="{}" url="{}">'.format(self.__class__.__name__, self.code, self.msg, self.url)
            else:
                return u'<{} code={} msg="{}">'.format(self.__class__.__name__, self.code, self.msg)
        else:
            if self.url:
                return '<{} code={} msg="{}" url="{}">'.format(self.__class__.__name__, self.code, self.msg, self.url)
            else:
                return '<{} code={} msg="{}">'.format(self.__class__.__name__, self.code, self.msg)


# --------- OpenLark SDK 定义的参数错误

class LarkInvalidArguments(OpenLarkException):
    code = 999901
    msg = 'feishu invalid arguments'


class LarkInvalidCallback(OpenLarkException):
    code = 999902
    msg = 'feishu callback error'


class LarkGetAppTicketFail(OpenLarkException):
    code = 999903
    msg = 'get app_ticket fail'


class LarkUnknownError(OpenLarkException):
    code = 999904
    msg = 'unknown error'


# --------- 机器人和服务端异常

class LarkSendMessageFailException(OpenLarkException):
    code = 10002
    msg = '发送消息失败'


class LarkRequestParamsInvalidException(OpenLarkException):
    code = 10003
    msg = '请求参数不合法'


class LarkGetUserInfoFailOrUserIDNotExistException(OpenLarkException):
    code = 10004
    msg = '获取用户信息失败或者用户 ID 不存在'


class LarkConflictAppIDException(OpenLarkException):
    code = 10005
    msg = '生成 token 的 app_id 和相关 chat、open_id 的 app_id 不一致'


class LarkGetOpenChatIDFailException(OpenLarkException):
    code = 10009
    msg = '获取 open_chat_id 失败'


class LarkForbiddenSendMessageException(OpenLarkException):
    code = 10010
    msg = '禁止发送消息，请检查 scope 权限，机器人可见性范围'


class LarkGetAppAccessTokenFailException(OpenLarkException):
    code = 10012
    msg = '获取 app access token 失败'


class LarkGetTenantAccessTokenFailException(OpenLarkException):
    code = 10013  # 10014
    msg = '获取 tenant access token 失败'


class LarkWrongAppSecretException(OpenLarkException):
    code = 10015
    msg = 'app_secret 不正确'


class LarkSendAppTicketFailException(OpenLarkException):
    code = 10016
    msg = '发送 app_ticket 失败'


class LarkUnsupportedUrgentTypeException(OpenLarkException):
    code = 10019
    msg = '加急类型不支持'


class LarkWrongMessageIDException(OpenLarkException):
    code = 10020
    msg = '消息 ID 不正确'


class LarkForbiddenUrgentException(OpenLarkException):
    code = 10023
    msg = '没有加急 scope 权限'


class LarkInvalidOpenChatIDException(OpenLarkException):
    code = 10029
    msg = 'open_chat_id 不合法'


class LarkBotNotInChatException(OpenLarkException):
    code = 10030
    msg = '机器人不在群里'


class LarkAllOpenIDInvalidException(OpenLarkException):
    code = 10032
    msg = '所有 open_id 都不合法'


class LarkUnsupportedCrossTenantException(OpenLarkException):
    code = 10034
    msg = '不支持跨企业操作'


class LarkGetMessageIDFailException(OpenLarkException):
    code = 10037
    msg = '获取 message_id 失败'


class LarkGetSSOAccessTokenFailException(OpenLarkException):
    code = 11000
    msg = '获取 sso_access_token 失败'


class LarkGetCheckSecurityTokenFailException(OpenLarkException):
    code = 11001
    msg = '获取 CheckSecurityToken 失败'


class LarkCheckOpenChatIDFailException(OpenLarkException):
    code = 11100
    msg = 'open_chat_id 不合法或者 chat 不存在'


class LarkOpenIDNotExistException(OpenLarkException):
    code = 11101
    msg = 'open_id 不存在'


class LarkGetOpenIDFailException(OpenLarkException):
    code = 11102
    msg = '查询用户 open_id 失败'


class LarkOpenDepartmentIDNotExistException(OpenLarkException):
    code = 11103
    msg = 'open_department_id 不存在'


class LarkGetOpenDepartmentIDFailException(OpenLarkException):
    code = 11104
    msg = '查询用户 open_department_id 失败'


class LarkEmployeeIDNotExistException(OpenLarkException):
    code = 11105
    msg = 'user_id 不存在'


class LarkGetEmployeeIDFailException(OpenLarkException):
    code = 11106
    msg = '查询用户 user_id 失败'


class LarkUpdateChatNameFailException(OpenLarkException):
    code = 11200
    msg = '更新群名称失败'


class LarkBotNotGroupAdminException(OpenLarkException):
    code = 11201  # 11208
    msg = '机器人不是群主'


class LarkOnlyChatAdminCanInviteUserException(OpenLarkException):
    code = 11202
    msg = '只有群主才能拉用户进群'


class LarkForbiddenBotBatchSendMessageToUserException(OpenLarkException):
    code = 11203
    msg = '机器人没有给用户批量发送权限'


class LarkForbiddenBotBatchSendMessageToDepartmentException(OpenLarkException):
    code = 11204
    msg = '机器人没有给部门批量发送权限'


class LarkAppHasNoBotException(OpenLarkException):
    code = 11205
    msg = '应用没有机器人'


class LarkUserCannotGrantToChatAdminException(OpenLarkException):
    code = 11206
    msg = '用户不在群中不能被设置为群主'


class LarkAppUnavailableException(OpenLarkException):
    code = 11207
    msg = 'app 不可用'


class LarkAppNotExistException(OpenLarkException):
    code = 11209
    msg = 'app 不存在'


class LarkAppUsageInfoNotExistException(OpenLarkException):
    code = 11210
    msg = 'AppUsageInfo 不存在'


class LarkInviteUserToChatInvalidParamsException(OpenLarkException):
    code = 11211
    msg = '拉人进群参数错误'


class LarkRemoveUserFromChatInvalidParamsException(OpenLarkException):
    code = 11212
    msg = '踢人出群参数错误'


class LarkUpdateChatInvalidParamsException(OpenLarkException):
    code = 11213
    msg = '更新群参数错误'


class LarkUploadImageInvalidParamsException(OpenLarkException):
    code = 11214
    msg = '上传图片参数错误'


class LarkEmptyChatIDException(OpenLarkException):
    code = 11215
    msg = 'chat_id 为空'


class LarkGetChatIDFailException(OpenLarkException):
    code = 11216
    msg = '获取chat_id失败'


class LarkInviteBotToChatFailException(OpenLarkException):
    code = 11217
    msg = '拉机器人进群失败'


class LarkBotInChatFullException(OpenLarkException):
    code = 11218
    msg = '群机器人已满'


class LarkUnsupportedChatCrossTenantException(OpenLarkException):
    code = 11219
    msg = '不支持 chat 跨租户'


class LarkForbiddenBotDisbandChatException(OpenLarkException):
    code = 11220
    msg = '禁止机器人解散群'


class LarkBotForbiddenToGetImageBelongToThemException(OpenLarkException):
    code = 11221
    msg = '机器人不能获取不属于自己的图片'


class LarkOwnerOfBotIsNotInChatException(OpenLarkException):
    code = 11222
    msg = '机器人的 Owner 不在群里'


class LarkNotOpenApplicationSendMessagePermissionException(OpenLarkException):
    code = 11223
    msg = '没有打开应用发消息权限'


class LarkInvalidMessageIDException(OpenLarkException):
    code = 11224
    msg = 'message_id 参数错误'


class LarkAppIsNotVisibleToUserException(OpenLarkException):
    code = 11225
    msg = '你的应用对用户不可见'


class LarkInvalidAppIDException(OpenLarkException):
    code = 11226
    msg = 'app_id 参数不对或者没传'


class LarkImageKeyNotExistException(OpenLarkException):
    code = 11227
    msg = '	image_key 不存在'


class LarkBotIsNotMessageOwnerException(OpenLarkException):
    code = 11234
    msg = 'bot非消息owner'


class LarkBanAtALLException(OpenLarkException):
    code = 11235
    msg = '禁止@所有人'


class LarkUserNotActiveException(OpenLarkException):
    code = 11236
    msg = '用户已离职'


class LarkChatDisbandedException(OpenLarkException):
    code = 11237
    msg = '群聊已解散'


class LarkMessageTooOldException(OpenLarkException):
    code = 11238
    msg = '消息过久，不能撤销'


class LarkNoPermissionToGotException(OpenLarkException):
    code = 11239
    msg = '无权限获取'


class LarkInvalidTenantAccessTokenException(OpenLarkException):
    code = 99991663
    msg = 'tenant access token 无效'


class LarkInvalidAppAccessTokenException(OpenLarkException):
    code = 99991664
    msg = 'app access token 无效'


class LarkInvalidTenantCodeException(OpenLarkException):
    code = 99991665
    msg = 'tenant code 无效'


class LarkInvalidAppTicketException(OpenLarkException):
    code = 99991666
    msg = 'app ticket 无效'


class LarkFrequencyLimitException(OpenLarkException):
    code = 99991400
    msg = '发消息频率超过频控限制，目前每个AppID每个接口50/s、1000/min的限制'


class LarkInternalException(OpenLarkException):
    code = 20000
    msg = '内部异常'


# --------- 审批异常 / 审批错误码

# 40xx 是审批的 v1 接口
class LarkApprovalNotExistException(OpenLarkException):
    code = 4002
    msg = 'approval not exist'


class LarkApprovalSubscriptionExistException(OpenLarkException):
    code = 4007
    msg = 'subscription exist'


# 600xxx 是审批的 v3 接口

class LarkApprovalInvalidRequestParamsException(OpenLarkException):
    code = 60001
    msg = '请求参数错误'


class LarkApprovalApprovalCodeNotFoundException(OpenLarkException):
    code = 60002
    msg = '审批定义 approval_code 找不到'


class LarkApprovalInstanceCodeNotFoundException(OpenLarkException):
    code = 60003
    msg = '审批实例 instance_code 找不到'


class LarkApprovalUserNotFoundException(OpenLarkException):
    code = 60004
    msg = '用户找不到'


class LarkApprovalForbiddenException(OpenLarkException):
    code = 60009
    msg = '权限不足'


class LarkApprovalTaskIDNotFoundException(OpenLarkException):
    code = 60010
    msg = '审批任务 task_id 找不到'


class LarkApprovalDepartmentValidFailedException(OpenLarkException):
    code = 60005
    msg = '部门验证失败'


class LarkApprovalFormValidFailedException(OpenLarkException):
    code = 60006
    msg = '表单验证失败'


class LarkApprovalNeedPayException(OpenLarkException):
    code = 60011
    msg = '该审批为付费审批，免费版用户不能发起这个审批'


class LarkApprovalInstanceCodeConflictException(OpenLarkException):
    code = 60012
    msg = '审批实例 uuid 冲突'


# --------- 审批异常 / 审批错误码


# --------- 云空间

class LarkDriveWrongRequestJsonException(OpenLarkException):
    code = 90201
    msg = '请求体不是一个 json'


class LarkDriveWrongRangeException(OpenLarkException):
    code = 90202
    msg = '请求中 range 格式有误'


class LarkDriveFailException(OpenLarkException):
    code = 90203
    msg = '不是预期内的 fail'


class LarkDriveWrongRequestBodyException(OpenLarkException):
    code = 90204
    msg = '请求体有误'


class LarkDriveInvalidUsersException(OpenLarkException):
    code = 90205
    msg = '非法的 user'


class LarkDriveEmptySheetIDException(OpenLarkException):
    code = 90206
    msg = 'sheet_id 为空'


class LarkDriveEmptySheetTitleException(OpenLarkException):
    code = 90207
    msg = 'sheet 名称为空'


class LarkDriveSameSheetIDOrTitleException(OpenLarkException):
    code = 90208
    msg = '请求中有相同的 sheet_id 或 title'


class LarkDriveExistSheetIDException(OpenLarkException):
    code = 90209
    msg = 'sheet_id 已经存在'


class LarkDriveExistSheetTitleException(OpenLarkException):
    code = 90210
    msg = 'sheet title 已经存在'


class LarkDriveWrongSheetIDException(OpenLarkException):
    code = 90211
    msg = '错误的 sheet_id'


class LarkDriveWrongRowOrColException(OpenLarkException):
    code = 90212
    msg = '非法的行列'


class LarkDrivePermissionFailException(OpenLarkException):
    code = 90213
    msg = '没有文件的权限 forbidden'


class LarkDriveSpreadSheetNotFoundException(OpenLarkException):
    code = 90214
    msg = 'sheet 没有找到'


class LarkDriveSheetIDNotFoundException(OpenLarkException):
    code = 90215
    msg = 'sheet_id 没有找到'


class LarkDriveEmptyValueException(OpenLarkException):
    code = 90216
    msg = '请求中有空值'


class LarkDriveTooManyRequestException(OpenLarkException):
    code = 90217
    msg = '请求太频繁'


class LarkDriveTimeoutException(OpenLarkException):
    code = 96402
    msg = '超时'


class LarkDriveProcessingException(OpenLarkException):
    code = 96403
    msg = '请求正在处理中'


class LarkDriveLoginRequiredException(OpenLarkException):
    code = 91404
    msg = '需要登录'


class LarkDriveFailedException(OpenLarkException):
    code = 90301  # 91201 / 96401
    msg = '失败'


class LarkDriveOutOfLimitException(OpenLarkException):
    code = 91206
    msg = '超过限制'


class LarkDriveDuplicateException(OpenLarkException):
    code = 91207
    msg = '重复记录'


class LarkDriveForbiddenException(OpenLarkException):
    code = 91002  # 90303 / 91204 / 91403
    msg = '没有权限'


class LarkDriveInvalidOperationException(OpenLarkException):
    code = 91003
    msg = '操作异常'


class LarkDriveUserNoSharePermissionException(OpenLarkException):
    code = 91004
    msg = '用户没有共享权限'


class LarkDriveParamErrorException(OpenLarkException):
    code = 90302  # 91001 / 91202 / 91401
    msg = '参数错误'


class LarkDriveMetaDeletedException(OpenLarkException):
    code = 90304  # 91205
    msg = '文件已删除'


class LarkDriveMetaNotExistException(OpenLarkException):
    code = 90305  # 91203 / 91402
    msg = '文件不存在'


class LarkDriveReviewNotPassException(OpenLarkException):
    code = 90306  # 91208
    msg = '评论内容审核不通过'


class LarkDriveInternalErrorException(OpenLarkException):
    code = 90399  # 95299 / 96201 / 96202 / 96001 / 95201 / 95201—95209
    msg = '内部错误'


# --------- 云空间

# --------- 会议室

class LarkMeetingRoomInvalidPageTokenException(OpenLarkException):
    code = 100001
    msg = 'page token 格式非法'


class LarkMeetingRoomInvalidFieldSelectionException(OpenLarkException):
    code = 100002
    msg = 'fields 中存在非法字段名'


class LarkMeetingRoomTimeFormatMustFollowRFC3339StandardException(OpenLarkException):
    code = 100003
    msg = '时间格式未遵循 RFC3339 标准'


class LarkMeetingRoomInvalidBuildingIDException(OpenLarkException):
    code = 100004
    msg = 'building ID 非法'


class LarkMeetingRoomInvalidRoomIDException(OpenLarkException):
    code = 100005
    msg = 'room ID 非法'


class LarkMeetingRoomInternalErrorException(OpenLarkException):
    code = 105001
    msg = '内部错误'


# --------- 会议室

def gen_exception(code, url, msg=''):
    """生成异常

    :type code: int
    :type url: str
    :type msg: str
    :rtype: OpenLarkException
    """
    exceptions = {
        # 自定义
        999901: LarkInvalidArguments,
        999902: LarkInvalidCallback,
        999903: LarkGetAppTicketFail,
        999904: LarkUnknownError,

        # 审批
        4002: LarkApprovalNotExistException,
        4007: LarkApprovalSubscriptionExistException,
        60001: LarkApprovalInvalidRequestParamsException,
        60002: LarkApprovalApprovalCodeNotFoundException,
        60003: LarkApprovalInstanceCodeNotFoundException,
        60004: LarkApprovalUserNotFoundException,
        60009: LarkApprovalForbiddenException,
        60010: LarkApprovalTaskIDNotFoundException,
        60005: LarkApprovalDepartmentValidFailedException,
        60006: LarkApprovalFormValidFailedException,
        60011: LarkApprovalNeedPayException,
        60012: LarkApprovalInstanceCodeConflictException,

        # 数字超级大的异常，
        99991400: LarkFrequencyLimitException,
        99991663: LarkInvalidTenantAccessTokenException,
        99991664: LarkInvalidAppAccessTokenException,
        99991665: LarkInvalidTenantCodeException,
        99991666: LarkInvalidAppTicketException,

        10002: LarkSendMessageFailException,
        10003: LarkRequestParamsInvalidException,
        10004: LarkGetUserInfoFailOrUserIDNotExistException,
        10005: LarkConflictAppIDException,
        10009: LarkGetOpenChatIDFailException,
        10010: LarkForbiddenSendMessageException,
        10012: LarkGetAppAccessTokenFailException,
        10013: LarkGetTenantAccessTokenFailException,
        10014: LarkGetTenantAccessTokenFailException,
        10015: LarkWrongAppSecretException,
        10016: LarkSendAppTicketFailException,
        10019: LarkUnsupportedUrgentTypeException,
        10020: LarkWrongMessageIDException,
        10023: LarkForbiddenUrgentException,
        10029: LarkInvalidOpenChatIDException,
        10030: LarkBotNotInChatException,
        10032: LarkAllOpenIDInvalidException,
        10034: LarkUnsupportedCrossTenantException,
        10037: LarkGetMessageIDFailException,
        11000: LarkGetSSOAccessTokenFailException,
        11001: LarkGetCheckSecurityTokenFailException,
        11100: LarkCheckOpenChatIDFailException,
        11101: LarkOpenIDNotExistException,
        11102: LarkGetOpenIDFailException,
        11103: LarkOpenDepartmentIDNotExistException,
        11104: LarkGetOpenDepartmentIDFailException,
        11105: LarkEmployeeIDNotExistException,
        11106: LarkGetEmployeeIDFailException,
        11200: LarkUpdateChatNameFailException,
        11201: LarkBotNotGroupAdminException,
        11208: LarkBotNotGroupAdminException,
        11202: LarkOnlyChatAdminCanInviteUserException,
        11203: LarkForbiddenBotBatchSendMessageToUserException,
        11204: LarkForbiddenBotBatchSendMessageToDepartmentException,
        11205: LarkAppHasNoBotException,
        11206: LarkUserCannotGrantToChatAdminException,
        11207: LarkAppUnavailableException,
        11209: LarkAppNotExistException,
        11210: LarkAppUsageInfoNotExistException,
        11211: LarkInviteUserToChatInvalidParamsException,
        11212: LarkRemoveUserFromChatInvalidParamsException,
        11213: LarkUpdateChatInvalidParamsException,
        11214: LarkUploadImageInvalidParamsException,
        11215: LarkEmptyChatIDException,
        11216: LarkGetChatIDFailException,
        11217: LarkInviteBotToChatFailException,
        11218: LarkBotInChatFullException,
        11219: LarkUnsupportedChatCrossTenantException,
        11220: LarkForbiddenBotDisbandChatException,
        11221: LarkBotForbiddenToGetImageBelongToThemException,
        11222: LarkOwnerOfBotIsNotInChatException,
        11223: LarkNotOpenApplicationSendMessagePermissionException,
        11224: LarkInvalidMessageIDException,
        11225: LarkAppIsNotVisibleToUserException,
        11226: LarkInvalidAppIDException,
        11227: LarkImageKeyNotExistException,
        11234: LarkBotIsNotMessageOwnerException,
        11235: LarkBanAtALLException,
        11236: LarkUserNotActiveException,
        11237: LarkChatDisbandedException,
        11238: LarkMessageTooOldException,
        11239: LarkNoPermissionToGotException,

        # 云空间
        90201: LarkDriveWrongRequestJsonException,
        90202: LarkDriveWrongRangeException,
        90203: LarkDriveFailException,
        90204: LarkDriveWrongRequestBodyException,
        90205: LarkDriveInvalidUsersException,
        90206: LarkDriveEmptySheetIDException,
        90207: LarkDriveEmptySheetTitleException,
        90208: LarkDriveSameSheetIDOrTitleException,
        90209: LarkDriveExistSheetIDException,
        90210: LarkDriveExistSheetTitleException,
        90211: LarkDriveWrongSheetIDException,
        90212: LarkDriveWrongRowOrColException,
        90213: LarkDrivePermissionFailException,
        90214: LarkDriveSpreadSheetNotFoundException,
        90215: LarkDriveSheetIDNotFoundException,
        90216: LarkDriveEmptyValueException,
        90217: LarkDriveTooManyRequestException,
        96402: LarkDriveTimeoutException,
        96403: LarkDriveProcessingException,
        91404: LarkDriveLoginRequiredException,
        91206: LarkDriveOutOfLimitException,
        91207: LarkDriveDuplicateException,
        91003: LarkDriveInvalidOperationException,
        91004: LarkDriveUserNoSharePermissionException,

        # 会议室
        100001: LarkMeetingRoomInvalidPageTokenException,
        100002: LarkMeetingRoomInvalidFieldSelectionException,
        100003: LarkMeetingRoomTimeFormatMustFollowRFC3339StandardException,
        100004: LarkMeetingRoomInvalidBuildingIDException,
        100005: LarkMeetingRoomInvalidRoomIDException,
    }

    if code in exceptions:
        return exceptions[code](code=code, msg=msg, url=url)
    if 18000 <= code <= 20000:
        return LarkInternalException(code=code, msg=msg, url=url)
    if code in [4002, 60002]:
        return LarkApprovalNotExistException(code=code, msg=msg, url=url)
    if code in [90303, 91002, 91204, 91403]:
        return LarkDriveForbiddenException(code=code, msg=msg, url=url)
    if code in [90301, 91201, 96401]:
        return LarkDriveFailedException(code=code, msg=msg, url=url)
    if code in [90302, 91001, 91202, 91401]:
        return LarkDriveParamErrorException(code=code, msg=msg, url=url)
    if code in [90304, 91205]:
        return LarkDriveMetaDeletedException(code=code, msg=msg, url=url)
    if code in [90305, 91203, 91402]:
        return LarkDriveMetaNotExistException(code=code, msg=msg, url=url)
    if code in [90306, 91208]:
        return LarkDriveReviewNotPassException(code=code, msg=msg, url=url)
    if code in [90399, 95201, 95299, 96201, 96202, 96001] or (code >= 95201 and code <= 95209):
        return LarkDriveInternalErrorException(code=code, msg=msg, url=url)
    return OpenLarkException(code=code, msg=msg, url=url)
