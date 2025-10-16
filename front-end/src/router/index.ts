import { createRouter, createWebHashHistory } from "vue-router";

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: "/",
      component: () => import("@/views/PageHome.vue"),
    },
    {
      path: "/security-policy",
      component: () => import("@/views/PageSecurityPolicy.vue"),
    },
  ],
});

export default router;
