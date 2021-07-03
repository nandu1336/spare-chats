<template>
  <div>
    <header class="navbar mt-2">
      <section class="navbar-section"></section>
      <section class="navbar-center">CHATS</section>
      <section class="navbar-section"></section>
    </header>

    <div class="hero bg-white">
      <div class="hero-body">
        <div class="container">
          <div class="columns">
            <div class="column h-70">
              <router-view></router-view>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  mounted() {
    this.$router.push("/intro");
  },
  data() {
    return {
      ws: this.$store.state.ws,
      slideNumber: 1,
      roomName: "",
      roomOwnerName: "",
      roomSuccessfullyCreated: false,
      roomCode: "",
    };
  },

  methods: {
    handleShowRoomCreationCardEvent() {
      this.slideNumber = 2;
    },
  },

  computed: {},
};
</script>

<style lang="css">
.bg-white {
  background-color: #ffffff;
}
.h-70 {
  height: 70vh;
}
</style>