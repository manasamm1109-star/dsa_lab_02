"""
Index Generation project
Usage: python index_generation.py INPUT.txt OUTPUT.txt
Indexes words by line number using Trie, Binary Search Tree, and Python dictionary.
"""

import re
import sys
from time import perf_counter


# Words are separated by whitespace or the specified punctuation.
DELIMITERS = re.compile(r"[\s.,:;]+")


def words_with_line_numbers(filename):
    """Yield (word, line_number) pairs, preserving word case and ASCII order."""
    with open(filename, "r", encoding="ascii", errors="replace", newline=None) as file:
        for line_number, line in enumerate(file, start=1):
            for word in DELIMITERS.split(line.strip()):
                if word:
                    yield word, line_number


class TrieNode:
    def __init__(self):
        self.children = {}
        self.line_numbers = None  # None means this character path is not a complete word


class TrieIndex:
    def __init__(self):
        self.root = TrieNode()

    def add(self, word, line_number):
        node = self.root
        for character in word:
            if character not in node.children:
                node.children[character] = TrieNode()
            node = node.children[character]
        if node.line_numbers is None:
            node.line_numbers = []
        node.line_numbers.append(line_number)

    def search(self, word):
        node = self.root
        for character in word:
            node = node.children.get(character)
            if node is None:
                return None
        return node.line_numbers

    def items_sorted(self):
        """Iterative lexicographic traversal; avoids Python recursion limits."""
        stack = [(self.root, "")]
        while stack:
            node, prefix = stack.pop()
            if node.line_numbers is not None:
                yield prefix, node.line_numbers
            # Reverse push order so popping visits characters in ASCII order.
            for character in sorted(node.children.keys(), reverse=True):
                stack.append((node.children[character], prefix + character))


class BSTNode:
    def __init__(self, word, line_number):
        self.word = word
        self.line_numbers = [line_number]
        self.left = None
        self.right = None


class BSTIndex:
    def __init__(self):
        self.root = None

    def add(self, word, line_number):
        if self.root is None:
            self.root = BSTNode(word, line_number)
            return
        node = self.root
        while True:
            if word == node.word:
                node.line_numbers.append(line_number)
                return
            if word < node.word:
                if node.left is None:
                    node.left = BSTNode(word, line_number)
                    return
                node = node.left
            else:
                if node.right is None:
                    node.right = BSTNode(word, line_number)
                    return
                node = node.right

    def search(self, word):
        node = self.root
        while node is not None:
            if word == node.word:
                return node.line_numbers
            node = node.left if word < node.word else node.right
        return None

    def items_sorted(self):
        stack = []
        node = self.root
        while stack or node is not None:
            while node is not None:
                stack.append(node)
                node = node.left
            node = stack.pop()
            yield node.word, node.line_numbers
            node = node.right


class DictionaryIndex:
    def __init__(self):
        self.data = {}

    def add(self, word, line_number):
        self.data.setdefault(word, []).append(line_number)

    def search(self, word):
        return self.data.get(word)

    def items_sorted(self):
        for word in sorted(self.data):
            yield word, self.data[word]


def write_index(index, output_filename):
    """Write words in lexicographic order and their occurrence line numbers."""
    with open(output_filename, "w", encoding="ascii", errors="replace") as output:
        for word, line_numbers in index.items_sorted():
            output.write(f"{word}\t{', '.join(map(str, line_numbers))}\n")


def build_index(index_class, input_filename):
    index = index_class()
    for word, line_number in words_with_line_numbers(input_filename):
        index.add(word, line_number)
    return index


def main():
    if len(sys.argv) != 3:
        print("Usage: python index_generation.py INPUT.txt OUTPUT.txt")
        raise SystemExit(2)

    input_filename, output_filename = sys.argv[1], sys.argv[2]
    # The required command-line utility uses the dictionary implementation by default.
    start = perf_counter()
    index = build_index(DictionaryIndex, input_filename)
    construction_time = perf_counter() - start

    start = perf_counter()
    write_index(index, output_filename)
    printing_time = perf_counter() - start

    print(f"Words indexed (distinct): {len(index.data)}")
    print(f"Construction time: {construction_time:.6f} seconds")
    print(f"Index output time: {printing_time:.6f} seconds")
    print(f"Index written to: {output_filename}")


if __name__ == "__main__":
    main()
