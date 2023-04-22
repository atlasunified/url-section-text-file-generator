import re
import os

def strip_html_tags(input_file_path, output_file_path):
    # Define a regular expression pattern to match HTML tags
    html_tag_pattern = re.compile(r'<[^>]+>')

    # Read the input file
    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Remove HTML tags using the regular expression pattern
    cleaned_content = html_tag_pattern.sub('', content)

    # Save the cleaned content to the output file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_content)

    print(f"Cleaned content saved to {output_file_path}")

def process_directory(input_directory, output_directory):
    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # List all items in the input directory
    items = os.listdir(input_directory)

    # Process each item in the input directory
    for item in items:
        input_path = os.path.join(input_directory, item)
        output_path = os.path.join(output_directory, item)

        # If the item is a directory, process it recursively
        if os.path.isdir(input_path):
            process_directory(input_path, output_path)
        # If the item is a file, strip HTML tags and save the cleaned content
        elif os.path.isfile(input_path):
            strip_html_tags(input_path, output_path)

def main():
    input_directory = 'sections'  # Input directory containing text files and subdirectories
    output_directory = 'cleaned_sections'  # Output directory to save cleaned files

    # Process the input directory and save cleaned content to the output directory
    process_directory(input_directory, output_directory)

if __name__ == "__main__":
    main()
