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
        <div class="column">
          <input placeholder="Enter a code or link" class="pl-2" />
        </div>
      </div>

      <div class="column col-3"></div>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    raiseShowRoomFormEvent() {
      this.$.emit("showRoomFormRaised");
    },
  },
};
</script>