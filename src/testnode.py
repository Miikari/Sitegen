import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, split_nodes_images, split_nodes_link, text_to_textnodes


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        node = TextNode("This is a text nodes", TextType.ITALIC)
        node2 = TextNode("This is a text nodes", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq2(self):
        node = TextNode("This is a text noe", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

        node = TextNode("This is a text node", TextType.BOLD, "https://")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://")
        self.assertEqual(node, node2)

        node = TextNode("Thsis is a text node", TextType.BOLD, "https://")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://")
        self.assertNotEqual(node, node2)

        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "https://")
        self.assertNotEqual(node, node2)

        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node, node2)
        self.assertEqual(text_node_to_html_node(node).to_html(), '<b>This is a text node</b>')

    def test_nodes(self):
        node = TextNode("Hello", TextType.LINK, "https://")
        self.assertEqual(text_node_to_html_node(node).to_html(), '<a href="https://">Hello</a>')
        node = TextNode("Hello", TextType.IMAGE, "https://")
        self.assertEqual(text_node_to_html_node(node).to_html(), '<img src="https://" alt="Hello"></img>')
        
        
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual([
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ], new_nodes)     

        
        node = TextNode("This is text with a **BOLD block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual([
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("BOLD block", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ], new_nodes)

        node = TextNode("This is text with a BOLD block** word", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(str(context.exception), "Invalid markdown syntax")

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )
        
        node = TextNode(
            "[to boot dev](https://www.boot.dev)This is text with a link and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode("This is text with a link and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

        node = TextNode(
            "[to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")
                ,
            ],
            new_nodes,
        )
    def test_split(self):
        node = TextNode(
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
            TextType.TEXT,
        )
        new_nodes = text_to_textnodes(node.text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )   




if __name__ == "__main__":
    unittest.main()