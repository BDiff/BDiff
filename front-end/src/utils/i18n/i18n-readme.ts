export const I18N_MESSAGES_README = {
  en: {
    chapter_classic_cases: {
      title: `🚩 Typical Real-world Cases`,
      case_titles: {
        "Changing the order of parameter and member variable assignments": `Changing the order of parameter and member variable assignments`,
        "Moving the try statement block": `Moving the try statement block`,
        "Adding conditional judgment": `Adding conditional judgment`,
        "Reusing interface elements": `Reusing interface elements`,
        "Copying function implementation": `Copying function implementation`,
        "Reuse test functions": `Reuse test functions`,
        "Line splits and block moves": `Line splits and block moves`,
        "Block copies and block moves": `Block copies and block moves`,
        "Converting spaces to indentation": `Converting spaces to indentation`,
      },
    },
    chapter_contribution: {
      title: `🎯 Contribution Guidelines`,
      content:
        `<p>We welcome contributions through the following methods:</p>` +
        `<ol>` +
        `<li>Submit an Issue to report problems or suggest improvements.</li>` +
        `<li>Fork the repository and submit a Pull Request.</li>` +
        `<li>Participate in discussions about the project.</li>` +
        `</ol>`,
    },
    chapter_contributors: {
      title: `🎅 Contributors`,
      content:
        `<ul>` +
        `<li>Lu Yao (卢遥)</li>` +
        `<li>Liu Wanwei (刘万伟)</li>` +
        `<li>Song Wansheng (宋万盛)</li>` +
        `<li>Chen Jing (陈璟)</li>` +
        `<li>Yan Zhikang (颜智康)</li>` +
        `</ul>`,
    },
    chapter_instructions: {
      title: `📜 Usage Instructions`,
      quick_start: {
        title: `Quick Start`,
        content:
          `<ol>` +
          `<li>Visit the BDiff online tool at <a href="http://bdiff.net/">http://bdiff.net/</a>.</li>` +
          `<li>Upload the old and new versions of your text file via the file selector.</li>` +
          `<li>Click to view the difference results.</li>` +
          `</ol>`,
      },
      settings: {
        title: `Option Settings`,
        content:
          `<ul>` +
          `<li><strong>Git Difference Algorithm</strong>: Choose from Git's four differencing algorithms. Results may vary slightly; the default Histogram algorithm typically produces the shortest edit scripts.</li>` +
          `<li><strong>Tab Length</strong>: Number of spaces a tab character represents, affecting alignment calculations.</li>` +
          `<li><strong>Minimum Length of Moved Block</strong>: The minimum number of lines a moved block should contain.</li>` +
          `<li><strong>Minimum Length of Copied Block</strong>: The minimum number of lines a copied block should contain.</li>` +
          `<li><strong>Context Length</strong>: The number of lines above or below a line/block when calculating context similarity.</li>` +
          `<li><strong>Line Similarity Weight</strong>: The proportion of line similarity in the overall line mapping similarity calculation, which also takes into account context similarity.</li>` +
          `<li><strong>Overall Line Similarity Threshold</strong>: If the overall line mapping similarity is greater than or equal to this threshold, it is considered a valid line mapping.</li>` +
          `<li><strong>Maximum Merged Lines</strong>: The maximum number of lines allowed when detecting line merges.</li>` +
          `<li><strong>Maximum Split Lines</strong>: The maximum number of lines allowed when detecting line splits.</li>` +
          `<li><strong>Identify Block Moves</strong>: Enable/disable detection of block moves.</li>` +
          `<li><strong>Identify Block Copies</strong>: Enable/disable detection of block copies.</li>` +
          `<li><strong>Include Updates in Moves</strong>: Detect line updates within moved blocks.</li>` +
          `<li><strong>Include Updates in Copies</strong>: Detect line updates within copied blocks.</li>` +
          `<li><strong>Include Lines with Only Stop Words in Moved Block Size Calculation</strong>: Whether to count lines containing only stop words when calculating the size of moved blocks.</li>` +
          `<li><strong>Include Lines with Only Stop Words in Copied Block Size Calculation</strong>: Whether to count lines containing only stop words when calculating the size of copied blocks.</li>` +
          `</ul>`,
      },
    },
    chapter_licenses: {
      title: `📋 License`,
      content:
        `<p>This software is licensed under <a href="http://openworks.org.cn/#/licenses/MulanPubL-v2">Mulan Public License，Version 2</a> (Mulan PubL v2).</p>` +
        `<div class="bg-light">` +
        `<pre class="p-3">` +
        `<code>Copyright (c) [2025] [**]
BDiff is licensed under Mulan PubL v2.
You can use this software according to the terms and conditions of the Mulan PubL v2.
You may obtain a copy of Mulan PubL v2 at:
         http://openworks.mulanos.cn/#/licenses/MulanPubL-v2
THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
See the Mulan PubL v2 for more details.</code>` +
        `</pre>` +
        `</div>`,
    },
    chapter_major_function: {
      title: `🎻 Main Features`,
      content:
        `<ul>` +
        `<li>Comprehensive Difference Identification: It can identify line deletions, line additions, line updates, line splits, line merges, block copies (including line updates), and block moves (including line updates).</li>` +
        `<li>Generate Edit Scripts: Produces edit scripts based on the identified differences.</li>` +
        `<li>Display Updated Difference Substrings: Shows the specific substrings that have been updated.</li>` +
        `<li>Edit Action Localization: Helps pinpoint the edit actions within the script.</li>` +
        `<li>View Before-and-After Mapped Lines/Blocks: Allows users to view the mapped lines or blocks before and after the changes.</li>` +
        `<li>Set Difference Display Modes: Offers alignment mode and compact mode for displaying differences.</li>` +
        `<li>Language Settings: Supports Chinese and English.</li>` +
        `<li>Theme Settings: Switch between light and dark themes for comfortable viewing.</li>` +
        `<li>Difference Option Settings: Customize comparison parameters for precise results.</li>` +
        `<li>Programming Language Highlighting: Syntax-aware highlighting for major programming languages.</li>` +
        `</ul>`,
    },
    chapter_open_source_project: {
      title: `🙆‍♂️ Open Source Project`,
      content:
        `<p>BDiff is open-source, with a GitHub App and Git plugin implemented. Welcome to use it and give it a star :)</p>` +
        `<ul>` +
        `<li>GitHub project address: <a href="https://github.com/BDiff/BDiff" target="_blank">https://github.com/BDiff/BDiff</a></li>` +
        `<li>GitHub App address: <a href="https://github.com/marketplace/bdiff" target="_blank">https://github.com/marketplace/bdiff</a></li>` +
        `<li>Git plugin project address: <a href="https://github.com/marketplace/bdiff" target="_blank">https://github.com/marketplace/bdiff</a></li>` +
        `<li>BDiff visualization result exporter project address: <a href="https://github.com/BDiff/BDiff-Visualization-Exporter" target="_blank">https://github.com/BDiff/BDiff-Visualization-Exporter</a></li>` +
        `</ul>`,
    },
    chapter_papers: {
      title: `📄 Research Paper`,
      content:
        `<p>Our research paper (<a href="https://arxiv.org/abs/2510.21094" target="_blank">https://arxiv.org/abs/2510.21094</a>) provides a detailed description of BDiff's implementation and evaluation. We welcome you to cite it and engage in academic exchanges :)</p>` +
        `<p>Paper citation:</p>` +
        `<div class="bg-light">` +
        `<pre class="p-3">` +
        `<code>&#64;misc&#123;lu2025bdiffblockawareaccuratetextbased,
      title=&#123;BDiff: Block-aware and Accurate Text-based Code Differencing&#125;,
      author=&#123;Yao Lu and Wanwei Liu and Tanghaoran Zhang and Kang Yang and Yang Zhang and Wenyu Xu and Longfei Sun and Xinjun Mao and Shuzheng Gao and Michael R. Lyu&#125;,
      year=&#123;2025&#125;,
      eprint=&#123;2510.21094&#125;,
      archivePrefix=&#123;arXiv&#125;,
      primaryClass=&#123;cs.SE&#125;,
      url=&#123;https://arxiv.org/abs/2510.21094&#125;,
&#125;</code>` +
        `</pre>` +
        `</div>`,
    },
    commit: "commit",
    desc: `BDiff is a browser-based file differencing tool that can identify precise differences between text files and generate corresponding edit scripts. It can be applied in scenarios such as code review and change analysis.`,
    filename: "filename",
    heading_one: {
      1: `I. `,
      2: `2. `,
      3: `3. `,
      4: `4. `,
      5: `5. `,
      6: `6. `,
      7: `7. `,
      8: `8. `,
      9: `9. `,
    },
    repo: "repo",
  },
  zh: {
    chapter_classic_cases: {
      title: `🚩典型真实案例`,
      case_titles: {
        "Changing the order of parameter and member variable assignments": `改变参数、成员变量赋值顺序`,
        "Moving the try statement block": `移动try语句块`,
        "Adding conditional judgment": `添加条件判断`,
        "Reusing interface elements": `复用界面元素`,
        "Copying function implementation": `复制函数实现`,
        "Reuse test functions": `复用测试函数`,
        "Line splits and block moves": `分割与块移动`,
        "Block copies and block moves": `块复制与块移动`,
        "Converting spaces to indentation": `空格改缩进`,
      },
    },
    chapter_contribution: {
      title: `🎯贡献指南`,
      content:
        `<p>欢迎小伙伴们通过以下方式参与开发：</p>` +
        `<ol>` +
        `<li>提交Issue报告问题或建议</li>` +
        `<li>Fork仓库并提交Pull Request</li>` +
        `<li>参与项目issue讨论</li>` +
        `</ol>`,
    },
    chapter_contributors: {
      title: `🎅贡献者`,
      content: `<ul>` + `<li>卢遥，刘万伟，宋万盛，陈璟，颜智康</li>` + `</ul>`,
    },
    chapter_instructions: {
      title: `📜使用说明`,
      quick_start: {
        title: `快速开始`,
        content:
          `<ol>` +
          `<li>访问 BDiff 在线工具：<a href="http://bdiff.net/">http://bdiff.net/</a>；</li>` +
          `<li>通过文件选择器选择上传旧版本和新版本；</li>` +
          `<li>点击查看差异结果。</li>` +
          `</ol>`,
      },
      settings: {
        title: `选项设置`,
        content:
          `<ul>` +
          `<li><strong>Git差异算法</strong>：Git的四个差异算法，本差异工具基于Git的差异结果计算，不同的Git差异算法所得结果小概率不同，默认的Histogram算法所得结果编辑脚本整体最小。</li>` +
          `<li><strong>制表符长度</strong>：一个制表符对应的空格数，主要用于计算块、行编辑的左右便宜量。</li>` +
          `<li><strong>移动块最小长度</strong>：移动块包含的最小的行数。</li>` +
          `<li><strong>复制块最小长度</strong>：移动块包含的最小的行数。</li>` +
          `<li><strong>上下文长度</strong>：计算上下文相似度时行/块以上或以下的行数。</li>` +
          `<li><strong>行相似度权重</strong>：计算行映射综合相似度用到行相似度和上下文相似度时行相似度所占的比重。</li>` +
          `<li><strong>综合行相似度临界值</strong>：行映射综合相似度大于等于该临界值即认为是行映射。</li>` +
          `<li><strong>最大合并行数</strong>：匹配行合并时允许的最大合并行数。</li>` +
          `<li><strong>最大分割行数</strong>：匹配行分割时允许的最大分割行数。</li>` +
          `<li><strong>识别块移动</strong>：是否识别块移动。</li>` +
          `<li><strong>识别块复制</strong>：是否识别块复制。</li>` +
          `<li><strong>识别移动块更新</strong>：识别块移动时是否包含行更新。</li>` +
          `<li><strong>识别移动块复制</strong>：识别块复制时是否包含行更新。</li>` +
          `<li><strong>纯停用词行计入移动块大小</strong>：计算移动块大小时，是否计入仅包含停用词的行。</li>` +
          `<li><strong>纯停用词行计入复制块大小</strong>：计算复制块大小时，是否计入仅包含停用词的行。</li>` +
          `</ul>`,
      },
    },
    chapter_licenses: {
      title: `📋许可证`,
      content:
        `<p>BDiff使用<a href="http://openworks.mulanos.cn/#/licenses/MulanPubL-v2" target="_blank">木兰公共许可证 v2</a>开源：</p>` +
        `<div class="bg-light">` +
        `<pre class="p-3">` +
        `<code>Copyright (c) [2025] [**]
BDiff is licensed under Mulan PubL v2.
You can use this software according to the terms and conditions of the Mulan PubL v2.
You may obtain a copy of Mulan PubL v2 at:
         http://openworks.mulanos.cn/#/licenses/MulanPubL-v2
THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
See the Mulan PubL v2 for more details.</code>` +
        `</pre>` +
        `</div>`,
    },
    chapter_major_function: {
      title: `🎻主要功能`,
      content:
        `<ul>` +
        `<li>全面的差异识别：可识别` +
        `<span style="background: var(--diff-delete)">行删除</span>` +
        `、<span style="background: var(--diff-insert)">行新增</span>` +
        `、<span style="background: var(--diff-update)">行更新</span>` +
        `、<span style="background: var(--diff-split)">行分割</span>` +
        `、<span style="background: var(--diff-merge)">行合并</span>` +
        `、<span style="background: var(--diff-copy)">块复制</span>（含<span style="background: var(--diff-update)">行更新</span>）` +
        `、<span style="background: var(--diff-move)">块移动</span>（含<span style="background: var(--diff-update)">行更新</span）` +
        `。` +
        `其中，块编辑（块复制和块移动）是指对连续的文本行整体地进行行位置或缩进位置的移动或复制，移动前后块内各行相对缩进保持不变。</li>` +
        `<li>生成编辑脚本</li>` +
        `<li>展示更新子串差异</li>` +
        `<li>编辑脚本定位编辑动作</li>` +
        `<li>查看前后映射行/块</li>` +
        `<li>设置差异显示模式：对齐模式、紧凑模式</li>` +
        `<li>设置语言：中文、英文</li>` +
        `<li>设置主题：日间主题、夜间主题</li>` +
        `<li>设置差异选项</li>` +
        `<li>高亮显示主流编程语言</li>` +
        `</ul>`,
    },
    chapter_open_source_project: {
      title: `🙆‍♂️开源项目`,
      content:
        `<p>BDiff完全开源，并实现了GitHub App和GIt插件，欢迎小伙伴们使用点赞：）</p>` +
        `<ul>` +
        `<li>GitHub项目地址：<a href="https://github.com/BDiff/BDiff" target="_blank">https://github.com/BDiff/BDiff</a></li>` +
        `<li>GitHub App地址：<a href="https://github.com/marketplace/bdiff" target="_blank">https://github.com/marketplace/bdiff</a></li>` +
        `<li>Git 插件项目地址：<a href="https://github.com/marketplace/bdiff" target="_blank">https://github.com/marketplace/bdiff</a></li>` +
        `<li>BDiff可视化结果导出工具项目地址：<a href="https://github.com/BDiff/BDiff-Visualization-Exporter" target="_blank">https://github.com/BDiff/BDiff-Visualization-Exporter</a></li>` +
        `</ul>`,
    },
    chapter_papers: {
      title: `📄研究论文`,
      content:
        `<p>我们的研究论文（<a href="https://arxiv.org/abs/2510.21094" target="_blank">https://arxiv.org/abs/2510.21094</a>）对BDiff的实现和评估做了详细描述，欢迎小伙伴们引用、交流：）</p>` +
        `<p>Bibtex引用：</p>` +
        `<div class="bg-light">` +
        `<pre class="p-3">` +
        `<code>&#64;misc&#123;lu2025bdiffblockawareaccuratetextbased,
      title=&#123;BDiff: Block-aware and Accurate Text-based Code Differencing&#125;,
      author=&#123;Yao Lu and Wanwei Liu and Tanghaoran Zhang and Kang Yang and Yang Zhang and Wenyu Xu and Longfei Sun and Xinjun Mao and Shuzheng Gao and Michael R. Lyu&#125;,
      year=&#123;2025&#125;,
      eprint=&#123;2510.21094&#125;,
      archivePrefix=&#123;arXiv&#125;,
      primaryClass=&#123;cs.SE&#125;,
      url=&#123;https://arxiv.org/abs/2510.21094&#125;,
&#125;</code>` +
        `</pre>` +
        `</div>`,
    },
    commit: "提交",
    desc: `BDiff 是一个基于浏览器的文本差异分析工具，<strong>可识别文本文件的精确差异，并生成对应的编辑脚本</strong>，可用于代码审查、变更分析等场景。`,
    filename: "文件",
    heading_one: {
      1: `一、`,
      2: `二、`,
      3: `三、`,
      4: `四、`,
      5: `五、`,
      6: `六、`,
      7: `七、`,
      8: `八、`,
      9: `九、`,
    },
    repo: "项目",
  },
} as const;
