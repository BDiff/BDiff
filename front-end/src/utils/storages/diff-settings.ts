/**
 * 注意：将 key 值去掉 setting_ 就可以得到 form_key
 */

type DIFF_SETTING_BASE = {
  key: string;
  parent?: string;
};

type DIFF_SETTING_SELECT = DIFF_SETTING_BASE & {
  type: "select";
  values: string[];
  defaultValue: string;
};

type DIFF_SETTING_SWITCH = DIFF_SETTING_BASE & {
  type: "switch";
  defaultValue: boolean;
};

const DIFF_SETTING_GENERAL__GIT_DIFF_ALGO: DIFF_SETTING_SELECT = {
  type: "select",
  key: "setting_general__git_diff_algo",
  values: ["Minimal", "Myers", "Histogram", "Patience"],
  defaultValue: "Histogram",
};

const DIFF_SETTING_GENERAL__TAB_SIZE: DIFF_SETTING_SELECT = {
  type: "select",
  key: "setting_general__tab_size",
  values: initRange(1, 20, 1).map((v) => v.toString()),
  defaultValue: "4",
};

const DIFF_SETTING_UPDATES__IDENTIFY: DIFF_SETTING_SWITCH = {
  type: "switch",
  key: "setting_updates__identify",
  defaultValue: true,
};

const DIFF_SETTING_UPDATES__CTX_LENGTH: DIFF_SETTING_SELECT = {
  type: "select",
  key: "setting_updates__ctx_length",
  values: initRange(2, 10, 1).map((v) => v.toString()),
  defaultValue: "4",
  parent: "setting_updates__identify",
};

const DIFF_SETTING_UPDATES__LINE_SIM_WEIGHT: DIFF_SETTING_SELECT = {
  type: "select",
  key: "setting_updates__line_sim_weight",
  values: initRange(0, 10, 1).map((v) => (v / 10).toString()),
  defaultValue: "0.6",
  parent: "setting_updates__identify",
};

const DIFF_SETTING_UPDATES__LINE_SIM_THLD: DIFF_SETTING_SELECT = {
  type: "select",
  key: "setting_updates__line_sim_threshold",
  values: initRange(0, 10, 1).map((v) => (v / 10).toString()),
  defaultValue: "0.5",
  parent: "setting_updates__identify",
};

const DIFF_SETTING_SPLITS__IDENTIFY: DIFF_SETTING_SWITCH = {
  type: "switch",
  key: "setting_splits__identify",
  defaultValue: true,
};

const DIFF_SETTING_SPLITS__MAX_SP_LINES: DIFF_SETTING_SELECT = {
  type: "select",
  key: "setting_splits__max_split_lines",
  values: initRange(2, 20, 1).map((v) => v.toString()),
  defaultValue: "8",
  parent: "setting_splits__identify",
};

const DIFF_SETTING_MERGES__IDENTIFY: DIFF_SETTING_SWITCH = {
  type: "switch",
  key: "setting_merges__identify",
  defaultValue: true,
};

const DIFF_SETTING_MERGES__MAX_MRG_LINES: DIFF_SETTING_SELECT = {
  type: "select",
  key: "setting_merges__max_merge_lines",
  values: initRange(2, 20, 1).map((v) => v.toString()),
  defaultValue: "8",
  parent: "setting_merges__identify",
};

const DIFF_SETTING_MOVES__IDENTIFY: DIFF_SETTING_SWITCH = {
  type: "switch",
  key: "setting_moves__identify",
  defaultValue: true,
};

const DIFF_SETTING_MOVES__MIN_BLOCK_LENGTH: DIFF_SETTING_SELECT = {
  type: "select",
  key: "setting_moves__min_block_length",
  values: initRange(2, 10, 1).map((v) => v.toString()),
  defaultValue: "2",
  parent: "setting_moves__identify",
};

const DIFF_SETTING_MOVES__MAX_BLOCK_DISTANCE: DIFF_SETTING_SELECT = {
  type: "select",
  key: "setting_moves__max_block_distance",
  // 注意 Infinity 的值在 i18n 中
  values: ["Infinity", ...initRange(5, 50, 5).map((v) => v.toString())],
  defaultValue: "Infinity",
  parent: "setting_moves__identify",
};

const DIFF_SETTING_MOVES__IDENTIFY_UPDATES: DIFF_SETTING_SWITCH = {
  type: "switch",
  key: "setting_moves__identify_updates",
  defaultValue: true,
  parent: "setting_moves__identify",
};

const DIFF_SETTING_MOVES__REC_STOP_WORDS: DIFF_SETTING_SWITCH = {
  type: "switch",
  key: "setting_moves__record_stop_words",
  defaultValue: false,
  parent: "setting_moves__identify",
};

const DIFF_SETTING_COPIES__IDENTIFY: DIFF_SETTING_SWITCH = {
  type: "switch",
  key: "setting_copies__identify",
  defaultValue: true,
};

const DIFF_SETTING_COPIES__MIN_BLOCK_LENGTH: DIFF_SETTING_SELECT = {
  type: "select",
  key: "setting_copies__min_block_length",
  values: initRange(2, 10, 1).map((v) => v.toString()),
  defaultValue: "2",
  parent: "setting_copies__identify",
};

const DIFF_SETTING_COPIES__MAX_BLOCK_DISTANCE: DIFF_SETTING_SELECT = {
  type: "select",
  key: "setting_copies__max_block_distance",
  // 注意 Infinity 的值在 i18n 中
  values: ["Infinity", ...initRange(5, 50, 5).map((v) => v.toString())],
  defaultValue: "Infinity",
  parent: "setting_copies__identify",
};

const DIFF_SETTING_COPIES__IDENTIFY_UPDATES: DIFF_SETTING_SWITCH = {
  type: "switch",
  key: "setting_copies__identify_updates",
  defaultValue: true,
  parent: "setting_copies__identify",
};

const DIFF_SETTING_COPIES__REC_STOP_WORDS: DIFF_SETTING_SWITCH = {
  type: "switch",
  key: "setting_copies__record_stop_words",
  defaultValue: false,
  parent: "setting_copies__identify",
};

export const DIFF_SETTINGS = [
  DIFF_SETTING_GENERAL__GIT_DIFF_ALGO,
  DIFF_SETTING_GENERAL__TAB_SIZE,
  DIFF_SETTING_UPDATES__IDENTIFY,
  DIFF_SETTING_UPDATES__CTX_LENGTH,
  DIFF_SETTING_UPDATES__LINE_SIM_WEIGHT,
  DIFF_SETTING_UPDATES__LINE_SIM_THLD,
  DIFF_SETTING_SPLITS__IDENTIFY,
  DIFF_SETTING_SPLITS__MAX_SP_LINES,
  DIFF_SETTING_MERGES__IDENTIFY,
  DIFF_SETTING_MERGES__MAX_MRG_LINES,
  DIFF_SETTING_MOVES__IDENTIFY,
  DIFF_SETTING_MOVES__MIN_BLOCK_LENGTH,
  DIFF_SETTING_MOVES__MAX_BLOCK_DISTANCE,
  DIFF_SETTING_MOVES__IDENTIFY_UPDATES,
  DIFF_SETTING_MOVES__REC_STOP_WORDS,
  DIFF_SETTING_COPIES__IDENTIFY,
  DIFF_SETTING_COPIES__MIN_BLOCK_LENGTH,
  DIFF_SETTING_COPIES__MAX_BLOCK_DISTANCE,
  DIFF_SETTING_COPIES__IDENTIFY_UPDATES,
  DIFF_SETTING_COPIES__REC_STOP_WORDS,
] as const;

export function initRange(start: number, end: number, step: number): number[] {
  return Array.from({ length: (end - start) / step + 1 }, (_v, i) => start + i * step);
}

export type DiffSettingKey = (typeof DIFF_SETTINGS)[number]["key"];
export type DiffSettingValue = (typeof DIFF_SETTINGS)[number]["defaultValue"];

export function getDiffSetting(
  key: DiffSettingKey,
  defaultValue: DiffSettingValue,
): DiffSettingValue {
  const value = localStorage.getItem(key);
  if (value === null) return defaultValue;
  if (typeof defaultValue === "boolean") {
    return value === "true";
  } else {
    return value;
  }
}

export function setDiffSetting(key: DiffSettingKey, value: DiffSettingValue): void {
  localStorage.setItem(key, value.toString());
}
