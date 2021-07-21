<template>
  <div>
    <link
      href="https://fonts.googleapis.com/icon?family=Material+Icons"
      rel="stylesheet"
    />
    <home></home>
  </div>
</template>

<script>
import Home from "./components/index.vue";

export default {
  name: "App",
  components: {
    Home,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;

  margin: 0px;
  padding: 0px;
  box-sizing: border-box;
}
* {
  margin: 0px;
  padding: 0px;
  box-sizing: border-box;
}
</style>
