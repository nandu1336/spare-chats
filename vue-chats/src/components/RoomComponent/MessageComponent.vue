<template>
  <div class="container">
    <div class="columns">
      <div class="column col-10">
        <p class="text-dark">{{ message }}</p>
      </div>
      <div class="column col-2">
        <sub>{{ message.time }}</sub>
      </div>
    </div>
    <div class="columns">
      <sub>{{ message.ownername }}</sub>
    </div>
  </div>
</template>

<script>
export default {
  props: ["message"],

  mounted() {
    console.log("message in message component:", this.message);
  },
};
</script>
