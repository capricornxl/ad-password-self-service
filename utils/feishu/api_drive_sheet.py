# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

from typing import TYPE_CHECKING, Any, Dict, List

from six.moves.urllib.parse import quote

from utils.feishu.dt_drive import (BatchSetDriveSheetStyleRequest, DriveInsertSheet, DriveSheetMergeType, DriveSheetMeta,
                             DriveSheetStyle, LockDriveSheetRequest, ReadDriveSheetRequest, UpdateDriveSheetResponse,
                             WriteDriveSheetRequest, join_range)
from utils.feishu.dt_help import make_datatype
from utils.feishu.helper import converter_enum

if TYPE_CHECKING:
    from utils.feishu.api import OpenLark

    from utils.feishu.dt_drive import BatchUpdateDriveSheetRequestAdd, BatchUpdateDriveSheetRequestCopy, \
        BatchUpdateDriveSheetRequestDelete


class APIDriveSheetMixin(object):
    def get_drive_sheet_meta(self, user_access_token, sheet_token):
        """获取 sheet 文件的元数据

        :type self: OpenLark
        :param user_access_token: user_access_token
        :type user_access_token: str
        :param sheet_token: 文件的 token 列表
        :type sheet_token: str
        :return: sheet 元信息
        :rtype: DriveSheetMeta

        该接口用于根据 token 获取各类文件的元数据

        https://open.feishu.cn/document/ukTMukTMukTM/uMjN3UjLzYzN14yM2cTN
        """
        url = self._gen_request_url('/open-apis/sheet/v2/spreadsheets/{}/metainfo'.format(sheet_token))
        res = self._get(url, auth_token=user_access_token)
        properties = res['data']['properties']
        for k, v in res['data'].items():
            if k != 'properties':
                properties[k] = v
        return make_datatype(DriveSheetMeta, properties)

    def update_drive_sheet_properties(self, user_access_token, sheet_token, title):
        """更新表格属性

        :type self: OpenLark
        :param user_access_token: user_access_token
        :type user_access_token: str
        :param sheet_token: 文件的 token 列表
        :type sheet_token: str
        :param title: 标题
        :type title: str

        该接口用于根据 sheet_token 更新表格属性，如更新表格标题。

        https://open.feishu.cn/document/ukTMukTMukTM/ucTMzUjL3EzM14yNxMTN
        """
        url = self._gen_request_url('/open-apis/sheet/v2/spreadsheets/{}/properties'.format(sheet_token))
        body = {
            'properties': {
                'title': title,
            }
        }
        self._put(url, body=body, auth_token=user_access_token)

    def batch_update_drive_sheet(self, user_access_token, sheet_token, adds=None, copys=None, deletes=None):
        """操作子表

        :type self: OpenLark
        :param user_access_token: user_access_token
        :type user_access_token: str
        :param sheet_token: 文件的 token 列表
        :type sheet_token: str
        :param adds: 参数
        :type adds: List[BatchUpdateDriveSheetRequestAdd]
        :param copys: 参数
        :type copys: List[BatchUpdateDriveSheetRequestCopy]
        :param deletes: 参数
        :type deletes: List[BatchUpdateDriveSheetRequestDelete]
        :rtype (list[UpdateDriveSheetResponse], list[UpdateDriveSheetResponse], list[UpdateDriveSheetResponse])

        该接口用于根据 sheet_token 操作表格，如增加sheet，复制sheet、删除sheet。

        https://open.feishu.cn/document/ukTMukTMukTM/uYTMzUjL2EzM14iNxMTN
        """
        url = self._gen_request_url('/open-apis/sheet/v2/spreadsheets/{}/sheets_batch_update'.format(sheet_token))
        requests = []
        if adds:
            for i in adds:
                requests.append(i.as_dict())
        if copys:
            for i in copys:
                requests.append(i.as_dict())
        if deletes:
            for i in deletes:
                requests.append(i.as_dict())

        res = self._post(url, body={'requests': requests}, auth_token=user_access_token)
        adds_resp = []  # type: List[UpdateDriveSheetResponse]
        copys_resp = []  # type: List[UpdateDriveSheetResponse]
        deletes_resp = []  # type: List[UpdateDriveSheetResponse]

        for i in res.get('data', {}).get('replies', []):
            if 'addSheet' in i:
                adds_resp.append(make_datatype(UpdateDriveSheetResponse, i['addSheet']['properties']))
            elif 'copySheet' in i:
                copys_resp.append(make_datatype(UpdateDriveSheetResponse, i['copySheet']['properties']))
            elif 'deleteSheet' in i:
                deletes_resp.append(make_datatype(UpdateDriveSheetResponse, i['deleteSheet']))

        return adds_resp, copys_resp, deletes_resp

    def update_drive_sub_sheet_properties(self, user_access_token, sheet_token, sheet_id, title=None, index=None,
                                          hidden=None, is_lock=None, lock_info=None, user_uids=None):
        """操作子表属性

        :type self: OpenLark
        :param user_access_token: user_access_token
        :type user_access_token: str
        :param sheet_token: 文件的 token 列表
        :type sheet_token: str
        :param sheet_id: 作为表格唯一识别参数
        :type sheet_id: str
        :param title: 更改 sheet 标题
        :type title: str
        :param index: 移动 sheet 的位置
        :type index: int
        :param hidden: 隐藏表格，默认 false
        :type hidden: bool
        :param is_lock: 上锁/解锁
        :type is_lock: bool
        :param lock_info: 锁定信息
        :type lock_info: str
        :param user_uids: 除了本人与所有者外，添加其他的可编辑人员
        :type user_uids: list[str]

        该接口用于根据 sheet_token 更新子表属性。

        https://open.feishu.cn/document/ukTMukTMukTM/ugjMzUjL4IzM14COyMTN
        """
        url = self._gen_request_url('/open-apis/sheet/v2/spreadsheets/{}/sheets_batch_update'.format(sheet_token))
        properties = {
            'sheetId': sheet_id,
            'protect': {
                'lock': 'LOCK' if is_lock else 'UNLOCK',
            }
        }
        if title is not None:
            properties['title'] = title
        if index is not None:
            properties['index'] = index
        if hidden is not None:
            properties['hidden'] = hidden
        if lock_info is not None:
            properties['protect']['lockInfo'] = lock_info
        if user_uids is not None:
            properties['protect']['userIds'] = user_uids
        body = {
            'requests': [
                {
                    'updateSheet': {
                        'properties': properties,
                    }
                }
            ]
        }
        self._post(url, body=body, auth_token=user_access_token)

    def prepend_write_drive_sheet_cells(self, user_access_token, sheet_token, sheet_id, range, values):
        """在表前面插入数据

        :type self: OpenLark
        :param user_access_token: user_access_token
        :type user_access_token: str
        :param sheet_token: 文件的 token 列表
        :type sheet_token: str
        :param sheet_id: 作为表格唯一识别参数
        :type sheet_id: str
        :param range: 范围，形如：'A1:D2'
        :type range: str
        :param values: 数据，二位数组，每个子数组就是一行数据
        :type values: list[list[Any]]
        :rtype: DriveInsertSheet

        该接口用于根据 sheet_token 和 range 向范围之前增加相应数据的行和相应的数据，相当于数组的插入操作；

        单次写入不超过5000行，100列，每个格子大小为0.5M。

        https://open.feishu.cn/document/ukTMukTMukTM/uIjMzUjLyIzM14iMyMTN
        """
        url = self._gen_request_url('/open-apis/sheet/v2/spreadsheets/{}/values_prepend'.format(sheet_token))
        body = {
            'valueRange': {
                'range': join_range(sheet_id, range),
                'values': [[i.as_sheet_dict() if hasattr(i, 'as_sheet_dict') else i for i in value] for value in values]
            }
        }
        res = self._post(url, body=body, auth_token=user_access_token)

        return _pack_insert_sheet(sheet_token, sheet_id, res)

    def append_write_drive_sheet_cells(self, user_access_token, sheet_token, sheet_id, range, values,
                                       overwrite_empty_line=False):
        """在表后面插入数据

        :type self: OpenLark
        :param user_access_token: user_access_token
        :type user_access_token: str
        :param sheet_token: 文件的 token 列表
        :type sheet_token: str
        :param sheet_id: 作为表格唯一识别参数
        :type sheet_id: str
        :param range: 范围，形如：'A1:D2'
        :type range: str
        :param values: 数据，二位数组，每个子数组就是一行数据
        :type values: list[list[Any]]
        :param overwrite_empty_line: 是否覆盖空行（第一个格子是空，就是空行）。
                                     如果：覆盖 && range 的左上角第一个格子为空，则：从这个格子开始，数据被覆盖
                                     如果：不覆盖 && range 的左上角第一个格子为空 && 其他数据不为空，则将将这些数据下移 N 格
                                     再插入数据
        :type overwrite_empty_line: bool
        :rtype: DriveInsertSheet

        该接口用于根据 sheet_token 和 range 遇到空行则进行覆盖追加或新增行追加数据。

        空行：默认该行第一个格子是空，则认为是空行；单次写入不超过5000行，100列，每个格子大小为0.5M。

        https://open.feishu.cn/document/ukTMukTMukTM/uMjMzUjLzIzM14yMyMTN
        """

        url = self._gen_request_url('/open-apis/sheet/v2/spreadsheets/{}/values_append'.format(sheet_token))
        if not overwrite_empty_line:
            url = url + '?insertDataOption=INSERT_ROWS'
        body = {
            'valueRange': {
                'range': join_range(sheet_id, range),
                'values': values
            }
        }
        res = self._post(url, body=body, auth_token=user_access_token)

        return _pack_insert_sheet(sheet_token, sheet_id, res)

    def insert_drive_sheet_rows_columns(self, user_access_token, sheet_token, sheet_id, start_index, end_index,
                                        is_rows=True, inherit_style=None):
        """插入行列


        :type self: OpenLark
        :param user_access_token: user_access_token
        :type user_access_token: str
        :param sheet_token: 文件的 token 列表
        :type sheet_token: str
        :param sheet_id: 作为表格唯一识别参数
        :type sheet_id: str
        :param start_index: 从这一行的下一行开始插入（或下一列）
        :type start_index: int
        :param end_index: 截止到这一行（列）
        :type end_index: int
        :param is_rows: 为 True 插入行，为 False 插入列
        :type is_rows: bool
        :param inherit_style: BEFORE 或 AFTER，不填为不继承 style
        :type inherit_style: str

        该接口用于根据 sheet_token 和维度信息 插入空行/列

        如 startIndex=3， endIndex=7，则从第 4 行开始开始插入行列，一直到第 7 行，共插入 4 行；单次操作不超过5000行或列。

        https://open.feishu.cn/document/ukTMukTMukTM/uQjMzUjL0IzM14CNyMTN
        """

        url = self._gen_request_url('/open-apis/sheet/v2/spreadsheets/{}/insert_dimension_range'.format(sheet_token))
        body = {
            'dimension': {
                'sheetId': sheet_id,
                'majorDimension': 'ROWS' if is_rows else 'COLUMNS',
                'startIndex': start_index,
                'endIndex': end_index,
            },
        }
        if inherit_style:
            body['inheritStyle'] = inherit_style

        self._post(url, body=body, auth_token=user_access_token)

    def add_drive_sheet_rows_columns(self, user_access_token, sheet_token, sheet_id, length, is_rows=True):
        """添加行列

        :type self: OpenLark
        :param user_access_token: user_access_token
        :type user_access_token: str
        :param sheet_token: 文件的 token 列表
        :type sheet_token: str
        :param sheet_id: 作为表格唯一识别参数
        :type sheet_id: str
        :param length: 需要添加的行数（列数）
        :type length: int
        :param is_rows: 为 True 插入行，为 False 插入列
        :type is_rows: bool

        该接口用于根据 sheet_token 和长度，在末尾增加空行/列；单次操作不超过5000行或列。

        https://open.feishu.cn/document/ukTMukTMukTM/uUjMzUjL1IzM14SNyMTN
        """

        url = self._gen_request_url('/open-apis/sheet/v2/spreadsheets/{}/dimension_range'.format(sheet_token))
        body = {
            'dimension': {
                'sheetId': sheet_id,
                'majorDimension': 'ROWS' if is_rows else 'COLUMNS',
                'length': length
            }
        }

        self._post(url, body=body, auth_token=user_access_token)

    def update_drive_sheet_rows_columns(self, user_access_token, sheet_token, sheet_id, start_index, end_index,
                                        visible=None, fixed_size=None, is_rows=True):
        """更新行列

        :type self: OpenLark
        :param user_access_token: user_access_token
        :type user_access_token: str
        :param sheet_token: 文件的 token 列表
        :type sheet_token: str
        :param sheet_id: 作为表格唯一识别参数
        :type sheet_id: str
        :param start_index: 从这一行的下一行开始插入（或下一列）
        :type start_index: int
        :param end_index: 截止到这一行（列）
        :type end_index: int
        :param visible: true 为显示，false 为隐藏行列
        :type visible: bool
        :param fixed_size: 行/列的大小
        :type fixed_size: int
        :param is_rows: 为 True 插入行，为 False 插入列
        :type is_rows: bool

        该接口用于根据 sheet_token 和维度信息更新隐藏行列、单元格大小；单次操作不超过5000行或列。

        https://open.feishu.cn/document/ukTMukTMukTM/uYjMzUjL2IzM14iNyMTN
        """

        url = self._gen_request_url('/open-apis/sheet/v2/spreadsheets/{}/dimension_range'.format(sheet_token))
        body = {
            'dimension': {
                'sheetId': sheet_id,
                'majorDimension': 'ROWS' if is_rows else 'COLUMNS',
                'startIndex': start_index,
                'endIndex': end_index
            },
            'dimensionProperties': {
            }
        }
        if visible is not None:
            body['dimensionProperties']['visible'] = visible
        if fixed_size is not None:
            body['dimensionProperties']['fixedSize'] = fixed_size

        self._put(url, body=body, auth_token=user_access_token)

    def delete_drive_sheet_rows_columns(self, user_access_token, sheet_token, sheet_id, start_index, end_index,
                                        is_rows=True):
        """删除行列

        :type self: OpenLark
        :param user_access_token: user_access_token
        :type user_access_token: str
        :param sheet_token: 文件的 token 列表
        :type sheet_token: str
        :param sheet_id: 作为表格唯一识别参数
        :type sheet_id: str
        :param start_index: 从这一行的下一行开始插入（或下一列）
        :type start_index: int
        :param end_index: 截止到这一行（列）
        :type end_index: int
        :param is_rows: 为 True 插入行，为 False 插入列
        :type is_rows: bool

        该接口用于根据 sheet_token 和维度信息删除行/列 ；单次操作不超过5000行或列。

        https://open.feishu.cn/document/ukTMukTMukTM/ucjMzUjL3IzM14yNyMTN
        """

        url = self._gen_request_url('/open-apis/sheet/v2/spreadsheets/{}/dimension_range'.format(sheet_token))
        body = {
            'dimension': {
                'sheetId': sheet_id,
                'majorDimension': 'ROWS' if is_rows else 'COLUMNS',
                'startIndex': start_index,
                'endIndex': end_index
            }
        }

        self._delete(url, body=body, auth_token=user_access_token)

    def set_drive_sheet_style(self, user_access_token, sheet_token, sheet_id, range, style=None, raw_style=None):
        """设置单元格样式

        :type self: OpenLark
        :param user_access_token: user_access_token
        :type user_access_token: str
        :param sheet_token: 文件的 token 列表
        :type sheet_token: str
        :param sheet_id: 作为表格唯一识别参数
        :type sheet_id: str
        :type sheet_id: str
        :param range: 范围，形如：'A1:D2'
        :type range: str
        :param style: 单元格样式，具体请参考文档：https://open.feishu.cn/document/ukTMukTMukTM/ukjMzUjL5IzM14SOyMTN
        :type style: DriveSheetStyle
        :param raw_style: 单元格样式 的 原始样式
        :type raw_style: Any

        该接口用于根据 sheet_token 、range 和样式信息更新单元格样式；单次写入不超过5000行，100列。

        https://open.feishu.cn/document/ukTMukTMukTM/ukjMzUjL5IzM14SOyMTN
        """

        if not raw_style and style:
            raw_style = style.as_sheet_style()

        url = self._gen_request_url('/open-apis/sheet/v2/spreadsheets/{}/style'.format(sheet_token))
        body = {
            'appendStyle': {
                'range': join_range(sheet_id, range),
                'style': raw_style
            }
        }

        self._put(url, body=body, auth_token=user_access_token)

    def batch_set_drive_sheet_style(self, user_access_token, sheet_token, sheet_id, styles):
        """批量设置单元格样式

        :type self: OpenLark
        :param user_access_token: user_access_token
        :type user_access_token: str
        :param sheet_token: 文件的 token 列表
        :type sheet_token: str
        :param sheet_id: 作为表格唯一识别参数
        :type sheet_id: str
        :type sheet_id: str
        :param styles: BatchSetDriveSheetStyleRequest 的数组
        :type styles: list[BatchSetDriveSheetStyleRequest]

        该接口用于根据 sheet_token 、range和样式信息 批量更新单元格样式；单次写入不超过5000行，100列。

        https://open.feishu.cn/document/ukTMukTMukTM/uAzMzUjLwMzM14CMzMTN
        """

        d = []
        for i in styles:
            d.append(i.as_dict(sheet_id))

        url = self._gen_request_url('/open-apis/sheet/v2/spreadsheets/{}/styles_batch_update'.format(sheet_token))
        body = {
            'data': d
        }

        self._put(url, body=body, auth_token=user_access_token)

    def batch_lock_drive_sheet_rows_columns(self, user_access_token, sheet_token, requests):
        """批量增加锁定单元格

        :type self: OpenLark
        :param user_access_token: user_access_token
        :type user_access_token: str
        :param sheet_token: 文件的 token 列表
        :type sheet_token: str
        :param requests: 参数
        :type requests: list[LockDriveSheetRequest]
        :rtype: dict[str, str]

        该接口用于根据 sheet_token 和维度信息增加多个范围的锁定单元格；单次操作不超过5000行或列。

        https://open.feishu.cn/document/ukTMukTMukTM/ugDNzUjL4QzM14CO0MTN
        """

        url = self._gen_request_url('/open-apis/sheet/v2/spreadsheets/{}/protected_dimension'.format(sheet_token))
        body = {
            'addProtectedDimension': [i.as_dict() for i in requests]
        }

        res = self._post(url, body=body, auth_token=user_access_token)
        return {i['dimension']['sheetId']: i['protectId'] for i in res['data']['addProtectedDimension']}

    def lock_drive_sheet_rows_columns(self, user_access_token, sheet_token, sheet_id, start_index, end_index,
                                      is_rows=True, editor_uids=None, lock_info=None):
        """增加锁定单元格

        :type self: OpenLark
        :param user_access_token: user_access_token
        :type user_access_token: str
        :param sheet_token: 文件的 token 列表
        :type sheet_token: str
        :param sheet_id: 作为表格唯一识别参数
        :type sheet_id: str
        :param start_index: 从这一行的下一行开始插入（或下一列）
        :type start_index: int
        :param end_index: 截止到这一行（列）
        :type end_index: int
        :param is_rows: 为 True 插入行，为 False 插入列
        :type is_rows: bool
        :param editor_uids: 可以编辑者
        :type editor_uids: list[int]
        :param lock_info: lock 信息
        :type lock_info: str
        :rtype: str

        该接口用于根据 sheet_token 和维度信息增加多个范围的锁定单元格；单次操作不超过5000行或列。

        https://open.feishu.cn/document/ukTMukTMukTM/ugDNzUjL4QzM14CO0MTN
        """
        res = self.batch_lock_drive_sheet_rows_columns(user_access_token=user_access_token,
                                                       sheet_token=sheet_token,
                                                       requests=[LockDriveSheetRequest(
                                                           sheet_id=sheet_id,
                                                           start_index=start_index,
                                                           end_index=end_index,
                                                           editor_uids=editor_uids,
                                                           is_rows=is_rows,
                                                           lock_info=lock_info,
                                                       )])
        return res.get(sheet_id, '')

    def merge_drive_sheet_cells(self, user_access_token, sheet_token, sheet_id, range, merge_type):
        """合并单元格

        :type self: OpenLark
        :param user_access_token: user_access_token
        :type user_access_token: str
        :param sheet_token: 文件的 token 列表
        :type sheet_token: str
        :param sheet_id: 作为表格唯一识别参数
        :type sheet_id: str
        :param range: 范围，形如：'A1:D2'
        :type range: str
        :param merge_type: lock 信息
        :type merge_type: DriveSheetMergeType
        :rtype: str

        该接口用于根据 sheet_token 和维度信息合并单元格；单次操作不超过5000行，100列。

        https://open.feishu.cn/document/ukTMukTMukTM/ukDNzUjL5QzM14SO0MTN
        """
        url = self._gen_request_url('/open-apis/sheet/v2/spreadsheets/{}/merge_cells'.format(sheet_token))
        body = {
            'range': join_range(sheet_id, range),
            'mergeType': converter_enum(merge_type),
        }

        self._post(url, body=body, auth_token=user_access_token)

    def unmerge_drive_sheet_cells(self, user_access_token, sheet_token, sheet_id, range):
        """拆分单元格

        :type self: OpenLark
        :param user_access_token: user_access_token
        :type user_access_token: str
        :param sheet_token: 文件的 token 列表
        :type sheet_token: str
        :param sheet_id: 作为表格唯一识别参数
        :type sheet_id: str
        :param range: 范围，形如：'A1:D2'
        :type range: str
        :rtype: str

        该接口用于根据 sheet_token 和维度信息合并单元格；单次操作不超过5000行，100列。

        https://open.feishu.cn/document/ukTMukTMukTM/ukDNzUjL5QzM14SO0MTN
        """
        url = self._gen_request_url('/open-apis/sheet/v2/spreadsheets/{}/unmerge_cells'.format(sheet_token))
        body = {
            'range': join_range(sheet_id, range),
        }

        self._post(url, body=body, auth_token=user_access_token)

    def read_drive_sheet_cells(self, user_access_token, sheet_token, sheet_id, range, to_str=False):
        """读取单元格

        :type self: OpenLark
        :param user_access_token: user_access_token
        :type user_access_token: str
        :param sheet_token: 文件的 token 列表
        :type sheet_token: str
        :param sheet_id: 作为表格唯一识别参数
        :type sheet_id: str
        :param range: 范围，形如：'A1:D2'
        :type range: str
        :param to_str: 是否返回 to_str 后的值
        :type to_str: bool
        :rtype: (int, list[list[Any]])
        :return: 版本，值的二维数组

        该接口用于根据 sheet_token 和 range 读取表格单个范围的值，返回数据限制为10M。

        https://open.feishu.cn/document/ukTMukTMukTM/ugTMzUjL4EzM14COxMTN
        """
        url = self._gen_request_url(
            '/open-apis/sheet/v2/spreadsheets/{}/values/{}'.format(sheet_token, join_range(sheet_id, range)))
        if to_str:
            url = url + '?valueRenderOption=ToString'
        res = self._get(url, auth_token=user_access_token)
        revision = res['data']['revision']  # type: int
        values = res['data']['valueRange'].get('values', [])  # type: List[List[Any]]
        return revision, values

    def batch_read_drive_sheet_cells(self, user_access_token, sheet_token, requests, to_str=False):
        """批量读取单元格

        :type self: OpenLark
        :param user_access_token: user_access_token
        :type user_access_token: str
        :param sheet_token: 文件的 token 列表
        :type sheet_token: str
        :param requests: 参数
        :type requests: list[ReadDriveSheetRequest]
        :param to_str: 是否返回 to_str 后的值
        :type to_str: bool
        :rtype: (int, dict[str, list[list[Any]]])
        :return: 版本，值的二维数组

        该接口用于根据 sheet_token 和 range 读取表格单个范围的值，返回数据限制为10M。

        https://open.feishu.cn/document/ukTMukTMukTM/ugTMzUjL4EzM14COxMTN
        """

        ranges = ','.join([i.as_str() for i in requests])
        url = self._gen_request_url(
            '/open-apis/sheet/v2/spreadsheets/{}/values_batch_get?ranges={}'.format(sheet_token, quote(ranges)))
        if to_str:
            url = url + '&valueRenderOption=ToString'
        res = self._get(url, auth_token=user_access_token)
        revision = res['data']['revision']  # type: int
        values = {i.get('range', ''): i.get('values', []) for i in
                  res['data']['valueRanges']}  # type: Dict[str, List[List[Any]]]
        return revision, values

    def write_drive_sheet_cells(self, user_access_token, sheet_token, sheet_id, range, values):
        """写入单元格

        :type self: OpenLark
        :param user_access_token: user_access_token
        :type user_access_token: str
        :param sheet_token: 文件的 token 列表
        :type sheet_token: str
        :param sheet_id: 作为表格唯一识别参数
        :type sheet_id: str
        :param range: 范围，形如：'A1:D2'
        :type range: str
        :param values: 数据，二位数组，每个子数组就是一行数据
        :type values: list[list[Any]]
        :rtype: (int, list[list[Any]])
        :return: 版本，值的二维数组

        该接口用于根据 sheet_token 和 range 向单个范围写入数据，若范围内有数据，将被更新覆盖；

        单次写入不超过5000行，100列，每个格子大小为0.5M。

        https://open.feishu.cn/document/ukTMukTMukTM/uAjMzUjLwIzM14CMyMTN
        """
        url = self._gen_request_url(
            '/open-apis/sheet/v2/spreadsheets/{}/values'.format(sheet_token))
        body = {
            'valueRange': {
                'range': join_range(sheet_id, range),
                'values': [[i.as_sheet_dict() if hasattr(i, 'as_sheet_dict') else i for i in value] for value in values]
            }
        }
        self._put(url, body=body, auth_token=user_access_token)

    def batch_write_drive_sheet_cells(self, user_access_token, sheet_token, requests):
        """批量写入单元格

        :type self: OpenLark
        :param user_access_token: user_access_token
        :type user_access_token: str
        :param sheet_token: 文件的 token 列表
        :type sheet_token: str
        :param requests: 参数
        :type requests: list[WriteDriveSheetRequest]
        :rtype: (int, list[list[Any]])
        :return: 版本，值的二维数组

        该接口用于根据 sheet_token 和 range 向多个范围写入数据，若范围内有数据，将被更新覆盖；

        单次写入不超过5000行，100列，每个格子大小为0.5M。

        https://open.feishu.cn/document/ukTMukTMukTM/uEjMzUjLxIzM14SMyMTN
        """
        url = self._gen_request_url('/open-apis/sheet/v2/spreadsheets/{}/values_batch_update'.format(sheet_token))

        body = {
            'valueRanges': [i.as_dict() for i in requests]
        }
        self._post(url, body=body, auth_token=user_access_token)


def _pack_insert_sheet(sheet_token, sheet_id, res):
    """
    :rtype: DriveInsertSheet
    """
    data = res['data']
    revision = data.get('revision', 0)
    updates = data.get('updates', {})
    updated_range = updates.get('updatedRange', '')
    rows = updates.get('updatedRows', 0)
    columns = updates.get('updatedColumns', 0)
    cells = updates.get('updatedCells', 0)

    return make_datatype(DriveInsertSheet, dict(sheet_token=sheet_token,
                                                sheet_id=sheet_id,
                                                revision=revision,
                                                updated_range=updated_range,
                                                rows=rows,
                                                columns=columns,
                                                cells=cells))
