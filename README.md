# String-Visualiser
# String Matching Visualizer — KMP vs Rabin-Karp

An interactive, step-by-step visual comparison of two classic string matching algorithms: **Knuth-Morris-Pratt (KMP)** and **Rabin-Karp**. Built with Python and Streamlit, this tool is designed for learning and academic exploration of algorithmic behaviour.

---

## Overview

String matching is a fundamental problem in computer science — finding where a pattern occurs inside a text. This project visualizes two well-known algorithms side by side, letting you watch each one work in real time and compare the number of steps each takes.

---

## Algorithms Implemented

### 1. KMP (Knuth-Morris-Pratt)

- Preprocesses the pattern to build an **LPS (Longest Proper Prefix which is also Suffix)** array
- Uses the LPS array to skip redundant comparisons, never re-scanning characters already matched
- Time complexity: **O(n + m)** — where n is text length and m is pattern length
- Space complexity: **O(m)** for the LPS array
- **Key Feature**: Guaranteed linear time with no backtracking in the text

### 2. Rabin-Karp

- Uses **rolling hashes** to compare the pattern hash against substrings of the text
- Only performs character-by-character verification on hash matches (to handle collisions)
- Average time complexity: **O(n + m)**
- Worst-case time complexity: **O(nm)** (when many hash collisions occur)
- **Key Feature**: Very efficient in practice; naturally extends to multi-pattern search

---

## Time Complexity Comparison

| Algorithm   | Preprocessing | Search (Average) | Search (Worst) | Space |
|-------------|---------------|------------------|----------------|-------|
| KMP         | O(m)          | O(n)             | O(n)           | O(m)  |
| Rabin-Karp  | O(m)          | O(n)             | O(nm)          | O(1)  |

---

## Features

- **Real-time step-by-step animation** of both algorithms running simultaneously
- **LPS array construction** visualized character by character for KMP
- **Colour-coded highlighting**: current character comparisons, matches, and mismatches
- **Step counter** for each algorithm so you can compare efficiency on your own input
- **Adjustable speed slider** to slow down or speed up the visualization
- **Bar chart** comparing total steps taken by each algorithm at the end
- **Custom input**: enter your own text and pattern to experiment

---

## Project Structure

```
String-Visualiser/
├── README.md          # This file
└── app.py             # Main Streamlit application
```

### `app.py` — Key Components

| Function | Description |
|---|---|
| `compute_lps_visual()` | Builds and animates the LPS array for KMP preprocessing |
| `render_kmp()` | Renders the KMP comparison state with colour-coded characters |
| `render_rk()` | Renders the Rabin-Karp sliding window state |
| Main loop | Runs both algorithms in lockstep with shared progress and timing |

---

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip

### Install Dependencies

```bash
pip install streamlit matplotlib
```

### Run the App

```bash
streamlit run app.py
```

Then open your browser to: **http://localhost:8501**

---

## How to Use

1. **Enter a text** in the "Text" input field (default: `ABABDABACDABABCABAB`)
2. **Enter a pattern** to search for (default: `ABABCABAB`)
3. **Adjust the speed** slider — lower values are slower and easier to follow
4. Click **"Start Comparison"** to begin the visualization
5. Watch both columns animate simultaneously:
   - **Left column**: KMP with LPS array being built first, then the search
   - **Right column**: Rabin-Karp sliding window hash search
6. After the run, a **bar chart** shows the total step count for each algorithm

---

## Visual Guide

| Color | Meaning |
|---|---|
| 🟠 Orange | Current character being processed in LPS construction |
| 🟢 Green | Match found at current position |
| 🔴 Red | Mismatch at current position / Rabin-Karp sliding window |
| 🔵 Blue | Pattern being aligned below the text |

---

## Example

**Text**: `ABABDABACDABABCABAB`  
**Pattern**: `ABABCABAB`

KMP will build the LPS array `[0, 0, 1, 2, 0, 1, 2, 3, 4]` first, then scan the text linearly. Rabin-Karp will slide a hash window across the text, verifying character-by-character only on hash matches. The step comparison bar chart will show which algorithm was more efficient for this particular input.

---

## Key Concepts

### LPS Array (KMP)

The LPS (Longest Proper Prefix which is also Suffix) array is the heart of KMP. For each position `i` in the pattern, `lps[i]` stores the length of the longest prefix of the pattern that is also a suffix of `pattern[0..i]`. This allows KMP to skip ahead intelligently on a mismatch rather than starting from scratch.

### Rolling Hash (Rabin-Karp)

Rabin-Karp computes a hash of the pattern and a hash of each m-length window of the text. When hashes match, it verifies character by character. The "rolling" part means the new window's hash is computed in O(1) from the old window's hash by removing the leftmost character and adding the new rightmost one.

---

## Academic References

1. **KMP**: Knuth, D. E., Morris, J. H., & Pratt, V. R. (1977). "Fast pattern matching in strings." *SIAM Journal on Computing*, 6(2), 323–350.
2. **Rabin-Karp**: Karp, R. M., & Rabin, M. O. (1987). "Efficient randomized pattern-matching algorithms." *IBM Journal of Research and Development*, 31(2), 249–260.

---

## License

MIT License — Free for academic and educational use.

---

## Author

Created as part of an Advanced Algorithms / Data Structures coursework project.
