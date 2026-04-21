import unittest

from textnode import TextNode, TextType
from htmlnode import *

class TestTextNode(unittest.TestCase):
	def test_eq(self):
		node = TextNode("This is a text node", TextType.TEXT_BOLD)
		node2 = TextNode("This is a text node", TextType.TEXT_BOLD)
		node3 = TextNode("This is a text node", TextType.TEXT_BOLD, "https://google.com/")
		node4 = TextNode("This is a text node", TextType.TEXT_BOLD, "https://google.com/")
		self.assertEqual(node, node2)
		self.assertEqual(node3, node4)

	def test_not_eq(self):
		node = TextNode("This is a text node", TextType.TEXT_BOLD)
		node2 = TextNode("This is a text node", TextType.TEXT_ITALIC)
		node3 = TextNode("This is a text node.", TextType.TEXT_BOLD)
		node4 = TextNode("This is a text node", TextType.TEXT_BOLD, "https://google.com/")
		node5 = TextNode("This is a text node", TextType.TEXT_BOLD, "https://go0gle.com/")
		node6 = TextNode("This is a text node", TextType.TEXT_BOLD, None)
		node7 = TextNode(None, TextType.TEXT_BOLD, "https://google.com/")
		node8 = TextNode("This is a text node", None, "https://google.com/")
		self.assertNotEqual(node, node2)
		self.assertNotEqual(node, node3)
		self.assertNotEqual(node4, node5)
		self.assertNotEqual(node4, node6)
		self.assertNotEqual(node7, node8)

	def test_edge(self):
		node = TextNode(None, None, None)
		self.assertEqual(node, node)

	def test_text(self):
	    node = TextNode("This is a text node", TextType.TEXT_PLAIN)
	    html_node = text_node_to_html_node(node)
	    self.assertEqual(html_node.tag, None)
	    self.assertEqual(html_node.value, "This is a text node")
	    #///
	    node = TextNode("This is a text node", TextType.TEXT_BOLD)
	    html_node = text_node_to_html_node(node)
	    self.assertEqual(html_node.tag, "b")
	    self.assertEqual(html_node.value, "This is a text node")
	    #///
	    node = TextNode("This is a text node", TextType.TEXT_CODE)
	    html_node = text_node_to_html_node(node)
	    self.assertEqual(html_node.tag, "code")
	    self.assertEqual(html_node.value, "This is a text node")
if __name__ == "__main__":
	unittest.main()
