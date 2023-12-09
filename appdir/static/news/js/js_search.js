function getQueryString(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) return decodeURIComponent(r[2]);
    return null;
}


function changeURLStaticTag(tag) {
    let type = getQueryString("type");
    history.replaceState(null, null, "?type=" + type + "?tag=" + tag);

    $.ajax({
        url: "/product_search/?type=" + type + "?tag=" + tag,
        method: "GET",
        success: function (res) {
            $(".collection_prod").html($(res).find('.collection_prod')[0].innerHTML);
            console.log("search ajax refresh");
        }
    });
}


// function changeURLStaticTag(tag) {
//     let type = getQueryString("type");
//     history.replaceState(null, null, "?type=" + type + "?tag=" + tag);
//
//     $.ajax({
//         url: "/product_search/?type=" + type + "?tag=" + tag,
//         method: "GET",
//         success: function (res) {
//             $(".collection_prod").html($(res).find('.collection_prod')[0].innerHTML);
//             console.log("search ajax refresh");
//         }
//     });
// }
