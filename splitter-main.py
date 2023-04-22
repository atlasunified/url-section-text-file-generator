import os
import re
import shutil
from bs4 import BeautifulSoup

def get_files_in_directory(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def select_file(files):
    print("Select a file:")
    for index, file in enumerate(files, 1):
        print(f"{index}. {file}")
    choice = int(input("Enter the file number: "))
    return files[choice - 1]

def sanitize_filename(filename):
    return re.sub(r'[\\/:"*?<>|]+', '-', filename)

def save_section_to_file(section_name, content, output_folder):
    sanitized_name = sanitize_filename(section_name)
    file_name = os.path.join(output_folder, f"{sanitized_name}.txt")
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Saved section '{section_name}' to {file_name}")

def extract_and_save_sections(file_path, output_folder):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    soup = BeautifulSoup(content, 'html.parser')
    headers = soup.find_all(['h1', 'h2', 'h3', 'h4'])
    h1_header = soup.find('h1')
    code_blocks = soup.select("div.codeblock pre code.lang-python")
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    h1_folder = output_folder
    if h1_header:
        h1_folder = os.path.join(output_folder, sanitize_filename(h1_header.get_text().strip()))
        if not os.path.exists(h1_folder):
            os.makedirs(h1_folder)

    if headers:
        for header in headers:
            section_name = header.get_text().strip()
            section_content = []
            for element in header.find_all_next():
                if element.name in ['h1', 'h2', 'h3', 'h4']:
                    break
                if element.name == 'p' or element in code_blocks:
                    section_content.append(element.get_text())
            save_section_to_file(section_name, '\n'.join(section_content), h1_folder)
    else:
        print("No h1, h2, h3, h4 headers found.")

def main():
    directory = 'html_files'
    output_folder = 'sections'

    while True:
        files = get_files_in_directory(directory)

        if not files:
            print(f"No files left in the '{directory}' directory.")
            break

        selected_file = select_file(files)
        file_path = os.path.join(directory, selected_file)
        output_file_path = os.path.join(output_folder, selected_file)
        shutil.copyfile(file_path, output_file_path)
        print(f"Copied the selected file to {output_folder}")
        extract_and_save_sections(output_file_path, output_folder)

        os.remove(file_path)
        print(f"Removed the processed file from '{directory}'\n")

if __name__ == "__main__":
    main()
