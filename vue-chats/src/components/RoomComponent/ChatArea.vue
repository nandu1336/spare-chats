<template>
  <div class="container">
    <div class="columns">
      <message-component
        v-for="(message, index) in messages"
        :key="index"
        :message="message"
      ></message-component>
    </div>
  </div>
</template>

<script>
import MessageComponent from "./MessageComponent.vue";
import store from "../../store/index";

export default {
  components: {
    MessageComponent,
  },

  data() {
    return {
      messages: store.state.messages,
    };
  },
};
</script>