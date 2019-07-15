$(function () {
    $(".content .con_right .left").click(function (e) {
        $(this).css({ "color": "#333333", "border-bottom": "2px solid #2e558e" });
        $(".content .con_right .right").css({ "color": "#999999", "border-bottom": "2px solid #dedede" });
        $(".content .con_right ul .con_r_left").css("display", "block");
        $(".content .con_right ul .con_r_right").css("display", "none");
    });

    $(".content .con_right .right").click(function (e) {
        $(this).css({ "color": "#333333", "border-bottom": "2px solid #2e558e" });
        $(".content .con_right .left").css({ "color": "#999999", "border-bottom": "2px solid #dedede" });
        $(".content .con_right ul .con_r_right").css("display", "block");
        $(".content .con_right ul .con_r_left").css("display", "none");
    });


    $('#btn_modify').click(function () {
        // ^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$\%\^\&\*\(\)])[0-9a-zA-Z!@#$\%\^\&\*\(\)]{8,32}$ 要求密码了里面包含字母、数字、特殊字符。
         // (?=.*[0-9])(?=.*[a-zA-Z])(?=.*[^a-zA-Z0-9]).{8,30}  密码必须同时包含大写、小写、数字和特殊字符其中三项且至少8位
        //  (?=.*?[a-z])(?=.*?[A-Z])(?=.*?\d)(?=.*?[!#@*&.])[a-zA-Z\d!#@*&.]*{8,30}$
        //    判断密码满足大写字母，小写字母，数字和特殊字符，其中四种组合都需要包含
        // (?=.*[0-9])(?=.*[a-zA-Z]).{8,30}   大小写字母+数字
        regex_mail = new RegExp('^\\w+((-\\w+)|(\\.\\w+))*\\@[A-Za-z0-9]+((\\.|-)[A-Za-z0-9]+)*\\.[A-Za-z0-9]+$')
        regex_pwd = new RegExp('(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[^a-zA-Z0-9]).{8,30}');
        if ($.trim($('#user_email').val()) === '') {
            alert('请输入邮箱账号');
            return false;
        } else if (!regex_mail.test($.trim($('#user_email').val()))) {
            alert('请输入正确的邮箱账号。\n');
            return false;
        } else if ($.trim($('#old_password').val()) === '') {
            alert('请输入旧密码');
            return false;
        } else if ($.trim($('#new_password').val()) === '') {
            alert('请输入新密码');
            return false;
        } else if ($.trim($('#new_password').val()) === '1qaz@WSX') {
            alert('密码1qaz@WSX为初始密码，禁止使用，请重新输入新密码。\n密码必须同时包含大写、小写、数字和特殊字符其中三项且至少8位。');
            return false;
        } else if (!regex_pwd.test($.trim($('#new_password').val()))) {
            alert('密码不符合复杂度规则，请重新输入新密码。\n密码必须同时包含大写、小写、数字和特殊字符其中三项且至少8位。');
            return false;
        } else if ($.trim($('#ensure_password').val()) === '') {
            alert('请再次输入新密码');
            return false;
        } else if ($.trim($('#new_password').val()) === $.trim($('#old_password').val())) {
            alert('新旧密码不能一样');
            return false;
        } else if ($.trim($('#ensure_password').val()) !== $.trim($('#new_password').val())) {
            alert('两次输入的新密码不一致');
            return false;
        } else {
            return true;
        }
    });     

    $('#btn_reset').click(function () {
        let regex_mail = new RegExp('^\\w+((-\\w+)|(\\.\\w+))*\\@[A-Za-z0-9]+((\\.|-)[A-Za-z0-9]+)*\\.[A-Za-z0-9]+$')
        let regex_pwd = new RegExp('(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[^a-zA-Z0-9]).{8,30}');
        if ($.trim($('#user_email').val()) === '') {
            alert('请输入邮箱账号');
            return false;
        } else if (!regex_mail.test($.trim($('#user_email').val()))) {
            alert('请输入正确的邮箱账号。\n');
            return false;
        } else if ($.trim($('#new_password').val()) === '') {
            alert('请输入密码');
            return false;
        } else if ($.trim($('#ensure_password').val()) === '') {
            alert('请再次输入新密码');
            return false;
        } else if ($.trim($('#new_password').val()) === '1qaz@WSX') {
            alert('密码1qaz@WSX为初始密码，禁止使用，请重新输入新密码。\n密码必须同时包含大写、小写、数字和特殊字符其中三项且至少8位。');
            return false;
        } else if (!regex_pwd.test($.trim($('#new_password').val()))) {
            alert('密码不符合复杂度规则，请重新输入新密码。\n密码必须同时包含大写、小写、数字和特殊字符其中三项且至少8位。\n例如：1qaz@WSX');
            return false;
        } else if ($.trim($('#ensure_password').val()) !== $.trim($('#new_password').val())) {
            alert('两次输入的新密码不一致');
            return false;
        } else {
            return true;
        }
    });
})
