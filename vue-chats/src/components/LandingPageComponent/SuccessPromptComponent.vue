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
            <h3>Room Created Successfully:</h3>
          </div>
        </div>

        <div class="columns">
          <div class="column">
            <p class="text-primary">
              Share Below Code With Your Friends To Invite Them To Room
            </p>
            <h5>{{ inviteCode }}</h5>
          </div>
        </div>
      </div>
    </div>
    <div class="card-footer">
      <button @click="raiseEnterRoom">Enter Room</button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    inviteCode: {
      type: Number,
    },
  },

  methods: {
    raiseEnterRoom() {
      this.$.emit("enterRoomRaised", this.inviteCode);
    },
  },
};
</script>