import os
import shutil
from src.copy_static import copy_files_recursive
from generate_page import generate_pages_recursive

static_dir = "./static/"
public_dir = "./public/"
content_dir = "./content"
template_path = "./template.html"


def main():
    print("Checking for static files...")
    if not os.path.exists(static_dir):
        raise Exception('"Static" directory not found in project root')
    print("Deleting public directory...")

    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)

    copy_files_recursive(static_dir, public_dir)

    generate_pages_recursive(content_dir, template_path, public_dir)


main()
