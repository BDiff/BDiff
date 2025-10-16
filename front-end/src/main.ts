import "./assets/main.css";

import { createApp, watchEffect } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import { i18n } from "@/utils/i18n/i18n.ts";
import { setLang } from "@/utils/storages/i18n.ts";
import { DiffModify } from "@/utils/diff/diff-modify.ts";
import { setTheme } from "@/utils/storages/page.ts";
import router from "@/router";

const pinia = createPinia();
const app = createApp(App);

watchEffect(() => {
  document.title = i18n.global.t("page_title");
  document.documentElement.lang = i18n.global.locale;
  setLang(i18n.global.locale);
});

setTheme();

app.use(router);
app.use(pinia);
app.use(i18n);
app.mount("#app");

window.mdfy = new DiffModify(); // mdfy 初始化
