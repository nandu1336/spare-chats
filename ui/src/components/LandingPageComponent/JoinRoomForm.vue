<template>
  <div style="margin: 20px"></div>
  <el-form
    v-loading.fullscreen="showLoadingScreen"
    element-loading-text="Requesting Room Owner. Please Wait."
    label-position="left"
    label-width="100px"
    :model="roomDetails"
    style="margin-top: 7vh"
  >
    <el-form-item label="Room ID">
      <el-input
        v-model="roomDetails.room_code"
        placeholder="Enter Room ID"
        style="max-width: 300px; margin-left: auto; margin-right: auto"
      ></el-input>
    </el-form-item>

    <el-form-item label="Your Name">
      <el-input
        v-model="roomDetails.username"
        placeholder="Enter Your Name"
        style="max-width: 300px; margin-left: auto; margin-right: auto"
      ></el-input>
    </el-form-item>

    <el-form-item>
      <el-button
        type="info"
        @click="enterRoom()"
        style="max-width: 300px; margin-left: auto; margin-right: auto"
        >Join Room</el-button
      >
    </el-form-item>
  </el-form>
</template>

<script>
import { v4 as uuid } from "uuid";
import config from "../../config.js";
export default {
  data() {
    return {
      roomDetails: {
        room_code: "",
        username: "",
      },
      ws: null,
      showLoadingScreen: false,
    };
  },

  methods: {
    enterRoom() {
      this.roomDetails.user_id = uuid();
      this.ws = new WebSocket(
        `ws://localhost:8000/join_room/${JSON.stringify(this.roomDetails)}`
      );
      this.$store.commit("setWebSocket", this.ws);
      this.startChat();
    },

    startChat() {
      this.showLoadingScreen = true;
      this.ws.onmessage = (e) => {
        this.showLoadingScreen = false;

        let data = JSON.parse(e.data);
        if ((data.purpose = config.ACCEPT_REQUEST)) {
          this.$router.push("/room");
        }
      };
    },
  },
};
</script>