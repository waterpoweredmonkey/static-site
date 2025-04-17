import os
import re
from conversion import markdown_to_html_node

def extract_title(markdown):
    matches = re.findall(r"^#\s([^\t\n\r]*)", markdown)
    if len(matches) == 0:
        raise Exception("Header not found")
    return matches[0]

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from: {from_path} to {dest_path} using template: {template_path}")
    if not os.path.exists(from_path):
        raise Exception(f"from_path does not exist: {from_path}")
    if not os.path.exists(template_path):
        dir_name = os.path.dirname(template_path)
        message = f"template_path does not exist: {template_path}, dir:{dir_name}"
        raise Exception(message)
    if not os.path.exists(os.path.dirname(dest_path)):
        os.mkdir(os.path.dirname(dest_path))

    in_file = open(from_path, "r")
    template_file = open(template_path, "r")
    out_file = open(dest_path, "w")
    try:
        from_content = in_file.read()
        content = markdown_to_html_node(from_content).to_html()
        title = extract_title(from_content)
        out_file.write(
            template_file.read()
                .replace("{{ Title }}", title)
                .replace("{{ Content }}", content)
        )
    finally:
        in_file.close()
        template_file.close()
        out_file.close()