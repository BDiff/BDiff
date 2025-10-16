import { formatHtmlToWords } from "@/utils/functions.ts";

export function formatUpdatesIntoHtmlContent(content: string, ranges: Array<UpdateRange>): string {
  const words = formatHtmlToWords(content);
  const sTag = `<span style="background-color: var(--diff-update-deep)">`;
  const eTag = `</span>`;

  const result = [];
  let charIndex = 0;

  for (let i = 0, j = 0; i < words.length && j <= ranges.length; ) {
    const word = words[i] as string;

    // 遇到tag或ranges已处理完时直接跳过
    if (word.startsWith("<") || j === ranges.length) {
      result.push(word);
      i += 1;
      continue;
    }

    const wordLength = word.startsWith("&") ? 1 : word.length;
    const range = ranges[j] as UpdateRange;

    // 只在另一边有多的内容
    if (range.length === 0) {
      j += 1;
      continue;
    }

    // range不在此处word时跳过
    if (range[0] >= charIndex + wordLength) {
      result.push(word);
      charIndex += wordLength;
      i += 1;
      continue;
    }

    const startI = range[0] <= charIndex ? 0 : range[0] - charIndex;
    const endI = range[1] + 1 >= charIndex + wordLength ? word.length : range[1] - charIndex + 1;

    result.push(word.slice(0, startI), sTag, word.slice(startI, endI), eTag, word.slice(endI));
    charIndex += wordLength;

    // 当 word 没有被截取完时，进入下一个 range
    if (endI < word.length) {
      j += 1;
    }

    // 当 word 被截取完时（或没有下一个 range 时），进入下一个 word
    if (endI === word.length || j === ranges.length) {
      i += 1;
    }
  }

  return result.join("");
}
