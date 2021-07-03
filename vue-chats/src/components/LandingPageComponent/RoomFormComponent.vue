<template>
  <div
    class="card"
    style="width: 30%; margin: auto; margin-top: 5%; height: 90%"
  >
    <div class="card-header">
      <div class="card-title h5 text-dark">Create Room</div>
      <div class="card-subtitle text-gray"></div>
    </div>
    <div class="card-body" style="margin-top: 10%">
      <div class="container">
        <div class="columns">
          <div class="column" style="margin-bottom: 5%">
            <input
              v-model="roomName"
              type="text"
              required
              placeholder="Enter Room Name"
              style="width: 50%; margin: auto"
            />
          </div>
        </div>

        <div class="columns">
          <div class="column">
            <input
              v-model="roomOwnerName"
              type="text"
              required
              placeholder="Enter Your Name"
              style="width: 50%; margin: auto"
            />
          </div>
        </div>
      </div>
    </div>
    <div class="card-footer">
      <button
        @click="raiseCreateRoomEvent"
        class="btn btn-primary"
        style="width: 33%"
      >
        Create Room
      </button>
    </div>
  </div>
</template>

<script>
import { v4 as uuid } from "uuid";
export default {
  data() {
    return {
      roomName: "",
      roomOwnerName: "",
      roomCode: "",
    };
  },

  methods: {
    raiseCreateRoomEvent() {
      if (this.roomName.length == 0 || this.roomOwnerName.length == 0) {
        alert("Please Enter Room Title and Owner Name Before Proceeding.");
      } else {
        let roomDetails = JSON.stringify({
          room_name: this.roomName,
          owner_name: this.roomOwnerName,
          owner_id: uuid(),
        });

        this.ws = new WebSocket(
          `ws://localhost:8000/create_room/${roomDetails}`
        );
        this.$store.commit("setWebSocket", this.ws);

        this.startChat();
      }
    },

    startChat() {
      this.ws.onopen = (e) => {
        console.log("Connection Established With WebSocketServer.", e);
      };

      this.ws.onmessage = (e) => {
        console.log("messgae received from server:", e);
        if (e.data.includes("200:")) {
          this.roomCode = e.data.split("200:")[1];
          console.log("this.roomCode:", this.roomCode);
          this.$router.push("/room");
        } else if (e.data.includes("<meta>request_accepted</meta>")) {
          this.$router.push("/room");
        }
      };
    },
  },
};
</script>