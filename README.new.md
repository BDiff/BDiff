<h1 align="center">BDiff</h1>

<p align="center"><img src="docs/logo.png" alt="Logo" title="Logo" width="128" /></p>

<p align="center">English · <a href="README.zh-Hans.md">简体中文</a></p>

<p align="center"><a title="Official Website" href="http://www.bdiff.net/">http://www.bdiff.net/</a></p>

<p align="center">
BDiff is a block-aware and accurate text-based difference tool
</p>

<!-- <p align="center">
<a href="https://github.com/BDiff/BDiff/releases"><img alt="Version" title="Version" src="https://img.shields.io/github/v/release/BDiff/BDiff?label=Version&logo=data:image/svg+xml;charset=utf-8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNiAxNiIgd2lkdGg9IjE2IiBoZWlnaHQ9IjE2Ij48cGF0aCBmaWxsPQoid2hpdGUiIGQ9Ik0xIDcuNzc1VjIuNzVDMSAxLjc4NCAxLjc4NCAxIDIuNzUgMWg1LjAyNWMuNDY0IDAgLjkxLjE4NCAxLjIzOC41MTNsNi4yNSA2LjI1YTEuNzUgMS43NSAwIDAgMSAwIDIuNDc0bC01LjAyNiA1LjAyNmExLjc1IDEuNzUgMCAwIDEtMi40NzQgMGwtNi4yNS02LjI1QTEuNzUyIDEuNzUyIDAgMCAxIDEgNy43NzVabTEuNSAwYzAgLjA2Ni4wMjYuMTMuMDczLjE3N2w2LjI1IDYuMjVhLjI1LjI1IDAgMCAwIC4zNTQgMGw1LjAyNS01LjAyNWEuMjUuMjUgMCAwIDAgMC0uMzU0bC02LjI1LTYuMjVhLjI1LjI1IDAgMCAwLS4xNzctLjA3M0gyLjc1YS4yNS4yNSAwIDAgMC0uMjUuMjVaTTYgNWExIDEgMCAxIDEgMCAyIDEgMSAwIDAgMSAwLTJaIj48L3BhdGg+PC9zdmc+" /></a>
<a href="https://pypistats.org/packages/BDiff"><img alt="Downloads" title="Downloads" src="https://img.shields.io/pypi/dm/BDiff?label=Downloads&logo=data:image/svg+xml;charset=utf-8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNiAxNiIgd2lkdGg9IjE2IiBoZWlnaHQ9IjE2Ij48cGF0aCBmaWxsPSJ3aGl0ZSIgZD0iTTIuNzUgMTRBMS43NSAxLjc1IDAgMCAxIDEgMTIuMjV2LTIuNWEuNzUuNzUgMCAwIDEgMS41IDB2Mi41YzAgLjEzOC4xMTIuMjUuMjUuMjVoMTAuNWEuMjUuMjUgMCAwIDAgLjI1LS4yNXYtMi41YS43NS43NSAwIDAgMSAxLjUgMHYyLjVBMS43NSAxLjc1IDAgMCAxIDEzLjI1IDE0WiI+PC9wYXRoPjxwYXRoIGZpbGw9IndoaXRlIiBkPSJNNy4yNSA3LjY4OVYyYS43NS43NSAwIDAgMSAxLjUgMHY1LjY4OWwxLjk3LTEuOTY5YS43NDkuNzQ5IDAgMSAxIDEuMDYgMS4wNmwtMy4yNSAzLjI1YS43NDkuNzQ5IDAgMCAxLTEuMDYgMEw0LjIyIDYuNzhhLjc0OS43NDkgMCAxIDEgMS4wNi0xLjA2bDEuOTcgMS45NjlaIj48L3BhdGg+PC9zdmc+" /></a>
<a href="https://github.com/BDiff/BDiff/actions"><img alt="Lint & Test" title="Lint & Test" src="https://img.shields.io/github/actions/workflow/status/BDiff/BDiff/python-package.yml?label=Lint%20%26%20Test&logo=data:image/svg+xml;charset=utf-8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNiAxNiIgd2lkdGg9IjE2IiBoZWlnaHQ9IjE2Ij48cGF0aCBmaWxsPSJ3aGl0ZSIgZD0iTTggMGE4IDggMCAxIDEgMCAxNkE4IDggMCAwIDEgOCAwWk0xLjUgOGE2LjUgNi41IDAgMSAwIDEzIDAgNi41IDYuNSAwIDAgMC0xMyAwWm00Ljg3OS0yLjc3MyA0LjI2NCAyLjU1OWEuMjUuMjUgMCAwIDEgMCAuNDI4bC00LjI2NCAyLjU1OUEuMjUuMjUgMCAwIDEgNiAxMC41NTlWNS40NDJhLjI1LjI1IDAgMCAxIC4zNzktLjIxNVoiPjwvcGF0aD48L3N2Zz4=" /></a>
<a href="https://codecov.io/gh/BDiff/BDiff"><img alt="Code Coverage" title="Code Coverage" src="https://img.shields.io/codecov/c/github/BDiff/BDiff?label=Code%20Coverage&logoColor=white&logo=codecov" /></a>
<br/>
<a href="https://github.com/BDiff/BDiff/watchers"><img alt="Watchers" title="Watchers" src="https://img.shields.io/github/watchers/BDiff/BDiff?label=Watchers&style=flat&logo=data:image/svg+xml;charset=utf-8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNiAxNiIgd2lkdGg9IjE2IiBoZWlnaHQ9IjE2Ij48cGF0aCBmaWxsPSJ3aGl0ZSIgZD0iTTggMmMxLjk4MSAwIDMuNjcxLjk5MiA0LjkzMyAyLjA3OCAxLjI3IDEuMDkxIDIuMTg3IDIuMzQ1IDIuNjM3IDMuMDIzYTEuNjIgMS42MiAwIDAgMSAwIDEuNzk4Yy0uNDUuNjc4LTEuMzY3IDEuOTMyLTIuNjM3IDMuMDIzQzExLjY3IDEzLjAwOCA5Ljk4MSAxNCA4IDE0Yy0xLjk4MSAwLTMuNjcxLS45OTItNC45MzMtMi4wNzhDMS43OTcgMTAuODMuODggOS41NzYuNDMgOC44OThhMS42MiAxLjYyIDAgMCAxIDAtMS43OThjLjQ1LS42NzcgMS4zNjctMS45MzEgMi42MzctMy4wMjJDNC4zMyAyLjk5MiA2LjAxOSAyIDggMlpNMS42NzkgNy45MzJhLjEyLjEyIDAgMCAwIDAgLjEzNmMuNDExLjYyMiAxLjI0MSAxLjc1IDIuMzY2IDIuNzE3QzUuMTc2IDExLjc1OCA2LjUyNyAxMi41IDggMTIuNWMxLjQ3MyAwIDIuODI1LS43NDIgMy45NTUtMS43MTUgMS4xMjQtLjk2NyAxLjk1NC0yLjA5NiAyLjM2Ni0yLjcxN2EuMTIuMTIgMCAwIDAgMC0uMTM2Yy0uNDEyLS42MjEtMS4yNDItMS43NS0yLjM2Ni0yLjcxN0MxMC44MjQgNC4yNDIgOS40NzMgMy41IDggMy41Yy0xLjQ3MyAwLTIuODI1Ljc0Mi0zLjk1NSAxLjcxNS0xLjEyNC45NjctMS45NTQgMi4wOTYtMi4zNjYgMi43MTdaTTggMTBhMiAyIDAgMSAxLS4wMDEtMy45OTlBMiAyIDAgMCAxIDggMTBaIj48L3BhdGg+PC9zdmc+" /></a>
<a href="https://github.com/BDiff/BDiff/forks"><img alt="Forks" title="Forks" src="https://img.shields.io/github/forks/BDiff/BDiff?label=Forks&style=flat&logo=data:image/svg+xml;charset=utf-8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNiAxNiIgd2lkdGg9IjE2IiBoZWlnaHQ9IjE2Ij48cGF0aCBmaWxsPSJ3aGl0ZSIgZD0iTTUgNS4zNzJ2Ljg3OGMwIC40MTQuMzM2Ljc1Ljc1Ljc1aDQuNWEuNzUuNzUgMCAwIDAgLjc1LS43NXYtLjg3OGEyLjI1IDIuMjUgMCAxIDEgMS41IDB2Ljg3OGEyLjI1IDIuMjUgMCAwIDEtMi4yNSAyLjI1aC0xLjV2Mi4xMjhhMi4yNTEgMi4yNTEgMCAxIDEtMS41IDBWOC41aC0xLjVBMi4yNSAyLjI1IDAgMCAxIDMuNSA2LjI1di0uODc4YTIuMjUgMi4yNSAwIDEgMSAxLjUgMFpNNSAzLjI1YS43NS43NSAwIDEgMC0xLjUgMCAuNzUuNzUgMCAwIDAgMS41IDBabTYuNzUuNzVhLjc1Ljc1IDAgMSAwIDAtMS41Ljc1Ljc1IDAgMCAwIDAgMS41Wm0tMyA4Ljc1YS43NS43NSAwIDEgMC0xLjUgMCAuNzUuNzUgMCAwIDAgMS41IDBaIj48L3BhdGg+PC9zdmc+" /></a>
<a href="https://github.com/BDiff/BDiff/stargazers"><img alt="Stars" title="Stars" src="https://img.shields.io/github/stars/BDiff/BDiff?label=Stars&color=gold&style=flat&logo=data:image/svg+xml;charset=utf-8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNiAxNiIgd2lkdGg9IjE2IiBoZWlnaHQ9IjE2Ij48cGF0aCBmaWxsPSJ3aGl0ZSIgZD0iTTggLjI1YS43NS43NSAwIDAgMSAuNjczLjQxOGwxLjg4MiAzLjgxNSA0LjIxLjYxMmEuNzUuNzUgMCAwIDEgLjQxNiAxLjI3OWwtMy4wNDYgMi45Ny43MTkgNC4xOTJhLjc1MS43NTEgMCAwIDEtMS4wODguNzkxTDggMTIuMzQ3bC0zLjc2NiAxLjk4YS43NS43NSAwIDAgMS0xLjA4OC0uNzlsLjcyLTQuMTk0TC44MTggNi4zNzRhLjc1Ljc1IDAgMCAxIC40MTYtMS4yOGw0LjIxLS42MTFMNy4zMjcuNjY4QS43NS43NSAwIDAgMSA4IC4yNVptMCAyLjQ0NUw2LjYxNSA1LjVhLjc1Ljc1IDAgMCAxLS41NjQuNDFsLTMuMDk3LjQ1IDIuMjQgMi4xODRhLjc1Ljc1IDAgMCAxIC4yMTYuNjY0bC0uNTI4IDMuMDg0IDIuNzY5LTEuNDU2YS43NS43NSAwIDAgMSAuNjk4IDBsMi43NyAxLjQ1Ni0uNTMtMy4wODRhLjc1Ljc1IDAgMCAxIC4yMTYtLjY2NGwyLjI0LTIuMTgzLTMuMDk2LS40NWEuNzUuNzUgMCAwIDEtLjU2NC0uNDFMOCAyLjY5NFoiPjwvcGF0aD48L3N2Zz4=" /></a>
<a href="https://github.com/BDiff/BDiff/issues"><img alt="Issues" title="Issues" src="https://img.shields.io/github/issues/BDiff/BDiff?label=Issues&logo=data:image/svg+xml;charset=utf-8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNiAxNiIgd2lkdGg9IjE2IiBoZWlnaHQ9IjE2Ij48cGF0aCBmaWxsPSJ3aGl0ZSIgZD0iTTggOS41YTEuNSAxLjUgMCAxIDAgMC0zIDEuNSAxLjUgMCAwIDAgMCAzWiI+PC9wYXRoPjxwYXRoIGZpbGw9IndoaXRlIiBkPSJNOCAwYTggOCAwIDEgMSAwIDE2QTggOCAwIDAgMSA4IDBaTTEuNSA4YTYuNSA2LjUgMCAxIDAgMTMgMCA2LjUgNi41IDAgMCAwLTEzIDBaIj48L3BhdGg+PC9zdmc+" /></a>
<a href="https://github.com/BDiff/BDiff/pulls"><img alt="Pull Requests" title="Pull Requests" src="https://img.shields.io/github/issues-pr/BDiff/BDiff?label=Pull%20Requests&logo=data:image/svg+xml;charset=utf-8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNiAxNiIgd2lkdGg9IjE2IiBoZWlnaHQ9IjE2Ij48cGF0aCBmaWxsPSJ3aGl0ZSIgZD0iTTEuNSAzLjI1YTIuMjUgMi4yNSAwIDEgMSAzIDIuMTIydjUuMjU2YTIuMjUxIDIuMjUxIDAgMSAxLTEuNSAwVjUuMzcyQTIuMjUgMi4yNSAwIDAgMSAxLjUgMy4yNVptNS42NzctLjE3N0w5LjU3My42NzdBLjI1LjI1IDAgMCAxIDEwIC44NTRWMi41aDFBMi41IDIuNSAwIDAgMSAxMy41IDV2NS42MjhhMi4yNTEgMi4yNTEgMCAxIDEtMS41IDBWNWExIDEgMCAwIDAtMS0xaC0xdjEuNjQ2YS4yNS4yNSAwIDAgMS0uNDI3LjE3N0w3LjE3NyAzLjQyN2EuMjUuMjUgMCAwIDEgMC0uMzU0Wk0zLjc1IDIuNWEuNzUuNzUgMCAxIDAgMCAxLjUuNzUuNzUgMCAwIDAgMC0xLjVabTAgOS41YS43NS43NSAwIDEgMCAwIDEuNS43NS43NSAwIDAgMCAwLTEuNVptOC4yNS43NWEuNzUuNzUgMCAxIDAgMS41IDAgLjc1Ljc1IDAgMCAwLTEuNSAwWiI+PC9wYXRoPjwvc3ZnPg==" /></a>
<a href="https://github.com/BDiff/BDiff/discussions"><img alt="Discussions" title="Discussions" src="https://img.shields.io/github/discussions/BDiff/BDiff?label=Discussions&logo=data:image/svg+xml;charset=utf-8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNiAxNiIgd2lkdGg9IjE2IiBoZWlnaHQ9IjE2Ij48cGF0aCBmaWxsPSJ3aGl0ZSIgZD0iTTEuNzUgMWg4LjVjLjk2NiAwIDEuNzUuNzg0IDEuNzUgMS43NXY1LjVBMS43NSAxLjc1IDAgMCAxIDEwLjI1IDEwSDcuMDYxbC0yLjU3NCAyLjU3M0ExLjQ1OCAxLjQ1OCAwIDAgMSAyIDExLjU0M1YxMGgtLjI1QTEuNzUgMS43NSAwIDAgMSAwIDguMjV2LTUuNUMwIDEuNzg0Ljc4NCAxIDEuNzUgMVpNMS41IDIuNzV2NS41YzAgLjEzOC4xMTIuMjUuMjUuMjVoMWEuNzUuNzUgMCAwIDEgLjc1Ljc1djIuMTlsMi43Mi0yLjcyYS43NDkuNzQ5IDAgMCAxIC41My0uMjJoMy41YS4yNS4yNSAwIDAgMCAuMjUtLjI1di01LjVhLjI1LjI1IDAgMCAwLS4yNS0uMjVoLTguNWEuMjUuMjUgMCAwIDAtLjI1LjI1Wm0xMyAyYS4yNS4yNSAwIDAgMC0uMjUtLjI1aC0uNWEuNzUuNzUgMCAwIDEgMC0xLjVoLjVjLjk2NiAwIDEuNzUuNzg0IDEuNzUgMS43NXY1LjVBMS43NSAxLjc1IDAgMCAxIDE0LjI1IDEySDE0djEuNTQzYTEuNDU4IDEuNDU4IDAgMCAxLTIuNDg3IDEuMDNMOS4yMiAxMi4yOGEuNzQ5Ljc0OSAwIDAgMSAuMzI2LTEuMjc1Ljc0OS43NDkgMCAwIDEgLjczNC4yMTVsMi4yMiAyLjIydi0yLjE5YS43NS43NSAwIDAgMSAuNzUtLjc1aDFhLjI1LjI1IDAgMCAwIC4yNS0uMjVaIj48L3BhdGg+PC9zdmc+" /></a>
</p>

<p align="center">
<a href="https://github.com/BDiff/BDiff/pulse"><img src="https://repobeats.axiom.co/api/embed/b4832e0ac90defe97c7e11e0c9e926793ec7135c.svg" /></a>
</p>

<p align="center">
    <a href="https://star-history.com/#BDiff/BDiff&Date">
        <picture>
            <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=BDiff/BDiff&type=Date&theme=dark" />
            <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=BDiff/BDiff&type=Date" />
            <img src="https://api.star-history.com/svg?repos=BDiff/BDiff&type=Date" />
        </picture>
    </a>
</p> -->

## 🔆 Overview

### 🎻 Introduction

<img width="3281" height="941" alt="image" src="https://github.com/user-attachments/assets/e7d2dc5e-90bd-400f-8a3f-8ef8fbc4cf83" />

Are you still struggling with reading such differencing results? **Now try** [**BDiff!**](http://www.bdiff.net/): 

![home-assitant_a2a580f0fe7a1354a109eb062b5393fbb330f508-urls](https://github.com/user-attachments/assets/d91a5adc-93e0-490b-a8c1-9d3c63824e82)  

BDiff is a text-based differencing algorithm that can identify accurate line-level and block-level differences between text files and generate corresponding edit scripts. It can be applied in scenarios such as code review and change analysis.

### ✨ Features

- **Language-independent**: BDiff is a text-based differencing algorithm and can thus be applied to code written in any programming language.
- **Comprehensive Difference Identification**: It can identify line deletions, line additions, line updates, line splits, line merges, block copies (including line updates), and block moves (including line updates).
- **Generate Edit Scripts**: Produces edit scripts based on the identified differences.
- **Display Updated Difference Substrings**: Shows the specific substrings that have been updated.
- **Edit Action Localization**: Helps pinpoint the edit actions within the script.
- **View Before-and-After Mapped Lines/Blocks**: Allows users to view the mapped lines or blocks before and after the changes.
- **Set Difference Display Modes**: Offers alignment mode and compact mode for displaying differences.
- **Language Settings**: Supports Chinese and English.
- **Theme Settings**: Switch between light and dark themes for comfortable viewing.
- **Difference Option Settings**: Customize comparison parameters for precise results.
- **Programming Language Highlighting**: Syntax-aware highlighting for major programming languages.

## 📦 Installation

To install this package, your Python version must be **`>=3.12`**. Install it with the following command:

```shell
pip install bdiff
```

Here are the dependencies that the project must need:

- [`numpy`](https://github.com/numpy/numpy): The fundamental package for scientific computing with Python.
- [`scipy`](https://github.com/scipy/scipy): SciPy library main repository.

## 📜 Usage

### Quick Start

1. Visit the BDiff online tool at <http://bdiff.net/>.
2. Upload the old and new versions of your text file via the file selector.
3. Click to view the difference results.

### Option Settings

- **Git Difference Algorithm**: Choose from Git's four differencing algorithms. Results may vary slightly; the default Histogram algorithm typically produces the shortest edit scripts.
- **Tab Length**: Number of spaces a tab character represents, affecting alignment calculations.
- **Minimum Length of Moved Block**: The minimum number of lines a moved block should contain.
- **Minimum Length of Copied Block**: The minimum number of lines a copied block should contain.
- **Context Length**: The number of lines above or below a line/block when calculating context similarity.
- **Line Similarity Weight**: The proportion of line similarity in the overall line mapping similarity calculation, which also takes into account context similarity.
- **Overall Line Similarity Threshold**: If the overall line mapping similarity is greater than or equal to this threshold, it is considered a valid line mapping.
- **Maximum Merged Lines**: The maximum number of lines allowed when detecting line merges.
- **Maximum Split Lines**: The maximum number of lines allowed when detecting line splits.
- **Identify Block Moves**: Enable/disable detection of block moves.
- **Identify Block Copies**: Enable/disable detection of block copies.
- **Include Updates in Moves**: Detect line updates within moved blocks.
- **Include Updates in Copies**: Detect line updates within copied blocks.
- **Include Lines with Only Stop Words in Moved Block Size Calculation**: Whether to count lines containing only stop words when calculating the size of moved blocks.
- **Include Lines with Only Stop Words in Copied Block Size Calculation**: Whether to count lines containing only stop words when calculating the size of copied blocks.

## 🖼️ Gallery

Typical Real-world Cases.

- 1. Changing the order of parameter and member variable assignments

kitao/pyxel, 3861523a200da507f36edf478729f4ec7c269775, app.py

![](http://test.bdiff.net/public/pyxel-3861523a200da507f36edf478729f4ec7c269775-app.py.png)

- 2. Moving the try statement block

psf/requests, cde3b88f3e93a9503810acc0ded890025fcbc119, core.py

![](http://test.bdiff.net/public/requests-cde3b88f3e93a9503810acc0ded890025fcbc119-core.py.png)

- 3. Adding conditional judgment

ansible/ansible, 3807824c6d0dae63b9f36dbafe8e100b0a3beaa6, \_\_init\_\_.py

![](http://test.bdiff.net/public/ansible-3807824c6d0dae63b9f36dbafe8e100b0a3beaa6-__init__.py.png)

- 4. Reusing interface elements

topjohnwu/Magisk, fc5c9647d829cad1b73338e42164decc4ab08a54, drawer.xml

![](http://test.bdiff.net/public/magisk-fc5c9647d829cad1b73338e42164decc4ab08a54-drawer.xml.png)

- 5. Copying function implementation

keras-team/keras, aa7f9cdae951bba824883cfa392224a292b284b, core.py

![](http://test.bdiff.net/public/keras-aa7f9cdae951bba824883cfa392224a292b284bb-core.py.png)

- 6. Reusing test functions

psf/black, e911c79809c4fd9b0773dea5b6a0e710b59614cf, test_black.py

![](http://test.bdiff.net/public/black-e911c79809c4fd9b0773dea5b6a0e710b59614cf-test_black.py.png)

- 7. Line splitting and block moving (Corresponds to the example at the beginning of this file)

wagtail/wagtail, a2a580f0fe7a1354a109eb062b5393fbb330f508, urls.py

![](http://test.bdiff.net/public/home-assitant-a2a580f0fe7a1354a109eb062b5393fbb330f508-urls.py.png)

- 8. Block copies and block moves

square/okhttp, c8638813ff5f90715417e489b342aae5e410c5b2, pom.xml

![](http://test.bdiff.net/public/okhttp-c8638813ff5f90715417e489b342aae5e410c5b2-pom.xml.png)

- 9. Converting spaces to indentation

scikit-learn/scikit-learn, 612312553118371289330f50b38653d1206246c0, gene.py

![](http://test.bdiff.net/public/scikit-learn-612312553118371289330f50b38653d1206246c0-gene.py.png)

## 👀 More

### 🔗 Links

Here are some links that may be helpful to you:

- License: [*MIT License*](LICENSE.txt)
- Contribution Guideline: [*CONTRIBUTING.md*](CONTRIBUTING.md)
- Code of Conduct: [*CODE_OF_CONDUCT.md*](CODE_OF_CONDUCT.md)

### 😉 Contributors

Many thanks to the contributions of:

- Lu Yao (卢遥)
- Liu Wanwei (刘万伟)
- Song Wansheng (宋万盛)
- Chen Jing (陈璟)
- Yan Zhikang (颜智康)

<!-- [![Contributors](https://contrib.rocks/image?repo=BDiff/BDiff)](https://github.com/BDiff/BDiff/graphs/contributors) -->
