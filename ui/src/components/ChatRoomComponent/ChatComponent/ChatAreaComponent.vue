
<template>
  <div>
    <message-component
      v-for="(message, index) in getMessages"
      :key="index"
      class="text item"
      :message="message"
    ></message-component>
  </div>
</template>

<script>
import MessageComponent from "@/components/ChatRoomComponent/ChatComponent/MessageComponent";

export default {
  components: { MessageComponent },
  data() {
    return {};
  },

  computed: {
    getMessages() {
      return this.$store.state.messages;
    },
    showMessages() {
      return this.$store.state.messages.length ? true : false;
    },
  },
};
</script>

<style>
.text {
  font-size: 14px;
}

.item {
  padding: 18px 0;
}

.box-card {
  width: 480px;
}
</style>
