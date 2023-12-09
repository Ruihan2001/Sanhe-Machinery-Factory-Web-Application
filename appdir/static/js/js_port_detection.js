// let letcheckUrl = function (url) {
//     return new Promise(function (resolve, reject) {
//         $.ajax({
//             url: url,
//             type: 'GET',
//             dataType: "jsonp", //跨域采用jsonp方式
//             complete: (response) => {
//                 if (response.status === 200) {
//                     $(".vr-factory")[0].style = "display:block";
//                 } else {
//                     console.log("detection failed");
//                 }
//             }
//         });
//     });
// }
//
//
// letcheckUrl("http://ipa-022.ucd.ie/vr")