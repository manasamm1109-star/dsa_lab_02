# Design Report: Index Generation

## Objective
Read a text file and create a lexicographically sorted word index. Each word is followed by all 1-based line numbers where it appears. Repeated occurrences must be retained, including repeated occurrences on the same line.

## Word extraction
The program reads the file line by line. Whitespace and `.`, `,`, `:` and `;` separate words. Empty tokens are ignored. Case is preserved; Python string comparison gives ASCII lexicographic ordering for ASCII input.

## Data structures
### Trie
Each node contains child characters and a line-number list. A `None` line-number field means the character path is only a prefix, not a complete word. Insertion and search follow one child per character, so their character-traversal cost is O(L), where L is word length, plus appending the occurrence line number.

### Binary Search Tree (BST)
Each node stores a complete word, its line-number list, and left/right child pointers. Smaller words are inserted left and larger words right. In-order traversal prints the words in sorted order. Search and insertion cost O(h) comparisons, where h is the tree height; a plain BST can degrade to O(n) in the worst case.

### Python dictionary
The dictionary maps each word to a list of line numbers. Insertion and search are average O(1) per key operation (excluding reading the word and appending line numbers). Sorted output requires sorting the n distinct keys, O(n log n), plus writing the occurrence lists.

## Performance experiment
`benchmark.py` generates a dataset with 1,100,000 total word occurrences for each distinct-word count: 1,000; 5,000; 10,000; 50,000; 100,000; and 500,000. For each data structure it measures full construction time, 100,000 random successful searches, and sorted index output time. Matplotlib is used to plot the three metrics separately. Measurements depend on computer hardware and should be taken on the machine used for evaluation; no benchmark values should be invented. Rerun the benchmark after changing the occurrence count so the CSV and graphs match this configuration.

## Test cases
1. Repeated word on the same line: `apple apple` should store line number 1 twice.
2. Word repeated on different lines: `apple` on lines 1 and 2 should store `[1, 2]`.
3. Punctuation delimiters split words.
4. Searching for a missing word returns `None`.
5. Output words are in lexicographic order and preserve case.

## Conclusion
The dictionary is typically the simplest and fastest option in Python for this task. Trie search is based on word length. The unbalanced BST may become slow for unfavorable insertion order. The benchmark output should be used to compare actual timings.
