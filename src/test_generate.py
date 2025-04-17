import unittest
from generate import extract_title

class TestHtmlNode(unittest.TestCase):

    def test_extract_title_from_first_line_on_only_line(self):
        markdown = "# Title"
        result = extract_title(markdown)
        self.assertEqual(result, "Title")

    def test_extract_title_from_first_line(self):
        markdown = """# Title
        Not a title
        ## Not the right title
        """
        result = extract_title(markdown)
        self.assertEqual(result, "Title")

    def test_extract_title_from_first_content_example(self):
        markdown = """# Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

"""
        result = extract_title(markdown)
        self.assertEqual(result, "Tolkien Fan Club")