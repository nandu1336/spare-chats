<template>
  <div class="container">
    <div class="columns">
      <div class="column col-8"><chat-component></chat-component></div>
      <div class="column col-4"><memebers-component></memebers-component></div>
    </div>
  </div>
</template>

<script>
import ChatComponent from "./ChatComponent.vue";
import MemebersComponent from "./MembersComponent.vue";

export default {
  components: {
    ChatComponent,
    MemebersComponent,
  },
};
</script>