# Project on Index Generation

## Files
- `index_generation.py`: Trie, BST and dictionary implementations; file parsing; sorted output; command-line utility.
- `benchmark.py`: performance test and Matplotlib graph generation.
- `test_index_generation.py`: automated tests.
- `DESIGN_REPORT.md`: design, complexity, benchmarking method and test-case explanation.

## Run the utility
```bash
python index_generation.py input.txt output.txt
```
The program accepts the required two command-line arguments: input filename and output filename. The command-line utility uses the dictionary implementation by default; all three implementations are available in the module and benchmarked by `benchmark.py`.

## Run tests
```bash
python -m unittest -v test_index_generation.py
```

## Run benchmarks and create graphs
Install Matplotlib if necessary:
```bash
python -m pip install matplotlib
python benchmark.py
```
The benchmark creates six datasets with 1,100,000 word occurrences each and the requested distinct-word counts (1,000, 5,000, 10,000, 50,000, 100,000 and 500,000). It compares construction, 100,000 random successful searches and sorted index printing for all three structures, then saves CSV results and three PNG graphs. The largest tests can be slow and memory-intensive. Timings are machine-dependent, so run the script to obtain real measurements before reporting them.

## Input handling
Words are separated by whitespace, line breaks, full stop, comma, colon or semicolon. Letter case is preserved. Every occurrence is recorded, including repeated words on the same line.
