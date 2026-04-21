import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
	def test_create(self):
		node = HTMLNode()
		node2 = HTMLNode("h1")
		node3 = HTMLNode("h1", "This is a paragraph")
		node4 = HTMLNode("h1", "This is a paragraph", node3)
		node5 = HTMLNode("h1", "This is a paragraph", node3, {"href": "https://www.google.com", "target": "_blank",})
		self.assertEqual(node3.__repr__(), "HTMLNode(h1, This is a paragraph, None, None)")
		self.assertEqual(node5.__repr__(), "HTMLNode(h1, This is a paragraph, HTMLNode(h1, This is a paragraph, None, None), {'href': 'https://www.google.com', 'target': '_blank'})")
		

	def test_to_html(self):
		node3 = HTMLNode("h1", "This is a paragraph")
		node = HTMLNode("h1", "This is a paragraph", node3, {"href": "https://www.google.com", "target": "_blank",})
		self.assertRaises(NotImplementedError, node.to_html)

	def test_properties_to_html(self):
		node3 = HTMLNode("h1", "This is a paragraph")
		node = HTMLNode("h1", "This is a paragraph", node3, {"href": "https://www.google.com", "target": "_blank",})
		self.assertEqual(node.properties_to_html(), "href=\"https://www.google.com\" target=\"_blank\" ")
		self.assertEqual(node3.properties_to_html(), "")
		

	def test_to_html_with_children(self):
	    child_node = LeafNode("span", "child")
	    parent_node = ParentNode("div", [child_node])
	    self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

	def test_to_html_with_grandchildren(self):
	    grandchild_node = LeafNode("b", "grandchild")
	    child_node = ParentNode("span", [grandchild_node])
	    parent_node = ParentNode("div", [child_node])
	    self.assertEqual(
	        parent_node.to_html(),
	        "<div><span><b>grandchild</b></span></div>",
	    )

if __name__ == "__main__":
	unittest.main()
