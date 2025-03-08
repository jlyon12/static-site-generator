import unittest
from src.generate_page import extract_title, generate_page


class TestExtractTitle(unittest.TestCase):

    # Test extracting a valid H1 title
    def test_valid_h1(self):
        md = "# Hello"
        self.assertEqual(extract_title(md), "Hello")

    # Test extracting an H1 with leading/trailing spaces
    def test_h1_with_extra_spaces(self):
        md = "#   Hello   "
        self.assertEqual(extract_title(md), "Hello")

    # Test extracting an H1 when other text follows
    def test_h1_with_text_after(self):
        md = "# Hello\n\nThis is some text."
        self.assertEqual(extract_title(md), "Hello")

    # Test extracting the first H1 when multiple headers exist
    def test_h1_among_other_headings(self):
        md = "# First Title\n\n## Second Title\n\n# Another H1"
        self.assertEqual(extract_title(md), "First Title")

    # Test extracting an H1 when it's not the first line
    def test_h1_not_first_line(self):
        md = "\n\n# Hello"
        self.assertEqual(extract_title(md), "Hello")

    # Test raising an exception when no H1 exists
    def test_no_h1(self):
        md = "## Subheading\n\nSome text."
        with self.assertRaises(ValueError):
            extract_title(md)

    # Test raising an exception for an empty input
    def test_empty_string(self):
        md = ""
        with self.assertRaises(ValueError):
            extract_title(md)

    # Test raising an exception when no headings exist
    def test_only_text_no_headings(self):
        md = "This is just some text."
        with self.assertRaises(ValueError):
            extract_title(md)

    # Test extracting an H1 with bold and italic formatting
    def test_h1_with_inline_formatting(self):
        md = "# **Hello** _World_"
        self.assertEqual(extract_title(md), "**Hello** _World_")

    # Test extracting an H1 with special characters
    def test_h1_with_special_characters(self):
        md = "# Welcome to @ChatGPT's Test Suite!"
        self.assertEqual(extract_title(md), "Welcome to @ChatGPT's Test Suite!")

    # Test extracting an H1 containing markdown-like syntax
    def test_h1_with_markdown_symbols(self):
        md = "# `Code` and *italic* and **bold**"
        self.assertEqual(extract_title(md), "`Code` and *italic* and **bold**")

    # Test extracting an H1 that contains numbers
    def test_h1_with_numbers(self):
        md = "# 1234 Heading 5678"
        self.assertEqual(extract_title(md), "1234 Heading 5678")

    # Test extracting an H1 with non-ASCII characters
    def test_h1_with_unicode(self):
        md = "# 你好，世界"
        self.assertEqual(extract_title(md), "你好，世界")

    # Test ensuring only single # headers are extracted
    def test_h1_with_multiple_hashes(self):
        md = "### Not a title\n\n# Actual Title\n\n## Another Subheading"
        self.assertEqual(extract_title(md), "Actual Title")

    # Test handling cases where # appears in text
    def test_h1_with_tricky_hash_symbol(self):
        md = "# Hello # World"
        self.assertEqual(extract_title(md), "Hello # World")


if __name__ == "__main__":
    unittest.main()
