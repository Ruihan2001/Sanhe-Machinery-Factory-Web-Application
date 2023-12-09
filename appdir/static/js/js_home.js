

$('.portfolio-carousel-home-products').ready(function () {
    var screenWidth = $(window).width();
    let itemNumber = 3;
    if (screenWidth <= 550) {
        itemNumber = 1;
    } else if (screenWidth <= 800) {
        itemNumber = 2;
    } else if (screenWidth <= 1200) {
        itemNumber = 3;
    }
    jQuery('.portfolio-carousel-home-products').owlCarousel({
        autoWidth: true,
        loop: true,
        autoplaySpeed: 3000,
        navSpeed: 3000,
        paginationSpeed: 3000,
        slideSpeed: 3000,
        smartSpeed: 3000,
        autoplay: 3000,
        margin: 0,
        nav: true,
        dots: false,
        navText: ['<i class="ti-arrow-left"></i>', '<i class="ti-arrow-right"></i>'],
        items: itemNumber,
        responsiveBaseElement: $('.portfolio-carousel-home-products'),
        responsive: {
            0: {
                items: 1
            },
            550: {
                items: 1
            },
            800: {
                items: 2
            },
            1200: {
                items: 3
            }
        }
    })
})

$('.portfolio-carousel-home-adv').ready(function () {
    var screenWidth = $(window).width();
    let itemNumber = 5
    if (screenWidth <= 767) {
        itemNumber = 2;
    } else if (screenWidth <= 1024) {
        itemNumber = 3;
    } else if (screenWidth <= 1200) {
        itemNumber = 4;
    }
    $('.portfolio-carousel-home-adv').owlCarousel({
        loop: true,
        autoplaySpeed: 3000,
        navSpeed: 3000,
        paginationSpeed: 3000,
        slideSpeed: 3000,
        smartSpeed: 3000,
        autoplay: 3000,
        margin: 30,
        nav: false,
        dots: true,
        navText: ['<i class="ti-arrow-left"></i>', '<i class="ti-arrow-right"></i>'],
        items: itemNumber,
        responsiveBaseElement: $('.portfolio-carousel-home-adv'),
        responsive: {
            0: {
                items: 2
            },
            767: {
                items: 3
            },
            1024: {
                items: 4
            }
        }
    })
})
