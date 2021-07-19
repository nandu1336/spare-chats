<template>
  <div class="chats">
    <div
      v-if="isChatMessage(message)"
      class="message-container"
      :class="getAlignment"
    >
      <div class="columns">
        <div class="col-8">
          {{ message.sender.username }}
        </div>
        <button class="col-2">
          <i class="material-icons icon">more_vert</i>
        </button>
      </div>

      <div class="text-container">
        <span class="msg">
          {{ message.content }}
        </span>
      </div>
      <div class="time-container">
        <sub class="time">{{ message.sent_time.split("-")[0] }}</sub>
      </div>
    </div>

    <el-alert
      v-else-if="isNewMemberJoinedNotification(message)"
      :title="message.content"
      type="success"
    >
    </el-alert>
  </div>
</template>

<script>
import config from "../../../config";
export default {
  mounted() {
    console.log("mesage component mounted with prop:", this.message);
  },
  props: ["message"],

  methods: {
    isChatMessage(message) {
      return message.purpose == config.CHAT;
    },

    isNewMemberJoinedNotification(message) {
      return message.purpose == config.NEW_MEMBER_JOINED;
    },
  },

  computed: {
    getAlignment() {
      // console.log("this.$store.state.userDetails.");
      let ml =
        this.message.sender.username == this.$store.state.userDetails.username
          ? "ml-auto"
          : "";
      console.log("ml :", ml);
      return ml;
    },
  },
};
</script>


<style>
.chats {
  display: flexbox;
}
.columns {
  background-color: black;
}
.columns .text-container {
  padding: 0%;
  margin: 0%;
  display: flexbox;
  flex-direction: row;
}
.text-container {
  padding: 5px;
}
.msg {
  display: flex;
  align-self: flex-end;
  text-align: start;
  margin-left: 5px;
}
.time-container {
  display: flexbox;
  flex-direction: row;
  padding: 2px;
  align-items: flex-end;
}
.time {
  width: fit-content;
  display: flex;
  align-self: flex-end;
  margin-left: auto;
  text-align: end;
}
.col-8 {
  align-self: flex-start;
  width: 90%;
  display: inline-flex;
  color: white;
  margin-top: 0px;
  margin-bottom: 5px;
  margin-left: 5px;
  font-weight: 400;
}

.col-2 {
  background: none;
  border: none;
  padding-top: 1%;
  width: 5%;
  height: 20px;
  text-align: end;
  align-self: flex-end;
  display: inline-flex;
}
.ml-auto {
  margin-left: auto;
}
.message-container {
  width: 400px;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  transition: 0.3s;
  border-radius: 5px;
}

.card:hover {
  box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
}
</style>
