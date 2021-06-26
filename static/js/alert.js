(function ($) {
  if (!$) {
    throw new Error('jQuery is undefined!');
  }
  $('head').append(
    "<style>.hide-scroll{height:100vh;overflow:hidden}.wrap_overlay_drak{position:fixed;top:0;bottom:0;left:0;right:0;background-color:rgba(99,99,99,.3);z-index:999999;font-size:14px}.wrap_overlay_drak .wrap_overlay{position:fixed;width:400px;margin-left:-220px;padding:10px 20px;transform:translate(0,-180px);left:50%;top:50%;opacity:.3;box-shadow:0 2px 10px rgba(99,99,99,.3);background:#fff;transition:all .15s linear;border-radius:5px}.wrap_overlay_drak .wrap_overlay.wrap_overlay_show{transform:translate(0,-150px);opacity:1}.wrap_overlay_drak .wrap_overlay #confirm_msg{z-index:9998}.wrap_overlay_drak .wrap_overlay .content_overlay{padding:20px;font-size:14px;text-align:left}.wrap_overlay_drak .wrap_overlay #alert_buttons,.wrap_overlay_drak .wrap_overlay #confirm_buttons{padding:10px;text-align:right;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none}.wrap_overlay_drak .wrap_overlay .alert_btn{padding:5px 15px;margin:0 5px;background:#3187de;cursor:pointer;color:#fff;border:none;border-radius:5px;font-size:14px;outline:0;-webkit-appearance:none}.wrap_overlay_drak .wrap_overlay .alert_btn_cancel{background:0 0;color:#409eff;border:1px solid #ddd}.wrap_overlay_drak .wrap_overlay #alert_buttons .alert_btn:hover,.wrap_overlay_drak .wrap_overlay #confirm_buttons .alert_btn:hover{opacity:.7}</style>"
  );
  $.extend({
    alert: function () {
      var args = arguments;
      if (
        args.length &&
        typeof args[0] == 'string' &&
        !$('#alert_msg').length
      ) {
        var dialog = $(
          '<div class="wrap_overlay_drak"><div class="wrap_overlay" id="alert_msg"><div class="content_overlay">' +
          args[0] +
          '</div><div id="alert_buttons"><button class="alert_btn alert_btn_ok">确定</button></div></div></div>'
        );
        dialog
          .on('click', '.alert_btn_ok', function () {
            $('.wrap_overlay').removeClass('wrap_overlay_show');
            setTimeout(function () {
              dialog.remove();
            }, 150);
            if (typeof args[1] == 'function') args[1].call($, !0);
          })
          .appendTo('body');
        setTimeout(function () {
          $('.wrap_overlay').addClass('wrap_overlay_show');
        }, 10);
      }
    },
    confirm: function () {
      var args = arguments;
      if (
        args.length &&
        typeof args[0] == 'string' &&
        !$('#confirm_msg').length
      ) {
        var dialog = $(
          '<div class="wrap_overlay_drak"><div class="wrap_overlay" id="confirm_msg"><div class="content_overlay">' +
          args[0] +
          '</div><div id="confirm_buttons"><button class="alert_btn alert_btn_ok">确定</button><button class="alert_btn alert_btn_cancel">取消</button></div></div></div>'
        );
        dialog
          .on('click', '#confirm_buttons .alert_btn_ok', function () {
            $('.wrap_overlay').removeClass('wrap_overlay_show');
            setTimeout(function () {
              dialog.remove();
              if (typeof args[1] == 'function') args[1].call($, !0);
            }, 200);
          })
          .on('click', '#confirm_buttons .alert_btn_cancel', function () {
            $('.wrap_overlay').removeClass('wrap_overlay_show');
            setTimeout(function () {
              dialog.remove();
              if (typeof args[1] == 'function') args[1].call($, !1);
            }, 200);
          })
          .appendTo('body');
        setTimeout(function () {
          $('.wrap_overlay').addClass('wrap_overlay_show');
        }, 10);
      }
    },
  });
})(jQuery);