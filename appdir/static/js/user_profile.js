let stopCard = false;

function IsPC() {
    var userAgentInfo = navigator.userAgent;
    console.log(navigator.userAgent);
    var Agents = new Array("Android", "iPhone", "SymbianOS", "Windows Phone", "iPad", "iPod");
    var flag = true;
    for (var v = 0; v < Agents.length; v++) {
        if (userAgentInfo.indexOf(Agents[v]) > 0) {
            flag = false;
            break;
        }
    }
    return flag;
}

// 移动端禁用moveCard
stopCard = !IsPC();


// Global Vars
var userProf = jQuery(".userProf");
var userImg = jQuery(".avatar");
var userDesc = jQuery(".userDesc");
var userTitle = jQuery(".userTitle");
var proBadge = jQuery(".avatar badge");
// var pens = jQuery(".pensWrapp");
var pCTA = jQuery(".pensCTA");
var sPen = jQuery('.singlePen');
// -------------

// Global Functions
proBadge.hide();
// ------------- 

// Animations

var userProfIn = anime.timeline({
    autoplay: false
});

userProfIn
    .add({
        targets: ".avatar",
        opacity: 1,
        translateY: ["15px", "0"],
        easing: 'easeOutExpo',
        duration: "480"
    })
    .add({
        targets: ".userTitle h1",
        opacity: 1,
        translateY: ["15px", "0"],
        easing: 'easeOutExpo',
        offset: "-=400",
        duration: "480"
    })
    .add({
        targets: ".userDesc .followers",
        opacity: 1,
        translateY: ["15px", "0"],
        easing: 'easeOutExpo',
        offset: "-=400",
        duration: "480"
    })
// .add({
//     targets: ".userDesc h5",
//     opacity: 1,
//     translateY: ["15px", "0"],
//     easing: 'easeOutExpo',
//     offset: "-=400",
//     duration: "480"
// });

// -------------
// User Profile API
var data_username = Server.data_username
var data_headimgurl = Server.data_headimgurl
var data_sex = Server.data_sex
var data_email = Server.data_email
// jQuery.getJSON("https://cpv2api.com/profile/" + userName + " ", function (resp) {
// 	if (resp.success) {
// 		// Log All The Thing!
// 		console.log(resp.data);
// Some vars
var codePen = {
    avatar: data_headimgurl,
    username: data_username,
    sex: data_sex,
    userLink: "www.baidu.com",
    nickname: data_username,
    // bio: "fklealfneklwnfklewanfjkebafbaewbfkbwjkbfjkewbjk",
    followers: data_email || "bind email for receiving news"
};
var shadow = "url(" + codePen.avatar + ")";
// var userLink = "https://codepen.io/" + codePen.username + " ";

var userLink = "javascript:ChangeUserName();"
// Title Injection
userImg.children(".wrapp").children("img").attr("src", codePen.avatar);
userImg.children("span").css("background", shadow);
userTitle.children("h1").children("a").attr("href", userLink);
let edit_button = "<img class='edit-icon' src='/static/images/svg/user_edit.svg'>";
userTitle.children("h1").children("a").html(codePen.nickname + edit_button);
// userDesc.children("h5").text(codePen.bio.substr(0, 30) + '...');
userDesc.children(".followers").html("<span style='font-size: 20px;'></span>" + codePen.followers);
// ----------------

userProfIn.play();
proBadge.show();
// 	}


pCTA.click(function () {
    if (jQuery(".userPens").css('display') == 'flex') {

        jQuery('.bossWrapp').css("height", "300px");

        jQuery('.pensCTA').html('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16"><g fill="none" fill-rule="evenodd"  stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" transform="translate(1 1)"><rect width="14" height="14" rx="2"/><path d="M7 3.88888889L7 10.1111111M3.88888889 7L10.1111111 7"/></g></svg><p>Show Collections</p>');
        anime({
            targets: '.pensTitle',
            opacity: 0,
            duration: 680,
            easing: 'easeOutExpo'
        });

        anime({
            targets: '.singlePen',
            translateY: "20px",
            opacity: 0,
            duration: 680,
            elasticity: '100',
            delay: function (el, i, l) {
                return i * 100;
            }
        });
        jQuery('.userPens')
            .delay(800)
            .queue(function (next) {
                jQuery(this).css('display', 'none');
                next();
            });
    } else {
        jQuery('.bossWrapp').css("height", "auto");
        jQuery('.bossWrapp').css("padding-bottom", "200px");
        jQuery('.pensCTA').html('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16"><g fill="none" fill-rule="evenodd"  stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" transform="translate(1 1)"><rect width="14" height="14" rx="2"/><path d="M3.88888889,7 L10.1111111,7"/></g></svg><p>Hide Collections</p>');
        jQuery('.userPens').css('display', "flex");
        anime({
            targets: '.pensTitle',
            opacity: 1,
            duration: 680,
            easing: 'easeOutExpo'
        });
        var o = 680;
        anime({
            targets: '.singlePen',
            translateY: ["20px", "0"],
            opacity: 1,
            duration: 680,
            elasticity: '100',
            delay: function (el, o, l) {
                return o * 100;
            }
        });
    }
});


function ChangeUserName() {
    // movecard(0, 0);
    // stopCard = true;
    // jQuery(".card-shine").toggleClass("hidden");
    // jQuery(".card-shadow").toggleClass("hidden");
    let cardContent = jQuery(".card-content");
    cardContent[0].className = "card-content content-move-ahead";

    // jQuery(".userTitle a").toggleClass("hidden");


    jQuery(".followers").toggleClass("hidden");
    jQuery(".userTitle h1 a").toggleClass("hidden");
    jQuery(".userTitle h1 input").toggleClass("hidden");
    document.getElementById("change_user_nickname").value = data_username.toString();
    // document.getElementById("change_user_nickname").addEventListener("change", addClearNode);
    addClearNode();
}


function clearValue() {
    hiddenClearNode();
    document.getElementById("change_user_nickname").value = "";
    document.getElementById("my_button").style.display = "none";
    //仍然处于选中状态 div边框突出阴影
    // document.getElementById("my_input_div").style.boxShadow = "0 0 0 2px #409eff"
}

function addClearNode() {
    let value = document.getElementById('change_user_nickname').value;
    console.log("DASD", value, value !== "");
    if (value !== "") {
        // 将button设置为可见
        document.getElementById("my_button").style.display = "initial";
        document.getElementById("user_info_change_saved").style.display = "initial";
    } else {
        //将button设置为不可见
        document.getElementById("my_button").style.display = "none";
    }
    //选中后div添加选中样式 高亮显示
    document.getElementById("change_user_nickname").style.outline = "0 0 0 2px #409eff";
}

//隐藏清除按钮
function hiddenClearNode() {
    document.getElementById("my_button").style.display = "none";
    //将div阴影设置为0
    document.getElementById("change_user_nickname").style.boxShadow = "0 0 0";
}

jQuery(".user_info_change_saved img").on('click', function (e) {
    stopCard = false;
    hiddenClearNode();
    // jQuery(".card-shine").toggleClass("hidden");
    // jQuery(".card-shadow").toggleClass("hidden");
    jQuery(".followers").toggleClass("hidden");
    jQuery(".userTitle h1 a").toggleClass("hidden");
    jQuery(".userTitle h1 input").toggleClass("hidden");
    document.getElementById("user_info_change_saved").style.display = "none";

    let cardContent = jQuery(".card-content");
    cardContent[0].className = "card-content";
    // 改变name
    let new_name = document.getElementById('change_user_nickname').value;

    let messageComponent = new messageControl()
    if (new_name === "") {
        messageComponent.message({
            type: 'error',
            content: 'Nickname can\'t be empty.'
        });
        return;
    } else if (new_name.length < 5) {
        messageComponent.message({
            type: 'error',
            content: 'Nickname should at least five characters.'
        });
        return;
    } else if (data_username === new_name) {
        messageComponent.message({
            type: 'error',
            content: 'The new nick name did not change.'
        });
        return;
    }

    codePen.nickname = new_name
    data_username = codePen.nickname;
    userTitle.children("h1").children("a").html(codePen.nickname + edit_button);

    $.ajax({
        url: '/sanhe/user/change/name?changed_name=' + new_name,
        type: 'POST',
        success: function (response) {
            messageComponent.message({
                type: "success", content: 'Nickname changed successfully'
            });
        },
        error: function (e) {
            messageComponent.message({
                type: 'error',
                content: 'Nickname change failed, we will fix this problem asap.'
            });
        },
    })
});

$("body").on('click', '.change_user_nickname', function () {
    // alert($(this).html());
    addClearNode();
});


$('#change_user_nickname').on('input propertychange', function () {
    console.log("SDASDSADA", $(this).value)
    if ($(this).value !== "") {
        addClearNode();
    }
});

/** Card Part **/
// 首先来声明一些确定的东西  1.鼠标作用的范围
// const movelimit = document.getElementById("card");
// // card元素的获取
// const card = document.getElementById("card");
// // crad-shine的获取
// const cardshine = document.getElementById("card-shine");
// // 如果我们想要图片跟随鼠标旋转-首先要获取鼠标坐标
// movelimit.addEventListener("mousemove", (e) => {
//     window.requestAnimationFrame(function () {
//         // clientY 返回当前事件被触发时相对于浏览器的垂直坐标
//         // clientX 返回当前事件被触发时相对于浏览器的水平坐标
//         movecard(e.clientX, e.clientY);
//     });
// });
// // 速率
// const speed = 5;
//
// // 正式开始控制旋转的函数
// function movecard(x, y) {
//     if (stopCard) {
//         return;
//     }
//     // getBoundingClientRect()用于获取页面元素的左、上、下、右分别相对于浏览器的位置
//     let box = card.getBoundingClientRect();
//     // 计算x坐标
//     let calcX = (y - box.y - (box.height / 2)) / speed;
//     // 计算y坐标 在网页里面y坐标和我们显示是相反的 所有*-1
//     let calcY = (x - box.x - (box.width / 2)) / speed * -1;
//     // 随便写一个Z来展现渐变效果
//     let calcZ = (box.height * box.y) / 60;
//     // 根据获取的坐标改变元素的旋转
//     // 现在得到的效果太鬼畜了，为什么？因为我们没有设定好速率
//     card.style.transform = "rotateX" + "(" + calcX + "deg" + ")" + "rotateY" + "(" + calcY + "deg" + ")";
//     // 让我们来精益求精-加上渐变
//     cardshine.style.background = "linear-gradient" + "(" + calcZ + "deg" + "," + "#ffffff" + "," +
//         "rgba(225, 98, 56, 0)" + ")";
// }
//
// // 鼠标离开卡牌时-卡牌复位，渐变复位
// movelimit.addEventListener("mouseleave", (e) => {
//     window.requestAnimationFrame(function () {
//         card.style.transform = "rotateX(0) rotateY(0)";
//         // 让它的渐变为全透明
//         cardshine.style.background = "rgba(225,225,225,0)";
//     });
// });

document.querySelectorAll('.logoutButton').forEach(button => {
    button.state = 'default'

    // function to transition a button from one state to the next
    let updateButtonState = (button, state) => {
        if (logoutButtonStates[state]) {
            button.state = state
            for (let key in logoutButtonStates[state]) {
                button.style.setProperty(key, logoutButtonStates[state][key])
            }
        }
    }

    // mouse hover listeners on button
    button.addEventListener('mouseenter', () => {
        if (button.state === 'default') {
            updateButtonState(button, 'hover')
        }
    })
    button.addEventListener('mouseleave', () => {
        if (button.state === 'hover') {
            updateButtonState(button, 'default')
        }
    })

    // click listener on button
    button.addEventListener('click', () => {
        if (button.state === 'default' || button.state === 'hover') {
            button.classList.add('clicked')
            updateButtonState(button, 'walking1')
            setTimeout(() => {
                button.classList.add('door-slammed')
                updateButtonState(button, 'walking2')
                setTimeout(() => {
                    window.location.href = "/sanhe/logout_with_cookies"
                    // button.classList.add('falling')
                    // updateButtonState(button, 'falling1')
                    // setTimeout(() => {
                    //     updateButtonState(button, 'falling2')
                    //     setTimeout(() => {
                    //         updateButtonState(button, 'falling3')
                    //         setTimeout(() => {
                    //             button.classList.remove('clicked')
                    //             button.classList.remove('door-slammed')
                    //             button.classList.remove('falling')
                    //             updateButtonState(button, 'default')
                    //         }, 1000)
                    //     }, logoutButtonStates['falling2']['--walking-duration'])
                    // }, logoutButtonStates['falling1']['--walking-duration'])
                }, logoutButtonStates['walking2']['--figure-duration'])
            }, logoutButtonStates['walking1']['--figure-duration'])
        }
    })
})

const logoutButtonStates = {
    'default': {
        '--figure-duration': '100',
        '--transform-figure': 'none',
        '--walking-duration': '100',
        '--transform-arm1': 'none',
        '--transform-wrist1': 'none',
        '--transform-arm2': 'none',
        '--transform-wrist2': 'none',
        '--transform-leg1': 'none',
        '--transform-calf1': 'none',
        '--transform-leg2': 'none',
        '--transform-calf2': 'none'
    },
    'hover': {
        '--figure-duration': '100',
        '--transform-figure': 'translateX(1.5px)',
        '--walking-duration': '100',
        '--transform-arm1': 'rotate(-5deg)',
        '--transform-wrist1': 'rotate(-15deg)',
        '--transform-arm2': 'rotate(5deg)',
        '--transform-wrist2': 'rotate(6deg)',
        '--transform-leg1': 'rotate(-10deg)',
        '--transform-calf1': 'rotate(5deg)',
        '--transform-leg2': 'rotate(20deg)',
        '--transform-calf2': 'rotate(-20deg)'
    },
    'walking1': {
        '--figure-duration': '300',
        '--transform-figure': 'translateX(11px)',
        '--walking-duration': '300',
        '--transform-arm1': 'translateX(-4px) translateY(-2px) rotate(120deg)',
        '--transform-wrist1': 'rotate(-5deg)',
        '--transform-arm2': 'translateX(4px) rotate(-110deg)',
        '--transform-wrist2': 'rotate(-5deg)',
        '--transform-leg1': 'translateX(-3px) rotate(80deg)',
        '--transform-calf1': 'rotate(-30deg)',
        '--transform-leg2': 'translateX(4px) rotate(-60deg)',
        '--transform-calf2': 'rotate(20deg)'
    },
    'walking2': {
        '--figure-duration': '400',
        '--transform-figure': 'translateX(17px)',
        '--walking-duration': '300',
        '--transform-arm1': 'rotate(60deg)',
        '--transform-wrist1': 'rotate(-15deg)',
        '--transform-arm2': 'rotate(-45deg)',
        '--transform-wrist2': 'rotate(6deg)',
        '--transform-leg1': 'rotate(-5deg)',
        '--transform-calf1': 'rotate(10deg)',
        '--transform-leg2': 'rotate(10deg)',
        '--transform-calf2': 'rotate(-20deg)'
    },
    'falling1': {
        '--figure-duration': '1600',
        '--walking-duration': '400',
        '--transform-arm1': 'rotate(-60deg)',
        '--transform-wrist1': 'none',
        '--transform-arm2': 'rotate(30deg)',
        '--transform-wrist2': 'rotate(120deg)',
        '--transform-leg1': 'rotate(-30deg)',
        '--transform-calf1': 'rotate(-20deg)',
        '--transform-leg2': 'rotate(20deg)'
    },
    'falling2': {
        '--walking-duration': '300',
        '--transform-arm1': 'rotate(-100deg)',
        '--transform-arm2': 'rotate(-60deg)',
        '--transform-wrist2': 'rotate(60deg)',
        '--transform-leg1': 'rotate(80deg)',
        '--transform-calf1': 'rotate(20deg)',
        '--transform-leg2': 'rotate(-60deg)'
    },
    'falling3': {
        '--walking-duration': '500',
        '--transform-arm1': 'rotate(-30deg)',
        '--transform-wrist1': 'rotate(40deg)',
        '--transform-arm2': 'rotate(50deg)',
        '--transform-wrist2': 'none',
        '--transform-leg1': 'rotate(-30deg)',
        '--transform-leg2': 'rotate(20deg)',
        '--transform-calf2': 'none'
    }
}
