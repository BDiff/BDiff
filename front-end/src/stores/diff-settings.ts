import { defineStore } from "pinia";
import {
  getDiffSetting,
  type DiffSettingKey,
  type DiffSettingValue,
  setDiffSetting,
  DIFF_SETTINGS,
} from "@/utils/storages/diff-settings.ts";
import { type Ref, ref } from "vue";

export const useDiffSettingsStore = defineStore("diffSettings", () => {
  const stores = Object.fromEntries(
    DIFF_SETTINGS.map((item) => [item.key, ref(getDiffSetting(item.key, item.defaultValue))]),
  ) as Record<DiffSettingKey, Ref<DiffSettingValue>>;

  function getStoreValue(key: DiffSettingKey): DiffSettingValue {
    return stores[key]!.value;
  }

  function saveStores(keyValues: Array<[DiffSettingKey, DiffSettingValue]>) {
    keyValues.forEach(([key, value]) => {
      stores[key]!.value = value;
      setDiffSetting(key, value);
    });
  }

  return {
    ...stores,
    getStoreValue,
    saveStores,
  };
});
