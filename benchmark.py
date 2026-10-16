"""
Optional benchmark runner.
Creates six text files, each with 1,100,000 word occurrences and a different
number of distinct words, then measures Trie, BST, and dictionary performance.

Run: python benchmark.py
Warning: the largest Trie/BST tests can take a long time and require substantial RAM.
"""

import gc
import random
import string
import time
from pathlib import Path

import matplotlib.pyplot as plt

from index_generation import TrieIndex, BSTIndex, DictionaryIndex, words_with_line_numbers, write_index

DISTINCT_COUNTS = [1000, 5000, 10000, 50000, 100000, 500000]
TOTAL_WORD_OCCURRENCES = 1_100_000
STRUCTURES = {
    "Trie": TrieIndex,
    "BST": BSTIndex,
    "Dictionary": DictionaryIndex,
}
DATA_DIR = Path("benchmark_data")
RESULTS_FILE = Path("benchmark_results.csv")


def make_word(number):
    """Create a unique ASCII word with a common prefix."""
    return "word" + format(number, "06d")


def generate_file(distinct_count):
    DATA_DIR.mkdir(exist_ok=True)
    path = DATA_DIR / f"words_{distinct_count}.txt"
    vocabulary = [make_word(i) for i in range(distinct_count)]
    rng = random.Random(12345 + distinct_count)
    with path.open("w", encoding="ascii") as file:
        batch = []
        for i in range(TOTAL_WORD_OCCURRENCES):
            batch.append(vocabulary[rng.randrange(distinct_count)])
            if len(batch) == 100:
                file.write(" ".join(batch) + "\n")
                batch.clear()
        if batch:
            file.write(" ".join(batch) + "\n")
    return path, vocabulary


def timed_build(index_class, path):
    index = index_class()
    start = time.perf_counter()
    for word, line_number in words_with_line_numbers(path):
        index.add(word, line_number)
    return index, time.perf_counter() - start


def timed_search(index, vocabulary):
    rng = random.Random(9876)
    queries = [vocabulary[rng.randrange(len(vocabulary))] for _ in range(100_000)]
    start = time.perf_counter()
    for word in queries:
        index.search(word)
    return time.perf_counter() - start


def timed_print(index, output_path):
    start = time.perf_counter()
    write_index(index, output_path)
    return time.perf_counter() - start


def main():
    results = []
    for distinct_count in DISTINCT_COUNTS:
        print(f"\nDataset: {distinct_count:,} distinct words")
        path, vocabulary = generate_file(distinct_count)

        for name, index_class in STRUCTURES.items():
            print(f"  Building {name}...")
            index, build_seconds = timed_build(index_class, path)
            search_seconds = timed_search(index, vocabulary)
            print_seconds = timed_print(index, DATA_DIR / f"{name.lower()}_{distinct_count}.txt")
            row = {
                "distinct_words": distinct_count,
                "structure": name,
                "construction_seconds": build_seconds,
                "search_100000_seconds": search_seconds,
                "printing_seconds": print_seconds,
            }
            results.append(row)
            print(f"    build={build_seconds:.3f}s, search={search_seconds:.3f}s, print={print_seconds:.3f}s")
            del index
            gc.collect()

    import csv
    with RESULTS_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    for metric, ylabel, filename in [
        ("construction_seconds", "Construction time (seconds)", "construction.png"),
        ("search_100000_seconds", "Time for 100,000 searches (seconds)", "search.png"),
        ("printing_seconds", "Sorted index printing time (seconds)", "printing.png"),
    ]:
        plt.figure()
        for name in STRUCTURES:
            rows = [r for r in results if r["structure"] == name]
            plt.plot([r["distinct_words"] for r in rows], [r[metric] for r in rows],
                     marker="o", label=name)
        plt.xlabel("Number of distinct words")
        plt.ylabel(ylabel)
        plt.title(ylabel + " vs. distinct words")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(filename, dpi=150)
        plt.close()

    print(f"\nSaved measurements to {RESULTS_FILE}")
    print("Saved graphs: construction.png, search.png, printing.png")


if __name__ == "__main__":
    main()
