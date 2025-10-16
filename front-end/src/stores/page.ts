import { defineStore } from "pinia";
import { ref } from "vue";
import { useFilesStore } from "@/stores/files.ts";
import { useDiffStore } from "@/stores/diff.ts";
import { getGithubFiles, getGithubFilesContents } from "@/utils/requests.ts";
import { getTheme } from "@/utils/storages/page.ts";
import { i18n } from "@/utils/i18n/i18n.ts";

export const usePageStore = defineStore("page", () => {
  const filesStore = useFilesStore();
  const diffStore = useDiffStore();

  /**
   * 是否测试版
   */
  const isTest = ref<boolean>(location.hostname.startsWith("test"));

  /**
   * 页面主题
   */
  const theme = ref<Theme>(getTheme());

  /**
   * 页头底部位置
   */
  const headerBottom = ref<number>(0);

  function setHeaderBottom(val: number) {
    headerBottom.value = val;
  }

  /**
   * 页面模式
   */
  const mode = ref<PageMode>("normal");

  function setMode(newMode: PageMode) {
    mode.value = newMode;
  }

  /**
   * 尝试初始化
   */
  if (
    typeof window.content1 === "string" &&
    typeof window.content2 === "string" &&
    typeof window.filename1 === "string" &&
    typeof window.filename2 === "string" &&
    Array.isArray(window.diffJson)
  ) {
    setMode("local");
    filesStore.setFile1({ content: window.content1, name: window.filename1 });
    filesStore.setFile2({ content: window.content2, name: window.filename2 });
    diffStore.setDiffDataMap(new Map(window.diffJson.map((item, index) => [index, item])));
    diffStore.run({ repaint: true }).finally(() => {});
  }

  /**
   * 尝试初始化 github
   */

  const githubLink = ref<string>("");
  const githubFiles = ref<Array<GithubFilesItem>>([]);
  const query = Object.fromEntries(new URLSearchParams(window.location.search));
  const { owner, repo, installation_id, pr_number } = query;

  if (owner && repo && installation_id && pr_number) {
    setMode("github");
    githubLink.value = `https://github.com/${owner}/${repo}/pull/${pr_number}`;
  }

  async function runGithub(filename?: string) {
    diffStore.setLoading(true);

    if (!filename) {
      try {
        githubFiles.value = await getGithubFiles({
          owner: owner!,
          repo: repo!,
          installation_id: installation_id!,
          pr_number: pr_number!,
        });
      } catch (_e) {
        diffStore.setLoading(false);
        return;
      }
    }

    let githubFilesContents: { base_file: string; head_file: string };
    filename = filename ?? githubFiles.value.find((f) => f.status === "modified")?.filename;

    if (!filename) {
      ElMessage.warning(i18n.global.t("diff_no_github_modified_file"));
      diffStore.setLoading(false);
      return;
    }

    try {
      githubFilesContents = await getGithubFilesContents({
        owner: owner!,
        repo: repo!,
        installation_id: installation_id!,
        pr_number: pr_number!,
        filename,
      });
    } catch (_e) {
      diffStore.setLoading(false);
      return;
    }

    filesStore.setFile1({ content: githubFilesContents.base_file, name: filename });
    filesStore.setFile2({ content: githubFilesContents.head_file, name: filename });

    diffStore.run().finally(() => {});
    diffStore.setLoading(false);
  }

  return {
    theme,
    isTest,
    mode,
    githubLink,
    githubFiles,
    runGithub,
    headerBottom,
    setHeaderBottom,
  };
});
