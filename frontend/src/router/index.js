import { createRouter, createWebHistory } from "vue-router";
import Index from "@/pages/Index.vue";

export const router = createRouter({
  history: createWebHistory(),
  routes: [{ path: "/", component: Index }],
});
