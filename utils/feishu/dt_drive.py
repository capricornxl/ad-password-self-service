# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

from enum import Enum
from typing import Any, List

import attr
from six import string_types

from utils.feishu.dt_help import to_json_decorator
from utils.feishu.exception import LarkInvalidArguments


def join_range(sheet_id, range):
    if not range or not isinstance(range, string_types):
        raise LarkInvalidArguments(msg='empty range')
    for i in [sheet_id, sheet_id + '!']:
        if range.startswith(i):
            range = range[len(i):]

    return sheet_id + '!' + range


# 文档类型，支持："doc", "sheet", "slide", "bitable", "mindnote", "file", "wiki"
class DriveFileType(Enum):
    doc = 'doc'  # doc
    sheet = 'sheet'  # sheet
    bitable = 'bitable'  # bitable
    folder = 'folder'  # folder
    slide = 'slide'
    mindnote = 'mindnote'
    file = 'file'
    wiki = 'wiki'


class DriveDeleteFlag(Enum):
    # 删除标志，0表示正常访问未删除，1表示在回收站，2表示已经彻底删除
    normal = 0
    in_recycle = 1
    complete_deletion = 2


@to_json_decorator
@attr.s
class DriveSheetCellURL(object):
    """有文本的url
    """
    title = attr.ib(type=str, default='')
    url = attr.ib(type=str, default='')

    def as_sheet_dict(self):
        return {'text': self.title, 'link': self.url, 'type': 'url'}


@to_json_decorator
@attr.s
class DriveSheetCellAt(object):
    """@人名

    个人邮箱，只支持同租户@，notify 为是否发送 Lark 消息
    """
    email = attr.ib(type=str, default='')
    notify = attr.ib(type=bool, default=False)

    def as_sheet_dict(self):
        return {'type': 'mention', 'text': self.email, 'notify': self.notify}


@to_json_decorator
@attr.s
class DriveFileToken(object):
    """表示一个文件， token + type
    """
    token = attr.ib(type=str, default='')
    type = attr.ib(type=DriveFileType, default=None)
    name = attr.ib(type=str, default='')


@to_json_decorator
@attr.s
class DriveFolderMeta(object):
    """文件夹元信息
    """
    id = attr.ib(type=str, default='')
    name = attr.ib(type=str, default='', metadata={'json': 'name'})
    token = attr.ib(type=str, default='')
    create_uid = attr.ib(type=str, default='', metadata={'json': 'createUid'})
    edit_uid = attr.ib(type=str, default='', metadata={'json': 'editUid'})
    parent_id = attr.ib(type=str, default='', metadata={'json': 'parentId'})
    own_uid = attr.ib(type=str, default='', metadata={'json': 'ownUid'})


@to_json_decorator
@attr.s
class DriveFileMeta(object):
    """文件元信息
    """
    name = attr.ib(type=str, default='', metadata={'json': 'title'})
    token = attr.ib(type=str, default='', metadata={'json': 'docs_token'})
    type = attr.ib(type=DriveFileType, default=None, metadata={'json': 'docs_type'})
    owner_open_id = attr.ib(type=str, default='', metadata={'json': 'owner_id'})
    create_time = attr.ib(type=int, default=0)
    latest_modify_open_id = attr.ib(type=str, default='', metadata={'json': 'latest_modify_user'})
    latest_modify_time = attr.ib(type=str, default='')


@to_json_decorator
@attr.s
class DriveCreateFile(object):
    """创建的文件对象
    """
    revision = attr.ib(type=int, default=0)
    token = attr.ib(type=str, default='')
    url = attr.ib(type=str, default='')


@to_json_decorator
@attr.s
class DriveDeleteFile(object):
    """删除的文件对象
    """
    id = attr.ib(type=str, default='')
    result = attr.ib(type=bool, default=False)


@to_json_decorator
@attr.s
class DriveCopyFile(object):
    """复制的文件对象
    """
    folder_token = attr.ib(type=str, default='', metadata={'json': 'folderToken'})
    revision = attr.ib(type=int, default=0)
    token = attr.ib(type=str, default='')
    url = attr.ib(type=str, default='')
    type = attr.ib(type=DriveFileType, default=None)


@to_json_decorator
@attr.s
class DriveDocFileMeta(object):
    create_date = attr.ib(type=str, default='')
    create_time = attr.ib(type=int, default=0)
    create_uid = attr.ib(type=str, default='')
    create_user_name = attr.ib(type=str, default='')
    delete_flag = attr.ib(type=DriveDeleteFlag, default=DriveDeleteFlag.normal)
    edit_time = attr.ib(type=int, default=0)
    edit_user_name = attr.ib(type=str, default='')
    is_external = attr.ib(type=bool, default=False)
    is_pined = attr.ib(type=bool, default=False)
    is_stared = attr.ib(type=bool, default=False)
    type = attr.ib(type=DriveFileType, default=None, metadata={'json': 'obj_type'})  # doc
    owner_uid = attr.ib(type=str, default='', metadata={'json': 'owner_id'})  # 这里不是 open_id，接口不标准
    owner_user_name = attr.ib(type=str, default='')
    server_time = attr.ib(type=int, default=0)
    tenant_id = attr.ib(type=str, default='')
    title = attr.ib(type=str, default='')
    url = attr.ib(type=str, default='')


@to_json_decorator
@attr.s
class DriveComment(object):
    """回复的对象
    """
    comment_id = attr.ib(type=str, default='')
    create_timestamp = attr.ib(type=int, default=0)
    reply_id = attr.ib(type=str, default='')
    update_timestamp = attr.ib(type=int, default=0)


@to_json_decorator
@attr.s
class DriveSubSheetMeta(object):
    id = attr.ib(type=str, default='', metadata={'json': 'sheetId'})
    title = attr.ib(type=str, default='')
    index = attr.ib(type=int, default=0)
    row_count = attr.ib(type=int, default=0, metadata={'json': 'rowCount'})
    column_count = attr.ib(type=int, default=0, metadata={'json': 'columnCount'})


@to_json_decorator
@attr.s
class DriveSheetMeta(object):
    title = attr.ib(type=str, default='')
    owner_uid = attr.ib(type=int, default=0, metadata={'json': 'ownerUser'})
    sheet_count = attr.ib(type=int, default=0, metadata={'json': 'sheetCount'})
    token = attr.ib(type=str, default='', metadata={'json': 'spreadsheetToken'})
    sheets = attr.ib(type=List[DriveSubSheetMeta], default=None)  # type: List[DriveSubSheetMeta]


@to_json_decorator
@attr.s
class DriveInsertSheet(object):
    sheet_token = attr.ib(type=str, default='')
    sheet_id = attr.ib(type=str, default='')
    revision = attr.ib(type=int, default=0)
    updated_range = attr.ib(type=str, default='')
    rows = attr.ib(type=int, default=0)
    columns = attr.ib(type=int, default=0)
    cells = attr.ib(type=int, default=0)


class DriveSheetStyleTextDecoration(Enum):
    normal = 0
    underline = 1  # 下划线
    line_through = 2  # 删除线
    underline_and_line_through = 3  # 下划线+删除线


class DriveSheetStyleNumber(Enum):
    normal = ''  # 常规
    plain_text = '@'  # 纯文本
    number = '0'  # 数字：1024
    number_thousandths = '#,##0'  # 数字(千分位)：1,024
    number_thousandths_decimal = '#,##0.00'  # 数字(千分位 小数点)：1024.56
    percent = '0%'  # 百分比：10%
    percent_decimal = '0.00%'  # 百分比(小数点)：10.24%
    scientific_notation = '0.00E+00'  # 科学计数：1.02E+03
    rmb = '¥#,##0'  # 人民币：¥1,024
    rmb_decimal = '¥#,##0.00'  # 人民币(小数点)：¥1,024.56
    usd = '$#,##0'  # 美元：$1,024
    usd_decimal = '$#,##0.00'  # 美元(小数点)：$1,024.56
    date_slash = 'yyyy/MM/dd'  # 日期：2017/08/10
    date_hor = 'yyyy-MM-dd'  # 日期：2017-08-10
    time = 'HH:mm:ss'  # 时间：23:24:25
    datetime = 'yyyy/MM/dd HH:mm:ss'  # 日期时间：2017/08/10 23:24:25


class DriveSheetStyleHorizontalAlign(Enum):
    left = 0  # 左
    center = 1
    right = 2  # 右


class DriveSheetStyleVerticalAlign(Enum):
    up = 0  # 上
    center = 1
    down = 2  # 下


class DriveSheetStyleBorderType(Enum):
    full_border = 'FULL_BORDER'
    outer_border = 'OUTER_BORDER'
    inner_border = 'INNER_BORDER'
    no_border = 'NO_BORDER'
    left_border = 'LEFT_BORDER'
    right_border = 'RIGHT_BORDER'
    top_border = 'TOP_BORDER'
    bottom_border = 'BOTTOM_BORDER'


@to_json_decorator
@attr.s
class DriveSheetStyleFont(object):
    bold = attr.ib(type=bool, default=False)  # 是否粗体
    italic = attr.ib(type=bool, default=False)  # 是否斜体
    font_size = attr.ib(type=str, default=None, metadata={'json': 'fontSize'})  # 10pt/1.5：字号大小为9~36 行距固定为1.5
    clean = attr.ib(type=bool, default=False)  # 清除font格式

    def as_sheet_style(self):
        d = {
            'bold': self.bold,
            'italic': self.italic,
            'clean': self.clean,
        }
        if self.font_size is not None:
            d['fontSize'] = self.font_size
        return d


@to_json_decorator
@attr.s
class DriveSheetStyle(object):
    font = attr.ib(type=DriveSheetStyleFont, default=None)  # 字体
    text_decoration = attr.ib(type=DriveSheetStyleTextDecoration, default=DriveSheetStyleTextDecoration.normal,
                              metadata={'json': 'textDecoration'})  # 文本装饰：0 默认，1 下划线，2 删除线，3 下划线和删除线
    formatter = attr.ib(type=DriveSheetStyleNumber, default=DriveSheetStyleNumber.normal)  # 数字格式
    horizontal_align = attr.ib(type=DriveSheetStyleHorizontalAlign, default=DriveSheetStyleHorizontalAlign.left,
                               metadata={'json': 'hAlign'})  # 水平对齐：0 左对齐，1 中对齐，2 右对齐
    vertical_align = attr.ib(type=DriveSheetStyleVerticalAlign, default=DriveSheetStyleVerticalAlign.up,
                             metadata={'json': 'vAlign'})  # 垂直对齐：0 上对齐，1 中对齐， 2 下对齐
    fore_color = attr.ib(type=str, default='', metadata={'json': 'foreColor'})  # 字体颜色
    back_color = attr.ib(type=str, default='', metadata={'json': 'backColor'})  # 背景颜色
    border_type = attr.ib(type=DriveSheetStyleBorderType, default=None, metadata={'json': 'borderType'})  # 边框颜色
    border_color = attr.ib(type=str, default='', metadata={'json': 'borderColor'})  # 边框颜色
    clean = attr.ib(type=bool, default=False)  # 清除格式

    def as_sheet_style(self):
        d = {
            'textDecoration': self.text_decoration.value,
            'formatter': self.formatter.value,
            'hAlign': self.horizontal_align.value,
            'vAlign': self.vertical_align.value,
            'foreColor': self.fore_color,
            'backColor': self.back_color,
            'borderColor': self.border_color,
            'clean': self.clean,
        }
        if self.border_type is not None:
            d['borderType'] = self.border_type.value
        if self.font is not None:
            d['font'] = self.font.as_sheet_style()
        return d


@to_json_decorator
@attr.s
class BatchSetDriveSheetStyleRequest(object):
    ranges = attr.ib(type=List[str], default=None)  # type: List[str]
    style = attr.ib(type=DriveSheetStyle, default=None)
    raw_style = attr.ib(type=dict, default=None)

    def as_dict(self, sheet_id):
        d = {
            'ranges': [join_range(sheet_id, i) for i in self.ranges],
        }
        if self.raw_style is not None:
            d['style'] = self.raw_style
            return d

        d['style'] = self.style.as_sheet_style()
        return d


@to_json_decorator
@attr.s
class LockDriveSheetRequest(object):
    sheet_id = attr.ib(type=str)
    start_index = attr.ib(type=int)
    end_index = attr.ib(type=int)
    editor_uids = attr.ib(type=List[int], default=None)  # type: List[int]
    is_rows = attr.ib(type=bool, default=True)
    lock_info = attr.ib(type=str, default=None)

    def as_dict(self):
        d = {
            "dimension": {
                "sheetId": self.sheet_id,
                "majorDimension": 'ROWS' if self.is_rows else "COLUMNS",
                "startIndex": self.start_index,
                "endIndex": self.end_index
            },
        }
        if self.editor_uids is not None:
            d['editors'] = self.editor_uids
        if self.lock_info is not None:
            d['lockInfo'] = self.lock_info

        return d


@to_json_decorator
@attr.s
class ReadDriveSheetRequest(object):
    sheet_id = attr.ib(type=str)
    range = attr.ib(type=str)

    def as_str(self):
        return join_range(self.sheet_id, self.range)


class DriveSheetMergeType(Enum):
    all = 'MERGE_ALL'  # 将所选区域直接合并
    rows = 'MERGE_ROWS'  # 将所选区域按行合并
    columns = 'MERGE_COLUMNS'  # 将所选区域按列合并响应


@to_json_decorator
@attr.s
class WriteDriveSheetRequest(object):
    sheet_id = attr.ib(type=str)
    range = attr.ib(type=str)
    values = attr.ib(type=List[List[Any]])  # type: List[List[Any]]

    def as_dict(self):
        return {
            'range': join_range(self.sheet_id, self.range),
            'values': [[i.as_sheet_dict() if hasattr(i, 'as_sheet_dict') else i for i in value]
                       for value in self.values]
        }


class DriveFilePermission(Enum):
    view = 'view'
    edit = 'edit'


@to_json_decorator
@attr.s
class DriveFileUser(object):
    email = attr.ib(type=str, default=None)  # 邮箱
    open_id = attr.ib(type=str, default=None)  # 人的 open_id
    chat_id = attr.ib(type=str, default=None)  # 群聊的 chat_id
    employee_id = attr.ib(type=str, default=None)  # lark_id

    def as_dict(self):
        d = {}
        if self.email is not None:
            d['member_id'] = self.email
            d['member_type'] = 'email'
        elif self.open_id is not None:
            d['member_type'] = 'openid'
            d['member_id'] = self.open_id
        elif self.chat_id is not None:
            d['member_type'] = 'openchat'
            d['member_id'] = self.chat_id
        elif self.employee_id is not None:
            d['member_type'] = 'userid'
            d['member_id'] = self.employee_id
        else:
            raise LarkInvalidArguments(msg='email / open_id / chat_id / uid 必须有一个')

        return d


@to_json_decorator
@attr.s
class DriveFileUserPermission(DriveFileUser):
    permission = attr.ib(type=DriveFilePermission, default=DriveFilePermission.view)

    def as_dict(self):
        d = super(DriveFileUserPermission, self).as_dict()
        d['perm'] = self.permission.value
        return d


def unmarshal_drive_user_permission(members,
                                    email_type='email',
                                    email_key='member_id',
                                    open_id_type='openid',
                                    open_id_key='member_id',
                                    chat_id_type='openchat',
                                    chat_id_key='member_id',
                                    employee_id_type='userid',
                                    employee_id_key='member_id',
                                    is_unmarshal_perm=False):
    d = []
    for i in members:
        member_type = i.get('member_type', '')

        if is_unmarshal_perm:
            v = DriveFileUserPermission(permission=i.get('perm', ''))
        else:
            v = DriveFileUser()

        if member_type == email_type:
            v.email = i.get(email_key) or ''
        elif member_type == open_id_type:
            v.open_id = i.get(open_id_key) or ''
        elif member_type == chat_id_type:
            v.chat_id = i.get(chat_id_key) or ''
        elif member_type == employee_id_type:
            v.employee_id = i.get(employee_id_key) or ''
        d.append(v)
    return d


class DriveFilePublicLinkSharePermission(Enum):
    tenant_readable = 'tenant_readable'  # 组织内获得链接的人可阅读
    tenant_editable = 'tenant_editable'  # 组织内获得链接的人可编辑
    anyone_readable = 'anyone_readable'  # 获得链接的任何人可阅读
    anyone_editable = 'anyone_editable'  # 获得链接的任何人可编辑


@to_json_decorator
@attr.s
class BatchUpdateDriveSheetRequestAdd(object):
    title = attr.ib(type=str)
    index = attr.ib(type=int, default=None)

    def as_dict(self):
        d = {'title': self.title}
        if self.index is not None:
            d['index'] = self.index
        return {
            'addSheet': {
                'properties': d
            }
        }


@to_json_decorator
@attr.s
class BatchUpdateDriveSheetRequestCopy(object):
    sheet_id = attr.ib(type=str)
    dst_title = attr.ib(type=str)

    def as_dict(self):
        return {
            'copySheet': {
                'source': {
                    'sheetId': self.sheet_id
                },
                'destination': {
                    'title': self.dst_title
                }
            }
        }


@to_json_decorator
@attr.s
class BatchUpdateDriveSheetRequestDelete(object):
    sheet_id = attr.ib(type=str)

    def as_dict(self):
        return {
            'deleteSheet': {
                'sheetId': self.sheet_id
            }
        }


@to_json_decorator
@attr.s
class UpdateDriveSheetResponse(object):
    sheet_id = attr.ib(type=str, default=None, metadata={'json': 'sheetId'})
    title = attr.ib(type=str, default=None)
    index = attr.ib(type=int, default=None)
