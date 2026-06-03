#!/usr/bin/env python3
"""
Script to fetch Rails best practices from the GitHub repository
https://github.com/flyerhzm/rails-bestpractices.com
and create markdown files for each practice.
"""

import os
import re
import subprocess
import tempfile
import shutil
from pathlib import Path
import yaml
from datetime import datetime

REPO_URL = "https://github.com/flyerhzm/rails-bestpractices.com.git"
BASE_URL = "https://rails-bestpractices.com"

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
    
    # Priority order: check for specific category matches
    # Some tags should take priority over others
    priority_tags = ['timezone', 'migration', 'route', 'rescue', 'exception', 
                     'security', 'performance', 'whitespace', 'test', 'rspec']
    
    # First check priority tags
    for tag in tags_lower:
        if tag in priority_tags and tag in CATEGORY_MAPPINGS:
            return CATEGORY_MAPPINGS[tag]
    
    # Then check model/active_record (these often appear with controller/view)
    if 'model' in tags_lower or 'active_record' in tags_lower:
        return 'active_record'
    
    # Then check other category matches
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

def parse_jekyll_post(file_path):
    """Parse a Jekyll post file and extract front matter and content."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split front matter and body
    if not content.startswith('---'):
        return None
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        return None
    
    front_matter = parts[1]
    body = parts[2].strip()
    
    # Parse YAML front matter
    try:
        metadata = yaml.safe_load(front_matter)
    except Exception as e:
        print(f"  Error parsing YAML for {file_path}: {e}")
        return None
    
    # Extract date from filename if not in front matter
    filename = os.path.basename(file_path)
    date_match = re.match(r'(\d{4})-(\d{2})-(\d{2})', filename)
    if date_match and 'date' not in metadata:
        year, month, day = date_match.groups()
        metadata['date'] = f"{year}-{month}-{day}"
    
    # Format date
    date_str = None
    if 'date' in metadata:
        date_obj = metadata['date']
        if isinstance(date_obj, datetime):
            date_str = date_obj.strftime('%d %b %Y')
        elif isinstance(date_obj, str):
            try:
                # Try parsing different date formats
                for fmt in ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M:%S %z']:
                    try:
                        parsed = datetime.strptime(date_obj, fmt)
                        date_str = parsed.strftime('%d %b %Y')
                        break
                    except ValueError:
                        continue
                if not date_str:
                    date_str = date_obj
            except:
                date_str = date_obj
    
    # Extract tags
    tags = metadata.get('tags', [])
    if isinstance(tags, str):
        tags = [tags]
    
    # Extract author
    author = metadata.get('author', 'Unknown')
    
    # Extract title
    title = metadata.get('title', 'Untitled')
    
    # Build URL from filename
    # Jekyll URLs are typically: /posts/YYYY/MM/DD/title/
    url = None
    if date_match:
        year, month, day = date_match.groups()
        slug = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', filename)
        slug = re.sub(r'\.(md|markdown)$', '', slug, flags=re.IGNORECASE)
        url = f"{BASE_URL}/posts/{year}/{month}/{day}/{slug}/"
    
    # Parse body content
    description = ""
    bad_example = ""
    good_example = ""
    why_text = ""
    
    # Jekyll posts often use "Before" and "Refactor" sections separated by dashes
    # Split by horizontal rules (------)
    sections = re.split(r'^---+$', body, flags=re.MULTILINE)
    
    before_section = None
    refactor_section = None
    
    # Look for "Before" and "Refactor" sections
    for i, section in enumerate(sections):
        section = section.strip()
        if not section:
            continue
        
        # Check if this section is labeled "Before" or "Refactor"
        if re.match(r'^Before\s*$', section, re.IGNORECASE | re.MULTILINE):
            # Next section is the Before content
            if i + 1 < len(sections):
                before_section = sections[i + 1].strip()
        elif re.match(r'^Refactor\s*$', section, re.IGNORECASE | re.MULTILINE):
            # Next section is the Refactor content
            if i + 1 < len(sections):
                refactor_section = sections[i + 1].strip()
    
    # Also try splitting by ## headers
    if not before_section or not refactor_section:
        header_sections = re.split(r'^##\s+', body, flags=re.MULTILINE)
        for section in header_sections:
            section = section.strip()
            if not section:
                continue
            
            lines = section.split('\n')
            section_title = lines[0].strip()
            section_content = '\n'.join(lines[1:]).strip()
            
            if section_title.lower() in ['before', 'bad', 'bad example', 'anti-pattern']:
                bad_example = section_content
            elif section_title.lower() in ['refactor', 'after', 'good', 'good example', 'solution']:
                good_example = section_content
            elif section_title.lower() in ['why', 'reason', 'rationale']:
                why_text = section_content
    
    # Use the found sections
    if before_section:
        bad_example = before_section
    if refactor_section:
        good_example = refactor_section
    
    # Extract description from first paragraph (before Before section)
    if sections:
        first_section = sections[0].strip()
        # Remove any "Before" label
        first_section = re.sub(r'^Before\s*$', '', first_section, flags=re.IGNORECASE | re.MULTILINE).strip()
        if first_section and len(first_section) > 50:
            description = first_section.split('\n\n')[0].strip()
    
    # If no description found, use first paragraph
    if not description:
        paragraphs = body.split('\n\n')
        for para in paragraphs:
            para = para.strip()
            if len(para) > 50 and not para.startswith('#') and not para.startswith('-'):
                description = para
                break
    
    return {
        'title': title,
        'date': date_str,
        'author': author,
        'tags': tags,
        'url': url,
        'description': description,
        'bad_example': bad_example,
        'good_example': good_example,
        'why': why_text,
        'body': body,
    }

def clone_repo():
    """Clone the GitHub repository to a temporary directory."""
    temp_dir = tempfile.mkdtemp()
    print(f"Cloning repository to {temp_dir}...")
    
    try:
        subprocess.run(
            ['git', 'clone', '--depth', '1', REPO_URL, temp_dir],
            check=True,
            capture_output=True
        )
        return temp_dir
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {e}")
        print(f"stdout: {e.stdout.decode()}")
        print(f"stderr: {e.stderr.decode()}")
        return None

def fetch_all_posts(repo_dir):
    """Fetch all posts from the _posts directory."""
    posts_dir = os.path.join(repo_dir, '_posts')
    
    if not os.path.exists(posts_dir):
        print(f"Error: _posts directory not found in {repo_dir}")
        return []
    
    posts = []
    # Look for both .md and .markdown files
    post_files = sorted(list(Path(posts_dir).glob('*.md')) + list(Path(posts_dir).glob('*.markdown')))
    
    print(f"Found {len(post_files)} post files")
    
    for post_file in post_files:
        print(f"  Processing: {post_file.name}")
        post_data = parse_jekyll_post(str(post_file))
        if post_data:
            posts.append(post_data)
        else:
            print(f"    Failed to parse {post_file.name}")
    
    return posts

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
    if bad_example_text:
        # Check if it already has code blocks
        if '```' not in bad_example_text:
            # Try to detect if it's code
            if any(keyword in bad_example_text for keyword in ['def ', 'class ', 'module ', 'end', '=', '(', ')']):
                bad_example_text = f"```ruby\n{bad_example_text}\n```"
    else:
        bad_example_text = "[Bad example - to be extracted from article content]"
    
    good_example_text = article_data['good_example']
    if good_example_text:
        if '```' not in good_example_text:
            if any(keyword in good_example_text for keyword in ['def ', 'class ', 'module ', 'end', '=', '(', ')']):
                good_example_text = f"```ruby\n{good_example_text}\n```"
    else:
        good_example_text = "[Good example - to be extracted from article content]"
    
    why_text = article_data['why'] or "[Reasons and benefits - to be extracted from article content]"
    description = article_data['description'] or "Description to be added based on article content."
    
    # Create markdown content
    md_content = f"""# {article_data['title']}

**Concept Source**: Based on practices from [rails-bestpractices.com]({article_data['url'] or BASE_URL})

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
    print("Fetching Rails best practices from GitHub repository...")
    
    output_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Clone repository
    repo_dir = clone_repo()
    if not repo_dir:
        print("Failed to clone repository")
        return
    
    try:
        # Fetch all posts
        posts = fetch_all_posts(repo_dir)
        
        print(f"\n\nFetched {len(posts)} posts total")
        
        # Create markdown files
        created_files = []
        for post in posts:
            filepath = create_markdown_file(post, output_dir)
            if filepath:
                created_files.append(filepath)
        
        print(f"\n\nCreated {len(created_files)} new markdown files")
        print("\nDone!")
        
    finally:
        # Clean up
        print(f"Cleaning up temporary directory...")
        shutil.rmtree(repo_dir, ignore_errors=True)

if __name__ == '__main__':
    main()
