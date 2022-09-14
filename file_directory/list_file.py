import os
import glob
import json
from tkinter import N


def list_file_with_extension_on_current_folder(folder):
    # NOTE: only list *.py file on current folder, not in sub-folder
    
    # cach 1
    os.chdir(folder)
    for file in glob.glob("*.py"):
        print(file)

    # cach 2
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


def list_files_with_parttern(folder, include_pattern, exclude_pattern):
    # for root, dirs, files in os.walk(rootdir):
    #     for file in files:
    #         if regex.match(file):
    #         print(file)
    
    # https://docs.python.org/3/library/glob.html
    include_pattern = folder + '/**/*.py'
    import glob
    for name in glob.glob(include_pattern, recursive=True):
        print(name)
        # if regex.match(exclude_pattern):
            # print(name)


if __name__ == "__main__":
    from pathlib import Path

    folder = Path(__file__).resolve(strict=True).parent.parent

    # list_file_with_extension_on_current_folder(folder)
    # list_file_with_extension_include_sub_folder(folder)

    list_files_with_parttern(str(folder), '', '')

    print("--> listed files in folder: ", folder)
