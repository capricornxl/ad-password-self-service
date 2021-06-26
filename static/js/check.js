
function BtnClick(btn, type, unsecpwd) {
    $(btn).click(function () {
        // ^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$\%\^\&\*\(\)])[0-9a-zA-Z!@#$\%\^\&\*\(\)]{8,32}$ 要求密码了里面包含字母、数字、特殊字符。
        // (?=.*[0-9])(?=.*[a-zA-Z])(?=.*[^a-zA-Z0-9]).{8,30}  密码必须同时包含大写、小写、数字和特殊字符其中三项且至少8位
        //  (?=.*?[a-z])(?=.*?[A-Z])(?=.*?\d)(?=.*?[!#@*&.])[a-zA-Z\d!#@*&.]*{8,30}$
        //    判断密码满足大写字母，小写字母，数字和特殊字符，其中四种组合都需要包含
        // (?=.*[0-9])(?=.*[a-zA-Z]).{8,30}   大小写字母+数字
        let regex_mail = new RegExp('^\\w+((-\\w+)|(\\.\\w+))*\\@[A-Za-z0-9]+((\\.|-)[A-Za-z0-9]+)*\\.[A-Za-z0-9]+$')
        let regex_pwd = new RegExp('(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[^a-zA-Z0-9]).{8,30}');
        let new_password = $('#new_password').val()
        let old_password = $('#old_password').val()
        let ensure_password = $('#ensure_password').val()
        if ($.trim(old_password) === '' && type === 'modify') {
            $.alert('请输入旧密码');
            return false;
        } else if ($.trim(new_password) === '') {
            $.alert('请输入新密码');
            return false;
        } else if (jQuery.inArray(new_password, unsecpwd) !== -1) {
            $.alert('弱密码禁止使用，请重新输入新密码。\n密码必须同时包含大写、小写、数字和特殊字符其中三项且至少8位。');
            return false;
        } else if (!regex_pwd.test($.trim(new_password))) {
            $.alert('密码不符合复杂度规则，请重新输入新密码。\n密码必须同时包含大写、小写、数字和特殊字符其中三项且至少8位。');
            return false;
        } else if ($.trim(ensure_password) === '') {
            $.alert('请再次输入新密码');
            return false;
        } else if ($.trim(new_password) === $.trim(old_password)) {
            $.alert('新旧密码不能一样');
            return false;
        } else if ($.trim(ensure_password) !== $.trim(new_password)) {
            $.alert('两次输入的新密码不一致');
            return false;
        } else {
            return true;
        }
    });
}