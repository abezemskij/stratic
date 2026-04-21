from textnode import TextNode, TextType
from helper_functions import *
import sys

def main():
	basepath = "/"
	if len(sys.argv) > 1:
		basepath = sys.argv[1]
	copy_directory_contents("static", "docs")
	#generate_page("content/index.md", "template.html", "public/index.html")
	#generate_page("content/blog/glorfindel/index.md", "template.html", "public/blog/glorfindel/index.html")
	#generate_page("content/blog/tom/index.md", "template.html", "public/blog/tom/index.html")
	#generate_page("content/blog/majesty/index.md", "template.html", "public/blog/majesty/index.html")
	#generate_page("content/contact/index.md", "template.html", "public/contact/index.html")
	generate_pages_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
	main()