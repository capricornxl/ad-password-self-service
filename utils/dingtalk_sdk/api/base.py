# -*- coding: utf-8 -*-
"""
Created on 2018-9-17

@author: xiaoxuan.lp
"""

try:
    import http.client
except ImportError:
    import http.client as httplib
import base64
import hashlib
import hmac
import itertools
import json
import mimetypes
import time
import urllib.error
import urllib.parse
import urllib.request

'''
定义一些系统变量
'''

SYSTEM_GENERATE_VERSION = "taobao-sdk-python-dynamicVersionNo"

P_APPKEY = "app_key"
P_API = "method"
P_ACCESS_TOKEN = "access_token"
P_VERSION = "v"
P_FORMAT = "format"
P_TIMESTAMP = "timestamp"
P_SIGN = "sign"
P_SIGN_METHOD = "sign_method"
P_PARTNER_ID = "partner_id"

P_CODE = 'errcode'
P_MSG = 'errmsg'


def sign(secret, parameters):
    # ===========================================================================
    # '''签名方法
    # @param secret: 签名需要的密钥
    # @param parameters: 支持字典和string两种
    # '''
    # ===========================================================================
    # 如果parameters 是字典类的话
    if hasattr(parameters, "items"):
        keys = list(parameters.keys())
        keys.sort()

        parameters = "%s%s%s" % (secret,
                                 str().join('%s%s' % (key, parameters[key]) for key in keys),
                                 secret)
    sign = hashlib.md5(parameters.encode("utf-8")).hexdigest().upper()
    return sign


def mixStr(pstr):
    if isinstance(pstr, str):
        return pstr
    elif isinstance(pstr, str):
        return pstr.encode('utf-8')
    else:
        return str(pstr)


class FileItem(object):
    def __init__(self, filename=None, content=None):
        self.filename = filename
        self.content = content


class MultiPartForm(object):
    """Accumulate the data to be used when posting a form."""

    def __init__(self):
        self.form_fields = []
        self.files = []
        self.boundary = "PYTHON_SDK_BOUNDARY"
        return

    def get_content_type(self):
        return 'multipart/form-data;charset=UTF-8; boundary=%s' % self.boundary

    def add_field(self, name, value):
        """Add a simple field to the form data."""
        self.form_fields.append((name, str(value)))
        return

    def add_file(self, fieldname, filename, fileHandle, mimetype=None):
        """Add a file to be uploaded."""
        body = fileHandle.read()
        if mimetype is None:
            mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        self.files.append((mixStr(fieldname), mixStr(filename), mixStr(mimetype), mixStr(body)))
        return

    def __str__(self):
        """Return a string representing the form data, including attached files."""
        # Build a list of lists, each containing "lines" of the
        # request.  Each part is separated by a boundary string.
        # Once the list is built, return a string where each
        # line is separated by '\r\n'.  
        parts = []
        part_boundary = '--' + self.boundary

        # Add the form fields
        parts.extend(
            [part_boundary,
             'Content-Disposition: form-data; name="%s"' % name,
             'Content-Type: text/plain; charset=UTF-8',
             '',
             value,
             ]
            for name, value in self.form_fields
        )

        # Add the files to upload
        parts.extend(
            [part_boundary,
             'Content-Disposition: form-data; name="%s"; filename="%s"' % (field_name, filename),
             'Content-Type: %s' % content_type,
             'Content-Transfer-Encoding: binary',
             '',
             body,
             ]
            for field_name, filename, content_type, body in self.files
        )

        # Flatten the list and add closing boundary marker,
        # then return CR+LF separated data
        flattened = list(itertools.chain(*parts))
        flattened.append('--' + self.boundary + '--')
        flattened.append('')
        return '\r\n'.join(flattened)


class TopException(Exception):
    # ===========================================================================
    # 业务异常类
    # ===========================================================================
    def __init__(self):
        self.errcode = None
        self.errmsg = None
        self.application_host = None
        self.service_host = None

    def __str__(self, *args, **kwargs):
        sb = "errcode=" + mixStr(self.errcode) + \
             " errmsg=" + mixStr(self.errmsg) + \
             " application_host=" + mixStr(self.application_host) + \
             " service_host=" + mixStr(self.service_host)
        return sb


class RequestException(Exception):
    # ===========================================================================
    # 请求连接异常类
    # ===========================================================================
    pass


class RestApi(object):
    # ===========================================================================
    # Rest api的基类
    # ===========================================================================

    def __init__(self, url=None):
        # =======================================================================
        # 初始化基类
        # Args @param domain: 请求的域名或者ip
        #      @param port: 请求的端口
        # =======================================================================
        if url is None:
            raise RequestException("domain must not be empty.")
        if url.find('http://') >= 0:
            self.__port = 80
            pathUrl = url.replace('http://', '')
        elif url.find('https://') >= 0:
            self.__port = 443
            pathUrl = url.replace('https://', '')
        else:
            raise RequestException("http protocol is not validate.")

        index = pathUrl.find('/')
        if index > 0:
            self.__domain = pathUrl[0:index]
            self.__path = pathUrl[index:]
        else:
            self.__domain = pathUrl
            self.__path = ''

        # print("domain:" + self.__domain + ",path:" + self.__path + ",port:" + str(self.__port))

    def get_request_header(self):
        return {
            'Content-type': 'application/json;charset=UTF-8',
            "Cache-Control": "no-cache",
            "Connection": "Keep-Alive",
        }

    def getHttpMethod(self):
        return "GET"

    def getapiname(self):
        return ""

    def getMultipartParas(self):
        return []

    def getTranslateParas(self):
        return {}

    def _check_requst(self):
        pass

    def getResponse(self, authrize='', accessKey='', accessSecret='', suiteTicket='', corpId='', timeout=30):
        # =======================================================================
        # 获取response结果
        # =======================================================================
        if self.__port == 443:
            connection = http.client.HTTPSConnection(self.__domain, self.__port, None, None, timeout)
        else:
            connection = http.client.HTTPConnection(self.__domain, self.__port, timeout)
        sys_parameters = {
            P_PARTNER_ID: SYSTEM_GENERATE_VERSION,
        }
        if authrize is not None:
            sys_parameters[P_ACCESS_TOKEN] = authrize
        application_parameter = self.getApplicationParameters()
        sign_parameter = sys_parameters.copy()
        sign_parameter.update(application_parameter)

        header = self.get_request_header()
        if self.getMultipartParas():
            form = MultiPartForm()
            for key, value in list(application_parameter.items()):
                form.add_field(key, value)
            for key in self.getMultipartParas():
                fileitem = getattr(self, key)
                if fileitem and isinstance(fileitem, FileItem):
                    form.add_file(key, fileitem.filename, fileitem.content)
            body = str(form)
            header['Content-type'] = form.get_content_type()
        else:
            body = urllib.parse.urlencode(application_parameter)

        if accessKey != '':
            timestamp = str(int(round(time.time()))) + '000'
            print(("timestamp:" + timestamp))
            canonicalString = self.getCanonicalStringForIsv(timestamp, suiteTicket)
            print(("canonicalString:" + canonicalString))
            print(("accessSecret:" + accessSecret))
            signature = self.computeSignature(accessSecret, canonicalString)
            print(("signature:" + signature))
            ps = {}
            ps["accessKey"] = accessKey
            ps["signature"] = signature
            ps["timestamp"] = timestamp
            if suiteTicket != '':
                ps["suiteTicket"] = suiteTicket
            if corpId != '':
                ps["corpId"] = corpId
            queryStr = urllib.parse.urlencode(ps)
            if self.__path.find("?") > 0:
                fullPath = self.__path + "&" + queryStr
            else:
                fullPath = self.__path + "?" + queryStr
            print(("fullPath:" + fullPath))
        else:
            if self.__path.find("?") > 0:
                fullPath = (self.__path + "&access_token=" + str(authrize)) if len(str(authrize)) > 0 else self.__path
            else:
                fullPath = (self.__path + "?access_token=" + str(authrize)) if len(str(authrize)) > 0 else self.__path

        if self.getHttpMethod() == "GET":
            if fullPath.find("?") > 0:
                fullPath = fullPath + "&" + body
            else:
                fullPath = fullPath + "?" + body
            connection.request(self.getHttpMethod(), fullPath, headers=header)
        else:
            if self.getMultipartParas():
                body = body
            else:
                body = json.dumps(application_parameter)
            connection.request(self.getHttpMethod(), fullPath, body=body, headers=header)
        response = connection.getresponse()
        if response.status != 200:
            raise RequestException('invalid http status ' + str(response.status) + ',detail body:' + str(response.read()))
        result = response.read()
        # print("result:" + result)
        jsonobj = json.loads(result)
        if P_CODE in jsonobj and jsonobj[P_CODE] != 0:
            error = TopException()
            error.errcode = jsonobj[P_CODE]
            error.errmsg = jsonobj[P_MSG]
            error.application_host = response.getheader("Application-Host", "")
            error.service_host = response.getheader("Location-Host", "")
            raise error
        return jsonobj

    def getCanonicalStringForIsv(self, timestamp, suiteTicket):
        if suiteTicket != '':
            return timestamp + '\n' + suiteTicket
        else:
            return timestamp

    def computeSignature(self, secret, canonicalString):
        message = canonicalString.encode(encoding="utf-8")
        sec = secret.encode(encoding="utf-8")
        return str(base64.b64encode(hmac.new(sec, message, digestmod=hashlib.sha256).digest()))

    def getApplicationParameters(self):
        application_parameter = {}
        for key, value in self.__dict__.items():
            if not key.startswith("__") and not key in self.getMultipartParas() and not key.startswith("_RestApi__") and value is not None:
                if key.startswith("_"):
                    application_parameter[key[1:]] = value
                else:
                    application_parameter[key] = value
        # 查询翻译字典来规避一些关键字属性
        translate_parameter = self.getTranslateParas()
        for key, value in application_parameter.items():
            if key in translate_parameter:
                application_parameter[translate_parameter[key]] = application_parameter[key]
                del application_parameter[key]
        return application_parameter
