from django.forms import fields as c_fields
from django import forms as c_forms


class CheckForm(c_forms.Form):
    new_password = c_fields.RegexField(
        '(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[^a-zA-Z0-9]).{8,30}',
        # 密码必须同时包含大写、小写、数字和特殊字符其中三项且至少8位
        strip=True,
        min_length=8,
        max_length=30,
        error_messages={'required': '新密码不能为空.',
                        'invalid': '密码必须包含数字，字母、特殊字符',
                        'min_length': "密码长度不能小于8个字符",
                        'max_length': "密码长度不能大于30个字符"}
    )
    old_password = c_fields.CharField(error_messages={'required': '确认密码不能为空'})
    ensure_password = c_fields.CharField(error_messages={'required': '确认密码不能为空'})
    username = c_fields.CharField(error_messages={'required': '账号不能为空', 'invalid': '账号格式错误'})

    def clean(self):
        pwd0 = self.cleaned_data.get('old_password')
        pwd1 = self.cleaned_data.get('new_password')
        pwd2 = self.cleaned_data.get('ensure_password')
        if pwd1 == pwd2:
            pass
        elif pwd0 == pwd1:
            # 这里异常模块导入要放在函数里面，放到文件开头有时会报错，找不到
            from django.core.exceptions import ValidationError
            raise ValidationError('新旧密码不能一样')
        else:
            from django.core.exceptions import ValidationError
            raise ValidationError('新密码和确认密码输入不一致')
