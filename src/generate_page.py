import os
import shutil
from src.markdown_blocks import markdown_to_html_node


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        words = line.split()
        if words and words[0] == "#":
            return line[1:].strip()
    raise ValueError("No H1 found in markdown")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        html = f.read()
        html = html.replace("{{ Title }}", extract_title(markdown))
        html = html.replace("{{ Content }}", markdown_to_html_node(markdown).to_html())

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    with open(os.path.join(dest_path), "w") as f:
        f.write(html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        print(f"Making directory: {dest_dir_path}")
        os.mkdir(dest_dir_path)
    for item in os.listdir(dir_path_content):
        source_item_path = os.path.join(dir_path_content, item)
        dest_item_path = os.path.join(dest_dir_path, item.replace(".md", ".html"))
        if os.path.isfile(source_item_path):
            generate_page(source_item_path, template_path, dest_item_path)
        else:
            generate_pages_recursive(source_item_path, template_path, dest_item_path)
