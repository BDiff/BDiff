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
![](https://camo.githubusercontent.com/229a726f52dddcfc628ffda45aeb1864263540e49424568649269b8f138a3241/687474703a2f2f746573742e62646966662e6e65742f7075626c69632f707978656c2d333836313532336132303064613530376633366564663437383732396634656337633236393737352d6170702e70792e706e67)
### 3.2 Moving the try statement block
psf/requests, cde3b88f3e93a9503810acc0ded890025fcbc119, core.py
![](https://camo.githubusercontent.com/38a36089719b9a70ec402b07ec23267377b8a42ffb2183b89ecb4495f7ee089d/687474703a2f2f746573742e62646966662e6e65742f7075626c69632f72657175657374732d636465336238386633653933613935303338313061636330646564383930303235666362633131392d636f72652e70792e706e67)
### 3.3 Adding conditional judgment
ansible/ansible, 3807824c6d0dae63b9f36dbafe8e100b0a3beaa6, __init__.py
![](https://camo.githubusercontent.com/a31e6fa80ce0f0de3d8aefaebeec27fedeccd007d33abe6a6a47c0fa47ef2355/687474703a2f2f746573742e62646966662e6e65742f7075626c69632f616e7369626c652d333830373832346336643064616536336239663336646261666538653130306230613362656161362d5f5f696e69745f5f2e70792e706e67)
### 3.4 Reusing interface elements
topjohnwu/Magisk, fc5c9647d829cad1b73338e42164decc4ab08a54, drawer.xml
![](https://camo.githubusercontent.com/d03dbe441dcbdb3afc0958cde389ac21fa274f0e0cc42d87d31e5a1421eaf0fd/687474703a2f2f746573742e62646966662e6e65742f7075626c69632f6d616769736b2d666335633936343764383239636164316237333333386534323136346465636334616230386135342d6472617765722e786d6c2e706e67)
### 3.5 Copying function implementation
keras-team/keras, aa7f9cdae951bba824883cfa392224a292b284b, core.py
![](https://camo.githubusercontent.com/ff6a32f4c12aeef23c19b7ac96a15d1d7d6fb6f62836b93f29d3c797465840c4/687474703a2f2f746573742e62646966662e6e65742f7075626c69632f6b657261732d616137663963646165393531626261383234383833636661333932323234613239326232383462622d636f72652e70792e706e67)
### 3.6 Reusing test functions
psf/black, e911c79809c4fd9b0773dea5b6a0e710b59614cf, test_black.py
![](https://camo.githubusercontent.com/0ed1ae9ebc052559ede6a9affd65fa62988bc3d77ce5c52a19d12dfcdb97ef53/687474703a2f2f746573742e62646966662e6e65742f7075626c69632f626c61636b2d653931316337393830396334666439623037373364656135623661306537313062353936313463662d746573745f626c61636b2e70792e706e67)
### 3.7 Line splitting and block moving (Corresponds to the example at the beginning of this file)
wagtail/wagtail, a2a580f0fe7a1354a109eb062b5393fbb330f508, urls.py
![](https://private-user-images.githubusercontent.com/11403509/496940973-d91a5adc-93e0-490b-a8c1-9d3c63824e82.jpg?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NjY4OTAwOTcsIm5iZiI6MTc2Njg4OTc5NywicGF0aCI6Ii8xMTQwMzUwOS80OTY5NDA5NzMtZDkxYTVhZGMtOTNlMC00OTBiLWE4YzEtOWQzYzYzODI0ZTgyLmpwZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTEyMjglMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUxMjI4VDAyNDMxN1omWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTRkNmY1MWVmYzQxMWNkYTg4YjkzMzJmNGM0ZWY4ZTU1YWJkMDMwZWZkNTRiZmM1M2IxNTNkODdlOTVhZWI5ZGMmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.2p6WbJcHfYZ6vZHtDvGTDs7mGs61gtl6W8y3MitM2dQ)
### 3.8 Block copies and block moves
square/okhttp, c8638813ff5f90715417e489b342aae5e410c5b2, pom.xml
![](https://camo.githubusercontent.com/cb827965b733f8ad90fa6688288094ce2a3704fa9e692252bcd0937e57a2e81f/687474703a2f2f746573742e62646966662e6e65742f7075626c69632f6f6b687474702d633836333838313366663566393037313534313765343839623334326161653565343130633562322d706f6d2e786d6c2e706e67)
### 3.9 Converting spaces to indentation
scikit-learn/scikit-learn, 612312553118371289330f50b38653d1206246c0, gene.py
![](https://camo.githubusercontent.com/709ab2f039dc07ddaa56c962943272ac5ceb1c5415414d25e86db34be05d870e/687474703a2f2f746573742e62646966662e6e65742f7075626c69632f7363696b69742d6c6561726e2d363132333132353533313138333731323839333330663530623338363533643132303632343663302d67656e652e70792e706e67)
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
We have conducted a comprehensive evaluation experiment on BDiff, with detailed results available in our paper: [https://arxiv.org/abs/2510.21094](https://arxiv.org/abs/2510.21094). We are glad if you cite the relevant article in the following bibtex:
```bibtex
@misc{lu2025bdiffblockawareaccuratetextbased,
      title={BDiff: Block-aware and Accurate Text-based Code Differencing}, 
      author={Yao Lu and Wanwei Liu and Tanghaoran Zhang and Kang Yang and Yang Zhang and Wenyu Xu and Longfei Sun and Xinjun Mao and Shuzheng Gao and Michael R. Lyu},
      year={2025},
      eprint={2510.21094},
      archivePrefix={arXiv},
      primaryClass={cs.SE},
      url={https://arxiv.org/abs/2510.21094}, 
}
```
