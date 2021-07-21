import { createStore } from "vuex";

export default createStore({
  state: {
    ws: "",
    roomDetails: {},
    userDetails: {},
    messages: [],
    notificatioins: [],
  },
  mutations: {

    setWebSocket(state, ws) {
      state.ws = ws;
    },

    setRoomDetails(state, roomDetails) {
      console.log("roomdetails in store:", roomDetails);
      state.roomDetails = roomDetails;
      console.log("state.roomDetails:", state.roomDetails);
    },

    appendToMessages(state, messages) {
      state.messages.push(messages);
      console.log("store.messages length:", state.messages.length);
    },

    appendToNotifications(state, notifications) {
      state.notificatioins.push(notifications);
    },

    setUserDetails(state, userDetails) {
      state.userDetails = userDetails;
    }

  },
  actions: {},
  modules: {},
});
