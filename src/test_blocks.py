import unittest

from blocks import BlockType, block_to_block_type, markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_empty(self):
        result = markdown_to_blocks("")
        want = []
        self.assertEqual(result, want)

    def test_only_new_lines(self):
        result = markdown_to_blocks(" \n\n \n \n\n")
        want = []
        self.assertEqual(result, want)

    def test_multiple_paragraphs(self):
        result = markdown_to_blocks("text\n\nmore text")
        want = ["text", "more text"]
        self.assertEqual(result, want)

    def test_full_doc(self):
        result = markdown_to_blocks(
            (
                "This is **bolded** paragraph\n\n"
                "This is another paragraph with _italic_ text and `code` here\n"
                "This is the same paragraph on a new line\n\n"
                "- This is a list\n"
                "- with items"
            )
        )
        want = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]
        self.assertEqual(result, want)


class TestBlockToBlockType(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)

    def test_headings(self):
        self.assertEqual(block_to_block_type("# heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#### heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("##### heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("##heading"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("####### heading"), BlockType.PARAGRAPH)

    def test_code(self):
        self.assertEqual(
            block_to_block_type("```\nlet a = 'test';\n```"), BlockType.CODE
        )

    def test_quotes(self):
        self.assertEqual(block_to_block_type(">quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(">quote\n> quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(">"), BlockType.QUOTE)

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- item 1 "), BlockType.UNORDERED_LIST)
        self.assertEqual(
            block_to_block_type("- item 2\n- item 3"), BlockType.UNORDERED_LIST
        )
        self.assertEqual(block_to_block_type("-text"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("- text\n-text"), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. item 1 "), BlockType.ORDERED_LIST)
        self.assertEqual(
            block_to_block_type("1. item 2\n2. item 3"), BlockType.ORDERED_LIST
        )
        self.assertEqual(block_to_block_type("1.text"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1. text\n3. text"), BlockType.PARAGRAPH)
