import os
import shutil

from textnode import TextNode, TextType

def copy_directory(src, dest):
    print(f"Copying directory: {src} to {dest}")
    if not os.path.exists(dest):
        os.mkdir(dest)
    for filename in os.listdir(src):
        src_path = os.path.join(src, filename)
        dest_path = os.path.join(dest, filename)
        try:
            if os.path.isfile(src_path):
                print(f"Copying file: {src_path} to {dest_path}")
                shutil.copy(src_path, dest_path)
            elif os.path.isdir(src_path):
                copy_directory(src_path, dest_path)
        except Exception as e:
            print('Failed to copy %s. Reason: %s' % (src_path, e))


def delete_directory(path):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                print(f"Deleting file: {file_path}")
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                print(f"Deleting directory: {file_path}")
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def refresh_public():
    delete_directory('./public')
    copy_directory('./static', './public')

def main():
    refresh_public()

main()