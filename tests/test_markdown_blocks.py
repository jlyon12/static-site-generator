import unittest

from src.textnode import text_node_to_html_node, TextNode, TextType
from src.markdown_blocks import (
    BlockType,
    markdown_to_html_node,
    markdown_to_blocks,
    block_to_block_type,
)


class TestTextToHtmlNode(unittest.TestCase):
    # Test conversion of a normal text node without formatting
    def test_text(self):
        text_node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    # Test conversion of a bold text node
    def test_text_node_to_html_node_bold(self):
        text_node = TextNode("bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<b>bold text</b>")

    # Test conversion of an italic text node
    def test_text_node_to_html_node_italic(self):
        text_node = TextNode("italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<i>italic text</i>")

    # Test conversion of a code text node
    def test_text_node_to_html_node_code(self):
        text_node = TextNode("print('Hello')", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<code>print('Hello')</code>")

    # Test conversion of a hyperlink text node
    def test_text_node_to_html_node_link(self):
        text_node = TextNode("Arch Linux", TextType.LINK, "http://archlinux.org")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(
            html_node.to_html(), '<a href="http://archlinux.org">Arch Linux</a>'
        )

    # Test conversion of an image text node with alt text
    def test_text_node_to_html_node_image(self):
        text_node = TextNode(
            "Arch Linux Logo", TextType.IMAGE, "http://archlinux.org/logo.png"
        )
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(
            html_node.to_html(),
            '<img src="http://archlinux.org/logo.png" alt="Arch Linux Logo"></img>',
        )

    # Test handling of an invalid text type
    def test_text_node_to_html_node_invalid_type(self):
        with self.assertRaises(Exception):
            text_node = TextNode("Invalid", "invalid_type")
            text_node_to_html_node(text_node)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestBlockType(unittest.TestCase):

    # Test for heading blocks (1-6 '#')
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)

    # Test for code blocks (3 backticks at the start and end)
    def test_code(self):
        self.assertEqual(block_to_block_type("```\nCode block\n```"), BlockType.CODE)

    # Test for quote blocks (">" at the start of each line)
    def test_quote(self):
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
        self.assertEqual(
            block_to_block_type("> This is a quote\n> Second line"), BlockType.QUOTE
        )

    # Test for unordered list blocks (starts with "- ")
    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- Item 1"), BlockType.UNORDERED_LIST)
        self.assertEqual(
            block_to_block_type("- Item 2\n- Item 3"), BlockType.UNORDERED_LIST
        )

    # Test for ordered list blocks (starts with "1. ")
    def test_ordered_list(self):
        self.assertEqual(
            block_to_block_type("1. Item 1\n2. Item 2\n3. Item 3"),
            BlockType.ORDERED_LIST,
        )

    # Test for paragraph blocks (no specific marker)
    def test_paragraph(self):
        self.assertEqual(
            block_to_block_type("This is a normal paragraph."), BlockType.PARAGRAPH
        )
        self.assertEqual(block_to_block_type("Another paragraph."), BlockType.PARAGRAPH)
        self.assertEqual(
            block_to_block_type("Random text with no special symbols."),
            BlockType.PARAGRAPH,
        )

    # Edge case: empty block (should default to paragraph)
    def test_empty_block(self):
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)

    # Edge case: heading with extra spaces
    def test_heading_with_spaces(self):
        self.assertEqual(
            block_to_block_type("###   Heading with extra spaces   "), BlockType.HEADING
        )


class TestMarkdownToHtml(unittest.TestCase):

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()
