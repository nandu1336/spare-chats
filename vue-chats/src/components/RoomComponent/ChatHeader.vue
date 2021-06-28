<template>
  <div>
    <div class="container">
      <div class="columns">
        <div class="column h-8 col-1 bg-dark">
          <!-- <button class="mt-2" style="border-radius: 50%; outline: none">
            <i class="icon icon-menu" style="width: 20px; height: 30px"></i>
          </button> -->
        </div>
        <div class="column h-8 col-10 bg-dark">
          <h3 class="mt-2">{{ roomName }}</h3>
        </div>
        <div class="column h-8 col-1 bg-dark"></div>
      </div>
    </div>
  </div>
</template>

<script>
import store from "../../store/index";
export default {
  data() {
    return {
      roomName: store.state.roomName,
    };
  },
};
</script>

<style lang="css">
.h-8 {
  height: 8vh;
}
</style>