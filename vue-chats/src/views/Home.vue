<template>
  <div class="home">
    <landing-page />
  </div>
</template>

<script>
// @ is an alias to /src
import LandingPage from "@/components/LandingPageComponent/LandingPage.vue";

export default {
  name: "Home",
  components: {
    LandingPage,
  },
};
</script>

    LandingPage