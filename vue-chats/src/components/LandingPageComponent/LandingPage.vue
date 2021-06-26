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
export default {
  components: {
    IntroComponent,
    RoomFormComponent,
    SuccessPromptComponent,
  },
  mounted() {},
  data() {
    return {
      ws: "",
      slideNumber: 1,
      roomTitle: "",
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
      this.roomTitle = e.roomTitle;
      this.roomOwnerName = e.roomOwnerName;

      let roomDetails = JSON.stringify({
        room_name: this.roomTitle,
        room_owner: this.roomOwnerName,
      });

      this.ws = new WebSocket(`ws://localhost:8000/create_room/${roomDetails}`);

      this.ws.onopen = (e) => {
        console.log("Room Created Successfully!!!", e);
      };

      this.ws.onmessage = (e) => {
        console.log("messgae received from server:", e);
        if (e.data.includes("200:")) {
          this.slideNumber = 3;
          this.roomCode = e.data.split("200:")[1];
          console.log("this.roomCode:", this.roomCode);
        }
      };
    },

    handleEnterRoomEvent(e) {
      console.log("e in handleEnterRoomEvent:", e);
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