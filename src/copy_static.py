import os
import shutil


def copy_files_recursive(current_source_path, current_dest_path):
    if not os.path.exists(current_dest_path):
        print(f"Making directory: {current_dest_path}")
        os.mkdir(current_dest_path)

    for item in os.listdir(current_source_path):
        source_item_path = os.path.join(current_source_path, item)
        dest_item_path = os.path.join(current_dest_path, item)

        if os.path.isfile(source_item_path):
            print(f"Copying: {source_item_path} > {dest_item_path}")
            shutil.copy(source_item_path, dest_item_path)
        else:
            copy_files_recursive(source_item_path, dest_item_path)
