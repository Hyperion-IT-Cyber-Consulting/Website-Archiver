import os
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from collections import deque
import re

def download_website(base_url):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    visited_urls = set()
    url_queue = deque([base_url])
    base_domain = urlparse(base_url).netloc
    
    output_dir = os.path.join(script_dir, 'website_files')
    file_types = {
        'html': 'html_files',
        'css': 'css_files', 
        'js': 'js_files',
        'images': 'image_files',
        'other': 'other_files'
    }
    
    for directory in file_types.values():
        os.makedirs(os.path.join(output_dir, directory), exist_ok=True)

    def is_valid_url(url):
        try:
            parsed = urlparse(url)
            return (parsed.netloc == base_domain and 
                   not any(url.endswith(ext) for ext in ['.pdf', '.zip', '.exe']))
        except:
            return False

    def extract_urls(soup, current_url):
        urls = set()
        # Find all elements with href or src
        for tag in soup.find_all(['a', 'link', 'script', 'img', 'source', 'iframe']):
            url = tag.get('href') or tag.get('src')
            if url:
                absolute_url = urljoin(current_url, url)
                if is_valid_url(absolute_url):
                    urls.add(absolute_url)
        
        # Find URLs in inline styles and CSS
        for tag in soup.find_all(['style', 'link']):
            if tag.string:
                style_urls = re.findall(r'url\(["\']?([^)"\']+)["\']?\)', tag.string)
                for url in style_urls:
                    absolute_url = urljoin(current_url, url)
                    if is_valid_url(absolute_url):
                        urls.add(absolute_url)
        return urls

    def get_file_type(url):
        extension = os.path.splitext(url)[1].lower()
        if extension in ['.html', '.htm', ''] or url.endswith('/'):
            return 'html'
        elif extension == '.css':
            return 'css'
        elif extension == '.js':
            return 'js'
        elif extension in ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico', '.webp']:
            return 'images'
        else:
            return 'other'

    def process_url(url):
        if url in visited_urls:
            return
        
        visited_urls.add(url)
        print(f'Processing: {url}')
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Save the file
            file_type = get_file_type(url)
            parsed_url = urlparse(url)
            path_parts = parsed_url.path.strip('/').split('/')
            filename = path_parts[-1] if path_parts[-1] else 'index.html'
            if not os.path.splitext(filename)[1]:
                filename += '.html'
            
            target_dir = os.path.join(output_dir, file_types[file_type])
            local_path = os.path.join(target_dir, filename)
            
            with open(local_path, 'wb') as f:
                f.write(response.content)
            print(f'Downloaded: {url} -> {local_path}')

            # Extract new URLs from HTML content
            if file_type == 'html':
                soup = BeautifulSoup(response.text, 'html.parser')
                new_urls = extract_urls(soup, url)
                for new_url in new_urls:
                    if new_url not in visited_urls:
                        url_queue.append(new_url)

        except Exception as e:
            print(f'Error processing {url}: {str(e)}')

    # Main crawling loop
    print(f'Starting download to: {output_dir}')
    while url_queue:
        current_url = url_queue.popleft()
        process_url(current_url)

    print(f'Download completed! Processed {len(visited_urls)} URLs')

if __name__ == '__main__':
    website_url = input('Enter the website URL (e.g., https://example.com): ')
    download_website(website_url)