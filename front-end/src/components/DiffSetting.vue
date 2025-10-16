<script setup lang="ts">
import { ref } from "vue";
import { DIFF_SETTINGS } from "@/utils/storages/diff-settings.ts";
import { useDiffSettingsStore } from "@/stores/diff-settings.ts";
import { useDiffStore } from "@/stores/diff.ts";
import BiGear from "@/components/icons/BiGear.vue";
import { useFilesStore } from "@/stores/files.ts";

const diffSettingsStore = useDiffSettingsStore();
const filesStore = useFilesStore();
const { run } = useDiffStore();

const drawer = ref<boolean>(false);

const settingRefs = ref(
  DIFF_SETTINGS.map((item) => ({
    type: item.type,
    key: item.key,
    id: `id-${item.key}`,
    value: diffSettingsStore.getStoreValue(item.key),
    values: "values" in item ? item.values : undefined,
    defaultValue: item.defaultValue,
    parent: item?.parent,
  })),
);

function handleConfirm() {
  diffSettingsStore.saveStores(settingRefs.value.map((item) => [item.key, item.value]));
  const { file1, file2 } = filesStore;
  if (file1.name && file2.name) run();
  drawer.value = false;
}

function handleReset(options: { initial: boolean }) {
  const { initial } = options;

  settingRefs.value.forEach((item) => {
    item.value = initial ? item.defaultValue : diffSettingsStore.getStoreValue(item.key);
  });
  document
    .getElementById(settingRefs.value[0]!.id)
    ?.closest(".el-drawer__body")
    ?.scrollTo({ top: 0, behavior: "smooth" });
}
</script>

<template>
  <button class="btn p-0" :style="{ lineHeight: 1 }" @click="drawer = !drawer">
    <bi-gear class="fs-4" />
  </button>

  <el-drawer
    v-model="drawer"
    direction="rtl"
    size="400px"
    :style="{
      '--el-drawer-bg-color': 'var(--bs-secondary-bg)',
      color: 'var(--bs-offcanvas-color)',
    }"
    header-class="drawer-header"
    @close="handleReset({ initial: false })"
  >
    <template #header>
      <span class="fs-5 fw-bold">{{ $t("diff_setting") }}</span>
    </template>

    <template #default>
      <template v-for="item in settingRefs" :key="item.id">
        <div
          v-if="!item.parent || settingRefs.find((v) => v.key === item.parent)?.value === true"
          class="mb-3"
          :class="{ 'ps-4': item.parent }"
        >
          <template v-if="item.type === 'select'">
            <label
              :for="item.id"
              class="form-label"
              :style="{ fontSize: item.parent ? undefined : '17px' }"
              >{{ $t(item.key) }}</label
            >
            <select
              v-model="item.value"
              :id="item.id"
              class="form-select"
              :style="{ '--bs-form-control-bg': 'white' }"
            >
              <option v-for="v in item.values" :key="v" :value="v">{{ v }}</option>
            </select>
          </template>

          <template v-if="item.type === 'switch'">
            <div class="form-check form-switch is-reverse">
              <input
                v-model="item.value"
                type="checkbox"
                class="form-check-input"
                role="switch"
                :id="item.id"
              />
              <label
                :for="item.id"
                class="form-check-label"
                :style="{ fontSize: item.parent ? undefined : '17px' }"
                >{{ $t(item.key) }}</label
              >
            </div>
          </template>
        </div>
      </template>
    </template>

    <template #footer>
      <div class="d-flex justify-content-between">
        <button class="btn btn-light rounded-5 px-4" @click="handleReset({ initial: true })">
          {{ $t("btn_reset") }}
        </button>

        <button class="btn btn-primary rounded-5 px-4" @click="handleConfirm">
          {{ $t("btn_confirm") }}
        </button>
      </div>
    </template>
  </el-drawer>
</template>
