<script setup lang="ts">
import { computed, inject } from "vue";
import { useDiffStore } from "@/stores/diff.ts";
import { codeContainerRects } from "@/utils/injection-keys.ts";
import { formatUpdatesIntoHtmlContent } from "@/utils/diff/diff-content.ts";
import { usePageStore } from "@/stores/page.ts";

const { tlh } = inject(codeContainerRects)!;
const tdStyle = computed(() => ({
  height: `${tlh.value}px`,
  lineHeight: `${tlh.value}px`,
  paddingTop: 0,
  paddingBottom: 0,
}));

const diffStore = useDiffStore();
const pageStore = usePageStore();

const { line, activeDiff } = defineProps<{
  line: ContentLinesItem;
  activeDiff?: DiffDataItem;
}>();

/**
 * 当前高亮的 diff 数据
 */

const currentDiff = computed<DiffDataItem | undefined>(() => {
  if (activeDiff) return activeDiff;

  // block_ids 是对齐模式下的特有属性，用于给连续的差异中被插入的空行显示填充色
  const ids = diffStore.diffAlign ? line.block_ids : line.ids;

  // 跳过空行（delete、insert 的另一边）或没有diff_id的行
  if (ids.length === 0) return undefined;

  // 默认显示最后添加的脚本
  for (let i = ids.length - 1; i >= 0; i -= 1) {
    const diff = diffStore.diffDataMap.get(ids[i]!);

    // 默认情况下不显示 x_update，跳过
    if (diff && diff.mode.endsWith("_update")) {
      continue;
    }

    return diff;
  }

  return undefined;
});

/**
 * active 时显示 update 高亮
 */

const highlightContent = computed(() => {
  if (!currentDiff.value) {
    return line.content;
  }

  const strDiffSide = line.belong === "src" ? 0 : 1;

  if (currentDiff.value.mode.endsWith("update")) {
    const ranges = currentDiff.value.str_diff![strDiffSide];
    return formatUpdatesIntoHtmlContent(line.content, ranges);
  }

  if (currentDiff.value.updates && currentDiff.value.updates.length > 0) {
    const diffDataMap = Array.from(diffStore.diffDataMap);

    for (const [line1, line2] of currentDiff.value.updates) {
      if (
        (strDiffSide === 0 && line.number === line1) ||
        (strDiffSide === 1 && line.number === line2)
      ) {
        const mapItem = diffDataMap.find(
          ([, diff]) =>
            diff.mode.endsWith("_update") && diff.src_line === line1 && diff.dest_line === line2,
        );
        if (!mapItem) continue;
        return formatUpdatesIntoHtmlContent(line.content, mapItem[1].str_diff![strDiffSide]);
      }
    }
  }

  return line.content;
});
</script>

<template>
  <tr
    :style="{
      backgroundColor: currentDiff
        ? `var(--diff-${currentDiff.mode})`
        : `var(${pageStore.theme === 'light' ? '--bs-tertiary-bg' : '--bs-body-bg'})`,
      color: 'var(--bs-body-color)',
    }"
  >
    <td
      class="blob-line"
      :style="tdStyle"
      :data-line-number="line.number?.toString() ?? undefined"
    ></td>
    <td class="blob-code overflow-hidden" :style="tdStyle">
      <span
        class="position-relative"
        :style="{ left: `var(--x-scroll)` }"
        v-html="highlightContent || '\uFEFF'"
      ></span>
    </td>
  </tr>
</template>
