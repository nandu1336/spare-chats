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
export default {
  data() {
    return {
      roomName: "",
      roomOwnerName: "",
    };
  },

  methods: {
    raiseCreateRoomEvent() {
      console.log(
        "roomName:",
        this.roomName,
        "roomOwnerName:",
        this.roomOwnerName
      );
      if (this.roomName.length == 0 || this.roomOwnerName.length == 0) {
        alert("Please Enter Room Title and Owner Name Before Proceeding.");
      } else {
        this.$.emit("createRoomRaised", {
          roomName: this.roomName,
          roomOwnerName: this.roomOwnerName,
        });
      }
    },
  },
};
</script>