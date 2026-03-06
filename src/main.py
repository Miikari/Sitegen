from textnode import TextNode, TextType
from file_functions import source_to_destination, generate_recursive
import sys

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    generate_recursive("content/", "template.html", "docs/", basepath)




if __name__ == "__main__":
    main()


