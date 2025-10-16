<script setup lang="ts">
import { computed, ref } from "vue";
import { getFileContent } from "@/utils/functions.ts";
import { usePageStore } from "@/stores/page.ts";
import LyFileNormal from "@/components/icons/LyFileNormal.vue";

const pageStore = usePageStore();

const { fileKey, filename } = defineProps<{
  fileKey: string;
  filename: string;
}>();

const emit = defineEmits<{
  onChange: [file: { content: string; name: string }];
}>();

const inputId = computed(() => `fileInput_${fileKey}`);

const loading = ref<boolean>(false);

async function handleChange(e: Event) {
  loading.value = true;

  const inputEl = e.target as HTMLInputElement;
  if (!inputEl.files || inputEl.files.length === 0) return;
  const file = inputEl.files[0]!;
  const content = await getFileContent(file);

  emit("onChange", { content, name: file.name });
  inputEl.value = ""; // 清空 input，方便触发 @change
  loading.value = false;
}
</script>

<template>
  <ly-file-normal class="flex-shrink-0" :style="{ marginRight: '5px' }" /><span
    class="fw-bold flex-shrink-0 me-1"
    >{{ $t("btn_select_file_label", { filename: fileKey }) }}</span
  ><template v-if="pageStore.mode === 'normal'"
    ><label
      class="btn btn-outline-secondary text-break"
      :class="[{ disabled: loading }]"
      :for="inputId"
      ><span v-show="loading" class="spinner-border spinner-border-sm me-2"></span
      >{{ filename || $t("btn_select_file") }}</label
    ><input :id="inputId" type="file" hidden @change="handleChange" /></template
  ><template v-if="pageStore.mode === 'local'"
    ><span class="text-break">{{ filename }}</span></template
  >
</template>
