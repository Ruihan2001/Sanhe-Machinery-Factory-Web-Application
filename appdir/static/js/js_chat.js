var chat_wrapper = $('.chat');
var chat_close = $(".app-close");
var chat_open = $(".app-open");

let conversation = $('.conversation');
let user_input = $('.typing input');
let chat_querying = $(".chat-querying");

// email, requirement
let flag_contact_me_mode = false;
let flag_contact_me_process = "email";
let user_contact_me_requirement = "*****"
let user_contact_me_email = "***@**.**"

function switchStatus() {
    chat_close.toggleClass("hidden");
    chat_open.toggleClass("hidden");
}

$(".trigger-profile").click(function () {
    window.parent.location.href = '/sanhe/user/profile/' + Server.userid;
});

$(".trigger-login").click(function () {
    window.parent.location.href = '/sanhe/auth/login';
});

$(".trigger-chat-open").click(function () {
    parent.openChat();
    switchStatus()
});

$(".trigger-chat-close").click(function () {
    parent.closeChat();
    switchStatus();
});

let products = [{
    name: "Log Frame Saw Machine",
    description: "designed to fit the log processing",
    image: "/static/images/blog_img/log1.jpg"
}, {
    name: "Square Frame Saw Machine",
    description: "suitable for square material processing",
    image: "/static/images/blog_img/squared1.jpg"
}, {
    name: "Automatic Production Line",
    description: "provide long-lasting high precision and the best surface quality of the material",
    image: "/static/images/blog_img/flow0.png"
}, {
    name: "Tea Twisting Machine",
    description: "for tea rolling and processing operations",
    image: "/static/images/blog_img/rounian2.png"
}]

let services = [{
    title: "",
    description: ""
}]

let robotHeader = "<div data-type=\"CAPTION\" data-bot=\"true\" class=\"message\">\n" +
    "                        <div class=\"caption\">\n" +
    "                            <div class=\"avatar\">\n" +
    "                                <div data-status=\"loaded\" data-cover=\"true\" class=\"lazy-img\"><img src=\"/static/images/icon/chat.png\" alt=\"ChatBot\" class=\"lazy-img-loaded\">\n" +
    "                                </div>\n" +
    "                            </div>\n" +
    "                            <span style=\"color: rgb(24, 25, 25);\">\n" +
    "                                SanHe\n" +
    "                            </span>\n" +
    "                        </div>\n" +
    "                    </div>"

let chat_querying_content = "<div data-type=\"CAPTION\" data-bot=\"true\" class=\"message chat-querying\">\n" +
    "                        <div class=\"caption\">\n" +
    "                            <div class=\"avatar\">\n" +
    "                                <div data-status=\"loaded\" data-cover=\"true\" class=\"lazy-img\"><img\n" +
    "                                        src=\"/static/images/icon/chat.png\" alt=\"ChatBot\" class=\"lazy-img-loaded\">\n" +
    "                                </div>\n" +
    "                            </div>\n" +
    "                            <span style=\"color: rgb(24, 25, 25);\">\n" +
    "                                SanHe\n" +
    "                            </span>\n" +
    "                        </div>\n" +
    "                    </div>" +
    "                    <div data-type=\"BOT_RESPONSE_text\" data-bot=\"true\" class=\"message chat-querying\">\n" +
    "                        <div data-first=\"true\" class=\"indicator\" style=\"background: rgb(255, 255, 255);\">\n" +
    "                            <div class=\"dot\" style=\"background: rgb(94, 94, 94);\"></div>\n" +
    "                            <div class=\"dot\" style=\"background: rgb(94, 94, 94);\"></div>\n" +
    "                            <div class=\"dot\" style=\"background: rgb(94, 94, 94);\"></div>\n" +
    "                        </div>\n" +
    "                    </div>"

/** Start Quick Replies **/
let specificationsQuickReplies3 = "<div data-type=\"BOT_RESPONSE_text\" data-bot=\"true\" class=\"message\">\n" +
    "    <div class=\"anchors bot-response text\" data-first=\"true\"\n" +
    "         style=\"background: rgb(255, 255, 255); color: rgb(0, 0, 0);\">\n" +
    "        Specifications you may need 🤔👇<br>" +
    "        -> suitable type of wood<br>" +
    "        -> suitable wood length<br>" +
    "        -> suitable wood width<br>" +
    "        -> suitable wood height<br>" +
    "        -> min processing diameter<br>" +
    "        -> max processing diameter<br>" +
    "        -> saw stroke<br>" +
    "        -> saw blade length<br>" +
    "        -> saw blade type<br>" +
    "        -> saw blade sawpath<br>" +
    "        -> feeding speed<br>" +
    "        -> machine weight<br>" +
    "        -> machine dimension<br>" +
    "        -> machine power<br>" +
    "    </div>\n" +
    "</div>"
let specificationsQuickReplies4 = "<div data-type=\"BOT_RESPONSE_text\" data-bot=\"true\" class=\"message\">\n" +
    "    <div class=\"anchors bot-response text\"\n" +
    "         style=\"background: rgb(255, 255, 255); color: rgb(0, 0, 0);\" data-middle=\"true\">\n" +
    "        Products I can provide infos now ☺️👇<br>" +
    "        -> log frame saw 3030<br>" +
    "        -> log frame saw 3535<br>" +
    "        -> square frame saw 2040<br>" +
    "        -> square frame saw 2050<br>" +
    "    </div>\n" +
    "</div>"
let specificationsQuickReplies1 = "<div data-type=\"BOT_RESPONSE_text\" data-bot=\"true\" class=\"message\">\n" +
    "    <div class=\"anchors bot-response text\"\n" +
    "         style=\"background: rgb(255, 255, 255); color: rgb(0, 0, 0);\" data-middle=\"true\">\n" +
    "        If you need information for specific product, please ask me like this:" +
    "         <br>(specification) for (product)\n" +
    "    </div>\n" +
    "</div>"
let specificationsQuickReplies2 = "<div data-type=\"BOT_RESPONSE_text\" data-bot=\"true\" class=\"message\">\n" +
    "    <div class=\"anchors bot-response text\" data-last=\"true\"\n" +
    "         style=\"background: rgb(255, 255, 255); color: rgb(0, 0, 0);\">\n" +
    "        Or just tell me the specification you would like to know 😉\n" +
    "    </div>\n" +
    "</div>"
let companyQuickReplies1 = "\n" +
    "<div data-type=\"BOT_RESPONSE_text\" data-bot=\"true\" class=\"message\">\n" +
    "    <div class=\"anchors bot-response text\" data-first=\"true\"\n" +
    "         style=\"background: rgb(255, 255, 255); color: rgb(0, 0, 0);\">\n" +
    "        Fujian Jianyang Sanhe Machinery is a professional manufacturer of machinery and equipment for the woodworking\n" +
    "        industry.\n" +
    "    </div>\n" +
    "</div>"
let companyQuickReplies2 = "<div data-type=\"BOT_RESPONSE_text\" data-bot=\"true\" class=\"message\">\n" +
    "    <div class=\"anchors bot-response text\" \n" +
    "         style=\"background: rgb(255, 255, 255); color: rgb(0, 0, 0);\">\n" +
    "        The company's leading products: log/square cutting frame sawing machine, heavy\n" +
    "        duty cutting frame sawing automatic production line.\n" +
    "    </div>\n" +
    "</div>"
let companyQuickReplies3 = "<div data-type=\"BOT_RESPONSE_text\" data-bot=\"true\" class=\"message\">\n" +
    "    <div class=\"anchors bot-response text\" data-last=\"true\"\n" +
    "         style=\"background: rgb(255, 255, 255); color: rgb(0, 0, 0);\">\n" +
    "        \As your reliable partner, Sanhe Machinery will provide you with high quality products and perfect after-sales\n" +
    "        service as always.\n" +
    "    </div>\n" +
    "</div>\n"
let startQuickReplies = "<div data-type=\"BOT_RESPONSE_quickReplies\" data-bot=\"true\" class=\"message\">\n" +
    "                        <div class=\"bot-response quick-replies\">\n" +
    "                            <div class=\"anchors quick-replies-text\" data-last=\"true\" style=\"background: rgb(255, 255, 255); color: rgb(0, 0, 0);\">\n" +
    "                                What information are you looking for? <br> Input or Select on from above 👇\n" +
    "                            </div>\n" +
    "                            <div class=\"quick-replies-buttons\">\n" +
    "                                <div data-conversation-quick-reply-title=\"📦Products\"\n" +
    "                                     class=\"single-button quick-query-products\"\n" +
    "                                     style=\"border-color: rgb(255 97 62 / 72%); color: rgb(255 97 62 / 72%); background: rgb(255, 255, 255);\">\n" +
    "                                    <span>📦 Products</span>\n" +
    "                                </div>\n" +
    "                                <div data-conversation-quick-reply-title=\"⚙️Specifications\"\n" +
    "                                     class=\"single-button quick-query-specifications\"\n" +
    "                                     style=\"border-color: rgb(255 97 62 / 72%); color: rgb(255 97 62 / 72%); background: rgb(255, 255, 255);\">\n" +
    "                                    <span>⚙️ Specifications</span>\n" +
    "                                </div>\n" +
    "                                <div data-conversation-quick-reply-title=\"💡About ChatBot\"\n" +
    "                                     class=\"single-button quick-query-company\"\n" +
    "                                     style=\"border-color: rgb(255 97 62 / 72%); color: rgb(255 97 62 / 72%); background: rgb(255, 255, 255);\">\n" +
    "                                    <span>💡 About SanHe</span>\n" +
    "                                </div>\n" +
    "                                <div data-conversation-quick-reply-title=\"📩️Inquiry Request\"\n" +
    "                                     class=\"single-button quick-query-inquiry\"\n" +
    "                                     style=\"border-color: rgb(255 97 62 / 72%); color: rgb(255 97 62 / 72%); background: rgb(255, 255, 255);\">\n" +
    "                                    <span>📩️ Inquiry</span>\n" +
    "                                </div>\n" +
    "                            </div>" +
    "                        </div>\n" +
    "                    </div>\n" +
    "                </div>"


let normalQuickReplies = "<div data-type=\"BOT_RESPONSE_quickReplies\" data-bot=\"true\" class=\"message\">\n" +
    "    <div class=\"bot-response quick-replies\">\n" +
    "        <div class=\"anchors quick-replies-text\" data-last=\"true\"\n" +
    "             style=\"background: rgb(255, 255, 255); color: rgb(0, 0, 0);\">What would you like to do next?\n" +
    "        </div>\n" +
    "        <div class=\"quick-replies-buttons\">\n" +
    "            <div data-conversation-quick-reply-title=\"👈 Back to menu\" class=\"single-button quick-query-back\"\n" +
    "                 style=\"border-color: rgb(255 97 62 / 72%); color: rgb(255 97 62 / 72%); background: rgb(255, 255, 255);\"><span>👈 Back to menu</span>\n" +
    "            </div>\n" +
    "            <div data-conversation-quick-reply-title=\"❌ Close chat\" class=\"single-button quick-query-close\"\n" +
    "               style=\"border-color: rgb(255 97 62 / 72%); color: rgb(255 97 62 / 72%); background: rgb(255, 255, 255);\"><span>❌ Close chat</span>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "    </div>\n" +
    "</div>"


let contactMeContentCheck = "<div data-type=\"BOT_RESPONSE_quickReplies\" data-bot=\"true\" class=\"message\">\n" +
    "        <div class=\"bot-response quick-replies\">\n" +
    "            <div class=\"anchors quick-replies-text\" data-last=\"true\" style=\"background: rgb(255, 255, 255); color: rgb(0, 0, 0);\">\n" +
    "                Is everything OK? <br>\n" +
    "            </div>\n" +
    "            <div class=\"quick-replies-buttons\">\n" +
    "                <div data-conversation-quick-reply-title=\"✅ Yes\" class=\"single-button quick-query-contact-yes\" style=\"border-color: rgb(255 97 62 / 72%); color: rgb(255 97 62 / 72%); background: rgb(255, 255, 255);\">\n" +
    "                    <span>✅ Yes</span></div>\n" +
    "                <div data-conversation-quick-reply-title=\"↩️ No, try again\" class=\"single-button quick-query-contact-no\" style=\"border-color: rgb(255 97 62 / 72%); color: rgb(255 97 62 / 72%); background: rgb(255, 255, 255);\">\n" +
    "                    <span>↩️ No, try again</span></div>\n" +
    "                 <div data-conversation-quick-reply-title=\"👈 Back to menu\" class=\"single-button quick-query-back\" style=\"border-color: rgb(255 97 62 / 72%); color: rgb(255 97 62 / 72%); background: rgb(255, 255, 255);\">\n" +
    "                    <span>👈 Back to menu</span></div>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "    </div>\n" +
    "</div>"

let contactMeContentStartConfirmButtons = "<div data-type=\"BOT_RESPONSE_quickReplies\" data-bot=\"true\" class=\"message\">\n" +
    "        <div class=\"bot-response quick-replies\">\n" +
    "            <div class=\"quick-replies-buttons\">\n" +
    "                <div data-conversation-quick-reply-title=\"✅ Yes\" class=\"single-button quick-query-contact-start-yes\" style=\"border-color: rgb(255 97 62 / 72%); color: rgb(255 97 62 / 72%); background: rgb(255, 255, 255);\">\n" +
    "                    <span>✅ Yes</span></div>\n" +
    "                <div data-conversation-quick-reply-title=\"❌ No, back to menu\" class=\"single-button quick-query-contact-start-no\" style=\"border-color: rgb(255 97 62 / 72%); color: rgb(255 97 62 / 72%); background: rgb(255, 255, 255);\">\n" +
    "                    <span>❌ No, back to menu</span></div>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "    </div>\n" +
    "</div>"


/** Start END Reply **/
let startAgain = "<div class=\"start-again\" style=\"background: rgb(234, 238, 243);\">" +
    "       <div class=\"button start-again-button\" style=\"background: rgb(255 97 62); color: rgb(255, 255, 255);\">\n" +
    "        Start Conversation Again :>\n" +
    "    </div></div>"


let startContent = "<div class=\"conversation\" style=\"background: rgb(234, 238, 243);\">\n" +
    "                    <div data-type=\"CAPTION\" data-bot=\"true\" class=\"message\">\n" +
    "                        <div class=\"caption\">\n" +
    "                            <div class=\"avatar\">\n" +
    "                                <div data-status=\"loaded\" data-cover=\"true\" class=\"lazy-img\"><img src=\"/static/images/icon/chat.png\" alt=\"ChatBot\" class=\"lazy-img-loaded\">\n" +
    "                                </div>\n" +
    "                            </div>\n" +
    "                            <span style=\"color: rgb(24, 25, 25);\">\n" +
    "                                SanHe\n" +
    "                            </span>\n" +
    "                        </div>\n" +
    "                    </div>\n" +
    "                    <div data-type=\"BOT_RESPONSE_text\" data-bot=\"true\" class=\"message\">\n" +
    "                        <div class=\"anchors bot-response text\" data-first=\"true\" style=\"background: rgb(255, 255, 255); color: rgb(0, 0, 0);\">\n" +
    "                            Hi, it's great to see you! 👋\n" +
    "                        </div>\n" +
    "                    </div>\n" +
    startQuickReplies +
    "                </div>"

let endChatContent = robotHeader + "<div data-type=\"BOT_RESPONSE_text\" data-bot=\"true\" class=\"message\">\n" +
    "    <div class=\"anchors bot-response text\" data-first=\"true\"\n" +
    "         style=\"background: rgb(255, 255, 255); color: rgb(0, 0, 0);\">👋 It was great talking with you. Goodbye!\n" +
    "    </div>\n" +
    "</div>"

let inputArea = "<div class=\"typing\" style=\"background: rgb(255, 255, 255); border-top-color: rgb(234, 234, 234);\">\n" +
    "                    <input type=\"text\" maxlength=\"256\" placeholder=\"Do you have any question?\" style=\"color: rgb(150, 155, 166);\">\n" +
    "                    <div class=\"send-icon\">\n" +
    "                        <svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 24 24\" xml:space=\"preserve\"><path fill=\"#d7d7d7\" d=\"M22,11.7V12h-0.1c-0.1,1-17.7,9.5-18.8,9.1c-1.1-0.4,2.4-6.7,3-7.5C6.8,12.9,17.1,12,17.1,12H17c0,0,0-0.2,0-0.2c0,0,0,0,0,0c0-0.4-10.2-1-10.8-1.7c-0.6-0.7-4-7.1-3-7.5C4.3,2.1,22,10.5,22,11.7z\"></path></svg>\n" +
    "                    </div>\n" +
    "                </div>"


/** Contact Me Content **/
let contactMeContent_confirm = "<div data-type=\"BOT_RESPONSE_text\" data-bot=\"true\" class=\"message\">\n" +
    "    <div class=\"anchors bot-response text\" data-last=\"true\"\n" +
    "         style=\"background: rgb(255, 255, 255); color: rgb(0, 0, 0);\">Do you need our staff contact with you? 😊\n" +
    "    </div>\n" +
    "</div>\n" + contactMeContentStartConfirmButtons;

let contactMeContent_Understand = robotHeader + "<div data-type=\"BOT_RESPONSE_text\" data-bot=\"true\" class=\"message\">\n" +
    "    <div class=\"anchors bot-response text\" data-first=\"true\"\n" +
    "         style=\"background: rgb(255, 255, 255); color: rgb(0, 0, 0);\">Understood! 😊\n" +
    "    </div>\n" +
    "</div>\n" +
    "<div data-type=\"BOT_RESPONSE_text\" data-bot=\"true\" class=\"message\">\n" +
    "    <div class=\"anchors bot-response text\" style=\"background: rgb(255, 255, 255); color: rgb(0, 0, 0);\"\n" +
    "         data-middle=\"true\">First of all, I need your usual email address to get in touch with you.\n" +
    "    </div>\n" +
    "</div>\n" +
    "<div data-type=\"BOT_RESPONSE_text\" data-bot=\"true\" class=\"message\">\n" +
    "    <div class=\"anchors bot-response text\" data-last=\"true\"\n" +
    "         style=\"background: rgb(255, 255, 255); color: rgb(0, 0, 0);\">What's your email address?\n" +
    "    </div>\n" +
    "</div>"


let contactMeContent_Error_Email = robotHeader + "<div data-type=\"BOT_RESPONSE_text\" data-bot=\"true\" class=\"message\">\n" +
    "    <div class=\"anchors bot-response text\" data-first=\"true\"\n" +
    "         style=\"background: rgb(255, 255, 255); color: rgb(0, 0, 0);\">Oops, it doesn't look like a valid email. Please\n" +
    "        recheck it.\n" +
    "    </div>\n" +
    "</div>"


let contactMeContent_Requirement = robotHeader + "<div data-type=\"BOT_RESPONSE_text\" data-bot=\"true\" class=\"message\">\n" +
    "    <div class=\"anchors bot-response text\" data-first=\"true\"\n" +
    "         style=\"background: rgb(255, 255, 255); color: rgb(0, 0, 0);\">\n" +
    "        Great, thank you! <br>\n" +
    "        Could you describe your requirements briefly?<br>\n" +
    "        1. Types of wood used<br>\n" +
    "        2. Length of wood used<br>\n" +
    "        3. Height of wood used<br>\n" +
    "        4. Width of wood used<br>\n" +
    "        5. Required plate thickness<br>\n" +
    "        ❗️ Please, don't hit enter if your message isn't complete.\n" +
    "    </div>\n" +
    "</div>"

let contactMeContent_Requirement_Error = robotHeader + "<div data-type=\"BOT_RESPONSE_text\" data-bot=\"true\" class=\"message\">\n" +
    "    <div class=\"anchors bot-response text\" data-first=\"true\"\n" +
    "         style=\"background: rgb(255, 255, 255); color: rgb(0, 0, 0);\">\n" +
    "        Sorry, I can't understand your input.<br> Please kindly describe the above points, so that I can let the personnel better help you\n" +
    "    </div>\n" +
    "</div>"

function getContactMeSummary() {
    return robotHeader + "<div data-type=\"BOT_RESPONSE_text\" data-bot=\"true\" class=\"message\">\n" +
        "    <div class=\"anchors bot-response text\" data-first=\"true\" style=\"background: rgb(255, 255, 255); color: rgb(0, 0, 0);\"\n" +
        "         data-middle=\"true\">Let's sum everything up ✍️\n" +
        "    </div>\n" +
        "</div>\n" +
        "<div data-type=\"BOT_RESPONSE_text\" data-bot=\"true\" class=\"message\">\n" +
        "    <div class=\"anchors bot-response text\" style=\"background: rgb(255, 255, 255); color: rgb(0, 0, 0);\"\n" +
        "         data-middle=\"true\">📝 Here's your requirement:\n" + user_contact_me_requirement +
        "    </div>\n" +
        "</div>\n" +
        "<div data-type=\"BOT_RESPONSE_text\" data-bot=\"true\" class=\"message\">\n" +
        "    <div class=\"anchors bot-response text\" style=\"background: rgb(255, 255, 255); color: rgb(0, 0, 0);\"\n" +
        "         data-middle=\"true\">✉️ We'll reach back to you at:\n" + user_contact_me_email +
        "    </div>\n" +
        "</div>"
}


let contactMeContent_SUCCESS = robotHeader + "<div data-type=\"BOT_RESPONSE_image\" data-bot=\"true\" class=\"message\">\n" +
    "    <div data-loaded=\"true\" class=\"bot-response image\">\n" +
    "        <div data-status=\"loaded\" data-cover=\"false\" class=\"lazy-img\">\n" +
    "            <img style=\"height: 200px;\" src=\"/static/images/svg/email_send.svg\" alt=\"email sent\" class=\"lazy-img-loaded\">\n" +
    "        </div>\n" +
    "    </div>\n" +
    "</div>\n" +
    "<div data-type=\"BOT_RESPONSE_text\" data-bot=\"true\" class=\"message\">\n" +
    "    <div class=\"anchors bot-response text\" style=\"background: rgb(255, 255, 255); color: rgb(0, 0, 0);\"\n" +
    "         data-middle=\"true\">I have informed the staff, they will contact you as soon as possible, please pay attention\n" +
    "        to the email 📮\n" +
    "    </div>\n" +
    "</div>"

function creatImageReply() {
    return "<div data-type=\"BOT_RESPONSE_image\" data-bot=\"true\" className=\"message\">\n" +
        "    <div data-loaded=\"true\" className=\"bot-response image\">\n" +
        "        <div data-status=\"loaded\" data-cover=\"false\" className=\"lazy-img\"><!----> <img\n" +
        "            src=\"https://cdn.chatbot.com/attachments/61f28451fdd7c5000728b4f6/GvYEn0QMm8_xLFjS.png\"\n" +
        "            alt=\"\" className=\"lazy-img-loaded\"></div>\n" +
        "    </div>\n" +
        "</div>"
}


function creatImageCardsReply() {
    let imageContentHtml = "";
    for (let product of products) {
        let html = "<div class=\"card-wrapper\">\n" +
            "   <div class=\"card\"\n" +
            "        style=\"border-color: rgb(219, 225, 232); background: rgb(255, 255, 255);\">\n" +
            "       <div class=\"card-image\">\n" +
            "           <div data-status=\"loaded\" data-cover=\"true\" class=\"lazy-img\">\n" +
            "               <img src=\"" + product.image + "\"\n" +
            "                    alt=\"\" class=\"lazy-img-loaded\"></div>\n" +
            "       </div>\n" +
            "       <div class=\"card-content\">\n" +
            "           <div class=\"anchors card-title\" style=\"color: rgb(0, 0, 0);\">\n" +
            product.name + "\n" +
            "           </div>\n" +
            "               <div class=\"anchors card-description\" style=\"color: rgb(0, 0, 0);\">\n" +
            product.description + "\n" +
            "               </div>\n" +
            "       </div>\n" +
            "       <div class=\"buttons\">\n" +
            "              <div data-conversation-button-tittle=\"🌐 Visit Product Page\"\n" +
            "                   class=\"single-button\"\n" +
            "                   style=\"background: rgb(255, 255, 255); border-top-color: rgb(219, 225, 232);\">\n" +
            "                  <div class=\"single-button-text\" style=\"color: rgb(0, 102, 255);\">\n" +
            "                      🌐 Visit Product Page\n" +
            "                  </div>\n" +
            "              </div>\n" +
            "          </div>\n" +
            "      </div>\n" +
            "  </div>\n"
        imageContentHtml = imageContentHtml + html;
    }

    return robotHeader + " <div data-type=\"BOT_RESPONSE_cards\" data-bot=\"true\" class=\"message\">\n" +
        "                        <div class=\"bot-response cards\">\n" +
        "                            <div class=\"cards-scroll cards-image-text owl-carousel\">\n" +
        imageContentHtml +
        "                            </div>\n" +
        "                        </div>\n" +
        "                    </div>"
}

function creatTextCardsReply() {
    return ""
}


function creatQueryHtml(input) {
    // new DOMParser().parseFromString(queryHtml, 'text/html');
    return " <div data-type=\"CAPTION\" data-user=\"true\" class=\"message\">\n" +
        "                        <div class=\"caption\">\n" +
        "                            <span style=\"color: rgb(24, 25, 25);\">\n" +
        "                                you\n" +
        "                            </span>\n" +
        "                        </div>\n" +
        "                    </div>\n" +
        "                    <div data-type=\"INPUT_MESSAGE\" data-user=\"true\" class=\"message\">\n" +
        "                        <div class=\"input-wrapper\">\n" +
        "                            <div class=\"anchors input-wrapper-text\" data-first=\"true\"\n" +
        "                                 style=\"background: rgb(255 97 62 / 72%); color: rgb(255, 255, 255);\">" +
        input + "\n" +
        "                            </div>\n" +
        "                        </div>\n" +
        "                    </div>";
}

function createReplyHtml(input) {
    return "                    <div data-type=\"CAPTION\" data-bot=\"true\" class=\"message\">\n" +
        "                        <div class=\"caption\">\n" +
        "                            <div class=\"avatar\">\n" +
        "                                <div data-status=\"loaded\" data-cover=\"true\" class=\"lazy-img\"><img\n" +
        "                                        src=\"/static/images/icon/chat.png\" alt=\"ChatBot\" class=\"lazy-img-loaded\">\n" +
        "                                </div>\n" +
        "                            </div>\n" +
        "                            <span style=\"color: rgb(24, 25, 25);\">\n" +
        "                                SanHe\n" +
        "                            </span>\n" +
        "                        </div>\n" +
        "                    </div>" +
        "                    <div data-type=\"BOT_RESPONSE_text\" data-bot=\"true\" class=\"message\">\n" +
        "                        <div class=\"anchors bot-response text\" data-first=\"true\"\n" +
        "                             style=\"background: rgb(255, 255, 255); color: rgb(0, 0, 0);\">\n" +
        input + "\n" +
        "                        </div>\n" +
        "                    </div>"
}

function chatScrollToBottom(html) {
    conversation = $('.conversation');
    conversation.append(html);
    conversation.scrollTop(conversation[0].scrollHeight);
}

// 提前设置的回答
function queryHandle(text) {
    conversation = $('.conversation');
    if ("all products".indexOf(text) !== -1) {
        conversation.append(chat_querying_content);
        conversation.scrollTop(conversation[0].scrollHeight);
        let replyHtml = creatImageCardsReply();
        setTimeout(function () {
            conversation.children('.chat-querying').each(function () {
                $(this).addClass('hidden')
            });
            conversation.append((replyHtml));
            conversation.scrollTop(conversation[0].scrollHeight);
            jQuery('.cards-image-text').owlCarousel({
                autoWidth: true,
                loop: true,
                autoplay: 3000,
                nav: true,
                dots: false,
                navText: ['<div class="navigation"><div data-direction="prev" class="arrow" style="background: rgb(255, 255, 255);"><svg width="8" height="12" viewBox="0 0 8 12" xmlns="http://www.w3.org/2000/svg"><path fill="#0066FF" d="M8 1.41L3.05533 6L8 10.59L6.47773 12L0 6L6.47773 0L8 1.41Z"></path></svg></div></div>',
                    '<div class="navigation"><div data-direction="next" class="arrow" style="background: rgb(255, 255, 255);"><svg width="8" height="12" viewBox="0 0 8 12" xmlns="http://www.w3.org/2000/svg"><path fill="#0066FF" d="M0 10.59L4.94467 6L0 1.41L1.52227 0L8 6L1.52227 12L0 10.59Z"></path></svg></div></div>'],
                items: 1,
            })
            throwNextQuickReply();
        }, 500)
        return true;
    } else if ("close chat".indexOf(text) !== -1) {
        conversation.append(chat_querying_content);
        conversation.scrollTop(conversation[0].scrollHeight);
        let replyHtml = endChatContent;
        $('.quick-replies-buttons').remove();
        setTimeout(function () {
            conversation.children('.chat-querying').each(function () {
                $(this).addClass('hidden')
            });
            conversation.append((replyHtml));
            conversation.scrollTop(conversation[0].scrollHeight);
            $('.typing').replaceWith(startAgain);
        }, 500)
        return true;
    } else if ("contact me".indexOf(text) !== -1) {
        // start mode detect user information
        flag_contact_me_mode = true;
        conversation.append(chat_querying_content);
        conversation.scrollTop(conversation[0].scrollHeight);
        let replyHtml = contactMeContent_Understand;
        $('.quick-replies-buttons').remove();
        setTimeout(function () {
            conversation.children('.chat-querying').each(function () {
                $(this).addClass('hidden')
            });
            conversation.append((replyHtml));
            conversation.scrollTop(conversation[0].scrollHeight);
        }, 500)
        return true;
    } else if ("company profile".indexOf(text) !== -1) {
        conversation.append(chat_querying_content);
        conversation.scrollTop(conversation[0].scrollHeight);
        let replyHtml = robotHeader + companyQuickReplies1;
        setTimeout(function () {
            conversation.children('.chat-querying').each(function () {
                $(this).addClass('hidden')
            });
            conversation.append(replyHtml);
            conversation.scrollTop(conversation[0].scrollHeight);

            conversation.append(chat_querying_content);
            conversation.scrollTop(conversation[0].scrollHeight);
            setTimeout(function () {
                conversation.children('.chat-querying').each(function () {
                    $(this).addClass('hidden')
                });
                conversation.append(companyQuickReplies2);
                conversation.scrollTop(conversation[0].scrollHeight);

                conversation.append(chat_querying_content);
                conversation.scrollTop(conversation[0].scrollHeight);
                setTimeout(function () {
                    conversation.children('.chat-querying').each(function () {
                        $(this).addClass('hidden')
                    });
                    conversation.append(companyQuickReplies3);
                    conversation.scrollTop(conversation[0].scrollHeight);
                    throwNextQuickReply();
                }, 1000)
            }, 1000)
        }, 500)
        return true;
    } else if ("specifications".indexOf(text) !== -1) {
        conversation.append(chat_querying_content);
        conversation.scrollTop(conversation[0].scrollHeight);
        let replyHtml = robotHeader + specificationsQuickReplies1;
        setTimeout(function () {
            conversation.children('.chat-querying').each(function () {
                $(this).addClass('hidden')
            });
            conversation.append(replyHtml);
            conversation.scrollTop(conversation[0].scrollHeight);

            conversation.append(chat_querying_content);
            conversation.scrollTop(conversation[0].scrollHeight);
            setTimeout(function () {
                conversation.children('.chat-querying').each(function () {
                    $(this).addClass('hidden')
                });
                conversation.append(specificationsQuickReplies2);
                conversation.scrollTop(conversation[0].scrollHeight);

                conversation.append(chat_querying_content);
                conversation.scrollTop(conversation[0].scrollHeight);
                setTimeout(function () {
                    conversation.children('.chat-querying').each(function () {
                        $(this).addClass('hidden')
                    });
                    conversation.append(specificationsQuickReplies3);
                    conversation.scrollTop(conversation[0].scrollHeight);

                    conversation.append(chat_querying_content);
                    conversation.scrollTop(conversation[0].scrollHeight);
                    setTimeout(function () {
                        conversation.children('.chat-querying').each(function () {
                            $(this).addClass('hidden')
                        });
                        conversation.append(specificationsQuickReplies4);
                        conversation.scrollTop(conversation[0].scrollHeight);
                    }, 1000)
                }, 1000)
            }, 1000)
        }, 1000)
        return true;
    }

    return false;
}


// 提前设置Contact Me
function handleContactMeMode(text) {
    conversation = $('.conversation');
    conversation.append(chat_querying_content);
    conversation.scrollTop(conversation[0].scrollHeight);
    if (flag_contact_me_process === "email") {
        let email_pattern = /^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/;
        let email_detect = email_pattern.test(text.replace(" ", ""))
        console.log(email_detect);
        if (email_detect) {
            user_contact_me_email = text;
            let replyHtml = contactMeContent_Requirement;
            setTimeout(function () {
                conversation.children('.chat-querying').each(function () {
                    $(this).addClass('hidden')
                });
                conversation.append((replyHtml));
                conversation.scrollTop(conversation[0].scrollHeight);
            }, 500)
            flag_contact_me_process = "requirement";
        } else {
            let replyHtml = contactMeContent_Error_Email;
            setTimeout(function () {
                conversation.children('.chat-querying').each(function () {
                    $(this).addClass('hidden')
                });
                conversation.append((replyHtml));
                conversation.scrollTop(conversation[0].scrollHeight);
            }, 500)
        }
    } else if (flag_contact_me_process === "requirement") {
        if (text.length >= 10) {
            user_contact_me_requirement = text;
            let replyHtml = getContactMeSummary();
            setTimeout(function () {
                conversation.children('.chat-querying').each(function () {
                    $(this).addClass('hidden')
                });
                conversation.append((replyHtml));
                conversation.scrollTop(conversation[0].scrollHeight);
                flag_contact_me_process = "check";
                throwNextQuickReply_CONTACT_CONFIRM();
            }, 500)
        } else {
            let replyHtml = contactMeContent_Requirement_Error;
            setTimeout(function () {
                conversation.children('.chat-querying').each(function () {
                    $(this).addClass('hidden')
                });
                conversation.append((replyHtml));
                conversation.scrollTop(conversation[0].scrollHeight);
            }, 500)
        }
    } else if (flag_contact_me_process === "check") {
        if ("yes".indexOf(text) !== -1) {
            let replyHtml = contactMeContent_SUCCESS;
            setTimeout(function () {
                conversation.children('.chat-querying').each(function () {
                    $(this).addClass('hidden')
                });
                conversation.append((replyHtml));
                conversation.scrollTop(conversation[0].scrollHeight);
                flag_contact_me_mode = false;
                throwNextQuickReply_NOWAIT();
            }, 2000)
        } else if ("no".indexOf(text) !== -1) {
            flag_contact_me_process = "email";
            let replyHtml = contactMeContent_Understand;
            setTimeout(function () {
                conversation.children('.chat-querying').each(function () {
                    $(this).addClass('hidden')
                });
                conversation.append((replyHtml));
                conversation.scrollTop(conversation[0].scrollHeight);
            }, 500);
        }
    }
}

function handleExtraAnswer(result) {
    console.log("额外处理：", result)
    conversation = $('.conversation');
    if (result.includes("contact us")) {
        conversation.append(chat_querying_content);
        conversation.scrollTop(conversation[0].scrollHeight);
        let replyHtml = contactMeContent_confirm
        setTimeout(function () {
            conversation.children('.chat-querying').each(function () {
                $(this).addClass('hidden')
            });
            conversation.append(replyHtml);
            conversation.scrollTop(conversation[0].scrollHeight);
        }, 500)
    }
}

function triggerQuery() {
    conversation = $('.conversation');
    let input_text = user_input.val();
    if (input_text === "") return;
    user_input.val("");
    conversation.append(creatQueryHtml(input_text));
    conversation.scrollTop(conversation[0].scrollHeight);
    console.log("user query text:", input_text);

    if (flag_contact_me_mode) {
        console.log("trigger information receive");
        handleContactMeMode(input_text);
        return;
    }

    if (queryHandle(input_text)) {
        console.log("trigger prepared templates");
        return;
    }

    let product_reg = RegExp(/suitable sawing thickness|suitable wood length|suitable wood width|suitable wood height|power|sawing stroke|min processing diameter|max processing diameter|saw blade length|saw blade type|saw blade sawpath|feeding speed|equipment weight|machine dimension|suitable type of wood/);
    if (product_reg.test(input_text)) {
        triggerProductsQuery(input_text)
        return;
    }

    $.ajax({
        crossDomain: true,
        url: 'http://ipa-022.ucd.ie/chat_api',
        dataType: 'json',
        type: 'post',
        contentType: 'application/json',
        data: JSON.stringify({"question": input_text}),
        processData: false,
        success: function (data, textStatus, jQxhr) {
            conversation.children('.chat-querying').each(function () {
                $(this).addClass('hidden')
            });
            let result = data;
            console.log("result:", result);
            let responseHtml = createReplyHtml(result.response);
            $('.conversation').append(responseHtml);
            conversation.scrollTop(conversation[0].scrollHeight);

            handleExtraAnswer(result.response);
        },
        error: function (jqXhr, textStatus, errorThrown) {
            setTimeout(function () {
                conversation.children('.chat-querying').each(function () {
                    $(this).addClass('hidden')
                });
                let errorHtml = createReplyHtml("Sorry, online customer service is temporarily unavailable.  " +
                    "If you have any question, please contact +86 13559329496 (WhatsApp/WeChat/Telegram)");
                conversation.append(errorHtml);
                conversation.scrollTop(conversation[0].scrollHeight);
                console.log(errorThrown);
            }, 1000)
        },
        beforeSend: function () {
            $('.conversation').append(chat_querying_content);
            conversation.scrollTop(conversation[0].scrollHeight);
        },
        //请求完毕后（不管成功还是失败），关闭提示框
        complete: function () {
        },
    });
}


function triggerProductsQuery(input_text) {
    $.ajax({
        crossDomain: true,
        url: 'http://ipa-022.ucd.ie/product_api',
        dataType: 'json',
        type: 'post',
        contentType: 'application/json',
        data: JSON.stringify({"question": input_text}),
        processData: false,
        success: function (data, textStatus, jQxhr) {
            conversation.children('.chat-querying').each(function () {
                $(this).addClass('hidden')
            });
            let result = data;
            console.log("result:", result);
            let responseHtml = createReplyHtml(result.response.replaceAll("\n", "<br>"));
            $('.conversation').append(responseHtml);
            conversation.scrollTop(conversation[0].scrollHeight);

            handleExtraAnswer(result.response);
        },
        error: function (jqXhr, textStatus, errorThrown) {
            setTimeout(function () {
                conversation.children('.chat-querying').each(function () {
                    $(this).addClass('hidden')
                });
                let errorHtml = createReplyHtml("Sorry, online customer service is temporarily unavailable.  " +
                    "If you have any question, please contact +86 13559329496 (WhatsApp/WeChat/Telegram)");
                conversation.append(errorHtml);
                conversation.scrollTop(conversation[0].scrollHeight);
                console.log(errorThrown);
            }, 1000)
        },
        beforeSend: function () {
            $('.conversation').append(chat_querying_content);
            conversation.scrollTop(conversation[0].scrollHeight);
        },
        //请求完毕后（不管成功还是失败），关闭提示框
        complete: function () {
        },
    });
}

function throwNextQuickReply() {
    conversation = $('.conversation');
    conversation.append(chat_querying_content);
    conversation.scrollTop(conversation[0].scrollHeight);
    let replyHtml = normalQuickReplies;
    setTimeout(function () {
        setTimeout(function () {
            conversation.children('.chat-querying').each(function () {
                $(this).addClass('hidden')
            });
            conversation.append((replyHtml));
            conversation.scrollTop(conversation[0].scrollHeight);
        }, 500)
    }, 500)
}

function throwNextQuickReply_NOWAIT() {
    conversation = $('.conversation');
    conversation.append(normalQuickReplies);
    conversation.scrollTop(conversation[0].scrollHeight);
}

function throwNextQuickReply_CONTACT_CONFIRM() {
    conversation = $('.conversation');
    conversation.append(contactMeContentCheck);
    conversation.scrollTop(conversation[0].scrollHeight);
}

// 关闭
chat_wrapper.on('click', '.quick-query-close', function () {
    conversation.append(creatQueryHtml($(this).text().replace("\n", "")));
    queryHandle("close chat");
});

// 主菜单
chat_wrapper.on('click', '.quick-query-back', function () {
    conversation = $('.conversation');
    conversation.append(creatQueryHtml($(this).text().replace("\n", "")));

    conversation.append(chat_querying_content);
    conversation.scrollTop(conversation[0].scrollHeight);
    let replyHtml = robotHeader + startQuickReplies
    setTimeout(function () {
        conversation.children('.chat-querying').each(function () {
            $(this).addClass('hidden')
        });
        conversation.append((replyHtml));
        conversation.scrollTop(conversation[0].scrollHeight);
    }, 500)
    $('.quick-replies-buttons').remove();
});

// 重新开始对话
chat_wrapper.on('click', '.start-again-button', function () {
    $('.start-again').replaceWith(inputArea);
    conversation = $('.conversation');
    conversation.replaceWith(startContent);

    user_input = $('.typing input');
    user_input.keydown(function (event) {
        if (event.keyCode == 13) {
            $(".send-icon").click();
        }
    });
});

// 商品
chat_wrapper.on('click', '.quick-query-products', function () {
    conversation = $('.conversation');
    conversation.append(creatQueryHtml($(this).text().replace("\n", "")));
    conversation.scrollTop(conversation[0].scrollHeight);
    queryHandle("all products");
    $('.quick-replies-buttons').remove();
});

// 关于公司
chat_wrapper.on('click', '.quick-query-company', function () {
    conversation = $('.conversation');
    conversation.append(creatQueryHtml($(this).text().replace("\n", "")));
    conversation.scrollTop(conversation[0].scrollHeight);
    queryHandle("company profile");
    $('.quick-replies-buttons').remove();
});

// 联系
chat_wrapper.on('click', '.quick-query-inquiry', function () {
    conversation = $('.conversation');
    conversation.append(creatQueryHtml($(this).text().replace("\n", "")));
    conversation.scrollTop(conversation[0].scrollHeight);
    queryHandle("contact me");
    $('.quick-replies-buttons').remove();
});

// 联系 - 确认
chat_wrapper.on('click', '.quick-query-contact-yes', function () {
    conversation = $('.conversation');
    conversation.append(creatQueryHtml($(this).text().replace("\n", "")));
    conversation.scrollTop(conversation[0].scrollHeight);
    handleContactMeMode("yes");
    $('.quick-replies-buttons').remove();
});

// 联系 - 重启
chat_wrapper.on('click', '.quick-query-contact-no', function () {
    conversation = $('.conversation');
    conversation.append(creatQueryHtml($(this).text().replace("\n", "")));
    conversation.scrollTop(conversation[0].scrollHeight);
    handleContactMeMode("no");
    $('.quick-replies-buttons').remove();
});


// 联系 - 确认开启
chat_wrapper.on('click', '.quick-query-contact-start-yes', function () {
    conversation = $('.conversation');
    conversation.append(creatQueryHtml($(this).text().replace("\n", "")));
    conversation.scrollTop(conversation[0].scrollHeight);
    queryHandle("contact me");
    $('.quick-replies-buttons').remove();
});

// 联系 - 取消开启
chat_wrapper.on('click', '.quick-query-contact-start-no', function () {
    conversation = $('.conversation');
    conversation.append(creatQueryHtml($(this).text().replace("\n", "")));

    conversation.append(chat_querying_content);
    conversation.scrollTop(conversation[0].scrollHeight);
    let replyHtml = robotHeader + startQuickReplies
    setTimeout(function () {
        conversation.children('.chat-querying').each(function () {
            $(this).addClass('hidden')
        });
        conversation.append((replyHtml));
        conversation.scrollTop(conversation[0].scrollHeight);
    }, 500)
    $('.quick-replies-buttons').remove();
});


// 关于公司
chat_wrapper.on('click', '.quick-query-specifications', function () {
    conversation = $('.conversation');
    conversation.append(creatQueryHtml($(this).text().replace("\n", "")));
    conversation.scrollTop(conversation[0].scrollHeight);
    queryHandle("specifications");
    $('.quick-replies-buttons').remove();
});


chat_wrapper.on('click', '.send-icon', function () {
    triggerQuery();
});


user_input.keydown(function (event) {
    if (event.keyCode == 13) {
        $(".send-icon").click();
    }
});
