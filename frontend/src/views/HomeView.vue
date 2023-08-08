<template>
  <div class="home">
    <MovieCarousel />
    <HelloWorld />
  </div>
</template>

<script>
import HelloWorld from "@/components/HelloWorld.vue";
import MovieCarousel from "@/components/MovieCarousel.vue";

export default {
  name: "HomeView",
  components: {
    HelloWorld,
    MovieCarousel,
  },
};
</script>
