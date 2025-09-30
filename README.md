BDiff is a browser-based file differencing tool that can identify precise differences between text files and generate corresponding edit scripts. It can be applied in scenarios such as code review and change analysis.

## I. 🎻 Main Features
- Comprehensive Difference Identification: It can identify line deletions, line additions, line updates, line splits, line merges, block copies (including line updates), and block moves (including line updates).
- Generate Edit Scripts: Produces edit scripts based on the identified differences.
- Display Updated Difference Substrings: Shows the specific substrings that have been updated.
- Edit Action Localization: Helps pinpoint the edit actions within the script.
- View Before-and-After Mapped Lines/Blocks: Allows users to view the mapped lines or blocks before and after the changes.
- Set Difference Display Modes: Offers alignment mode and compact mode for displaying differences.
- Language Settings: Supports Chinese and English.
- Theme Settings: Switch between light and dark themes for comfortable viewing.
- Difference Option Settings: Customize comparison parameters for precise results.
- Programming Language Highlighting: Syntax-aware highlighting for major programming languages.
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
## 3. 🚩 Real-world Cases
### 3.1 Changing the order of parameter and member variable assignments
kitao/pyxel, 3861523a200da507f36edf478729f4ec7c269775, app.py
![](http://test.bdiff.net/public/pyxel-3861523a200da507f36edf478729f4ec7c269775-app.py.png)
### 3.2 Moving the try statement block
psf/requests, cde3b88f3e93a9503810acc0ded890025fcbc119, core.py
![]{http://test.bdiff.net/public/requests-cde3b88f3e93a9503810acc0ded890025fcbc119-core.py.png}
