import sys

from static import copy_static_resources


def main():
    try:
        copy_static_resources("static", "public")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
