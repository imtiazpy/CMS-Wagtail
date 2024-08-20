const multipleImageSlider = document.querySelector("#sliderCarouselGallery");

if (window.matchMedia("(min-width: 768px)").matches) {
  const carouselWidth = $(".gallery-carousel-inner")[0].scrollWidth;
  const itemWidth = $(".gallery-carousel-item").width();

  let scrollPosition = 0;


  $(".gallery-carousel-control-next").on("click", function () {
    if (scrollPosition < (carouselWidth - itemWidth * 4)) { //check if you can go any further
      scrollPosition += itemWidth;  //update scroll position
      $(".gallery-carousel-inner").animate({ scrollLeft: scrollPosition }, 600); //scroll left
    }
  });

  $(".gallery-carousel-control-prev").on("click", function () {
    if (scrollPosition > 0) {
      scrollPosition -= itemWidth;
      $(".gallery-carousel-inner").animate(
        { scrollLeft: scrollPosition },
        600
      );
    }
  });

  const carousel = new bootstrap.Carousel(multipleImageSlider, {
    interval: false
  });
} else {
  $(multipleImageSlider).addClass("slide");
}

