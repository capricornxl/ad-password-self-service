# -*- coding: utf-8 -*-
"""
密码管理表单验证 - 使用新的PasswordValidator
"""
from django import forms
from django.core.exceptions import ValidationError
from utils.password_validator import get_password_validator

password_validator = get_password_validator()


class CheckForm(forms.Form):
    """
    检查表单 - 密码变更/解锁验证
    
    使用集中管理的PasswordValidator进行密码策略验证
    """
    username = forms.CharField(
        label='用户名',
        min_length=1,
        max_length=100,
        required=True,
        error_messages={
            'required': '用户名不能为空',
            'max_length': '用户名长度不能超过100字符'
        }
    )
    
    old_password = forms.CharField(
        label='旧密码',
        widget=forms.PasswordInput(),
        required=True,
        error_messages={
            'required': '旧密码不能为空'
        }
    )
    
    new_password = forms.CharField(
        label='新密码',
        widget=forms.PasswordInput(),
        required=True,
        error_messages={
            'required': '新密码不能为空'
        }
    )
    
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(),
        required=True,
        error_messages={
            'required': '确认密码不能为空'
        }
    )
    
    def clean(self):
        """
        表单级别验证
        """
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password', '')
        confirm_password = cleaned_data.get('confirm_password', '')
        
        # 验证密码确认
        if new_password and confirm_password:
            if new_password != confirm_password:
                raise ValidationError('两次输入的密码不一致')
        
        return cleaned_data
    
    def clean_username(self):
        """验证用户名格式"""
        username = self.cleaned_data.get('username', '').strip()
        
        if not username:
            raise ValidationError('用户名不能为空')
        
        # 基本格式检查
        if len(username) > 100:
            raise ValidationError('用户名长度不能超过100字符')
        
        return username
    
    def clean_new_password(self):
        """
        验证新密码符合策略
        
        使用集中管理的PasswordValidator进行验证
        """
        new_password = self.cleaned_data.get('new_password', '')
        
        if not new_password:
            raise ValidationError('新密码不能为空')
        
        # 使用PasswordValidator验证密码格式
        is_valid, error_msg = password_validator.validate_format(new_password)
        
        if not is_valid:
            raise ValidationError(error_msg)
        
        return new_password
    
    def clean_old_password(self):
        """验证旧密码不为空"""
        old_password = self.cleaned_data.get('old_password', '')
        
        if not old_password:
            raise ValidationError('旧密码不能为空')
        
        return old_password
