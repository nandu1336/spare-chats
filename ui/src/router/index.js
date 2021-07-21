import { createRouter, createWebHashHistory } from "vue-router";
import LandingPage from "../components/LandingPageComponent/index.vue";
import ChatRoom from "../components/ChatRoomComponent/index.vue";

const routes = [
  {
    path: "/",
    name: "LandingPage",
    component: LandingPage,
  },

  {
    path: "/room",
    name: "ChatRoom",
    component: ChatRoom,
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
