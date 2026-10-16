import tempfile
import unittest
from pathlib import Path

from index_generation import TrieIndex, BSTIndex, DictionaryIndex, build_index, write_index


class IndexTests(unittest.TestCase):
    def test_all_structures_handle_duplicates_and_line_numbers(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "input.txt"
            source.write_text("apple apple, banana.\nbanana: apple;cat\n", encoding="ascii")
            for index_class in (TrieIndex, BSTIndex, DictionaryIndex):
                index = build_index(index_class, source)
                self.assertEqual(index.search("apple"), [1, 1, 2])
                self.assertEqual(index.search("banana"), [1, 2])
                self.assertEqual(index.search("missing"), None)

    def test_output_is_lexicographic(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "input.txt"
            output = Path(temp) / "output.txt"
            source.write_text("zebra apple Mango\n", encoding="ascii")
            index = build_index(DictionaryIndex, source)
            write_index(index, output)
            lines = output.read_text(encoding="ascii").splitlines()
            self.assertEqual([line.split("\t")[0] for line in lines], ["Mango", "apple", "zebra"])


if __name__ == "__main__":
    unittest.main()
