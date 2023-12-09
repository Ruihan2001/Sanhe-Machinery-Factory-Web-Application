function copy(str) {
    var save = function (e) {
        e.clipboardData.setData('text/plain', str);//下面会说到clipboardData对象
        e.preventDefault();//阻止默认行为
    }
    document.addEventListener('copy', save);
    document.execCommand("copy");//使文档处于可编辑状态，否则无效
}

var leftSider = function () {
    "use strict";
    $(".navbar-nav").ready(function () {
        var screenWidth = $(window).width();
        if (screenWidth <= 991) {
            jQuery(".navbar-nav > li > a, .sub-menu > li > a")
                .unbind()
                .on("click", function (e) {
                    if (jQuery(this).parent().hasClass("open")) {
                        jQuery(this).parent().removeClass("open");
                    } else {
                        jQuery(this).parent().parent().find("li").removeClass("open");
                        jQuery(this).parent().addClass("open");
                    }
                });
        }

        jQuery('.copy-phone').on('click', function (e) {
            copy("+86 13559329496")
            this.messageComponent = new messageControl()
            this.messageComponent.message({content: 'phone number: +86 13559329496 has been copied'})
        });
        if (jQuery('.copy-email')) {
            jQuery('.copy-email').on('click', function (e) {
                copy("han.weng.sanhe@gmail.com")
                this.messageComponent = new messageControl()
                this.messageComponent.message({content: 'email: han.weng.sanhe@gmail.com has been copied'})
            });
        }
        if (jQuery('.copy-qq')) {
            jQuery('.copy-qq').on('click', function (e) {
                copy("1053924276")
                this.messageComponent = new messageControl()
                this.messageComponent.message({content: 'QQ number: 1053924276 has been copied'})
            });
        }
    })
}
leftSider();

jQuery(window).on("resize", function () {
    "use strict";
    if (jQuery(window).width() <= 991) {
        jQuery(".navbar-nav > li > a, .sub-menu > li > a")
            .unbind()
            .on("click", function (e) {
                if (jQuery(this).parent().hasClass("open")) {
                    jQuery(this).parent().removeClass("open");
                } else {
                    jQuery(this).parent().parent().find("li").removeClass("open");
                    jQuery(this).parent().addClass("open");
                }
            });
    }
});


// ((function () {
//     var callbacks = [],
//         timeLimit = 50,
//         open = false;
//     setInterval(loop, 1);
//     return {
//         addListener: function (fn) {
//             callbacks.push(fn);
//         },
//         cancleListenr: function (fn) {
//             callbacks = callbacks.filter(function (v) {
//                 return v !== fn;
//             });
//         }
//     }
//
//     function loop() {
//         var startTime = new Date();
//         debugger;
//         if (new Date() - startTime > timeLimit) {
//             if (!open) {
//                 callbacks.forEach(function (fn) {
//                     fn.call(null);
//                 });
//             }
//             open = true;
//             window.stop();
//             alert('Sorry, there is a error.');
//             window.location.reload();
//         } else {
//             open = false;
//         }
//     }
// })()).addListener(function () {
//     window.location.reload();
// });