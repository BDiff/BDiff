<script setup lang="ts">
import BiChevronRight from "@/components/icons/BiChevronRight.vue";
import BiChevronLeft from "@/components/icons/BiChevronLeft.vue";
import { computed, nextTick, onBeforeUnmount, onMounted, ref, useTemplateRef, watch } from "vue";
import { usePageStore } from "@/stores/page.ts";
import { throttle } from "lodash";
import { i18n } from "@/utils/i18n/i18n.ts";

const pageStore = usePageStore();

/**
 * 侧边栏尺寸
 */

const sidebarVisible = ref(true);
const sidebarTop = computed(() => pageStore.headerBottom);
const sidebarWidth = ref<number>(400);

function handleDragLineMousedown(mousedownEvent: MouseEvent) {
  const WIDTH_MIN = 200; // px
  const WIDTH_MAX = window.innerWidth / 2;
  const startWidth = sidebarWidth.value;
  const startX = mousedownEvent.clientX;

  function handleMousemove(mousemoveEvent: MouseEvent) {
    const endX = mousemoveEvent.clientX;
    const moveX = startX - endX;
    const endWidth = startWidth - moveX;

    if (endWidth < WIDTH_MIN) {
      sidebarWidth.value = WIDTH_MIN;
    } else if (endWidth > WIDTH_MAX) {
      sidebarWidth.value = WIDTH_MAX;
    } else {
      sidebarWidth.value = endWidth;
    }
  }

  function handleMouseup() {
    window.removeEventListener("mousemove", handleMousemove);
    window.removeEventListener("mouseup", handleMouseup);
  }

  window.addEventListener("mousemove", handleMousemove);
  window.addEventListener("mouseup", handleMouseup);
}

/**
 * 侧边栏交互
 */

type HeadingsItem = {
  id: string;
  indent: number;
  text: string;
  targetEl: HTMLElement;
};

const headings = ref<Array<HeadingsItem>>([]);

const realHeadings = computed(() => {
  const min = Math.min(...headings.value.map((h) => h.indent));
  return headings.value.map((h) => ({ ...h, indent: h.indent - min }));
});

const readmeContainerRef = useTemplateRef("readme-container");
const activeHeading = ref<HeadingsItem | null>(null);

onMounted(() => {
  nextTick(() => {
    initHeadings(readmeContainerRef.value);
    window.addEventListener("scroll", throttleScrollHandler);
  });
});

onBeforeUnmount(() => {
  window.removeEventListener("scroll", throttleScrollHandler);
});

watch(
  () => i18n.global.locale,
  () => {
    nextTick(() => initHeadings(readmeContainerRef.value));
  },
);

function initHeadings(readmeContainerEl: HTMLElement | null): void {
  headings.value = [];
  if (!readmeContainerEl) return;
  readmeContainerEl
    .querySelectorAll<HTMLElement>("h1, h2, h3, h4, h5, h6")
    .forEach((headingEl, index) => {
      headings.value.push({
        id: `${new Date().getTime()}-${index}`,
        indent: Number(headingEl.tagName.replace(/\D/g, "")) || 0,
        text: headingEl.innerText,
        targetEl: headingEl,
      });
    });

  const min = Math.min(...headings.value.map((h) => h.indent));
  headings.value.forEach((h) => (h.indent -= min));
}

const throttleScrollHandler = throttle(scrollHandler, 50);
function scrollHandler() {
  const tops = headings.value.map(({ targetEl }) => targetEl.getBoundingClientRect().top);
  const firstIndex = tops.findIndex((top) => top - pageStore.headerBottom > 0);
  if (firstIndex === -1) {
    return (activeHeading.value = null);
  }
  if (tops[firstIndex]! - window.innerHeight >= -10) {
    const activeItem = headings.value[firstIndex - 1];
    return (activeHeading.value = activeItem || null);
  }
  activeHeading.value = headings.value[firstIndex]!;
}

const CLASSIC_CASES = [
  {
    title: "Changing the order of parameter and member variable assignments",
    repo: "pyxel",
    sha: "3861523a200da507f36edf478729f4ec7c269775",
    filename: "app.py",
  },
  {
    title: "Moving the try statement block",
    repo: "requests",
    sha: "cde3b88f3e93a9503810acc0ded890025fcbc119",
    filename: "core.py",
  },
  {
    title: "Adding conditional judgment",
    repo: "ansible",
    sha: "3807824c6d0dae63b9f36dbafe8e100b0a3beaa6",
    filename: "__init__.py",
  },
  {
    title: "Reusing interface elements",
    repo: "magisk",
    sha: "fc5c9647d829cad1b73338e42164decc4ab08a54",
    filename: "drawer.xml",
  },
  {
    title: "Copying function implementation",
    repo: "keras",
    sha: "aa7f9cdae951bba824883cfa392224a292b284bb",
    filename: "core.py",
  },
  {
    title: "Reuse test functions",
    repo: "black",
    sha: "e911c79809c4fd9b0773dea5b6a0e710b59614cf",
    filename: "test_black.py",
  },
  {
    title: "Line splits and block moves",
    repo: "wagtail",
    sha: "a2a580f0fe7a1354a109eb062b5393fbb330f508",
    filename: "urls.py",
  },
  {
    title: "Block copies and block moves",
    repo: "okhttp",
    sha: "c8638813ff5f90715417e489b342aae5e410c5b2",
    filename: "pom.xml",
  },
  {
    title: "Converting spaces to indentation",
    repo: "scikit-learn",
    sha: "612312553118371289330f50b38653d1206246c0",
    filename: "gene.py",
  },
] as const;
const caseImages = CLASSIC_CASES.map(
  (c) => `http://test.bdiff.net/public/${c.repo}-${c.sha}-${c.filename}.png`,
);

const showCasePreview = ref<boolean>(false);
const showCasePreviewIndex = ref<number>(0);
</script>

<template>
  <div ref="readme-container" class="readme-container">
    <p v-html="$t('readme.desc')"></p>
    <h4 v-html="$t('readme.heading_one.1') + $t('readme.chapter_major_function.title')"></h4>
    <div v-html="$t('readme.chapter_major_function.content')"></div>
    <h4 v-html="$t('readme.heading_one.2') + $t('readme.chapter_instructions.title')"></h4>
    <h5 v-html="'2.1 ' + $t('readme.chapter_instructions.quick_start.title')"></h5>
    <div v-html="$t('readme.chapter_instructions.quick_start.content')"></div>
    <h5 v-html="'2.2 ' + $t('readme.chapter_instructions.settings.title')"></h5>
    <div v-html="$t('readme.chapter_instructions.settings.content')"></div>
    <h4 v-html="$t('readme.heading_one.3') + $t('readme.chapter_classic_cases.title')"></h4>
    <div class="row" :style="{ '--bs-gutter-x': '1.5rem', '--bs-gutter-y': '1.5rem' }">
      <div v-for="(item, i) in CLASSIC_CASES" :key="item.title" class="col-4">
        <div
          class="h-100 clear-table rounded-4 overflow-hidden case-item"
          :style="{ cursor: 'pointer' }"
          @click="
            () => {
              showCasePreviewIndex = i;
              showCasePreview = true;
            }
          "
        >
          <el-image :src="caseImages[i]" fit="cover" :style="{ height: '200px', width: '100%' }" />
          <div class="px-3" :style="{ paddingBottom: '4px' }">
            <h5 class="text-center my-3">
              3.{{ i + 1 }} {{ $t(`readme.chapter_classic_cases.case_titles.${item.title}`) }}
            </h5>
            <div class="my-2 text-secondary small text-break">
              <span>{{ $t("readme.repo") }}{{ $t("symbol_colon") }}{{ item.repo }}</span>
            </div>
            <div class="my-2 text-secondary small text-break">
              <span>{{ $t("readme.commit") }}{{ $t("symbol_colon") }}{{ item.sha }}</span>
            </div>
            <div class="my-2 text-secondary small text-break">
              <span>{{ $t("readme.filename") }}{{ $t("symbol_colon") }}{{ item.filename }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <el-image-viewer
      v-if="showCasePreview"
      :url-list="caseImages"
      :initial-index="showCasePreviewIndex"
      :zoom-rate="1.2"
      :max-scale="2"
      :min-scale="0.5"
      @close="() => (showCasePreview = false)"
    >
      <template #progress="{ activeIndex }">
        <div
          class="text-bg-secondary px-3 py-2 rounded-3"
          :style="{ cursor: 'auto', userSelect: 'text' }"
        >
          <div class="text-center fw-bold">
            <span
              >3.{{ activeIndex + 1 }}
              {{
                $t(`readme.chapter_classic_cases.case_titles.${CLASSIC_CASES[activeIndex]!.title}`)
              }}</span
            >
          </div>
          <div class="text-center small">
            <span
              >{{ CLASSIC_CASES[activeIndex]!.repo }}-{{ CLASSIC_CASES[activeIndex]!.sha }}-{{
                CLASSIC_CASES[activeIndex]!.filename
              }}</span
            >
          </div>
        </div>
      </template>
    </el-image-viewer>
    <h4 v-html="$t('readme.heading_one.4') + $t('readme.chapter_contributors.title')"></h4>
    <div v-html="$t('readme.chapter_contributors.content')"></div>
    <h4 v-html="$t('readme.heading_one.5') + $t('readme.chapter_contribution.title')"></h4>
    <div v-html="$t('readme.chapter_contribution.content')"></div>
    <h4 v-html="$t('readme.heading_one.6') + $t('readme.chapter_licenses.title')"></h4>
    <div v-html="$t('readme.chapter_licenses.content')"></div>
    <div class="bg-light">
      <pre class="p-3"><code>Copyright (c) [2025] [Lu YAO]
BDiff is licensed under Mulan PubL v2.
You can use this software according to the terms and conditions of the Mulan PubL v2.
You may obtain a copy of Mulan PubL v2 at:
         http://openworks.org.cn/#/licenses/MulanPubL-v2
THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
See the Mulan PubL v2 for more details.
</code></pre>
    </div>
  </div>

  <div
    class="offcanvas offcanvas-start border-0 shadow bg-body-secondary text-body-secondary visible"
    :class="[{ show: sidebarVisible }]"
    :style="{
      top: `${sidebarTop - 20}px`,
      paddingTop: `20px`,
      width: `${sidebarWidth}px`,
    }"
  >
    <div class="offcanvas-body px-0">
      <el-scrollbar class="px-3">
        <div
          v-for="item in realHeadings"
          :key="item.id"
          class="py-2 hover-item"
          :style="{ paddingLeft: `${item.indent * 20}px`, cursor: 'pointer' }"
          @click="() => item.targetEl.scrollIntoView({ block: 'center' })"
        >
          <span :class="[{ 'text-primary': item.id === activeHeading?.id }]">{{ item.text }}</span>
        </div>
      </el-scrollbar>
    </div>

    <div @mousedown="handleDragLineMousedown" class="offcanvas-drag-line"></div>

    <div
      class="drawer-toggle-button bg-body-secondary lh-sm"
      style="box-shadow: 0.125rem 0 0.25rem rgba(var(--bs-body-color-rgb), 0.15) !important"
      @click="() => (sidebarVisible = !sidebarVisible)"
    >
      <div>
        <bi-chevron-left v-if="sidebarVisible" />
        <bi-chevron-right v-else />
      </div>
      <div class="mt-1 label-edit-script" style="overflow-wrap: break-word">
        {{ $t("btn_readme_directory") }}
      </div>
    </div>
  </div>
</template>

<style>
.readme-container img {
  width: 100%;
}

.readme-container p {
  margin: 1em 0;
}

.readme-container h1,
.readme-container h2,
.readme-container h3,
.readme-container h4,
.readme-container h5,
.readme-container h6 {
  font-weight: bold;
  margin: 1em 0;
}

.readme-container .case-item {
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1);
}

.readme-container .case-item:hover {
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.25);
}

.readme-container .case-item > .el-image > .el-image__inner {
  transform: scale(1) translateZ(0);
  transition: transform 0.75s;
}
.readme-container .case-item:hover > .el-image > .el-image__inner {
  transform: scale(1.1);
  transition: transform 0.75s cubic-bezier(0, 1, 0.75, 1);
}

.readme-container .el-image-viewer__img {
  cursor: grab;
}
.readme-container .el-image-viewer__img:active {
  cursor: grabbing;
}
</style>
