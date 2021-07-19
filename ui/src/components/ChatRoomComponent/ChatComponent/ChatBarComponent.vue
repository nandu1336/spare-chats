<template>
  <el-row :gutter="20">
    <el-col :span="2" class="mt-2"
      ><span class="icon material-icons md-48">face</span></el-col
    >
    <el-col class="mt-1" :span="20">
      <input
        type="text"
        name="message-box"
        id="message-box"
        class="message-box"
        v-model="message"
        @keyup.enter="sendMessage"
      />
    </el-col>

    <el-col class="mt-2" :span="1">
      <span class="icon material-icons md-light md-48">send</span>
    </el-col>
  </el-row>
</template>

<script>
import config from "../../../config.js";
import { makeMessage } from "../../../classes.js";
export default {
  mounted() {
    this.ws.onmessage = this.handleNewMessage;
  },

  data() {
    return {
      ws: this.$store.state.ws,
      message: "",
    };
  },

  methods: {
    sendMessage() {
      console.log("sendMessage called");
      if (this.message.length) {
        if (this.ws) {
          this.message = makeMessage(this.message, config.CHAT);
          this.ws.send(this.message.as_json());
        }
        this.$store.commit("appendToMessages", this.message);
        this.message = "";
      }
    },
  },
};
</script>

<style lang="css">
.contaier {
  background-color: grey;
}
.chat-bar-container {
  background-color: black;
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

.icon {
  color: white;
  width: 48px;
  height: 48px;
}

.mt-2 {
  margin-top: 2%;
}

.mt-1 {
  margin-top: 1%;
}
/* .send-button { */

/* @media max-width(600px) {
    width: 100%;
  }

  height: 40px; */
/* } */
</style>