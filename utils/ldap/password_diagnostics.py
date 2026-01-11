# -*- coding: utf-8 -*-
"""
AD密码错误诊断模块

用于诊断AD密码修改失败（特别是0000052D错误）的具体原因，
提供精确的错误提示信息。
"""

from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional
from utils.logger_factory import get_logger

logger = get_logger(__name__)


class PasswordDiagnostics:
    """AD密码错误诊断器
    
    用于分析AD密码策略并诊断密码修改失败的具体原因。
    
    AD时间格式说明：
    - AD使用100纳秒间隔（FILETIME格式）
    - 时间从1601-01-01开始计算
    - minPwdAge是负数，表示"距离过去多久"
    - 转换公式：days = abs(ad_time) / 864000000000
    """
    
    # AD时间常量
    AD_TIME_INTERVAL = 10000000  # 100纳秒单位（1秒 = 10,000,000）
    SECONDS_PER_DAY = 86400
    AD_TIME_UNITS_PER_DAY = AD_TIME_INTERVAL * SECONDS_PER_DAY  # 864000000000
    
    # AD时间纪元：1601-01-01 00:00:00
    AD_EPOCH = datetime(1601, 1, 1, 0, 0, 0)
    
    # 密码复杂度标志位
    PASSWORD_COMPLEXITY_ENABLED = 1  # pwdProperties & 1 = 启用复杂度
    
    @classmethod
    def diagnose_52d_error(cls, user_attrs: Dict, policy: Dict, 
                          new_password: str) -> Tuple[str, str]:
        """诊断 0000052D 错误的具体原因
        
        0000052D 错误通常表示"密码不符合策略要求"，需要分析具体原因：
        1. 密码期限未满足（minPwdAge）
        2. 密码长度不足
        3. 密码历史冲突
        4. 密码复杂度不足
        
        Args:
            user_attrs: 用户密码相关属性
                - pwdLastSet: 上次密码修改时间（AD时间戳）
                - badPwdCount: 错误密码计数（可选）
            policy: 域密码策略
                - minPwdAge: 最小密码期限（100纳秒间隔）
                - pwdHistoryLength: 密码历史长度
                - minPwdLength: 最小密码长度
                - pwdProperties: 密码复杂度标志
            new_password: 新密码（用于本地检查）
        
        Returns:
            Tuple[str, str]: (错误标题, 详细错误信息)
        """
        try:
            diagnoses = []
            
            # 1. 检查密码期限
            min_age_diagnosis = cls._check_min_pwd_age(user_attrs, policy)
            if min_age_diagnosis:
                diagnoses.append(min_age_diagnosis)
            
            # 2. 检查密码长度
            length_diagnosis = cls._check_password_length(new_password, policy)
            if length_diagnosis:
                diagnoses.append(length_diagnosis)
            
            # 3. 检查密码历史
            history_diagnosis = cls._check_password_history(policy)
            if history_diagnosis:
                diagnoses.append(history_diagnosis)
            
            # 4. 检查密码复杂度
            complexity_diagnosis = cls._check_password_complexity(new_password, policy)
            if complexity_diagnosis:
                diagnoses.append(complexity_diagnosis)
            
            # 返回诊断结果
            if diagnoses:
                # 返回第一个（最可能的）诊断结果
                return diagnoses[0]
            
            # 未找到具体原因，返回通用提示
            return (
                "密码不符合策略要求",
                "新密码不符合域密码策略要求，请检查密码是否符合复杂度、长度和历史记录要求。"
            )
            
        except Exception as e:
            logger.error(f"密码诊断过程中发生异常: {e}")
            # 诊断失败时降级到通用错误提示
            return (
                "密码不符合策略要求",
                "新密码不符合域密码策略要求，请检查密码是否符合复杂度、长度和历史记录要求。"
            )
    
    @classmethod
    def _check_min_pwd_age(cls, user_attrs: Dict, policy: Dict) -> Optional[Tuple[str, str]]:
        """检查密码期限限制
        
        检查距离上次修改密码的时间是否满足最小密码期限要求。
        
        Args:
            user_attrs: 用户属性（包含pwdLastSet）
            policy: 域策略（包含minPwdAge）
        
        Returns:
            如果违反期限限制，返回错误信息元组；否则返回None
        """
        try:
            pwd_last_set = user_attrs.get('pwdLastSet')
            min_pwd_age = policy.get('minPwdAge')
            
            # 如果没有配置最小密码期限或值为0，跳过检查
            if not min_pwd_age or min_pwd_age == 0:
                logger.debug("未配置最小密码期限(minPwdAge)，跳过期限检查")
                return None
            
            # 如果从未设置过密码或必须更改密码，跳过检查
            # pwdLastSet = 0: 用户从未设置过密码
            # pwdLastSet = -1: 用户必须在下次登录时更改密码
            if not pwd_last_set or pwd_last_set == 0 or pwd_last_set == -1:
                logger.debug(f"跳过期限检查 (pwdLastSet={pwd_last_set})")
                return None
            
            # 计算最小密码期限（天数）
            min_age_days = cls._parse_ad_time(min_pwd_age)
            
            if min_age_days <= 0:
                return None
            
            # 计算上次修改密码的时间
            last_set_datetime = cls._ad_time_to_datetime(pwd_last_set)
            
            # 计算允许修改密码的最早时间
            earliest_change = last_set_datetime + timedelta(days=min_age_days)
            
            # 当前时间
            now = datetime.utcnow()
            
            # 检查是否满足期限要求
            if now < earliest_change:
                remaining = earliest_change - now
                remaining_days = remaining.days
                remaining_hours = remaining.seconds // 3600
                
                if remaining_days > 0:
                    time_str = f"{remaining_days}天"
                    if remaining_hours > 0:
                        time_str += f"{remaining_hours}小时"
                else:
                    time_str = f"{remaining_hours}小时"
                
                logger.info(f"密码期限检查失败: 距离上次修改已过{(now - last_set_datetime).days}天，"
                           f"需要{min_age_days}天，还需等待{time_str}")
                
                return (
                    "密码修改时间间隔不足",
                    f"根据域策略，距离上次修改密码不足 {min_age_days} 天，"
                    f"还需等待 {time_str} 后才能再次修改密码。"
                )
            
            logger.debug(f"密码期限检查通过: 距离上次修改已过{(now - last_set_datetime).days}天")
            return None
            
        except Exception as e:
            logger.error(f"检查密码期限时发生异常: {e}")
            return None
    
    @classmethod
    def _check_password_length(cls, new_password: str, policy: Dict) -> Optional[Tuple[str, str]]:
        """检查密码长度
        
        Args:
            new_password: 新密码
            policy: 域策略（包含minPwdLength）
        
        Returns:
            如果长度不足，返回错误信息元组；否则返回None
        """
        try:
            min_length = policy.get('minPwdLength', 0)
            
            if not min_length or min_length <= 0:
                logger.debug("未配置最小密码长度，跳过长度检查")
                return None
            
            actual_length = len(new_password) if new_password else 0
            
            if actual_length < min_length:
                logger.info(f"密码长度检查失败: 实际长度{actual_length}，要求{min_length}")
                return (
                    "密码长度不足",
                    f"密码长度至少需要 {min_length} 个字符，当前密码长度为 {actual_length} 个字符。"
                )
            
            logger.debug(f"密码长度检查通过: 长度{actual_length}，要求{min_length}")
            return None
            
        except Exception as e:
            logger.error(f"检查密码长度时发生异常: {e}")
            return None
    
    @classmethod
    def _check_password_history(cls, policy: Dict) -> Optional[Tuple[str, str]]:
        """检查密码历史
        
        注意：无法直接检查新密码是否在历史中（AD不暴露密码历史），
        只能提示用户可能的原因。
        
        Args:
            policy: 域策略（包含pwdHistoryLength）
        
        Returns:
            如果配置了密码历史，返回提示信息；否则返回None
        """
        try:
            history_length = policy.get('pwdHistoryLength', 0)
            
            if not history_length or history_length <= 0:
                logger.debug("未配置密码历史长度，跳过历史检查")
                return None
            
            logger.debug(f"密码历史长度: {history_length}")
            
            # 无法直接检查，返回提示
            return (
                "密码可能在历史记录中",
                f"域策略要求新密码不能与最近 {history_length} 次使用过的密码相同，"
                "请尝试使用一个从未使用过的密码。"
            )
            
        except Exception as e:
            logger.error(f"检查密码历史时发生异常: {e}")
            return None
    
    @classmethod
    def _check_password_complexity(cls, new_password: str, policy: Dict) -> Optional[Tuple[str, str]]:
        """检查密码复杂度
        
        AD密码复杂度要求（当pwdProperties & 1 = 1时）：
        1. 至少包含一个大写字母
        2. 至少包含一个小写字母
        3. 至少包含一个数字
        4. 至少包含一个特殊字符
        5. 不能包含用户账号名或全名
        
        Args:
            new_password: 新密码
            policy: 域策略（包含pwdProperties）
        
        Returns:
            如果复杂度不足，返回错误信息元组；否则返回None
        """
        import re
        
        try:
            pwd_properties = policy.get('pwdProperties', 0)
            
            # 检查是否启用了密码复杂度要求
            if not (pwd_properties & cls.PASSWORD_COMPLEXITY_ENABLED):
                logger.debug("未启用密码复杂度要求，跳过复杂度检查")
                return None
            
            if not new_password:
                return (
                    "密码复杂度不足",
                    "密码不能为空。"
                )
            
            # 检查复杂度要求
            missing_requirements = []
            
            # 检查大写字母
            if not re.search(r'[A-Z]', new_password):
                missing_requirements.append("大写字母(A-Z)")
            
            # 检查小写字母
            if not re.search(r'[a-z]', new_password):
                missing_requirements.append("小写字母(a-z)")
            
            # 检查数字
            if not re.search(r'\d', new_password):
                missing_requirements.append("数字(0-9)")
            
            # 检查特殊字符
            if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', new_password):
                missing_requirements.append("特殊字符(!@#$%^&*等)")
            
            if missing_requirements:
                logger.info(f"密码复杂度检查失败: 缺少 {', '.join(missing_requirements)}")
                return (
                    "密码复杂度不足",
                    f"密码必须包含以下字符类型：{', '.join(missing_requirements)}。"
                )
            
            logger.debug("密码复杂度检查通过")
            return None
            
        except Exception as e:
            logger.error(f"检查密码复杂度时发生异常: {e}")
            return None
    
    @classmethod
    def _parse_ad_time(cls, ad_time: int) -> float:
        """将AD时间格式转换为天数
        
        AD时间以100纳秒为单位，minPwdAge是负数表示"距离过去"。
        
        Args:
            ad_time: AD时间值（100纳秒单位）
        
        Returns:
            天数（正数）
        
        Examples:
            >>> cls._parse_ad_time(-864000000000)  # 1天
            1.0
            >>> cls._parse_ad_time(-1728000000000)  # 2天
            2.0
        """
        try:
            # 取绝对值并转换为天数
            return abs(ad_time) / cls.AD_TIME_UNITS_PER_DAY
        except (TypeError, ValueError) as e:
            logger.error(f"解析AD时间失败: {ad_time}, 错误: {e}")
            return 0.0
    
    @classmethod
    def _ad_time_to_datetime(cls, ad_time: int) -> datetime:
        """将AD时间戳转换为datetime
        
        AD时间戳从1601-01-01开始计算，以100纳秒为单位。
        
        Args:
            ad_time: AD时间戳
        
        Returns:
            datetime对象（UTC时间）
        
        Examples:
            >>> dt = cls._ad_time_to_datetime(132000000000000000)  # 某个时间戳
        """
        try:
            # AD时间戳是从1601-01-01开始的100纳秒间隔数
            # 转换为秒
            seconds = ad_time / cls.AD_TIME_INTERVAL
            # 加上AD纪元
            return cls.AD_EPOCH + timedelta(seconds=seconds)
        except (TypeError, ValueError) as e:
            logger.error(f"转换AD时间戳失败: {ad_time}, 错误: {e}")
            return datetime.utcnow()
    
    @classmethod
    def format_diagnosis_result(cls, title: str, detail: str) -> str:
        """格式化诊断结果为用户友好的消息
        
        Args:
            title: 错误标题
            detail: 详细信息
        
        Returns:
            格式化后的错误消息
        """
        return f"{title}。{detail}"


# 便捷函数
def diagnose_password_error(user_attrs: Dict, policy: Dict, 
                           new_password: str) -> Tuple[str, str]:
    """诊断密码错误的便捷函数
    
    Args:
        user_attrs: 用户密码相关属性
        policy: 域密码策略
        new_password: 新密码
    
    Returns:
        Tuple[str, str]: (错误标题, 详细错误信息)
    """
    return PasswordDiagnostics.diagnose_52d_error(user_attrs, policy, new_password)