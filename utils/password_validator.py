# -*- coding: utf-8 -*-
"""
密码验证器 - 统一的密码策略和验证逻辑
"""
import re
import os
from typing import Tuple, List, Optional
from dataclasses import dataclass, field
from utils.config import get_config
from utils.logger_factory import get_logger

logger = get_logger(__name__)


@dataclass
class PasswordPolicy:
    """密码策略配置"""
    min_length: int = 8
    max_length: int = 30
    require_uppercase: bool = True
    require_lowercase: bool = True
    require_digits: bool = True
    require_special_chars: bool = True
    forbidden_patterns: List[str] = field(default_factory=list)
    forbidden_password_file: str = ""
    forbidden_regex: List[str] = field(default_factory=list)
    check_history: bool = False
    history_count: int = 3

    @classmethod
    def from_config(cls) -> 'PasswordPolicy':
        """从配置文件加载密码策略"""
        config = get_config()
        policy_config = config.get_dict('password_policy')
        
        forbidden = policy_config.get('forbidden_patterns', [])
        forbidden_file = policy_config.get('forbidden_password_file', '')
        forbidden_regex = policy_config.get('forbidden_regex', [])
        
        return cls(
            min_length=policy_config.get('min_length', 8),
            max_length=policy_config.get('max_length', 30),
            require_uppercase=policy_config.get('require_uppercase', True),
            require_lowercase=policy_config.get('require_lowercase', True),
            require_digits=policy_config.get('require_digits', True),
            require_special_chars=policy_config.get('require_special_chars', True),
            forbidden_patterns=forbidden if isinstance(forbidden, list) else [],
            forbidden_password_file=forbidden_file,
            forbidden_regex=forbidden_regex if isinstance(forbidden_regex, list) else [],
            check_history=policy_config.get('check_history', False),
            history_count=policy_config.get('history_count', 3)
        )


class PasswordValidator:
    """
    密码验证器
    
    支持：
    - 基础格式验证（长度、字符类型）
    - 禁用模式验证（精确匹配、正则表达式）
    - 外部弱密码字典验证
    - 密码强度评估
    
    Example:
        validator = PasswordValidator()
        is_valid, message = validator.validate('NewPass123!@#')
        
        # 获取密码强度
        strength = validator.get_password_strength('NewPass123!@#')
    """
    
    def __init__(self, policy: Optional[PasswordPolicy] = None):
        """
        初始化验证器
        
        Args:
            policy: 密码策略，如果为None则从配置加载
        """
        self.policy = policy or PasswordPolicy.from_config()
        self._weak_passwords = self._load_weak_passwords()
        self._compiled_regex = self._compile_forbidden_regex()

    def _load_weak_passwords(self) -> List[str]:
        """从外部文件加载弱密码字典"""
        weak_passwords = []
        file_path = self.policy.forbidden_password_file
        
        if not file_path or not file_path.strip():
            return weak_passwords
        
        if not os.path.isabs(file_path):
            # 相对路径，相对于项目根目录
            import sys
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(project_root, file_path)
        
        if not os.path.exists(file_path):
            logger.warning(f"弱密码字典文件不存在: {file_path}")
            return weak_passwords
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):  # 忽略空行和注释
                        weak_passwords.append(line.lower())
            logger.info(f"已加载 {len(weak_passwords)} 条弱密码规则从文件: {file_path}")
        except Exception as e:
            logger.error(f"加载弱密码字典失败: {file_path}, 错误: {e}")
        
        return weak_passwords
    
    def _compile_forbidden_regex(self) -> List[re.Pattern]:
        """编译禁用正则表达式列表"""
        compiled = []
        for pattern in self.policy.forbidden_regex:
            try:
                compiled.append(re.compile(pattern, re.IGNORECASE))
            except re.error as e:
                logger.error(f"正则表达式编译失败: {pattern}, 错误: {e}")
        return compiled

    def validate(self, password: str) -> Tuple[bool, str]:
        """
        验证密码
        
        Args:
            password: 待验证的密码
            
        Returns:
            (是否有效, 错误消息)
        """
        # 检查长度
        if not password:
            return False, "密码不能为空"
        
        if len(password) < self.policy.min_length:
            return False, f"密码长度不能少于{self.policy.min_length}个字符"
        
        if len(password) > self.policy.max_length:
            return False, f"密码长度不能超过{self.policy.max_length}个字符"
        
        # 检查必需字符类型
        errors = []
        
        if self.policy.require_uppercase and not re.search(r'[A-Z]', password):
            errors.append("需包含大写字母")
        
        if self.policy.require_lowercase and not re.search(r'[a-z]', password):
            errors.append("需包含小写字母")
        
        if self.policy.require_digits and not re.search(r'\d', password):
            errors.append("需包含数字")
        
        if self.policy.require_special_chars and not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password):
            errors.append("需包含特殊字符")
        
        if errors:
            return False, f"密码必须{' 、'.join(errors)}"
        
        # 检查禁用模式
        for forbidden in self.policy.forbidden_patterns:
            if forbidden.lower() in password.lower():
                return False, f"密码包含禁用词汇，请重新设置"
        
        # 检查弱密码字典
        if password.lower() in self._weak_passwords:
            return False, f"密码过于简单或常见，请使用更复杂的密码"
        
        # 检查正则表达式规则
        for regex_pattern in self._compiled_regex:
            if regex_pattern.search(password):
                return False, f"密码格式不符合安全要求，请重新设置"
        
        return True, ""

    def validate_format(self, password: str) -> Tuple[bool, str]:
        """验证格式（长度和字符类型）"""
        return self.validate(password)

    def validate_not_reused(self, new_password: str, old_password: str) -> Tuple[bool, str]:
        """
        检查新密码是否与旧密码相同
        
        Args:
            new_password: 新密码
            old_password: 旧密码
            
        Returns:
            (是否有效, 错误消息)
        """
        if new_password == old_password:
            return False, "新旧密码不能相同"
        return True, ""

    def validate_confirmation(self, password: str, confirmation: str) -> Tuple[bool, str]:
        """
        检查密码确认是否一致
        
        Args:
            password: 密码
            confirmation: 确认密码
            
        Returns:
            (是否有效, 错误消息)
        """
        if password != confirmation:
            return False, "两次输入的密码不一致"
        return True, ""

    def get_password_strength(self, password: str) -> str:
        """
        获取密码强度
        
        Args:
            password: 密码
            
        Returns:
            强度等级：weak, medium, strong
        """
        if not password:
            return "weak"
        
        score = 0
        
        # 长度评分
        if len(password) >= self.policy.min_length:
            score += 1
        if len(password) >= 12:
            score += 1
        if len(password) >= 16:
            score += 1
        
        # 字符类型评分
        if re.search(r'[a-z]', password):
            score += 1
        if re.search(r'[A-Z]', password):
            score += 1
        if re.search(r'\d', password):
            score += 1
        if re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password):
            score += 1
        
        # 重复字符扣分
        if re.search(r'(.)\1{2,}', password):
            score -= 1
        
        # 顺序字符扣分
        if re.search(r'(abc|bcd|cde|123|234|345|qwe|wer|ert)', password.lower()):
            score -= 1
        
        # 判断强度
        if score >= 6:
            return "strong"
        elif score >= 4:
            return "medium"
        else:
            return "weak"

    def get_policy_description(self) -> str:
        """
        获取密码策略描述
        
        Returns:
            人类可读的密码策略描述
        """
        requirements = []
        requirements.append(f"{self.policy.min_length}到{self.policy.max_length}个字符")
        
        if self.policy.require_uppercase:
            requirements.append("包含大写字母")
        if self.policy.require_lowercase:
            requirements.append("包含小写字母")
        if self.policy.require_digits:
            requirements.append("包含数字")
        if self.policy.require_special_chars:
            requirements.append("包含特殊字符")
        
        return "，".join(requirements)

    @staticmethod
    def build_regex_pattern(policy: PasswordPolicy) -> str:
        """
        构建正则表达式模式
        
        Args:
            policy: 密码策略
            
        Returns:
            可用于HTML5 pattern属性的正则表达式
        """
        pattern = f"(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[!@#$%^&*()_+\\-=\\[\\]{{}};:'\",.<>?/\\\\|`~]).{{{policy.min_length},{policy.max_length}}}"
        return pattern


# 全局密码验证器单例
_password_validator = None


def get_password_validator(policy: Optional[PasswordPolicy] = None) -> PasswordValidator:
    """获取全局密码验证器实例"""
    global _password_validator
    if _password_validator is None:
        _password_validator = PasswordValidator(policy)
    return _password_validator
