<template>
  <div>
    <div class="" style="margin-top: 10%">
      <h1>Hello!!</h1>
      <p>
        Connect with you friends immediately by clicking on
        <b>Create New Room</b> button. <br />Already have a room code? Click on
        <b>Join Room</b> button belowl.
      </p>
    </div>
    <div class="columns" style="margin-top: 10%">
      <div class="column col-3"></div>

      <div class="column">
        <button class="bg-blue" @click="raiseShowRoomFormEvent">
          Create New Room
          <i class="icon icon-plus ml-2"></i>
        </button>
      </div>

      <div class="column">
        <div>
          <input
            type="text"
            v-model="username"
            placeholder="Enter Your Name"
            class="pl-2 mb-2"
          />
        </div>

        <div class="column">
          <input
            type="text"
            v-model="roomCode"
            @keyup.enter="raiseRoomEnterEvent"
            placeholder="Enter a code or link"
            class="pl-2 mb-2"
          />
        </div>

        <div>
          <button @click="raiseRoomEnterEvent">Join</button>
        </div>
      </div>

      <div class="column col-3"></div>
    </div>
  </div>
</template>

<script>
import { v4 as uuid } from "uuid";

export default {
  data() {
    return {
      username: "",
      roomCode: "",
    };
  },
  methods: {
    raiseShowRoomFormEvent() {
      this.$.emit("showRoomFormRaised");
    },

    raiseRoomEnterEvent() {
      this.$.emit("enterRoom", {
        room_id: this.roomCode,
        username: this.username,
        user_id: uuid(),
      });
    },
  },
};
</script>