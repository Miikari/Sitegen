from enum import Enum
import re
from htmlnode import LeafNode
from regex import extract_markdown_images, extract_markdown_links

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
    
def text_node_to_html_node(text_node):
    if text_node.text_type not in TextType:
        raise Exception("text type not supported")
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for on in old_nodes:
        if on.text_type == TextType.TEXT:
            split_nodes = on.text.split(delimiter)
            if len(split_nodes)%2 == 0:
                raise Exception("Invalid markdown syntax") 
            for i, sn in enumerate(split_nodes):
                if i % 2 != 0:
                    new_nodes.append(TextNode(sn, text_type))
                else:
                    if sn != "":
                        new_nodes.append(TextNode(sn, TextType.TEXT))
        else:
            new_nodes.append(on)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for on in old_nodes:
        if on.text_type != TextType.TEXT:
            new_nodes.append(on)
            continue
        links = extract_markdown_links(on.text)
        if not links:
            new_nodes.append(on)
            continue
        
        text_now = on.text

        for i in range(len(links)):
            split_nodes = text_now.split(f"[{links[i][0]}]({links[i][1]})")
            if split_nodes[0]:
                new_nodes.append(TextNode(split_nodes[0], TextType.TEXT))
            new_nodes.append(TextNode(links[i][0], TextType.LINK, links[i][1]))
            text_now = split_nodes[1]

        if text_now:
            new_nodes.append(TextNode(text_now, TextType.TEXT))

    return new_nodes

def split_nodes_images(old_nodes):
    new_nodes = []
    for on in old_nodes:
        if on.text_type != TextType.TEXT:
            new_nodes.append(on)
            continue
        imgs = extract_markdown_images(on.text)
        if not imgs:
            new_nodes.append(on)
            continue
        
        text_now = on.text

        for i in range(len(imgs)):
            #print(f"-----TÄSSÄ NYT IMGS KOKONAAN JA EKA ESIINTYMÄ {imgs, imgs[i][0]+imgs[i][1]}")
            split_nodes = text_now.split(f"![{imgs[i][0]}]({imgs[i][1]})")
            if split_nodes[0]:
                new_nodes.append(TextNode(split_nodes[0], TextType.TEXT))
            new_nodes.append(TextNode(imgs[i][0], TextType.IMAGE, imgs[i][1]))
            text_now = split_nodes[1]

        if text_now:
            new_nodes.append(TextNode(text_now, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_link(nodes)
    return nodes