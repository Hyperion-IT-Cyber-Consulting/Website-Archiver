# Website Downloader

A Python script that downloads entire websites for offline viewing by crawling through all internal links and saving assets.

## Features
- Downloads HTML, CSS, JavaScript files
- Saves images and other media assets
- Organizes files by type in separate directories
- Respects same-domain policy
- Skips binary files like PDFs, ZIPs, and executables
- Handles relative and absolute URLs

## Requirements
- beautifulsoup4
- requests

## Scraping Capabilities

### Content Types
- Full HTML documents with complete structure
- CSS stylesheets
  - Internal styles
  - External stylesheet files
- JavaScript resources
  - Inline scripts
  - External .js files
- Media assets
  - Images (PNG, JPG, GIF, SVG)
  - Video files
  - Audio files
- Web fonts and icons
- Other static assets

### Smart Link Processing
- URL handling
  - Relative URL resolution
  - Absolute URL processing
  - Base URL preservation
- Link structure maintenance
  - Directory hierarchy preservation
  - Path remapping for offline access
- Domain controls
  - Same-origin policy enforcement
  - External link cataloging
  - Subdomain handling

### Recursive Crawling Features
- Domain-restricted crawling for security
- Recursive crawling through internal pages

### Key Differentiators
Our downloader stands out through:

#### 1. Organized Output Structure

#### 2. Safety Features
- Skips potentially harmful binary files
- Respects same-domain policy
- No external domain crawling

#### 3. Lightweight & Simple
- Minimal dependencies (just requests + BeautifulSoup)
- Single-file implementation
- No complex configuration needed

### Limitations
Compared to tools like HTTrack, this downloader:
- Does not support JavaScript rendering
- Cannot handle login-protected content
- No dynamic content loading capability
- Does not perform link rewriting
- Lacks custom filtering rules

## Installation
1. Clone this repository
2. Install dependencies:

    ```
    pip install -r requirements.txt
    ```


## Usage
Run the script and enter the website URL when prompted:

    python website-downloader.py
  

The script will:
1. Create a `website_files` directory in the script location
2. Download and organize files into subdirectories:
   - `html_files/` - HTML documents
   - `css_files/` - Stylesheets  
   - `js_files/` - JavaScript files
   - `image_files/` - Images and media
   - `other_files/` - Other asset types

## Limitations
- Only downloads from the specified domain
- Skips PDFs, ZIPs and EXE files
- May not handle all JavaScript-generated content
- Does not modify internal links in downloaded files

## License
MIT
