import sys

from content import generate_pages_recursive
from static import copy_static_resources

STATIC_DIR = "./static"
PUBLIC_DIR = "./public"
CONTENT_DIR = "./content"
TEMPLATE_PATH = "./template.html"


def main():
    try:
        copy_static_resources(STATIC_DIR, PUBLIC_DIR)
        generate_pages_recursive(CONTENT_DIR, TEMPLATE_PATH, PUBLIC_DIR)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
