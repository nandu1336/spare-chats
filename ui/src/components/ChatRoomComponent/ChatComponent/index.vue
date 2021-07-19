<template>
  <el-container>
    <el-header class="chat-header">
      <chat-header-component></chat-header-component>
    </el-header>
    <el-main class="chat-area">
      <chat-area-component></chat-area-component>
    </el-main>
    <el-footer class="chat-bar">
      <chat-bar-component class="bg-black"></chat-bar-component>
    </el-footer>
  </el-container>
</template>


<script>
import ChatHeaderComponent from "@/components/ChatRoomComponent/ChatComponent/ChatHeaderComponent";
import ChatAreaComponent from "@/components/ChatRoomComponent/ChatComponent/ChatAreaComponent";
import ChatBarComponent from "@/components/ChatRoomComponent/ChatComponent/ChatBarComponent";

export default {
  components: { ChatHeaderComponent, ChatAreaComponent, ChatBarComponent },

  data() {
    return {};
  },
};
</script>

<style scoped>
.chat-header {
  height: 5vh;
}
.chat-area {
  height: 84vh;
}
.chat-bar {
  height: 5vh;
  background-color: black;
}

.chat-header {
  background-color: black;
  color: white;
  padding-top: 15px;
  text-transform: capitalize;
  font-family: "Franklin Gothic Medium", "Arial Narrow", Arial, sans-serif;
  font-size: 24px;
}
</style>