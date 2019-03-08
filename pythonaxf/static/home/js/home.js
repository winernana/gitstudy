$(function () {
    // 恢复盒子大小
    $('.home').width(innerWidth)

    var topSwiper = new Swiper('#topSwiper', {
        pagination: '.swiper-pagination',
        // nextButton: '.swiper-button-next',
        // prevButton: '.swiper-button-prev',
        slidesPerView: 1,
        paginationClickable: true,
        spaceBetween: 30,
        loop: true,
        autoplay: 1000,
        effect: 'flip',
        // coverflow
    });


    var buySwiper = new Swiper('#buySwiper', {
        slidesPerView: 3,
        spaceBetween: 6,
        loop: true,
        // autoplay: 10,
        // effect: 'flip',
    });
})