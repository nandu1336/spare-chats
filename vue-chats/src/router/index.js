import { createRouter, createWebHashHistory } from "vue-router";
import Home from "../views/Home.vue";
import RoomComponent from '../components/RoomComponent/RoomComponent';
import IntroComponent from '@/components/LandingPageComponent/IntroComponent';
import RoomFormComponent from '@/components/LandingPageComponent/RoomFormComponent';
import SuccessPromptComponent from '@/components/LandingPageComponent/SuccessPromptComponent'

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },

  {
    path: "/room",
    name: "Room",
    component: RoomComponent
  },

  {
    path: "/intro",
    name: "Intro",
    component: IntroComponent
  },

  {
    path: "/roomForm",
    name: "Room Form",
    component: RoomFormComponent
  },

  {
    path: "/successPrompt",
    name: "SuccessPrompt",
    component: SuccessPromptComponent
  }
  // {
  //   path: "/about",
  //   name: "About",
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () =>
  //     import(/* webpackChunkName: "about" */ "../views/About.vue"),
  // },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

router.beforeEach((to, from) => {
  if (to.name == "Home" && from.name == "Room") return false;
})

export default router;
