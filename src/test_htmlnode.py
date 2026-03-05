import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import text_node_to_html_node

class TestHtmlNode(unittest.TestCase):
    def test_print(self):
        d = dict()
        d["href"] = "https://www.google.com"
        d["target"] = "_blank"
        d2 = dict()
        d2["href"] = "https://www.google.com"
        d2["target"] = "_blank"
        d3 = dict()
        d3["href"] = "https://www.google.com"
        d3["target"] = "_ablank"
        node = HTMLNode("<p>", "Hello", None, d)
        node2 = HTMLNode("<p>", "Hello", None, d3)
        self.assertEqual(
        ' href="https://www.google.com" target="_blank"', node.props_to_html()
        )
        self.assertNotEqual(
        ' href="https://www.google.com" target="_ablank"', node.props_to_html()
        )
    
    def test_leaf_to_html_p(self):
        l = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual("<p>This is a paragraph of text.</p>", l.to_html())
        n = LeafNode("p", "Hello, world!")
        self.assertEqual(n.to_html(), "<p>Hello, world!</p>")
        x = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual('<a href="https://www.google.com">Click me!</a>', x.to_html())

    def test_parent_to_html(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        parent2_node = ParentNode("a", [child_node], {"href": "https://www.google.com"})
        parent3_node = ParentNode("a",None ,{"href": "https://www.google.com"})
        parent4_node = ParentNode(None, [child_node])
        self.assertEqual(
        parent_node.to_html(),
        "<div><span><b>grandchild</b></span></div>",
        )
        self.assertEqual(
        parent2_node.to_html(),
        '<a href="https://www.google.com"><span><b>grandchild</b></span></a>',
        )
        with self.assertRaises(ValueError) as context:
            parent3_node.to_html()
        self.assertEqual(str(context.exception), "No children found")
        
        with self.assertRaises(ValueError) as context:
            parent4_node.to_html()
        self.assertEqual(str(context.exception), "No tag found")

if __name__ == "__main__":
    unittest.main()