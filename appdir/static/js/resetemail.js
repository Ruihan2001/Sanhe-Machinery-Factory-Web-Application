$(document).ready(function () {

    $("#submitLogin").on("click", user_login)

});

var zlalert = {
    /*
        功能：提示错误
        参数：
            - msg：提示的内容（可选）
    */
    'alertError': function (msg) {
        swal('Note', msg, 'error');
    },
    /*
        功能：信息提示
        参数：
            - msg：提示的内容（可选）
    */
    'alertInfo': function (msg) {
        swal('Note', msg, 'warning');
    },
    /*
        功能：可以自定义标题的信息提示
        参数：
            - msg：提示的内容（可选）
    */
    'alertInfoWithTitle': function (title, msg) {
        swal(title, msg);
    },
    /*
        功能：成功的提示
        参数：
            - msg：提示的内容（必须）
            - confirmCallback：确认按钮的执行事件（可选）
    */
    'alertSuccess': function (msg, confirmCallback) {
        args = {
            'title': 'Note',
            'text': msg,
            'type': 'success',
        }
        swal(args, confirmCallback);
    },
    /*
        功能：带有标题的成功提示
        参数：
            - title：提示框的标题（必须）
            - msg：提示的内容（必须）
    */
    'alertSuccessWithTitle': function (title, msg) {
        swal(title, msg, 'success');
    },
    /*
        功能：确认提示
        参数：字典的形式
            - title：提示框标题（可选）
            - type：提示框的类型（可选）
            - confirmText：确认按钮文本（可选）
            - cancelText：取消按钮文本（可选）
            - msg：提示框内容（必须）
            - confirmCallback：确认按钮点击回调（可选）
            - cancelCallback：取消按钮点击回调（可选）
    */
    'alertConfirm': function (params) {
        swal({
            'title': params['title'] ? params['title'] : 'Note',
            'showCancelButton': true,
            'showConfirmButton': true,
            'type': params['type'] ? params['type'] : '',
            'confirmButtonText': params['confirmText'] ? params['confirmText'] : '确定',
            'cancelButtonText': params['cancelText'] ? params['cancelText'] : '取消',
            'text': params['msg'] ? params['msg'] : ''
        }, function (isConfirm) {
            if (isConfirm) {
                if (params['confirmCallback']) {
                    params['confirmCallback']();
                }
            } else {
                if (params['cancelCallback']) {
                    params['cancelCallback']();
                }
            }
        });
    },
    /*
        功能：带有一个输入框的提示
        参数：字典的形式
            - title：提示框的标题（可选）
            - text：提示框的内容（可选）
            - placeholder：输入框的占位文字（可选）
            - confirmText：确认按钮文字（可选）
            - cancelText：取消按钮文字（可选）
            - confirmCallback：确认后的执行事件
    */
    'alertOneInput': function (params) {
        swal({
            'title': params['title'] ? params['title'] : 'Please enter',
            'text': params['text'] ? params['text'] : '',
            'type': 'input',
            'showCancelButton': true,
            'animation': 'slide-from-top',
            'closeOnConfirm': false,
            'showLoaderOnConfirm': true,
            'inputPlaceholder': params['placeholder'] ? params['placeholder'] : '',
            'confirmButtonText': params['confirmText'] ? params['confirmText'] : 'Confirm',
            'cancelButtonText': params['cancelText'] ? params['cancelText'] : 'Cancel',
        }, function (inputValue) {
            if (inputValue === false) return false;
            if (inputValue === '') {
                swal.showInputError('Input cannot be empty！');
                return false;
            }
            if (params['confirmCallback']) {
                params['confirmCallback'](inputValue);
            }
        });
    },
    /*
        功能：网络错误提示
        参数：无
    */
    'alertNetworkError': function () {
        this.alertErrorToast('网络错误');
    },
    /*
        功能：信息toast提示（1s后消失）
        参数：
            - msg：提示消息
    */
    'alertInfoToast': function (msg) {
        this.alertToast(msg, 'info');
    },
    /*
        功能：错误toast提示（1s后消失）
        参数：
            - msg：提示消息
    */
    'alertErrorToast': function (msg) {
        this.alertToast(msg, 'error');
    },
    /*
        功能：成功toast提示（1s后消失）
        参数：
            - msg：提示消息
    */
    'alertSuccessToast': function (msg) {
        if (!msg) {
            msg = '成功！';
        }
        this.alertToast(msg, 'success');
    },
    /*
        功能：弹出toast（1s后消失）
        参数：
            - msg：提示消息
            - type：toast的类型
    */
    'alertToast': function (msg, type) {
        swal({
            'title': msg,
            'text': '',
            'type': type,
            'showCancelButton': false,
            'showConfirmButton': false,
            'timer': 3000,
        });
    },
    // 关闭当前对话框
    'close': function () {
        swal.close();
    }
};

var zlajax = {
    'get': function (args) {
        args['method'] = 'get';
        this.ajax(args);
    },
    'post': function (args) {
        args['method'] = 'post';
        this.ajax(args);
    },
    'ajax': function (args) {
        // 设置csrftoken
        this._ajaxSetup();
        $.ajax(args);
    },
    '_ajaxSetup': function () {
        $.ajaxSetup({
            'beforeSend': function (xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    var csrftoken = $('meta[name=csrf-token]').attr('content');
                    xhr.setRequestHeader("X-CSRFToken", csrftoken)
                }
            }
        });
    }
};

$(function () {
    $("#captcha-btn").click(function (event) {
        event.preventDefault();
        var email = $("input[name='email']").val();
        this.messageComponent = new messageControl();
        this.messageComponent.message({
            type: "success",
            content: 'Email has been sent to:' + jQuery("input[name='email']").val()
        })
        if (!email) {
            zlalert.alertInfoToast('Please enter the email address');
        }
        zlajax.get({
            'url': 'email_captcha/',
            'data': {'email': email},
            'success': function (data) {
                if (data['code'] === 200) {
                    zlalert.alertSuccessToast('Verification code has been sent to you Email!');
                } else {
                    zlalert.alertInfo(data['message']);
                }
            },
            'fail': function (error) {
                zlalert.alertNetworkError();
            }
        });
    });
});


$(function () {
    $("#submit").click(function (event) {
        event.preventDefault();
        var emailE = $("input[name='email']");
        var captcheE = $("input[name='captcha']");
        var userpw = $("input[name='userpw']").val();

        var email = emailE.val();
        var captcha = captcheE.val();

        zlajax.get({
            'url': 'verification/',
            'data': {'email': email, 'captcha': captcha, 'userpw': userpw},
            'success': function (data) {
                if (data['code'] === 200) {
                    emailE.val("");
                    captcheE.val("");
                    zlalert.alertSuccessToast('Congratulation! You\' have registered successfully!');
                    setTimeout(function () {
                        window.location.href = "/sanhe/set_jwt_cookie/" + data['message']
                    }, 1000)
                } else {
                    zlalert.alertInfo(data['message']);
                }
            },
            'fail': function (error) {
                zlalert.alertNetworkError();
            }
        });
    });
});

function user_login() {
    let user = $("#user");
    let password = $("#password")

    $.post(
        'login',
        {
            name: user.val(),
            password: password.val(),
            // type: type
        }
    ).done(function (response) {
        console.log(response)
        if (response['result'] === "success") {
            window.location.href = "/sanhe/set_jwt_cookie/" + response['user_unicode']
        }
        let server_code = response['returnValue'];
        if (server_code === 0) {
            $.ajax(
                {
                    type: 'POST',
                    async: false,
                    url: '/api/get_user',
                    success: function (data) {
                        if (data['type'] === 'user')
                            $(location).attr("href", "/sanhe/index")
                        else
                            $(location).attr("href", "/staff/index")
                    }
                }
            );
        } else if (server_code === 1) {
            //window.alert("no such user")
            console.dir("No such user")
            zlalert.alertInfoToast('No such user');
        } else if (server_code === 2) {
            zlalert.alertInfoToast('Wrong password');
        }
    }).fail(function () {
        zlalert.alertInfoToast('Login fail');
        // window.alert("login fail")
    })
}


$(function () {
    $("#confirm").click(function (event) {
        event.preventDefault();
        var emailE = $("input[name='email']");
        var captcheE = $("input[name='captcha']");

        var email = emailE.val();
        var captcha = captcheE.val();
        var time = 4;

        zlajax.get({
            'url': 'verification/',
            'data': {'email': email, 'captcha': captcha},
            'success': function (data) {
                if (data['code'] === 200) {
                    emailE.val("");
                    captcheE.val("");
                    zlalert.alertSuccessToast('Congratulation! Password has been reset successfully!');
                    setInterval(function () {
                        if (time == 0) {
                            window.location.href = "/sanhe/auth/a"
                        } else {

                            time--;
                        }
                    }, 1000);


                } else {
                    zlalert.alertInfo(data['message']);
                }
            },
            'fail': function (error) {
                zlalert.alertNetworkError();
            }
        });
    });
});