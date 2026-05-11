from genericpath import isfile
import os

from markdown import markdown_to_html_node


def extract_title(markdown):
    lines = markdown.split("\n\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No title found in markdown")


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as md_file:
        content = md_file.read()

    with open(template_path, "r") as t_file:
        template = t_file.read()

    html_string = markdown_to_html_node(content).to_html()
    title = extract_title(content)
    output = template.replace("{{ Title }}", title)
    output = template.replace("{{ Content }}", html_string)
    output = output.replace('href="/', f'href="{basepath}')
    output = output.replace('src="/', f'src="{basepath}')

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, "w") as o_file:
        o_file.write(output)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for item in os.listdir(dir_path_content):
        content_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(content_path):
            dest_path = dest_path.replace(".md", ".html")
            generate_page(content_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(content_path, template_path, dest_path, basepath)
