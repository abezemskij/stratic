import unittest

from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
	def test_create(self):
		node = LeafNode()
		node2 = LeafNode("h1")
		node3 = LeafNode("h1", "This is a paragraph")
		node5 = LeafNode("h1", "This is a paragraph", {"href": "https://www.google.com", "target": "_blank",})
		self.assertEqual(node5.__repr__(), "LeafNode(h1, This is a paragraph, {'href': 'https://www.google.com', 'target': '_blank'})")
		self.assertEqual(node3.__repr__(), "LeafNode(h1, This is a paragraph, None)")

	def test_to_html(self):
		node3 = LeafNode("h1", "")
		node = LeafNode("h1", None, {"href": "https://www.google.com", "target": "_blank",})
		self.assertRaises(ValueError, node.to_html)
		self.assertRaises(ValueError, node3.to_html)
		self.assertEqual(LeafNode("a", "Click me!", {"href": "https://www.google.com"}).to_html(), "<a href=\"https://www.google.com\" >Click me!</a>")

if __name__ == "__main__":
	unittest.main()
