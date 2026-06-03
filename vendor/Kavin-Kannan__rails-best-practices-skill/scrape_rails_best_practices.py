#!/usr/bin/env python3
"""
Script to scrape all Rails best practices from rails-bestpractices.com
and create markdown files for each practice.
"""

import requests
from bs4 import BeautifulSoup
import re
import os
from urllib.parse import urljoin
import time

BASE_URL = "https://rails-bestpractices.com"
START_URL = f"{BASE_URL}/"

# Category mappings based on tags/content analysis
CATEGORY_MAPPINGS = {
    'timezone': 'timezone',
    'active_record': 'active_record',
    'model': 'active_record',
    'controller': 'controllers',
    'params': 'controllers',
    'view': 'views',
    'helper': 'code_organization',
    'migration': 'migrations',
    'route': 'routes',
    'rescue': 'error_handling',
    'exception': 'error_handling',
    'security': 'security',
    'performance': 'performance',
    'query': 'performance',
    'cache': 'performance',
    'whitespace': 'code_quality',
    'refactor': 'code_organization',
    'naming': 'code_organization',
    'test': 'testing',
    'rspec': 'testing',
    'cucumber': 'testing',
    'deployment': 'general',
    'capistrano': 'general',
    'gem': 'general',
    'plugin': 'general',
    'bundler': 'general',
    'background job': 'general',
    'mailer': 'general',
    'observer': 'general',
    'i18n': 'general',
    'restful': 'routes',
    'collection': 'active_record',
    'upload': 'active_record',
    'javascript': 'views',
    'css': 'views',
    'assets': 'general',
    'comment': 'code_quality',
    'tab': 'code_quality',
    'task': 'general',
    'version control': 'general',
    'search': 'general',
    'system administration': 'general',
    'convention': 'general',
    'dry': 'code_organization',
}

def get_category_from_tags(tags):
    """Determine category from tags."""
    if not tags:
        return 'general'
    
    tags_lower = [tag.lower() for tag in tags]
    
    # Check for specific category matches
    for tag in tags_lower:
        if tag in CATEGORY_MAPPINGS:
            return CATEGORY_MAPPINGS[tag]
    
    # Default fallback
    return 'general'

def sanitize_filename(title):
    """Convert title to filename-safe string."""
    # Convert to lowercase
    filename = title.lower()
    # Replace spaces and special chars with underscores
    filename = re.sub(r'[^\w\s-]', '', filename)
    filename = re.sub(r'[-\s]+', '_', filename)
    # Remove leading/trailing underscores
    filename = filename.strip('_')
    return filename

def scrape_article(url):
    """Scrape a single article page."""
    print(f"  Scraping: {url}")
    try:
        response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title (h1)
        title_elem = soup.find('h1')
        title = title_elem.get_text().strip() if title_elem else "Untitled"
        
        # Extract date - look for date text near the title
        date = None
        date_patterns = [
            r'(\d{1,2}\s+\w+\s+\d{4})',  # "22 Oct 2014"
        ]
        # Look in post header area
        post_header = soup.find('div', class_='post') or soup.find('article')
        if post_header:
            text = post_header.get_text()
            for pattern in date_patterns:
                match = re.search(pattern, text)
                if match:
                    date = match.group(1)
                    break
        
        # Extract author - look for author name after date
        author = None
        if post_header:
            # Look for text that appears to be author name (capitalized words after date)
            author_match = re.search(r'\d{1,2}\s+\w+\s+\d{4}\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', text)
            if author_match:
                author = author_match.group(1)
        
        if not author:
            author = "Unknown"
        
        # Extract main content
        content_div = soup.find('div', class_='post') or soup.find('article')
        if not content_div:
            content_div = soup.find('main') or soup.find('body')
        
        # Extract description and content sections
        description = ""
        bad_example = ""
        good_example = ""
        why_text = ""
        
        if content_div:
            # Find "Before" section (bad example)
            before_heading = content_div.find('h2', string=re.compile(r'Before', re.I))
            if before_heading:
                before_section = before_heading.find_next_sibling()
                if before_section:
                    bad_example = before_section.get_text().strip()
                    # Also look for code blocks
                    code_blocks = before_section.find_all(['pre', 'code'])
                    if code_blocks:
                        bad_example = '\n'.join([cb.get_text().strip() for cb in code_blocks])
            
            # Find "Refactor" or "After" section (good example)
            refactor_heading = content_div.find('h2', string=re.compile(r'Refactor|After', re.I))
            if refactor_heading:
                refactor_section = refactor_heading.find_next_sibling()
                if refactor_section:
                    good_example = refactor_section.get_text().strip()
                    # Also look for code blocks
                    code_blocks = refactor_section.find_all(['pre', 'code'])
                    if code_blocks:
                        good_example = '\n'.join([cb.get_text().strip() for cb in code_blocks])
            
            # Extract description (first meaningful paragraph)
            paragraphs = content_div.find_all('p')
            for p in paragraphs:
                text = p.get_text().strip()
                if len(text) > 50 and not text.startswith('Tag'):  # Skip short or tag paragraphs
                    description = text
                    break
            
            # Extract "Why" from content
            why_section = content_div.find('h2', string=re.compile(r'Why', re.I))
            if why_section:
                why_elem = why_section.find_next_sibling()
                if why_elem:
                    why_text = why_elem.get_text().strip()
        
        # Extract tags
        tags = []
        # Look for tag links
        tag_elements = soup.find_all('a', href=re.compile(r'/tag/'))
        for tag_elem in tag_elements:
            tag_text = tag_elem.get_text().strip()
            if tag_text and tag_text not in tags:
                tags.append(tag_text)
        
        return {
            'url': url,
            'title': title,
            'date': date,
            'author': author,
            'description': description,
            'bad_example': bad_example,
            'good_example': good_example,
            'why': why_text,
            'tags': tags,
        }
    except Exception as e:
        print(f"    Error scraping {url}: {e}")
        return None

def scrape_all_pages():
    """Scrape all pages from the site."""
    all_articles = []
    current_url = START_URL
    page_num = 1
    seen_urls = set()
    
    while current_url:
        print(f"\nScraping page {page_num}: {current_url}")
        try:
            response = requests.get(current_url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all article links - look for h2 > a links (article titles)
            article_links = []
            for h2 in soup.find_all('h2'):
                link = h2.find('a', href=True)
                if link:
                    href = link['href']
                    if '/posts/' in href:
                        full_url = urljoin(BASE_URL, href)
                        if full_url not in seen_urls:
                            article_links.append(full_url)
                            seen_urls.add(full_url)
            
            print(f"Found {len(article_links)} articles on page {page_num}")
            
            # Scrape each article
            for article_url in article_links:
                article_data = scrape_article(article_url)
                if article_data:
                    all_articles.append(article_data)
                time.sleep(0.5)  # Be polite
            
            # Find next page link - look for "Next »" link
            next_link = None
            # Try finding link with "Next" text
            for link in soup.find_all('a', href=True):
                link_text = link.get_text().strip()
                if 'Next' in link_text or '»' in link_text:
                    next_link = link
                    break
            
            if next_link and 'href' in next_link.attrs:
                current_url = urljoin(BASE_URL, next_link['href'])
                page_num += 1
            else:
                current_url = None
            
            time.sleep(1)  # Be polite between pages
            
        except Exception as e:
            print(f"Error scraping page {current_url}: {e}")
            import traceback
            traceback.print_exc()
            break
    
    return all_articles

def create_markdown_file(article_data, output_dir):
    """Create a markdown file for an article."""
    category = get_category_from_tags(article_data['tags'])
    category_dir = os.path.join(output_dir, category)
    os.makedirs(category_dir, exist_ok=True)
    
    filename = sanitize_filename(article_data['title']) + '.md'
    filepath = os.path.join(category_dir, filename)
    
    # Check if file already exists
    if os.path.exists(filepath):
        print(f"    File already exists: {filepath}")
        return None
    
    # Format code examples
    bad_example_text = article_data['bad_example']
    if bad_example_text and not bad_example_text.startswith('```'):
        bad_example_text = f"```ruby\n{bad_example_text}\n```"
    elif not bad_example_text:
        bad_example_text = "[Bad example - to be extracted from article content]"
    
    good_example_text = article_data['good_example']
    if good_example_text and not good_example_text.startswith('```'):
        good_example_text = f"```ruby\n{good_example_text}\n```"
    elif not good_example_text:
        good_example_text = "[Good example - to be extracted from article content]"
    
    why_text = article_data['why'] or "[Reasons and benefits - to be extracted from article content]"
    description = article_data['description'] or "Description to be added based on article content."
    
    # Create markdown content
    md_content = f"""# {article_data['title']}

**Concept Source**: Based on practices from [rails-bestpractices.com]({article_data['url']})

**Original Article Date**: {article_data['date'] or 'Unknown'}

**Original Author**: {article_data['author']}

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

## Description

{description}

## Why

{why_text}

## Bad Example

{bad_example_text}

## Good Example

{good_example_text}

## Related Practices

[Related practices - to be identified]

## Tags

{', '.join(article_data['tags']) if article_data['tags'] else 'general'}
"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"    Created: {filepath}")
    return filepath

def main():
    """Main function."""
    print("Starting scrape of rails-bestpractices.com...")
    
    output_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Scrape all articles
    articles = scrape_all_pages()
    
    print(f"\n\nScraped {len(articles)} articles total")
    
    # Create markdown files
    created_files = []
    for article in articles:
        filepath = create_markdown_file(article, output_dir)
        if filepath:
            created_files.append(filepath)
    
    print(f"\n\nCreated {len(created_files)} new markdown files")
    print("\nDone!")

if __name__ == '__main__':
    main()
