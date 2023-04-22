import requests
from bs4 import BeautifulSoup
import os

def read_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        urls = [url.strip() for url in file.readlines()]
    return urls

def fetch_html(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Error fetching {url}: {response.status_code}")
    except Exception as e:
        print(f"Error fetching {url}: {e}")

def save_html_to_file(html, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(html)

def main():
    input_file = 'urls.txt'  # Replace with the path to your text file containing URLs
    output_folder = 'html_files'  # Replace with the desired output folder for the HTML files

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    urls = read_urls_from_file(input_file)

    for url in urls:
        html_content = fetch_html(url)
        if html_content:
            file_name = os.path.join(output_folder, f"{url.replace('://', '-').replace('/', '-')}.txt")
            save_html_to_file(html_content, file_name)
            print(f"Saved HTML from {url} to {file_name}")

if __name__ == "__main__":
    main()
