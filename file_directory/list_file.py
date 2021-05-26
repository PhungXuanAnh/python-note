import os
import glob
import json


def list_file_by_pattern_on_current_folder(folder):
    # NOTE: only list *.py file on current folder, not in sub-folder
    os.chdir(folder)
    for file in glob.glob("*.py"):
        print(file)


def list_file_with_extension_on_current_folder(folder):
    for file in os.listdir(folder):
        if file.endswith(".py"):
            print(file)


def list_file_with_extension_include_sub_folder(folder):
    for root, dirs, files in os.walk(folder):
        # print(root)
        # print(dirs)
        # print(files)

        for file in files:
            if file.endswith(".py"):
                print(os.path.join(root, file))
            


if __name__ == "__main__":
    from pathlib import Path
    folder = Path(__file__).resolve(strict=True).parent             # file_directory folder
    # folder = Path(__file__).resolve(strict=True).parent.parent    # python-note folder


    # list_file_by_pattern_on_current_folder(folder)
    # list_file_with_extension_on_current_folder(folder)
    list_file_with_extension_include_sub_folder(folder)
