<script setup lang="ts">
import { computed } from "vue";
import { useRouter } from "vue-router";
import { usePageStore } from "@/stores/page.ts";
import ThemeToggleButton from "@/components/ThemeToggleButton.vue";
import LanguageSelector from "@/components/LanguageSelector.vue";

const router = useRouter();
const pageStore = usePageStore();

const logoSrc = computed(() =>
  pageStore.theme === "light"
    ? `https://vue.learnerhub.net/diff-ly/logo.png`
    : `https://vue.learnerhub.net/diff-ly/logo-dark.png`,
);
</script>

<template>
  <header ref="header-top" class="shadow-sm bg-body-secondary sticky-top">
    <div class="px-5 py-3">
      <div class="position-relative d-flex align-items-center gap-3" :style="{ margin: '6px 0' }">
        <div class="flex-shrink-0 d-flex align-items-center">
          <div class="d-flex align-items-center gap-3" role="button" @click="router.push('/')">
            <img :src="logoSrc" alt="logo" :style="{ height: '40px', width: '40px' }" /><span
              class="fw-bold"
              :style="{ fontSize: '22px' }"
              >{{ $t("page_title") }}</span
            >
          </div>
        </div>

        <div class="position-absolute end-0 pe-auto">
          <div class="d-flex align-items-center gap-4">
            <language-selector />

            <theme-toggle-button />
          </div>
        </div>
      </div>
    </div>
  </header>

  <main>
    <div class="container">
      <div class="px-3 my-3 bg-body-secondary rounded-3 clear-table">
        <div class="my-3">
          <h1>{{ $t(`privacy_policy.title`) }}</h1>
          <div v-html="$t(`privacy_policy.content`)"></div>
        </div>
      </div>
    </div>
  </main>
</template>
