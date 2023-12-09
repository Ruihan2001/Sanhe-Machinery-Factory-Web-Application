let max_page;
let page;
let searchInput;

$(document).ready(function () {
    ready_page();
    $("#search-button").click(function () {
        searchInput = document.getElementById("search-input").value;
        if (searchInput === "") {
            searchInput = "null";
        }
        get_max();
        page = 1;
        get_pros(page);
        document.getElementById("page").value = "1";
    });

    $("#redirect").click(function () {
        console.log("click");
        let inputPage = document.getElementById("page").value;
        if (inputPage.match(/\D/) != null) {
            alert("Please input integer.");
        } else {
            inputPage = parseInt(inputPage);
            if (inputPage <= 0 || inputPage > max_page) {
                alert("Please input reachable page number.");
            } else {
                get_pros(inputPage);
            }
        }
    });
    $("#before").click(function () {
        if (parseInt(page) - 1 <= 0) {
            alert("This page is the first page.");
        } else {
            page = parseInt(page) - 1;
            get_pros(page);
        }
    });
    $("#after").click(function () {
        console.log(page);
        if (parseInt(page) + 1 > max_page) {
            alert("This page is the last page.");
        } else {
            page = parseInt(page) + 1;
            get_pros(page);
        }
    });
    $(document).on('click', '.delete', function () {
        console.log('delete')
        element = $(this).parent().parent().parent()
        p_id = $(this).parent().parent().parent().attr('id')
        console.log(p_id)
        $.post('/staff/del_pro', {'id': p_id}).done(function (request) {
            let server = request['returnValue'];
            console.log(server);
            if (server === 200) {
                element.remove();
                alert('successfully deleted')
            } else {
                console.log(server);
            }
        });
    })
});

function ready_page() {
    searchInput = "null";
    page = 1;
    get_max();
    get_pros(page);
}

function get_max() {
    $.post('/staff/get_max_pro', {search: searchInput}).done(function (data) {
        max_page = parseInt(data.pages);
        $("#all_page").text("/ " + max_page)
        $("#total").text("find " + data.total_num + " products in total")
        console.log(max_page);
    });
}

function get_pros(inputPage) {
    $.post('/staff/get_pros', {page: inputPage, search: searchInput}).done(function (data) {
        console.log(data.length);
        empty_pros();
        let grid = document.getElementById("products");
        let length = data.length;
        for (let i = 0; i < length; i++) {
            let product = produce_row(data[i]);
            grid.appendChild(product);
        }

        document.getElementById("page").value = inputPage;
        page = parseInt(inputPage);
    });
}

function empty_pros() {
    $(".shown_products").each(function () {
        this.remove()
    })
}


function produce_row(pro) {

    let product = document.createElement("div");
    product.className = "intro-y col-span-12 md:col-span-6 lg:col-span-4 xl:col-span-6 shown_products";
    product.id = pro.product_id;
    let lowcase = pro.product_name.toLowerCase().replace(/ /g, "_")
    console.log(lowcase)
    let img = pro.product_poster
    product.innerHTML = "<div class=\"box\">\n" +
        "                    <div class=\"p-5\">\n" +
        "                        <div class=\"h-56 2xl:h-56 image-fit rounded-md overflow-hidden before:block before:absolute before:w-full before:h-full before:top-0 before:left-0 before:z-10 before:bg-gradient-to-t before:from-black before:to-black/10\">\n" +
        "                            <img alt=\"product\" class=\"rounded-md\" src=\"/static/images/blog_img/" + img + "\">\n" +
        "                            <div class=\"absolute bottom-0 text-white px-5 pb-6 z-10\">\n" +
        "                                <a href=\"\" class=\"block font-medium text-base\">" + pro.product_name + "</a>\n" +
        "                            </div>\n" +
        "                        </div>\n" +
        "                        <div class=\"text-slate-600 dark:text-slate-500 mt-5\">\n" +
        "                            <div class=\"flex items-center\">\n" +
        "                                <svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" icon-name=\"link\" data-lucide=\"link\" class=\"lucide lucide-link w-4 h-4 mr-2\"><path d=\"M10 13a5 5 0 007.54.54l3-3a5 5 0 00-7.07-7.07l-1.72 1.71\"></path><path d=\"M14 11a5 5 0 00-7.54-.54l-3 3a5 5 0 007.07 7.07l1.71-1.71\"></path></svg>\n" +
        "                                /sanhe/products/" + pro.product_name + "\n" +
        "                            </div>\n" +
        "                            <div class=\"flex items-center mt-2\">\n" +
        "                                                             <svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" icon-name=\"check-square\" data-lucide=\"check-square\" class=\"lucide lucide-check-square w-4 h-4 mr-2\"><polyline points=\"9 11 12 14 22 4\"></polyline><path d=\"M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11\"></path></svg>\n" +
        "                                Status: Active\n" +
        "                            </div>\n" +
        "                        </div>\n" +
        "                    </div>\n" +
        "                    <div class=\"flex justify-center lg:justify-end items-center p-5 border-t border-slate-200/60 dark:border-darkmode-400\">\n" +
        "                        <a class=\"flex items-center text-primary mr-auto\" href=\"/sanhe/product_detail/" + lowcase + "\">\n" +
        "                            <svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" icon-name=\"eye\" data-lucide=\"eye\" class=\"lucide lucide-eye w-4 h-4 mr-1\"><path d=\"M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z\"></path><circle cx=\"12\" cy=\"12\" r=\"3\"></circle></svg> View\n" +
        "                        </a>\n" +
        "                        <a class=\"flex items-center mr-3\" href=\"/staff/modify_product/" + lowcase + "\">\n" +
        "                            <svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" icon-name=\"check-square\" data-lucide=\"check-square\" class=\"lucide lucide-check-square w-4 h-4 mr-1\"><polyline points=\"9 11 12 14 22 4\"></polyline><path d=\"M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11\"></path></svg> Edit\n" +
        "                        </a>\n" +
        "                        <a class=\"flex items-center text-danger delete\" href=\"javascript:;\" data-tw-toggle=\"modal\"\n" +
        "                           data-tw-target=\"#delete-confirmation-modal\">\n" +
        "                            <svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" icon-name=\"trash-2\" data-lucide=\"trash-2\" class=\"lucide lucide-trash-2 w-4 h-4 mr-1\"><polyline points=\"3 6 5 6 21 6\"></polyline><path d=\"M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2\"></path><line x1=\"10\" y1=\"11\" x2=\"10\" y2=\"17\"></line><line x1=\"14\" y1=\"11\" x2=\"14\" y2=\"17\"></line></svg> Delete\n" +
        "                        </a>\n" +
        "                    </div>\n" +
        "                </div>"


    return product;

}


