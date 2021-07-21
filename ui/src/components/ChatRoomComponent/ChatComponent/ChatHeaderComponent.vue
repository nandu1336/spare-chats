<template>
  <h5>{{ roomName }}</h5>
</template>

<script>
export default {
  data() {
    return {
      roomName: this.$store.state.roomDetails.room_name,
    };
  },
};
</script>