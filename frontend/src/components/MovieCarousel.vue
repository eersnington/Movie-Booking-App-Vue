<template>
    <div id="movieCarousel" class="carousel Slider">
      <div class="carousel-indicators">
        <button type="button" data-bs-target="#movieCarousel" data-bs-slide-to="0" class="active"></button>
        <button type="button" data-bs-target="#movieCarousel" data-bs-slide-to="1"></button>
        <button type="button" data-bs-target="#movieCarousel" data-bs-slide-to="2"></button>
      </div>
      <div class="carousel-inner">
        <div class="carousel-item active">
          <img class="w-100" src="@/assets/Slideshow1.jpg" width="1280" height="500" alt="First Slide">
        </div>
        <div class="carousel-item">
          <img class="w-100" src="@/assets/Slideshow2.jpg" width="1280" height="500" alt="Second Slide">
        </div>
        <div class="carousel-item">
          <img class="w-100" src="@/assets/Slideshow3.jpg" width="1280" height="500" alt="Third slide">
        </div>
      </div>
      <button class="carousel-control-prev" type="button" data-bs-target="#movieCarousel" data-bs-slide="prev">
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
        <span class="sr-only">Previous</span>
      </button>
      <button class="carousel-control-next" type="button" data-bs-target="#movieCarousel" data-bs-slide="next">
        <span class="sr-only">Next</span>
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
      </button>
    </div>
  </template>
  
  <script>
  export default {
    name: "MovieCarousel",
  };
  </script>
  
  <style lang="scss" scoped></style>
  