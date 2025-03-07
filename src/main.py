import os
import shutil
from src.copy_static import copy_files_recursive

static_dir = "./static/"
public_dir = "./public/"


def main():
    print("Checking for static files...")
    if not os.path.exists(static_dir):
        raise Exception('"Static" directory not found in project root')
    print("Deleting public directory...")
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    copy_files_recursive(static_dir, public_dir)


main()
