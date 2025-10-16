<script setup lang="ts">
import { computed, useTemplateRef } from "vue";
import CodeTableTr from "@/components/code-container/CodeTableTr.vue";
import { useDiffStore } from "@/stores/diff.ts";
import { findLastIndex } from "lodash";
import { usePageStore } from "@/stores/page.ts";

const pageStore = usePageStore();
const diffStore = useDiffStore();

const { cLines, xScroll } = defineProps<{
  cLines: Array<ContentLinesItem>;
  xScroll: number;
  visibleRows?: [number, number];
}>();

const tableRef = useTemplateRef("table");
defineExpose({ tableRef });

/**
 * 高亮处理（放在 tr 中会太多次调用）
 */

const currentDiffId = computed(() => diffStore.dialogDiffId || diffStore.activeDiffId);
const activeDiff = computed(() =>
  currentDiffId.value ? diffStore.diffDataMap.get(currentDiffId.value) : undefined,
);
function findLineIndexFn(line: ContentLinesItem): boolean {
  if (!currentDiffId.value) return false;
  return !!(line.number && line.ids.includes(currentDiffId.value));
}
const activeLineIndexesRange = computed(() => [
  cLines.findIndex(findLineIndexFn),
  findLastIndex(cLines, findLineIndexFn),
]);
</script>

<template>
  <table ref="table" :style="{ '--x-scroll': `-${xScroll}px` }">
    <colgroup>
      <col :style="{ width: '40px' }" />
      <col />
    </colgroup>
    <tbody>
      <code-table-tr
        v-for="(line, i) in cLines"
        :key="`${i}_${line.toString()}`"
        :line="line"
        :active-diff="
          i >= activeLineIndexesRange[0]! && i <= activeLineIndexesRange[1]! ? activeDiff : undefined
        "
        :title="
          pageStore.isTest
            ? `表格第 ${i} 行，ids=[${line.ids}]，block_ids=[${line.block_ids}]`
            : undefined
        "
        v-bind="Object.fromEntries(line.ids.map((id) => [`data-id-${id}`, id]))"
      />
    </tbody>
  </table>
</template>
