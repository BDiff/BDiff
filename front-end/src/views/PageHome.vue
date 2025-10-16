<script setup lang="ts">
import FileSelectItem from "@/components/FileSelectItem.vue";
import LanguageSelector from "@/components/LanguageSelector.vue";
import DiffSetting from "@/components/DiffSetting.vue";
import { useFilesStore } from "@/stores/files.ts";
import { useDiffStore } from "@/stores/diff.ts";
import RootReadme from "@/components/RootReadme.vue";
import DiffLegendItems from "@/components/DiffLegendItems.vue";
import DiffDisplayAlignedSwitch from "@/components/DiffDisplayAlignedSwitch.vue";
import CodeContainer from "@/components/code-container/CodeContainer.vue";
import { computed, nextTick, onBeforeUnmount, onMounted, provide, useTemplateRef } from "vue";
import { throttle } from "lodash";
import DiffScriptsSidebar from "@/components/DiffScriptsSidebar.vue";
import { mainCodeContainerComponent } from "@/utils/injection-keys.ts";
import { usePageStore } from "@/stores/page.ts";
import GithubFilesSelector from "@/components/GithubFilesSelector.vue";
import PageMenuContainer from "@/components/page-menu/PageMenuContainer.vue";
import ThemeToggleButton from "@/components/ThemeToggleButton.vue";

const fileStore = useFilesStore();
const diffStore = useDiffStore();
const pageStore = usePageStore();

/**
 * 只绑定一次的 activeId 事件
 */

function handleMousemove(e: MouseEvent) {
  const diffLine: HTMLElement | null = e.target && (e.target as Element).closest("[data-line-id]");
  const id = diffLine?.dataset.lineId; // 注意 lineId 和 diffId 是对应的
  diffStore.setActiveDiffId(id ? Number(id) : null);
}

const throttleMousemove = throttle(handleMousemove, 50);

onMounted(() => window.addEventListener("mousemove", throttleMousemove));
onBeforeUnmount(() => window.removeEventListener("mousemove", throttleMousemove));

/**
 * 控制 dialog_diff
 */

const dialogDiffVisible = computed(() => {
  const diff = diffStore.diffDataMap.get(diffStore.dialogDiffId!);
  return diff && diff.mode !== "delete" && diff.mode !== "insert";
});

/**
 * 脚本左侧边栏 top 计算
 */

const headerRef = useTemplateRef("header");

function handleScroll() {
  const top = headerRef.value?.getBoundingClientRect().bottom || 0;
  const topMin = headerStickyTopRef.value?.getBoundingClientRect().bottom || 0;
  pageStore.setHeaderBottom(top < topMin ? topMin : top);
}

onMounted(() => {
  nextTick(() => {
    handleScroll();
    window.addEventListener("scroll", handleScroll);
  });
});
onBeforeUnmount(() => window.removeEventListener("scroll", handleScroll));

/**
 * 提供 mainCodeContainer
 */

const mainCodeContainerRef = useTemplateRef("main-code-container");
provide(mainCodeContainerComponent, mainCodeContainerRef);

const isLinesValid = computed(() => diffStore.f1Lines.length > 0 || diffStore.f1Lines.length > 0);

/**
 * header-sticky-top
 */

const headerStickyTopRef = useTemplateRef("header-top");
const headerBottomToStickyTopBottom = computed(
  () => pageStore.headerBottom - (headerStickyTopRef.value?.getBoundingClientRect().bottom || 0),
);

/**
 * theme 相关
 */
const logoSrc = computed(() =>
  pageStore.theme === "light"
    ? `https://vue.learnerhub.net/diff-ly/logo.png`
    : `https://vue.learnerhub.net/diff-ly/logo-dark.png`,
);
</script>

<template>
  <!-- header z-index 用于覆盖在差异脚本侧边栏之上 -->
  <header
    ref="header-top"
    class="position-fixed top-0 start-0 end-0"
    :class="{
      'shadow-sm bg-body-secondary': headerBottomToStickyTopBottom <= 0,
      'pe-none': headerBottomToStickyTopBottom > 10,
    }"
    :style="{ zIndex: 2002 }"
  >
    <div class="px-5 py-3">
      <div class="position-relative d-flex align-items-center gap-3" :style="{ margin: '6px 0' }">
        <div
          class="flex-shrink-0 d-flex align-items-center"
          :class="[{ transition: 'opacity 0.5s ease-in-out' }]"
          :style="{ opacity: (100 - headerBottomToStickyTopBottom) / 100 }"
        >
          <div class="d-flex align-items-center gap-3" role="button" @click="diffStore.clearDiff()">
            <img :src="logoSrc" alt="logo" :style="{ height: '40px', width: '40px' }" /><span
            class="fw-bold"
            :style="{ fontSize: '22px' }"
          >{{ $t("page_title") }}</span
          >
          </div>
        </div>

        <div
          v-if="!diffStore.loading && isLinesValid"
          class="flex-shrink-0 header-top-legends bg-body-secondary p-3"
          :class="[{ transition: 'opacity 0.5s ease-in-out;' }]"
          :style="{ opacity: (100 - headerBottomToStickyTopBottom) / 100 }"
        >
          <div class="d-flex align-items-center justify-content-center gap-3">
            <diff-legend-items />
          </div>
        </div>

        <div class="position-absolute end-0 pe-auto">
          <div class="d-flex align-items-center gap-4">
            <language-selector />

            <theme-toggle-button />

            <diff-setting v-if="pageStore.mode !== 'local'" />
          </div>
        </div>
      </div>
    </div>
  </header>

  <header
    ref="header"
    class="position-relative bg-body-secondary shadow-sm clear-table"
    :style="{ zIndex: 2001 }"
  >
    <div class="px-5" :style="{ opacity: headerBottomToStickyTopBottom / 100 }">
      <div class="my-5 d-flex justify-content-center">
        <div
          class="d-flex align-items-center justify-content-center gap-3"
          role="button"
          @click="diffStore.clearDiff()"
        >
          <img :src="logoSrc" alt="logo" :style="{ height: '60px', width: '60px' }" /><span
          class="fs-2 fw-bold"
        >{{ $t("page_title") }}</span
        >
        </div>
      </div>

      <template v-if="pageStore.mode === 'github'">
        <div class="my-4 row justify-content-center">
          <div class="col-4">
            <div class="mb-1">
              <a :href="pageStore.githubLink" target="_blank">{{ pageStore.githubLink }}</a>
            </div>

            <github-files-selector />
          </div>
        </div>
      </template>

      <template v-else>
        <div class="my-4 row">
          <div class="col d-flex align-items-center justify-content-end">
            <file-select-item
              file-key="1"
              :filename="fileStore.file1.name"
              @on-change="fileStore.setFile1"
            />
          </div>

          <div class="col d-flex align-items-center justify-content-start">
            <file-select-item
              file-key="2"
              :filename="fileStore.file2.name"
              @on-change="fileStore.setFile2"
            />
          </div>
        </div>

        <div v-if="pageStore.mode === 'normal'" class="my-4 d-flex justify-content-center">
          <button type="button" class="btn btn-primary rounded-5 px-4" @click="diffStore.run()">
            <span v-if="diffStore.loading" class="spinner-border spinner-border-sm me-2"></span
            ><span>{{ $t("btn_request_diff") }}</span>
          </button>
        </div>
      </template>
    </div>
  </header>

  <main>
    <div class="container">
      <div class="px-3 my-3 bg-body-secondary rounded-3 clear-table">
        <template v-if="!diffStore.loading && isLinesValid">
          <div
            class="my-3 position-relative d-flex align-items-center justify-content-center gap-3"
          >
            <diff-legend-items />

            <div class="position-absolute end-0 d-flex align-items-center">
              <diff-display-aligned-switch />
            </div>
          </div>

          <div class="my-3">
            <code-container ref="main-code-container" />
          </div>
        </template>

        <template v-else-if="pageStore.mode !== 'github' && !diffStore.loading && !isLinesValid">
          <div class="rounded-top-3 overflow-hidden" :style="{ margin: '0 -16px' }">
            <img
              src="http://test.bdiff.net/public/readme-cover.png"
              alt="cover"
              class="w-100"
              :style="{ height: '300px', objectFit: 'cover', objectPosition: '50% bottom' }"
            />
          </div>
          <div class="my-3">
            <root-readme />
          </div>
        </template>
      </div>
    </div>
  </main>

  <page-menu-container v-show="diffStore.diffDataMap.size > 0" />

  <diff-scripts-sidebar />

  <el-dialog
    :model-value="dialogDiffVisible"
    :width="1320"
    :align-center="true"
    body-class="dialog-diff-body-class"
    @closed="() => diffStore.setDialogDiffId(null)"
  >
    <code-container v-if="dialogDiffVisible" :focus-id="diffStore.dialogDiffId!" />
  </el-dialog>
</template>

<style>
.dialog-diff-body-class {
  min-height: 150px;
  display: flex;
  align-items: center;
}
.dialog-diff-body-class .code-container {
  width: 100%;
}

.header-top-legends {
  display: none;
}

@media (min-width: 1340px) {
  .header-top-legends {
    display: block;
    position: absolute;
    left: 50%;
    transform: translate(-50%, 0);
    text-wrap: nowrap;
  }
}
</style>
