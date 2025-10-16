import { findLastIndex } from "lodash";

/**
 * 将 content 拆解成 contentLines
 */
export function formatContentToContentLines(
  content: string,
  belong: ContentLinesItem["belong"],
): Array<ContentLinesItem> {
  return content
    .split(/\r\n|\n/)
    .map((string, index) => initContentLine(belong, { number: index + 1, content: string }));
}

/**
 * 把 diff 信息写入每行
 *
 * 注意不能直接传入 ref.value 值，需要 toRow(ref.value)
 */
export function formatDiffDataIntoContentLines(
  f1Lines: Array<ContentLinesItem>,
  f2Lines: Array<ContentLinesItem>,
  diffDataMap: DiffDataMap,
): { lines1: Array<ContentLinesItem>; lines2: Array<ContentLinesItem> } {
  const lines1 = f1Lines.slice();
  const lines2 = f2Lines.slice();

  for (const [id, diff] of diffDataMap) {
    // 只取这三个最好理解的、不容易参数重名的
    const {
      src_line,
      dest_line,
      block_length = 1, // 部分脚本没有连续行，默认为 1 行
    } = diff;

    let lines1StartIndex: number | undefined = undefined;
    let lines1EndIndex: number | undefined = undefined;
    let lines2StartIndex: number | undefined = undefined;
    let lines2EndIndex: number | undefined = undefined;

    switch (diff.mode) {
      case "delete": {
        lines1StartIndex = lines1.findIndex((line) => line.number === src_line);
        lines1EndIndex = lines1StartIndex + block_length - 1;
        break;
      }
      case "insert": {
        lines2StartIndex = lines2.findIndex((line) => line.number === dest_line);
        lines2EndIndex = lines2StartIndex + block_length - 1;
        break;
      }
      case "move":
      case "copy":
      case "update":
      case "m_update":
      case "c_update": {
        lines1StartIndex = lines1.findIndex((line) => line.number === src_line);
        lines1EndIndex = lines1StartIndex + block_length - 1;
        lines2StartIndex = lines2.findIndex((line) => line.number === dest_line);
        lines2EndIndex = lines2StartIndex + block_length - 1;
        break;
      }

      case "split": {
        lines1StartIndex = lines1.findIndex((line) => line.number === src_line);
        lines1EndIndex = lines1StartIndex;
        lines2StartIndex = lines2.findIndex((line) => line.number === dest_line);
        lines2EndIndex = lines2StartIndex + block_length - 1;
        break;
      }

      case "merge": {
        lines1StartIndex = lines1.findIndex((line) => line.number === src_line);
        lines1EndIndex = lines1StartIndex + block_length - 1;
        lines2StartIndex = lines2.findIndex((line) => line.number === dest_line);
        lines2EndIndex = lines2StartIndex;
        break;
      }

      default: {
        console.warn(`未识别的 mode: ${diff.mode}`);
        break;
      }
    }

    if (
      lines1StartIndex !== undefined &&
      lines1StartIndex > -1 &&
      lines1EndIndex !== undefined &&
      lines1EndIndex > -1
    ) {
      for (let i = lines1StartIndex; i <= lines1EndIndex; i += 1) {
        lines1[i]!.ids.push(id);
      }
    }
    if (
      lines2StartIndex !== undefined &&
      lines2StartIndex > -1 &&
      lines2EndIndex !== undefined &&
      lines2EndIndex > -1
    ) {
      for (let i = lines2StartIndex; i <= lines2EndIndex; i += 1) {
        lines2[i]!.ids.push(id);
      }
    }
  }

  return { lines1, lines2 };
}

/**
 * 处理对齐
 *
 * 注意不能直接传入 ref.value 值，需要 toRow(ref.value)
 */
export function formatContentLinesToAlign(
  f1Lines: Array<ContentLinesItem>,
  f2Lines: Array<ContentLinesItem>,
  diffDataMap: DiffDataMap,
): { lines1: Array<ContentLinesItem>; lines2: Array<ContentLinesItem> } {
  /**
   * 末尾插入一个空行，避免对齐出错。最后再删掉
   * /public/blank_line_required_at_the_end.png
   */

  const lines1 = f1Lines.concat(initContentLine("src"));
  const lines2 = f2Lines.concat(initContentLine("dest"));

  /**
   * 先处理可以按行号插入、不会相互交叉的脚本：删除、新增、分割、合并
   */
  for (const [id, diff] of Array.from(diffDataMap).sort(
    ([, a], [, b]) => a.src_line - b.src_line || a.dest_line - b.dest_line,
  )) {
    const { src_line, dest_line, block_length = 1 } = diff;

    switch (diff.mode) {
      // 删除：右边插入空行
      case "delete": {
        // 实质上是 typeof dest_line === "number"，卢指出可能有算法不提供 delete、insert 对应的 dest_line 和 src_line。在后面处理
        if (dest_line || dest_line === 0) {
          const l2i = lines2.findIndex((line) => line.number === dest_line);
          const insertLines = initContentLines("dest", block_length, { ids: [id] });
          lines2.splice(l2i, 0, ...insertLines);
        }
        break;
      }

      // 新增：左边插入空行
      case "insert": {
        // 实质上是 typeof dest_line === "number"
        if (src_line || src_line === 0) {
          const l1i = lines1.findIndex((line) => line.number === src_line);
          const insertLines = initContentLines("src", block_length, { ids: [id] });
          lines1.splice(l1i, 0, ...insertLines);
        }
        break;
      }

      // 分割：在左边第一行下插入空行
      case "split": {
        const l1i = lines1.findIndex((line) => line.number === src_line) + 1;
        const insertLines = initContentLines("src", block_length - 1, { ids: [id] });
        lines1.splice(l1i, 0, ...insertLines);
        break;
      }

      // 合并：在右侧第一行下插入空行
      case "merge": {
        const l2i = lines2.findIndex((line) => line.number === dest_line) + 1;
        const insertLines = initContentLines("dest", block_length - 1, { ids: [id] });
        lines2.splice(l2i, 0, ...insertLines);
        break;
      }
    }
  }

  /**
   * 再处理需要按行下标往另一边插入空行的脚本，
   * 这种脚本存在相互交叉的连线，先插入的空行会导致后续的下标偏移。
   * 不能用 immer produce，它会将空行插到奇怪的地方
   */

  interface insertLinesDataItem {
    belong: ContentLinesItemBelong;
    index: number;
    diff: DiffDataItem;
    insertLines: Array<ContentLinesItem>;
  }

  /**
   * 对要插入的空行数据进行排序（从上往下，避免影响下标计算）
   */
  function sortEmptyLinesData(a: insertLinesDataItem, b: insertLinesDataItem) {
    const { belong: ab, index: ai, diff: ad } = a;
    const { belong: bb, index: bi, diff: bd } = b;

    if (ai !== bi) return ai - bi; // 一、小的在前
    if (ab !== bb) return ab === "dest" ? -1 : 1; // 二、现在右侧插入空行（先删除后新增）
    if (ab === "dest") return ad.src_line - bd.src_line; // 三、都在右侧插空行，看谁左侧在上
    return ad.dest_line - bd.dest_line; // 四、都在左侧插空行，看谁右侧在上

    // 交叉移动（或复制）的情况，因为有确定的 dest_line，在第一步就判断了
  }

  /**
   * 处理插入空行的结果
   */
  function runEmptyLinesData(data: insertLinesDataItem) {
    const { belong, index, insertLines } = data;
    if (belong === "dest") lines2.splice(index, 0, ...insertLines);
    else lines1.splice(index, 0, ...insertLines);
  }

  /**
   * 循环找寻没有对齐（空行也行）的差异行，注意一次只插一个脚本的半边
   */

  while (true) {
    const emptyLinesData: Array<insertLinesDataItem> = [];

    for (const [id, diff] of diffDataMap) {
      const { src_line, dest_line, block_length = 1 } = diff;
      const i1 = lines1.findIndex((line) => line.number === src_line);
      const i2 = lines2.findIndex((line) => line.number === dest_line);

      if (diff.mode === "move" && i1 === i2) continue;

      switch (diff.mode) {
        // 删除：往右边插入空行
        case "delete": {
          // 卢指出可能有算法不提供 delete、insert 对应的 dest_line 和 src_line。此时在这里处理
          if (!dest_line && dest_line !== 0 && (!lines2[i1] || !lines2[i1].ids.includes(id))) {
            const insertLines = initContentLines("dest", block_length, { ids: [id] });
            emptyLinesData.push({ belong: "dest", index: i1, diff, insertLines });
          }
          break;
        }

        // 新增：往左边插入空行
        case "insert": {
          if (!src_line && src_line !== 0 && (!lines1[i2] || !lines1[i2].ids.includes(id))) {
            const insertLines = initContentLines("src", block_length, { ids: [id] });
            emptyLinesData.push({ belong: "src", index: i2, diff, insertLines });
          }
          break;
        }

        // 复制：往左边插入空行
        case "copy": {
          // 1. 没有行对齐；2. 是有内容的行；3. 行内容与本差异无关；
          if (!lines1[i2] || lines1[i2].number || !lines1[i2].ids.includes(id)) {
            const insertLines = initContentLines("src", block_length, { ids: [id] });
            emptyLinesData.push({ belong: "src", index: i2, diff, insertLines });
          }

          break;
        }

        // 移动：两边插入空行
        case "move": {
          if (!lines2[i1] || lines2[i1].number || !lines2[i1].ids.includes(id)) {
            const insertLines = initContentLines("dest", block_length, { ids: [id] });
            emptyLinesData.push({ belong: "dest", index: i1, diff, insertLines });
          }

          if (!lines1[i2] || lines1[i2].number || !lines1[i2].ids.includes(id)) {
            const insertLines = initContentLines("src", block_length, { ids: [id] });
            emptyLinesData.push({ belong: "src", index: i2, diff, insertLines });
          }

          break;
        }
      }
    }

    if (emptyLinesData.length === 0) break;

    emptyLinesData.sort(sortEmptyLinesData);
    runEmptyLinesData(emptyLinesData[0]!);
  }

  /**
   * 删掉最开始添加的空行
   */

  lines1.splice(lines1.length - 1, 1);
  lines2.splice(lines2.length - 1, 1);

  return { lines1, lines2 };
}

/**
 * 生成 contentLine，用于绘图
 */
export function initContentLine(
  belong: ContentLinesItem["belong"],
  options: {
    content?: string;
    ids?: DiffDataId[];
    number?: number;
  } = {},
): ContentLinesItem {
  const { content = "", ids = [], number = null } = options;

  return {
    belong: belong,
    content: content,
    ids: ids,
    number: number,
    block_ids: [],
  };
}

/**
 * 生成多个 contentLine
 */
export function initContentLines(
  belong: ContentLinesItem["belong"],
  length: number,
  options: {
    content?: string;
    ids?: DiffDataId[];
    number?: number;
  } = {},
): Array<ContentLinesItem> {
  return Array.from({ length }, () => initContentLine(belong, options));
}

/**
 * 为了实现空行也有类似内容行填充效果，在 diff 范围内显示同一个颜色
 */
export function fillBlankLines(
  f1Lines: Array<ContentLinesItem>,
  f2Lines: Array<ContentLinesItem>,
  diffDataMap: DiffDataMap,
): { lines1: Array<ContentLinesItem>; lines2: Array<ContentLinesItem> } {
  const lines1 = f1Lines.slice();
  const lines2 = f2Lines.slice();

  for (const [id] of diffDataMap) {
    function findLine(line: ContentLinesItem): boolean {
      return !!(line.number && line.ids.includes(id));
    }

    const l1s = lines1.findIndex(findLine);
    const l1e = findLastIndex(lines1, findLine);

    if (l1s > -1 && l1e > -1) {
      for (let i = l1s; i <= l1e; i += 1) {
        lines1[i]!.block_ids.push(id);
      }
    }

    const l2s = lines2.findIndex(findLine);
    const l2e = findLastIndex(lines2, findLine);

    if (l2s > -1 && l2e > -1) {
      for (let i = l2s; i <= l2e; i += 1) {
        lines2[i]!.block_ids.push(id);
      }
    }
  }

  return { lines1, lines2 };
}
