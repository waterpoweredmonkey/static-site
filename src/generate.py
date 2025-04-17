import os
import re
from conversion import markdown_to_html_node

def extract_title(markdown):
    matches = re.findall(r"^#\s([^\t\n\r]*)", markdown)
    if len(matches) == 0:
        raise Exception("Header not found")
    return matches[0]

def generate_page(basepath, from_path, template_path, dest_path):
    print(f"Generating page from: {from_path} to {dest_path} using template: {template_path}, basepath: {basepath}")
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
                .replace("href=\"/", f"href=\"{basepath}")
                .replace("src=\"/", f"src=\"{basepath}")
        )
    finally:
        in_file.close()
        template_file.close()
        out_file.close()

def generate_pages_recursive(base_path, from_dir, template_path, dest_dir):
    print(f"Generating pages at base_path: {base_path},  from: {from_dir} to {dest_dir} using template: {template_path}")
    if not os.path.exists(from_dir):
        print(f"from_dir does not exist: {from_dir}")
        return
    if not os.path.exists(dest_dir):
        print(f"dest_dir does not exist so creating: {dest_dir}")
        os.mkdir(dest_dir)
    for filename in os.listdir(from_dir):
        from_path = os.path.join(from_dir, filename)
        dest_path = os.path.join(dest_dir, filename.replace(".md", ".html"))
        if os.path.isfile(from_path) or os.path.islink(from_path):
            generate_page(base_path, from_path, template_path, dest_path)
        elif os.path.isdir(from_path):
            generate_pages_recursive(base_path, from_path, template_path, dest_path)