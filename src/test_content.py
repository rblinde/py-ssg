import unittest

from content import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_empty(self):
        self.assertRaises(ValueError, extract_title, "")

    def test_no_heading(self):
        self.assertRaises(
            ValueError,
            extract_title,
            "some text here\n\n## heading two\n\nanother paragraph",
        )

    def test_simple_heading(self):
        self.assertEqual(extract_title("# simple "), "simple")

    def test_heading_not_first(self):
        result = extract_title("some text here\n\n# heading one\n\nanother paragraph")
        self.assertEqual(result, "heading one")
