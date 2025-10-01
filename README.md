BDiff is a browser-based file differencing tool that can identify precise differences between text files and generate corresponding edit scripts. It can be applied in scenarios such as code review and change analysis.

## I. 🎻 Main Features
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
- **Identify Block Copies**: Enable/disable detection of block copies.
- **Include Updates in Moves**: Detect line updates within moved blocks.
- **Include Updates in Copies**: Detect line updates within copied blocks.
- **Include Lines with Only Stop Words in Moved Block Size Calculation**: Whether to count lines containing only stop words when calculating the size of moved blocks.
- **Include Lines with Only Stop Words in Copied Block Size Calculation**: Whether to count lines containing only stop words when calculating the size of copied blocks.
## 3. 🚩 Typical Real-world Cases
### 3.1 Changing the order of parameter and member variable assignments
kitao/pyxel, 3861523a200da507f36edf478729f4ec7c269775, app.py
![](http://test.bdiff.net/public/pyxel-3861523a200da507f36edf478729f4ec7c269775-app.py.png)
### 3.2 Moving the try statement block
psf/requests, cde3b88f3e93a9503810acc0ded890025fcbc119, core.py
![](http://test.bdiff.net/public/requests-cde3b88f3e93a9503810acc0ded890025fcbc119-core.py.png)
### 3.3 Adding conditional judgment
ansible/ansible, 3807824c6d0dae63b9f36dbafe8e100b0a3beaa6, __init__.py
![](http://test.bdiff.net/public/ansible-3807824c6d0dae63b9f36dbafe8e100b0a3beaa6-__init__.py.png)
### 3.4 Reusing interface elements
topjohnwu/Magisk, fc5c9647d829cad1b73338e42164decc4ab08a54, drawer.xml
![](http://test.bdiff.net/public/magisk-fc5c9647d829cad1b73338e42164decc4ab08a54-drawer.xml.png)
### 3.5 Copying function implementation
keras-team/keras, aa7f9cdae951bba824883cfa392224a292b284b, core.py
![](http://test.bdiff.net/public/keras-aa7f9cdae951bba824883cfa392224a292b284bb-core.py.png)
### 3.6 Reuse test functions
psf/black, e911c79809c4fd9b0773dea5b6a0e710b59614cf, test_black.py
![](http://test.bdiff.net/public/black-e911c79809c4fd9b0773dea5b6a0e710b59614cf-test_black.py.png)
### 3.7 Line splits and block moves
wagtail/wagtail, a2a580f0fe7a1354a109eb062b5393fbb330f508, urls.py
![](http://test.bdiff.net/public/home-assitant-a2a580f0fe7a1354a109eb062b5393fbb330f508-urls.py.png)
### 3.8 Block copies and block moves
square/okhttp, c8638813ff5f90715417e489b342aae5e410c5b2, pom.xml
![](http://test.bdiff.net/public/okhttp-c8638813ff5f90715417e489b342aae5e410c5b2-pom.xml.png)
### 3.9 Converting spaces to indentation
scikit-learn/scikit-learn, 612312553118371289330f50b38653d1206246c0, gene.py
![](http://test.bdiff.net/public/scikit-learn-612312553118371289330f50b38653d1206246c0-gene.py.png)
## 4. 🎯 Contribution Guidelines
We welcome contributions through the following methods:
1. Submit an Issue to report problems or suggest improvements.
2. Fork the repository and submit a Pull Request.
3. Participate in discussions about the project.
## 5. License
This software is licensed under [Mulan Public License，Version 2](http://openworks.mulanos.cn/#/licenses/MulanPubL-v2) (Mulan PubL v2).
```
Copyright (c) [2025] [National University of Defense Technology]
BDiff is licensed under Mulan PubL v2.
You can use this software according to the terms and conditions of the Mulan PubL v2.
You may obtain a copy of Mulan PubL v2 at:
         http://openworks.mulanos.cn/#/licenses/MulanPubL-v2
THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
See the Mulan PubL v2 for more details.
```
## 6. 🎅 Contributors
- Lu Yao (卢遥)
- Liu Wanwei (刘万伟)
- Song Wansheng (宋万盛)
- Chen Jing (陈璟)
- Yan Zhikang (颜智康)
