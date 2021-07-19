<template>
  <div>
    <el-dialog title="Join Request" v-model="dialogProp.showDialog" width="30%">
      <span>{{ dialogProp.dialogMessage }}</span>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="denyUser">Deny</el-button>
          <el-button type="info" @click="acceptUser">Accept</el-button>
        </span>
      </template>
    </el-dialog>

    <el-container>
      <!-- <el-header>Header</el-header> -->
      <el-container>
        <!-- Left side area for chatting -->

        <el-aside width="600px">
          <chat-area-component></chat-area-component>
        </el-aside>

        <!-- Right side area -->
        <el-main>Main</el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
// import Dialog from "@/components/misc/Dialog";
import ChatAreaComponent from "./ChatComponent/index.vue";
import config from "../../config.js";
import { makeMessage } from "../../classes.js";

export default {
  components: { ChatAreaComponent },
  mounted() {
    this.ws.onmessage = this.handleNewMessage;
  },

  data() {
    return {
      ws: this.$store.state.ws,
      message: "",
      dialogProp: {
        showDialog: false,
        dialogMessage: "",
      },
      userName: "",
      userID: "",
    };
  },

  methods: {
    sendMessage() {
      console.log("sendMessage called");
      if (this.message.length) {
        if (this.ws) {
          this.ws.send(this.message);
        }
        this.$store.commit("appendToMessages", this.message);
        this.message = "";
      }
    },

    handleNewMessage(e) {
      let data = JSON.parse(e.data);
      console.log("prased data:", data);
      if (data.purpose == config.JOIN_REQUEST) {
        this.userID = data.sender.user_id;
        this.userName = data.sender.username;
        this.dialogProp.dialogMessage = `${this.userName} ${data.content}. Accept?`;
        this.dialogProp.showDialog = true;
      } else if (data.purpose == config.OTHERS) {
        this.$store.commit("appendToNotifications", data);
      } else {
        this.$store.commit("appendToMessages", data);
      }
    },

    acceptUser() {
      let response = "<meta>accept_request</meta>::" + this.userID;
      response = makeMessage(response, config.ACCEPT_REQUEST, this.userID);
      this.ws.send(response.as_json());
      this.dialogProp.showDialog = false;
    },

    denyUser() {
      let response = "<meta>deny_request</meta>::" + this.userID;
      response = makeMessage(response, config.DENY_REQUEST, this.userID);
      this.ws.send(response.as_json());
      this.dialogProp.showDialog = false;
    },
  },
};
</script>