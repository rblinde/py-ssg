import shutil
import os


def validate_dir(dir):
    cwd = os.path.abspath(os.curdir)
    target_path = os.path.normpath(os.path.join(cwd, dir))

    if os.path.commonpath([cwd, target_path]) != cwd:
        raise Exception(f"Invalid directory: {dir}")

    return target_path


def copy_recursive(src_path, dest_path):
    for item in os.listdir(src_path):
        src = os.path.join(src_path, item)
        dest = os.path.join(dest_path, item)

        if not os.path.isdir(src):
            print(f"Copying: {src} to {dest}")
            shutil.copy(src, dest)
            continue

        os.mkdir(dest)
        copy_recursive(src, dest)


def copy_static_resources(src, dest):
    src_path = validate_dir(src)
    dest_path = validate_dir(dest)

    # Empty dest
    shutil.rmtree(dest_path, ignore_errors=True)
    os.mkdir(dest_path)

    copy_recursive(src_path, dest_path)
