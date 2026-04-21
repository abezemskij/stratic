import unittest

from helper_functions import *

class TestLeafNode(unittest.TestCase):
	def test_extract_markdown_images(self):
		matches = extract_markdown_images("This is text with an ![image](https://twizzer.com/shared.png)")
		self.assertListEqual([("image", "https://twizzer.com/shared.png")], matches)

	def extract_markdown_links(self):
		matches = extract_markdown_images("This is text with an [external](https://www.google.com:443/test)")
		self.assertListEqual([("external", "https://i.imgur.com/zjjcJKZ.png")], matches)

if __name__ == "__main__":
	unittest.main()
