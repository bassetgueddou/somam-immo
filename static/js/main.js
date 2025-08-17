// JS minimal pour interactions futures
console.log('SOMAM site loaded');
document.addEventListener('DOMContentLoaded', () => {
  // Carrousel vertical
  const swiper = new Swiper('.myVerticalSwiper', {
    direction: 'vertical',
    loop: true,
    autoplay: { delay: 4000, disableOnInteraction: false },
    pagination: { el: '.swiper-pagination', clickable: true },
    navigation: { nextEl: '.swiper-button-next', prevEl: '.swiper-button-prev' },
    mousewheel: true,
    keyboard: { enabled: true },
  });
});
