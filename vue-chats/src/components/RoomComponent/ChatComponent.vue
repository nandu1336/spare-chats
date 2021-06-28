<template>
  <div class="d-flex h-100 bg-primary m-auto">
    <chat-header></chat-header>

    <div class="chat-area">
      <chat-area></chat-area>
    </div>

    <chat-bar></chat-bar>
  </div>
</template>

<script>
import ChatHeader from "./ChatHeader";
import ChatBar from "./ChatBar.vue";
import ChatArea from "./ChatArea.vue";

export default {
  components: {
    ChatHeader,
    ChatBar,
    ChatArea,
  },
};
</script>

<style lang="css">
.d-flex {
  display: flex;
  flex-direction: column;
  align-items: stretch;
}

.header {
  height: 8vh;
}

.chat-bar {
  height: 8vh;
}

.chat-area {
  height: 92vh;
  background-color: #edf6f9;
}

.h-80 {
  height: 80vh;
}

.h-100 {
  height: 100vh;
}
</style>