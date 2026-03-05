from textnode import TextNode, TextType
from file_functions import source_to_destination, generate_recursive
def main():
    source_to_destination()
    generate_recursive("content/", "template.html", "public/")




if __name__ == "__main__":
    main()


