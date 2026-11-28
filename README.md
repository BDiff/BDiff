<img width="3281" height="941" alt="image" src="https://github.com/user-attachments/assets/e7d2dc5e-90bd-400f-8a3f-8ef8fbc4cf83" />

Are you still struggling with reading such differencing results? **Now try** [**BDiff!**](http://www.bdiff.net/): 
![home-assitant_a2a580f0fe7a1354a109eb062b5393fbb330f508-urls](https://github.com/user-attachments/assets/d91a5adc-93e0-490b-a8c1-9d3c63824e82)  

## 🔆 Overview
BDiff is a text-based differencing algorithm that can identify accurate line-level and block-level differences between text files and generate corresponding edit scripts. It can be applied in scenarios such as code review and change analysis.

## I. 🎻 Main Features
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
## 2. 📜 Usage Instructions
### 2.1 Quick Start
1. Visit the BDiff online tool at http://bdiff.net/.
2. Upload the old and new versions of your text file via the file selector.
3. Click to view the difference results.
### 2.2 Option Settings
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
- **Include Updates in Moves**: Detect line updates within moved blocks.
- **Include Lines with Only Stop Words in Moved Block Size Calculation**: Whether to count lines containing only stop words when calculating the size of moved blocks.
- **Maximal move-block distance**: The maximum relative distance between the two blocks in a block-move edit action.
- **Identify Block Copies**: Enable/disable detection of block copies.
- **Include Updates in Copies**: Detect line updates within copied blocks.
- **Include Lines with Only Stop Words in Copied Block Size Calculation**: Whether to count lines containing only stop words when calculating the size of copied blocks.
- **Maximal copying-block distance**: The maximum relative distance between the two blocks in a block-copy edit action.
## 3. 🚩 Typical Real-world Cases
### 3.1 Changing the order of parameter and member variable assignments
kitao/pyxel, 3861523a200da507f36edf478729f4ec7c269775, app.py
![](https://github.com/user-attachments/assets/bcc940b9-49ca-43d0-9953-0d1e9805e495)
### 3.2 Moving the try statement block
psf/requests, cde3b88f3e93a9503810acc0ded890025fcbc119, core.py
![](https://github.com/user-attachments/assets/da22a8df-9a07-47c2-a4fa-d69e366897bd)
### 3.3 Adding conditional judgment
ansible/ansible, 3807824c6d0dae63b9f36dbafe8e100b0a3beaa6, __init__.py
![](https://github.com/user-attachments/assets/7b3d660d-48a9-4d9c-b43c-f95c5dec7b03)
### 3.4 Reusing interface elements
topjohnwu/Magisk, fc5c9647d829cad1b73338e42164decc4ab08a54, drawer.xml
![](https://github.com/user-attachments/assets/41f7125c-760a-492c-9bcb-1324b345c636)
### 3.5 Copying function implementation
keras-team/keras, aa7f9cdae951bba824883cfa392224a292b284b, core.py
![](https://github.com/user-attachments/assets/235c37d3-e1f5-4615-b51e-10f75aaebb47)
### 3.6 Reusing test functions
psf/black, e911c79809c4fd9b0773dea5b6a0e710b59614cf, test_black.py
![](https://github.com/user-attachments/assets/33004e2f-16bd-4b2e-b0a9-2dfb12589bf0)
### 3.7 Line splitting and block moving (Corresponds to the example at the beginning of this file)
wagtail/wagtail, a2a580f0fe7a1354a109eb062b5393fbb330f508, urls.py
![](https://github.com/user-attachments/assets/04398ac4-2607-4ee6-8e4a-86d84cbf7506)
### 3.8 Block copies and block moves
square/okhttp, c8638813ff5f90715417e489b342aae5e410c5b2, pom.xml
![](https://github.com/user-attachments/assets/7e4df8fc-004d-4809-ab3e-3501f23bbb03)
### 3.9 Converting spaces to indentation
scikit-learn/scikit-learn, 612312553118371289330f50b38653d1206246c0, gene.py
![](https://github.com/user-attachments/assets/924bb6fc-8145-41e1-94c4-c1af4f147571)
## 4. 📃 License
This software is licensed under [Mulan Public License，Version 2](http://openworks.mulanos.cn/#/licenses/MulanPubL-v2) (Mulan PubL v2).
```
Copyright (c) [2025] [Lu YAO]
BDiff is licensed under Mulan PubL v2.
You can use this software according to the terms and conditions of the Mulan PubL v2.
You may obtain a copy of Mulan PubL v2 at:
         http://openworks.mulanos.cn/#/licenses/MulanPubL-v2
THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
See the Mulan PubL v2 for more details.
```
## 5. 🎅 Contributors
- Lu Yao
- Liu Wanwei
- Song Wansheng
- Chen Jing
- Yan Zhikang
## 6. 📎 Citing BDiff
We have conducted a comprehensive evaluation experiment on BDiff, with detailed results available in our paper: [https://doi.org/10.1145/3832783.3837431](https://doi.org/10.1145/3832783.3837431). We are glad if you cite the relevant article in the following bibtex:
```bibtex
@inproceedings{10.1145/3832783.3837431,
author = {Lu, Yao and Liu, Wanwei and Zhang, Tanghaoran and Yang, Kang and Zhang, Yang and Xu, Wenyu and Sun, Longfei and Mao, Xinjun and Gao, Shuzheng and Lyu, Michael R.},
title = {BDiff: Block-Aware and Accurate Text-Based Code Differencing},
year = {2026},
isbn = {9798400728822},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3832783.3837431},
doi = {10.1145/3832783.3837431},
booktitle = {Proceedings of the 41st IEEE/ACM International Conference on Automated Software Engineering},
pages = {1702–1714},
numpages = {13},
keywords = {Block-level edit action, Code differencing, Code review, Edit script},
location = {Munich, Germany},
series = {ASE '26}
}
```
