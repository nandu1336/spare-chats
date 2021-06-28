<template>
  <div class="container">
    <div class="columns chat-bar-container">
      <div class="column col-2"></div>
      <div class="column col-9">
        <input
          type="text"
          name="message-box"
          id="message-box"
          class="message-box"
          v-model="message"
          @keyup.enter="sendMessage"
        />
      </div>
      <div class="column col-1">
        <button class="mt-1">
          <i class="icon icon-arrow-right"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import store from "../../store/index";
export default {
  mounted() {
    this.ws.onmessage = this.handleNewMessage;
  },

  data() {
    return {
      ws: store.state.ws,
      message: "",
    };
  },

  methods: {
    sendMessage() {
      console.log("sendMessage called");
      if (this.message.length) {
        if (this.ws) {
          store.commit("appendToMessages", this.message);
          this.ws.send(this.message);
        }
        // store.commit("appendToMessages", this.message);
        this.message = "";
      }
    },

    handleNewMessage(e) {
      console.log("new message received", e);
      if (e.data.includes("<meta>join_request</meta>")) {
        let query = e.data.split("::");

        let username = query[1];
        let roomId = query[2];
        let response = prompt(query[3]);
        if (response.toLowerCase() == "yes") {
          response = "<meta>accept_request</meta>::" + roomId + "::" + username;
          this.ws.send(response);
        }
      }
    },
  },
};
</script>

<style lang="css">
.chat-bar-container {
  padding: 1%;
}
.message-box {
  width: 100%;
  height: 40px;
  border-radius: 50px;
  outline: none;
  border: none;
  padding: 2%;
}

/* .send-button { */

/* @media max-width(600px) {
    width: 100%;
  }

  height: 40px; */
/* } */
</style>