<template>
  <div style="margin: 20px"></div>
  <el-form
    label-position="left"
    label-width="100px"
    :model="roomDetails"
    style="margin-top: 7vh"
  >
    <el-form-item label="Room Name">
      <el-input
        v-model="roomDetails.room_name"
        placeholder="Give Your Room a Name"
        style="max-width: 300px; margin-left: auto; margin-right: auto"
      ></el-input>
    </el-form-item>

    <el-form-item label="Your Name">
      <el-input
        v-model="roomDetails.owner_name"
        placeholder="Enter Your Name"
        style="max-width: 300px; margin-left: auto; margin-right: auto"
      ></el-input>
    </el-form-item>

    <el-form-item>
      <el-button
        type="info"
        @click="createRoom"
        style="max-width: 300px; margin-left: auto; margin-right: auto"
      >
        Create Room
      </el-button>
    </el-form-item>
  </el-form>
</template>

<script>
import { v4 as uuid } from "uuid";

export default {
  data() {
    return {
      roomDetails: {
        room_name: "",
        owner_name: "",
      },
    };
  },

  methods: {
    createRoom() {
      if (!this.roomDetails.room_name || !this.roomDetails.owner_name) {
        alert("Please Enter Room Title and Owner Name Before Proceeding.");
      } else {
        this.roomDetails.owner_id = uuid();
        let roomDetails = JSON.stringify(this.roomDetails);

        this.ws = new WebSocket(
          `ws://localhost:8000/create_room/${roomDetails}`
        );
        this.$store.commit("setWebSocket", this.ws);

        this.ws.onopen = (e) => {
          console.log("Connection Established With WebSocketServer.", e);
        };

        this.ws.onmessage = (e) => {
          console.log("messgae received from server:", e);
          if (e.data.includes("200:")) {
            this.roomCode = e.data.split("200:")[1];
            this.roomDetails.room_code = this.roomCode;
            console.log("roomDetails:", this.roomDetails);
            this.$store.commit("setRoomDetails", this.roomDetails);
            this.$store.commit("setUserDetails", {
              username: this.roomDetails.owner_name,
              userID: this.roomDetails.owner_id,
            });

            this.$router.push("/room");
          }
        };
      }
    },
  },
};
</script>