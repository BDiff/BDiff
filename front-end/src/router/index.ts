import { createRouter, createWebHashHistory } from "vue-router";

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: "/",
      component: () => import("@/views/PageHome.vue"),
    },
    {
      path: "/privacy_policy",
      component: () => import("@/views/PagePrivacyPolicy.vue"),
    },
  ],
});

export default router;
