var SanHe = (function () {

    var headerFix = function () {
        jQuery(window).bind("scroll", function () {
            if (jQuery(".sticky-header").length) {
                var menu = jQuery(".sticky-header");
                if ($(window).scrollTop() > menu.offset().top) {
                    menu.addClass("is-fixed");
                } else {
                    menu.removeClass("is-fixed");
                }
            }
        });
    };

    var handleBannerResize = function () {
        $(".full-height").css("height", $(window).height());
    };

    var handleCustomScroll = function () {
        // if ($(".content-scroll").length > 0) {
        //     $(".content-scroll").mCustomScrollbar({
        //         setWidth: false,
        //         setHeight: false,
        //         axis: "y",
        //     });
        // }
    };

    var wow_animation = function () {
        if (jQuery(".wow").length > 0) {
            var wow = new WOW({
                boxClass: "wow",
                animateClass: "animated",
                offset: 50,
                mobile: false,
            });
            wow.init();
        }
    };

    return {
        init: function () {
            wow_animation();
            headerFix();
            handleCustomScroll();
            handleBannerResize();
        },
        // load: function () {
        //     handleCustomScroll();
        // },

        resize: function () {
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
        },
    };
})();

jQuery(window).on("resize", function () {
    "use strict";
    SanHe.resize();
});


function smoothscroll() {
    const currentScroll = document.documentElement.scrollTop || document.body.scrollTop; // 已经被卷掉的高度
    const clientHeight = document.documentElement.clientHeight; // 浏览器高度
    const scrollHeight = document.documentElement.scrollHeight; // 总高度
    if (scrollHeight - 10 > currentScroll + clientHeight) {
        window.requestAnimationFrame(smoothscroll);
        window.scrollTo(0, currentScroll + (scrollHeight - currentScroll - clientHeight) / 2);
    }
}


console.log("e.key");
console.log("e.key");
console.log("e.key");

document.addEventListener('keyup', (e) => {
    console.log(e);
})
document.addEventListener('keydown', (e) => {
    console.log(e);
})
document.addEventListener('keypress', (e) => {
    console.log(e);
})

// document.addEventListener("keydown", function (e) {
//     if (e.key == e.ctrlKey) {
//         console.log(e.key);
//         console.log('scrollToBottom');
//     }
//     if (e.key == "Enter") {
//         console.log(e.key);
//         console.log('scrollToBottom');
//         console.log('scrollToBottom');
//         console.log('scrollToBottom');
//         console.log('scrollToBottom');
//     }
// })

function openChat() {
    $("#chatbot-sanhe").css("height", 700).css("width", 410);
}

function closeChat() {
    $("#chatbot-sanhe").css("height", 250).css("width", 100);
}