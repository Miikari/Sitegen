import shutil
import os
from pathlib import Path
from markdown_blocks import markdown_to_blocks, markdown_to_html_node, extract_title

source = "static/"
destination = "public/"

def source_to_destination():
    shutil.rmtree(destination, ignore_errors=False)
    os.mkdir(destination)
    print_files(source, destination)
    print("onnistui!")

def print_files(src, dst):
    print(f"copying contents of dir 1: {src}")
    files = os.listdir(src)
    print(files)
    for file in files:
        print(file)
        if not os.path.isfile(f"{src}/{file}"):
            os.mkdir(f"{dst}/{file}")
            print_files(f"{src}{file}/", f"{dst}{file}/")
        else:
            shutil.copy(f"{src}{file}", dst)
            print(f"copying: {file}")


    return

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    f = open(from_path)
    contents = f.read()
    f.close()
    t = open(template_path)
    template_contents = t.read()
    t.close()
    markdown = markdown_to_html_node(contents)
    html_string = markdown.to_html()
    title_to_be = extract_title(contents)
    updated_template = template_contents.replace("{{ Title }}", title_to_be)
    updated_template = updated_template.replace("{{ Content }}", html_string)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    d = open(dest_path, "w")
    d.write(updated_template)
    d.close()

def generate_recursive(from_dir_path, template_path, dest_dir):
    files = os.listdir(from_dir_path)
    print(files)
    for file in files:
        print(file)
        if not os.path.isfile(f"{from_dir_path}/{file}"):
            generate_recursive(os.path.join(from_dir_path, file), template_path, os.path.join(dest_dir, file),)
        elif file.endswith(".md"):
            generate_page(os.path.join(from_dir_path, file),template_path,os.path.join(dest_dir, Path(file).with_suffix(".html")))
            print(f"copying: {file}")
        else:
            shutil.copy(os.path.join(from_dir_path, file), dest_dir)
            print(f"copying: {file}")

