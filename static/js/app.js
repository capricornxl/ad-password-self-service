/**
 * AD 自助密码服务平台 - 公共 JS 模块
 * 基于 Layui 封装，提供统一的 AJAX 请求、消息提示、SMS 验证等功能
 * 兼容移动端显示
 *
 * @version 2.0
 * @requires layui
 */
layui.define(['jquery', 'layer', 'form'], function(exports) {
    var $ = layui.jquery;
    var layer = layui.layer;
    var form = layui.form;
    
    // 配置 Layui 模板界定符，避免与 Django 模板冲突
    layui.laytpl.config({
        open: '<%',
        close: '%>'
    });
    
    /**
     * 设备检测工具
     */
    var DeviceUtil = {
        /**
         * 判断是否为移动设备
         * @returns {boolean}
         */
        isMobile: function() {
            return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
                || window.innerWidth < 768;
        },
        
        /**
         * 获取弹层适配宽度
         * @param {string} defaultWidth - 默认宽度（PC端）
         * @returns {string}
         */
        getLayerWidth: function(defaultWidth) {
            return this.isMobile() ? '90%' : defaultWidth;
        }
    };
    
    /**
     * 应用核心模块
     */
    var App = {
        // CSRF Token
        csrfToken: null,
        
        // 默认请求超时时间（毫秒）
        requestTimeout: 30000,
        
        /**
         * 初始化应用
         */
        init: function() {
            this.csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
            // 如果页面上没有 CSRF token，尝试从 cookie 获取
            if (!this.csrfToken) {
                this.csrfToken = this.getCookie('csrftoken');
            }
        },
        
        /**
         * 获取 Cookie 值
         * @param {string} name - Cookie 名称
         * @returns {string|null} Cookie 值
         */
        getCookie: function(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = $.trim(cookies[i]);
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        },
        
        /**
         * AJAX 请求封装
         * @param {string} url - 请求 URL
         * @param {object} data - 请求数据
         * @param {object} options - 额外选项
         * @returns {Promise} jQuery Promise
         */
        request: function(url, data, options) {
            var self = this;
            var defaults = {
                type: 'POST',
                dataType: 'json',
                timeout: this.requestTimeout,
                headers: { 'X-CSRFToken': this.csrfToken }
            };
            $.extend(defaults, options || {});
            defaults.url = url;
            defaults.data = data;
            
            // 返回带错误处理的 Promise
            return $.ajax(defaults).fail(function(xhr, status, error) {
                // 统一处理网络错误
                if (status === 'timeout') {
                    self.showError('请求超时，请稍后重试');
                } else if (status === 'parsererror') {
                    self.showError('服务器响应格式错误');
                } else if (xhr.status === 0) {
                    self.showError('网络连接失败，请检查网络');
                } else if (xhr.status === 403) {
                    self.showError('会话已过期，请刷新页面重试');
                } else if (xhr.status === 500) {
                    self.showError('服务器内部错误，请稍后重试');
                }
            });
        },
        
        /**
         * 显示错误提示（兼容移动端）
         * 使用 layer.alert() 显示错误，方便用户复制或截图
         * @param {string} message - 错误消息
         * @param {string} errorCode - 错误码（可选）
         */
        showError: function(message, errorCode) {
            var displayMsg = message;
            if (errorCode) {
                displayMsg += '<br><small style="color:#999;">错误码: ' + errorCode + '</small>';
            }
            layer.alert(displayMsg, {
                title: '错误',
                icon: 2,
                btn: ['确定'],
                area: DeviceUtil.getLayerWidth('400px')
            });
        },
        
        /**
         * 显示成功提示
         * @param {string} message - 成功消息
         * @param {function} callback - 回调函数（可选）
         */
        showSuccess: function(message, callback) {
            layer.msg(message, {
                icon: 1,
                time: 2000,
                maxWidth: DeviceUtil.isMobile() ? 260 : 380
            }, callback);
        },
        
        /**
         * 显示警告提示
         * @param {string} message - 警告消息
         */
        showWarning: function(message) {
            layer.msg(message, {
                icon: 0,
                time: 3000,
                shade: [0.1, '#000'],
                shadeClose: true,
                maxWidth: DeviceUtil.isMobile() ? 260 : 380
            });
        },
        
        /**
         * 显示信息提示
         * @param {string} message - 信息消息
         */
        showInfo: function(message) {
            layer.msg(message, {
                icon: 3,
                time: 2500,
                maxWidth: DeviceUtil.isMobile() ? 260 : 380
            });
        },
        
        /**
         * 显示加载中
         * @param {string} message - 加载提示消息（可选）
         * @returns {number} layer 索引，用于关闭
         */
        showLoading: function(message) {
            return layer.load(1, {
                shade: [0.3, '#000']
            });
        },
        
        /**
         * 关闭加载
         * @param {number} index - layer 索引
         */
        hideLoading: function(index) {
            if (index !== undefined && index !== null) {
                layer.close(index);
            }
        },
        
        /**
         * 确认弹层（兼容移动端）
         * @param {string} message - 确认消息
         * @param {function} yesCallback - 确认回调
         * @param {function} cancelCallback - 取消回调（可选）
         * @param {object} options - 额外选项（可选）
         */
        confirm: function(message, yesCallback, cancelCallback, options) {
            var defaults = {
                type: 0,
                content: message,
                btn: ['确定', '取消'],
                area: DeviceUtil.getLayerWidth('400px'),
                yes: yesCallback,
                btn2: cancelCallback,
                closeBtn: 0,
                anim: DeviceUtil.isMobile() ? 0 : 4
            };
            if (options) {
                $.extend(defaults, options);
            }
            layer.open(defaults);
        },
        
        /**
         * 弹出输入框（兼容移动端）
         * @param {object} options - 配置选项
         * @returns {number} layer 索引
         */
        prompt: function(options) {
            var defaults = {
                formType: 0,
                title: '请输入',
                area: DeviceUtil.getLayerWidth('400px')
            };
            $.extend(defaults, options);
            return layer.prompt(defaults, options.yes);
        },
        
        /**
         * 关闭指定 layer
         * @param {number} index - layer 索引
         */
        close: function(index) {
            layer.close(index);
        },
        
        /**
         * 关闭所有 layer
         */
        closeAll: function() {
            layer.closeAll();
        }
    };
    
    /**
     * SMS 短信验证工具类
     */
    var SMSUtil = {
        // 倒计时定时器
        timer: null,
        
        /**
         * 发送验证码
         * @param {string} username - 用户名
         * @param {string} code - OAuth code
         * @param {element|string} btnElement - 按钮元素
         * @param {function} callback - 回调函数 callback(error, response)
         */
        sendCode: function(username, code, btnElement, callback) {
            var $btn = $(btnElement);
            var originalText = $btn.text();
            
            // 禁用按钮，显示发送中
            $btn.prop('disabled', true).text('发送中...');
            
            App.request('/api/sms/send', {
                username: username,
                code: code
            }).done(function(res) {
                if (res.success) {
                    App.showSuccess(res.message);
                    // 更新手机号显示
                    if (res.data && res.data.mobile) {
                        $('#sms_mobile').val(res.data.mobile);
                        $('#sms_mobile_display').text(res.data.mobile);
                        $('#sms-tip').show();
                    }
                    // 开始倒计时
                    var waitSeconds = (res.data && res.data.wait_seconds) || 60;
                    SMSUtil.countdown(waitSeconds, btnElement, originalText);
                    if (callback) callback(null, res);
                } else {
                    App.showError(res.message, res.error_code);
                    $btn.prop('disabled', false).text(originalText);
                    // 如果有等待时间，开始倒计时
                    if (res.data && res.data.wait_seconds) {
                        SMSUtil.countdown(res.data.wait_seconds, btnElement, originalText);
                    }
                    if (callback) callback(res);
                }
            }).fail(function(xhr) {
                App.showError('网络错误，请重试');
                $btn.prop('disabled', false).text(originalText);
                if (callback) callback({ message: '网络错误' });
            });
        },
        
        /**
         * 倒计时
         * @param {number} seconds - 倒计时秒数
         * @param {element|string} btnElement - 按钮元素
         * @param {string} originalText - 原始按钮文本
         */
        countdown: function(seconds, btnElement, originalText) {
            var $btn = $(btnElement);
            $btn.prop('disabled', true);
            
            // 清除之前的定时器
            if (SMSUtil.timer) {
                clearInterval(SMSUtil.timer);
            }
            
            SMSUtil.timer = setInterval(function() {
                seconds--;
                $btn.text(seconds + '秒后重发');
                
                if (seconds <= 0) {
                    clearInterval(SMSUtil.timer);
                    SMSUtil.timer = null;
                    $btn.prop('disabled', false);
                    $btn.text(originalText || '获取验证码');
                }
            }, 1000);
        },
        
        /**
         * 验证验证码格式（前端校验）
         * @param {string} smsCode - 短信验证码
         * @returns {object} {valid: boolean, message: string}
         */
        validateCodeFormat: function(smsCode) {
            if (!smsCode) {
                return { valid: false, message: '请输入短信验证码' };
            }
            if (!/^\d{6}$/.test(smsCode)) {
                return { valid: false, message: '验证码必须是6位数字' };
            }
            return { valid: true, message: '' };
        },
        
        /**
         * 验证验证码
         * @param {string} username - 用户名
         * @param {string} mobile - 手机号
         * @param {string} smsCode - 短信验证码
         * @param {function} callback - 回调函数 callback(success, response)
         */
        verifyCode: function(username, mobile, smsCode, callback) {
            // 前端格式校验
            var validation = SMSUtil.validateCodeFormat(smsCode);
            if (!validation.valid) {
                App.showWarning(validation.message);
                callback(false, { message: validation.message });
                return;
            }
            
            App.request('/api/sms/verify', {
                username: username,
                mobile: mobile,
                sms_code: smsCode
            }).done(function(res) {
                if (res.success) {
                    App.showSuccess('验证成功');
                } else {
                    App.showError(res.message, res.error_code);
                }
                callback(res.success, res);
            }).fail(function() {
                App.showError('网络错误，请重试');
                callback(false, { message: '网络错误' });
            });
        },
        
        /**
         * 停止倒计时
         */
        stopCountdown: function() {
            if (SMSUtil.timer) {
                clearInterval(SMSUtil.timer);
                SMSUtil.timer = null;
            }
        }
    };
    
    /**
     * 密码工具类
     */
    var PasswordUtil = {
        /**
         * 从后端获取密码规则
         * @param {function} callback - 回调函数 callback(rules)
         */
        getRules: function(callback) {
            App.request('/api/config/password-rules', {}, { type: 'GET' })
                .done(function(res) {
                    if (res.success && res.data) {
                        callback(res.data);
                    } else {
                        // 使用默认规则
                        callback({
                            pattern: '^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9]).{8,30}$',
                            message: '密码必须8到30位，必须包含大写字母、小写字母、数字与特殊字符，且不能出现空格！',
                            min_length: 8,
                            max_length: 30
                        });
                    }
                })
                .fail(function() {
                    // 使用默认规则
                    callback({
                        pattern: '^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9]).{8,30}$',
                        message: '密码必须8到30位，必须包含大写字母、小写字母、数字与特殊字符，且不能出现空格！',
                        min_length: 8,
                        max_length: 30
                    });
                });
        },
        
        /**
         * 设置表单密码验证规则
         * @param {object} rules - 密码规则对象
         */
        setVerifyRules: function(rules) {
            form.verify({
                pass: [
                    new RegExp(rules.pattern),
                    rules.message
                ],
                repass: function(value) {
                    var newPass = $('input[name="new_password"]').val();
                    if (!newPass) {
                        newPass = $('#new_password').val();
                    }
                    if (value !== newPass) {
                        return '两次密码输入不一致';
                    }
                },
                newpass: function(value) {
                    var oldPass = $('input[name="old_password"]').val();
                    var newPass = $('input[name="new_password"]').val();
                    if (!newPass) {
                        newPass = $('#new_password').val();
                    }
                    if (oldPass && newPass && oldPass === newPass) {
                        return '新旧密码不能相同，请修改！';
                    }
                }
            });
        }
    };
    
    // 导出模块
    exports('app', {
        App: App,
        DeviceUtil: DeviceUtil,
        SMSUtil: SMSUtil,
        PasswordUtil: PasswordUtil,
        init: function() {
            App.init();
        }
    });
});