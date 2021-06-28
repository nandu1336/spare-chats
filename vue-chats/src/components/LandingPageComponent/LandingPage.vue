<template>
  <div>
    <header class="navbar mt-2">
      <section class="navbar-section"></section>
      <section class="navbar-center">CHATS</section>
      <section class="navbar-section"></section>
    </header>

    <div class="hero bg-white">
      <div class="hero-body">
        <div class="container">
          <div class="columns">
            <div class="column h-70">
              <intro-component
                v-if="slideNumber == 1"
                @showRoomFormRaised="handleShowRoomCreationCardEvent"
                @enterRoom="handleEnterRoomEvent"
              ></intro-component>

              <room-form-component
                v-else-if="slideNumber == 2"
                @createRoomRaised="handleCreateRoomEvent"
              ></room-form-component>

              <success-prompt-component
                v-else-if="slideNumber == 3"
                :inviteCode="roomCode"
                @enterRoomRaised="handleEnterRoomEvent"
              ></success-prompt-component>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import IntroComponent from "./IntroComponent";
import RoomFormComponent from "./RoomFormComponent";
import SuccessPromptComponent from "./SuccessPromptComponent";
import store from "../../store/index";
import router from "../../router/index";
import { v4 as uuid } from "uuid";

export default {
  components: {
    IntroComponent,
    RoomFormComponent,
    SuccessPromptComponent,
  },
  mounted() {},
  data() {
    return {
      ws: store.state.ws,
      slideNumber: 1,
      roomName: "",
      roomOwnerName: "",
      roomSuccessfullyCreated: false,
      roomCode: "",
    };
  },

  methods: {
    handleShowRoomCreationCardEvent() {
      this.slideNumber = 2;
    },

    handleCreateRoomEvent(e) {
      this.roomName = e.roomName;
      this.roomOwnerName = e.roomOwnerName;

      let roomDetails = JSON.stringify({
        room_name: this.roomName,
        room_owner: this.roomOwnerName,
        user_id: uuid(),
      });

      this.ws = new WebSocket(`ws://localhost:8000/create_room/${roomDetails}`);
      store.commit("setWebSocket", this.ws);

      this.startChat();
    },

    handleEnterRoomEvent(details) {
      console.log("e in handleEnterRoomEvent:", details);
      if (!this.roomName) {
        console.log("the person who is trying to enter is not the owner.");
        this.ws = new WebSocket(
          `ws://localhost:8000/join_room/${JSON.stringify(details)}`
        );
        store.commit("setWebSocket", this.ws);
        this.startChat();
      } else {
        store.commit("setRoomName", this.roomName);
        console.log("this.roomName::", this.roomName);
        router.push("/room");
      }
    },

    startChat() {
      this.ws.onopen = (e) => {
        console.log("Connection Established With WebSocketServer.", e);
      };

      this.ws.onmessage = (e) => {
        console.log("messgae received from server:", e);
        if (e.data.includes("200:")) {
          this.slideNumber = 3;
          this.roomCode = e.data.split("200:")[1];
          console.log("this.roomCode:", this.roomCode);
          router.push("/room");
        }
      };
    },
  },

  computed: {},
};
</script>

<style lang="css">
.bg-white {
  background-color: #ffffff;
}
.h-70 {
  height: 70vh;
}
</style>