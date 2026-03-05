import unittest

from markdown_blocks import markdown_to_blocks, extract_title
class TestMarkdownBlocks(unittest.TestCase):

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

        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is `the` same paragraph on a new line
And this is last

- This is a list
- with items
- something
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is `the` same paragraph on a new line\nAnd this is last",
                "- This is a list\n- with items\n- something",
            ],
        )
    
    def test_header(self):
        md = """
#  This is **bolded** paragraph  

This is another paragraph with _italic_ text and `code` here
This is `the` same paragraph on a new line
And this is last

- This is a list
- with items
- something
"""
        markdown = extract_title(md)
        self.assertEqual(
            markdown,
            "This is **bolded** paragraph",
        )
        markdown = extract_title(md)
        self.assertNotEqual(
            markdown,
            "  This is **bolded** paragraph",
        )
        md = """
This is **bolded** paragraph  

## This is another paragraph with _italic_ text and `code` here
#This is `the` same paragraph on a new line
# And this is last

- This is a list
- with items
- something
"""
        markdown = extract_title(md)
        self.assertEqual(
            markdown,
            "And this is last",
        )
        


if __name__ == "__main__":
    unittest.main()