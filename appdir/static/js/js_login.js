!function (a, b, c) {
    function d(a) {
        var c = "default";
        a.self_redirect === !0 ? c = "true" : a.self_redirect === !1 && (c = "false");
        var d = b.createElement("iframe"),
            e = "https://open.weixin.qq.com/connect/qrconnect?appid=" + a.appid + "&lang=" + a.lang + "&scope=" + a.scope + "&redirect_uri=" + a.redirect_uri + "&state=" + a.state + "&login_type=jssdk&self_redirect=" + c + '&styletype=' + (a.styletype || '') + '&sizetype=' + (a.sizetype || '') + '&bgcolor=' + (a.bgcolor || '') + '&rst=' + (a.rst || '');
        e += a.style ? "&style=" + a.style : "", e += a.href ? "&href=" + a.href : "", d.src = e, d.frameBorder = "0", d.allowTransparency = "true", d.scrolling = "no", d.width = "300px", d.height = "400px";
        var f = b.getElementById(a.id);
        f.innerHTML = "", f.appendChild(d)
    }

    a.WxLogin = d
}(window, document);


jQuery(".weixin-signin").click(function () {
    jQuery(".a-container .weixin-window").toggleClass("hidden")
    jQuery(".a-container form").toggleClass("hidden")
});

jQuery(".weixin-signup").click(function () {
    jQuery(".b-container .weixin-window").toggleClass("hidden")
    jQuery(".b-container form").toggleClass("hidden")
});

jQuery(".b-container .weixin-window-close").click(function () {
    jQuery(".b-container .weixin-window").toggleClass("hidden")
    jQuery(".b-container form").toggleClass("hidden")
});

jQuery(".a-container .weixin-window-close").click(function () {
    jQuery(".a-container .weixin-window").toggleClass("hidden")
    jQuery(".a-container form").toggleClass("hidden")
});

var obj_signin = new WxLogin({
    lang: "en",
    self_redirect: true,
    id: "weixin-signin-qrcode",
    appid: "wx76aab163c8731d27",
    scope: "snsapi_login",
    // redirect_uri: "http://global.sanhejxzz.com",
    redirect_uri: "http://ipa-020.ucd.ie/sanhe/auth/weixin_signin",
    state: "",
    style: "",
    href: "https://global.sanhejxzz.com/static/css/wechat_custom.css"
});

var obj_signup = new WxLogin({
    lang: "en",
    self_redirect: true,
    id: "weixin-signup-qrcode",
    appid: "wx76aab163c8731d27",
    scope: "snsapi_login",
    redirect_uri: "http://ipa-020.ucd.ie/sanhe/auth/weixin_signin",
    state: "",
    style: "",
    href: "https://global.sanhejxzz.com/static/css/wechat_custom.css"
});


jQuery(".form_link").click(function () {
    let fg_window = jQuery(".forget-pw-window");
    fg_window.toggleClass("hidden");
    // jQuery(".ps-login-way").toggleClass("hidden");
    if (fg_window[0].classList.contains("hidden")) {
        this.style.color = "#181818";
    } else {
        this.style.color = "#bf3030";
    }
});