import { createStore } from "vuex";

export default createStore({
  state: {
    ws: "",
    roomName: "Temporary Room",
    messages: [],
  },
  mutations: {

    setWebSocket(state, ws) {
      state.ws = ws;
    },

    setRoomName(state, name) {
      state.roomName = name;
    },

    appendToMessages(state, messages) {
      console.log("message in store:", messages);
      state.messages.push(messages);
      console.log("store.messages length:", state.messages.length);
    }
  },
  actions: {},
  modules: {},
});
