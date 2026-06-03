#!/usr/bin/env python3
"""
Script to enhance existing practice files by extracting complete content
from the GitHub repository posts.
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

def parse_jekyll_post(file_path):
    """Parse a Jekyll post file and extract all content sections."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if not content.startswith('---'):
        return None
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        return None
    
    front_matter = parts[1]
    body = parts[2].strip()
    
    try:
        metadata = yaml.safe_load(front_matter)
    except Exception as e:
        return None
    
    filename = os.path.basename(file_path)
    date_match = re.match(r'(\d{4})-(\d{2})-(\d{2})', filename)
    
    # Format date
    date_str = None
    if 'date' in metadata:
        date_obj = metadata['date']
        if isinstance(date_obj, datetime):
            date_str = date_obj.strftime('%d %b %Y')
        elif isinstance(date_obj, str):
            try:
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
    
    tags = metadata.get('tags', [])
    if isinstance(tags, str):
        tags = [tags]
    
    author = metadata.get('author', 'Unknown')
    title = metadata.get('title', 'Untitled')
    description = metadata.get('description', '')
    
    # Build URL
    url = None
    if date_match:
        year, month, day = date_match.groups()
        slug = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', filename)
        slug = re.sub(r'\.(md|markdown)$', '', slug, flags=re.IGNORECASE)
        url = f"{BASE_URL}/posts/{year}/{month}/{day}/{slug}/"
    
    # Parse body content - look for different section patterns
    bad_example = ""
    good_example = ""
    why_text = ""
    related_practices = []
    
    # Pattern 1: "Bad Smell\n---------\n<content>\n\nRefactor\n--------\n<content>"
    bad_smell_match = re.search(r'Bad\s+Smell\s*\n-+\s*\n(.*?)(?=\n\nRefactor|\n##|\Z)', body, re.DOTALL | re.IGNORECASE)
    if bad_smell_match:
        bad_example = bad_smell_match.group(1).strip()
    
    refactor_match = re.search(r'Refactor\s*\n-+\s*\n(.*?)(?=\n\n(?:Similar|Related|See also|##)|\Z)', body, re.DOTALL | re.IGNORECASE)
    if refactor_match:
        good_example = refactor_match.group(1).strip()
    
    # Pattern 2: Markdown headers (## Before, ## Refactor)
    if not bad_example or not good_example:
        header_sections = re.split(r'^##+\s+', body, flags=re.MULTILINE)
        for section in header_sections:
            section = section.strip()
            if not section:
                continue
            
            lines = section.split('\n')
            section_title = lines[0].strip()
            section_content = '\n'.join(lines[1:]).strip()
            
            title_lower = section_title.lower()
            if title_lower in ['before', 'bad smell', 'bad example', 'anti-pattern']:
                bad_example = section_content
            elif title_lower in ['refactor', 'after', 'good example', 'solution']:
                good_example = section_content
            elif title_lower in ['why', 'reason', 'rationale', 'benefits']:
                why_text = section_content
            elif title_lower in ['similar methods', 'related', 'see also', 'related practices']:
                related_practices.append(section_content)
    
    # Extract code blocks from examples
    def extract_code_blocks(text):
        """Extract code blocks from text, preserving indented code."""
        if not text:
            return ""
        
        # Find indented code blocks (4+ spaces) - these are the main code examples
        code_blocks = []
        in_code_block = False
        current_block = []
        
        lines = text.split('\n')
        for i, line in enumerate(lines):
            # Check if line starts with 4+ spaces (code block)
            if re.match(r'^ {4,}', line):
                if not in_code_block:
                    in_code_block = True
                    current_block = []
                # Remove leading spaces but keep relative indentation
                current_block.append(line)
            else:
                if in_code_block:
                    # End of code block
                    if current_block:
                        code_blocks.append('\n'.join(current_block))
                    current_block = []
                    in_code_block = False
        
        if in_code_block and current_block:
            code_blocks.append('\n'.join(current_block))
        
        # Also look for markdown code blocks
        code_block_pattern = r'```(?:\w+)?\n(.*?)```'
        matches = re.findall(code_block_pattern, text, re.DOTALL)
        code_blocks.extend(matches)
        
        if code_blocks:
            # Return all code blocks joined, or the largest one
            if len(code_blocks) > 1:
                # Join multiple code blocks
                return '\n\n'.join(code_blocks).strip()
            return code_blocks[0].strip()
        
        return text.strip()
    
    # Extract code from examples
    if bad_example:
        bad_code = extract_code_blocks(bad_example)
        if bad_code:
            bad_example = bad_code
    
    if good_example:
        good_code = extract_code_blocks(good_example)
        if good_code:
            good_example = good_code
    
    # Extract explanatory text after code blocks as "why" content
    def extract_explanatory_text(text, code_content):
        """Extract text that comes after code blocks."""
        if not text or not code_content:
            return ""
        
        # Find where the code block ends
        code_start = text.find(code_content)
        if code_start == -1:
            return ""
        
        # Get text after the code block
        after_code = text[code_start + len(code_content):].strip()
        
        # Extract paragraphs (non-code text)
        paragraphs = []
        for para in after_code.split('\n\n'):
            para = para.strip()
            # Skip code blocks and very short paragraphs
            if len(para) > 30 and not re.match(r'^ {4,}', para) and not para.startswith('```'):
                paragraphs.append(para)
        
        return '\n\n'.join(paragraphs[:2])  # Take first 2 paragraphs
    
    # Add explanatory text from examples to why_text
    if bad_example and bad_example in body:
        explanatory = extract_explanatory_text(body, bad_example)
        if explanatory and not why_text:
            why_text = explanatory
        elif explanatory:
            why_text = why_text + '\n\n' + explanatory
    
    # Extract "Why" from description or content
    if not why_text:
        # Look for explanatory text before "Bad Smell" or "Before" section
        before_match = re.search(r'^(.*?)(?:Bad\s+Smell|Before|##\s+Before)', body, re.DOTALL | re.IGNORECASE)
        if before_match:
            first_section = before_match.group(1).strip()
            
            # Get paragraphs that aren't code
            paragraphs = first_section.split('\n\n')
            why_paragraphs = []
            for para in paragraphs:
                para = para.strip()
                # Skip code blocks and very short paragraphs
                if len(para) > 50 and not re.match(r'^ {4,}', para) and not para.startswith('```'):
                    why_paragraphs.append(para)
            
            if why_paragraphs:
                why_text = '\n\n'.join(why_paragraphs[:2])  # Take first 2 paragraphs
    
    # If still no why_text, use description
    if not why_text and description:
        why_text = description
    
    # Extract related practices from "Similar methods" or other sections
    if not related_practices:
        # Look for sections mentioning similar methods
        similar_pattern = r'(?:Similar|Related|See also|Also see)[^:]*:\s*(.*?)(?=\n##|\Z)'
        matches = re.findall(similar_pattern, body, re.IGNORECASE | re.DOTALL)
        if matches:
            related_practices = matches
    
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
        'related_practices': related_practices,
    }

def clone_repo():
    """Clone the GitHub repository."""
    temp_dir = tempfile.mkdtemp()
    print(f"Cloning repository to {temp_dir}...")
    
    try:
        subprocess.run(
            ['git', 'clone', '--depth', '1', REPO_URL, temp_dir],
            check=True,
            capture_output=True
        )
        return temp_dir
    except Exception as e:
        print(f"Error cloning repository: {e}")
        return None

def get_post_by_url_slug(repo_dir, url_slug):
    """Find a post file by URL slug."""
    posts_dir = os.path.join(repo_dir, '_posts')
    if not os.path.exists(posts_dir):
        return None
    
    # Normalize slug for matching
    url_slug_normalized = url_slug.replace('_', '-').lower()
    
    # Try exact match first
    for post_file in Path(posts_dir).glob('*.markdown'):
        filename_slug = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', post_file.stem).lower()
        if filename_slug == url_slug_normalized:
            return str(post_file)
    
    for post_file in Path(posts_dir).glob('*.md'):
        filename_slug = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', post_file.stem).lower()
        if filename_slug == url_slug_normalized:
            return str(post_file)
    
    # Try partial match
    for post_file in Path(posts_dir).glob('*.markdown'):
        filename_slug = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', post_file.stem).lower()
        if url_slug_normalized in filename_slug or filename_slug in url_slug_normalized:
            return str(post_file)
    
    for post_file in Path(posts_dir).glob('*.md'):
        filename_slug = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', post_file.stem).lower()
        if url_slug_normalized in filename_slug or filename_slug in url_slug_normalized:
            return str(post_file)
    
    return None

def get_post_by_title(repo_dir, title):
    """Find a post file by matching title."""
    posts_dir = os.path.join(repo_dir, '_posts')
    if not os.path.exists(posts_dir):
        return None
    
    # Normalize title for matching
    title_normalized = title.lower().strip()
    
    for post_file in Path(posts_dir).glob('*.markdown'):
        try:
            with open(post_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) >= 2:
                        metadata = yaml.safe_load(parts[1])
                        post_title = metadata.get('title', '').lower().strip()
                        if post_title == title_normalized:
                            return str(post_file)
        except:
            continue
    
    # Also try .md files
    for post_file in Path(posts_dir).glob('*.md'):
        try:
            with open(post_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) >= 2:
                        metadata = yaml.safe_load(parts[1])
                        post_title = metadata.get('title', '').lower().strip()
                        if post_title == title_normalized:
                            return str(post_file)
        except:
            continue
    
    return None

def enhance_existing_file(md_file_path, repo_dir):
    """Enhance an existing markdown file with content from the repo."""
    # Read current file to get title
    title = None
    slug = None
    
    try:
        with open(md_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Extract title from first line
            first_line = content.split('\n')[0]
            if first_line.startswith('#'):
                title = first_line[1:].strip()
            else:
                return False
            
            # Extract URL to find matching post
            url_match = re.search(r'\[rails-bestpractices\.com\]\((.*?)\)', content)
            if url_match:
                url = url_match.group(1)
                # Extract slug from URL
                slug_match = re.search(r'/posts/\d+/\d+/\d+/([^/]+)/', url)
                if slug_match:
                    slug = slug_match.group(1)
    except Exception as e:
        print(f"  Error reading {md_file_path}: {e}")
        return False
    
    # Find matching post in repo - try by slug first (more reliable)
    post_file = None
    if slug:
        post_file = get_post_by_url_slug(repo_dir, slug)
    
    # Fall back to title matching
    if not post_file and title:
        post_file = get_post_by_title(repo_dir, title)
    
    if not post_file:
        print(f"  Could not find source post for: {title}")
        return False
    
    # Parse the post
    post_data = parse_jekyll_post(post_file)
    if not post_data:
        return False
    
    # Update the markdown file
    return update_markdown_file(md_file_path, post_data)

def update_markdown_file(file_path, post_data):
    """Update a markdown file with enhanced content."""
    # Read current file to extract header (title, source, date, author)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            current_content = f.read()
        
        # Extract header (everything before first ##)
        header_match = re.match(r'(.*?)(?:^##\s+)', current_content, re.DOTALL | re.MULTILINE)
        if header_match:
            header = header_match.group(1).strip()
        else:
            # Fallback: get first few lines
            lines = current_content.split('\n')[:10]
            header = '\n'.join(lines)
    except:
        # If we can't read, create basic header
        header = f"""# {post_data['title']}

**Concept Source**: Based on practices from [rails-bestpractices.com]({post_data['url'] or BASE_URL})

**Original Article Date**: {post_data['date'] or 'Unknown'}

**Original Author**: {post_data['author']}

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.
"""
    
    # Format code examples
    def format_code_example(code):
        if not code or (code.startswith('[') and 'to be extracted' in code):
            return code or '[Code example - to be extracted from article content]'
        
        code = code.strip()
        
        # Remove markdown links but keep the text
        code = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', code)
        
        # If it doesn't have code fences and looks like code, add them
        if '```' not in code:
            # Check if it looks like code
            looks_like_code = any([
                code.startswith('    '),  # Indented
                'def ' in code,
                'class ' in code,
                'module ' in code,
                '<%' in code,  # ERB
                'end' in code,
                '=' in code and '(' in code,  # Method calls
            ])
            
            if looks_like_code:
                # Determine language
                lang = 'ruby'
                if '<%' in code or '<%=' in code:
                    lang = 'erb'
                elif 'javascript' in code.lower() or 'js' in code.lower():
                    lang = 'javascript'
                
                return f"```{lang}\n{code}\n```"
        
        return code
    
    bad_example = format_code_example(post_data['bad_example'])
    good_example = format_code_example(post_data['good_example'])
    
    # Format why text
    why_text = post_data['why'] or "[Reasons and benefits - to be extracted from article content]"
    if why_text and not why_text.startswith('['):
        # Clean up the why text
        why_text = why_text.strip()
    
    # Format related practices
    related_text = ""
    if post_data['related_practices']:
        related_items = []
        for rp in post_data['related_practices']:
            # Extract method names or practice names
            methods = re.findall(r'\[([^\]]+)\]\([^\)]+\)', rp)
            if methods:
                related_items.extend(methods)
            else:
                # Just add the text
                related_items.append(rp.strip())
        if related_items:
            related_text = '\n'.join([f"- {item}" for item in related_items[:5]])
    
    if not related_text:
        related_text = "[Related practices - to be identified]"
    
    # Format tags
    tags_text = ', '.join(post_data['tags']) if post_data['tags'] else 'general'
    
    # Ensure header ends with newline
    header = header.rstrip() + '\n\n'
    
    # Build new content - always include all sections
    new_content = f"""{header}## Description

{post_data['description'] or 'Description to be added based on article content.'}

## Why

{why_text}

## Bad Example

{bad_example or '[Bad example - to be extracted from article content]'}

## Good Example

{good_example or '[Good example - to be extracted from article content]'}

## Related Practices

{related_text}

## Tags

{tags_text}
"""
    
    # Write updated file
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    except Exception as e:
        print(f"  Error writing {file_path}: {e}")
        return False

def main():
    """Main function."""
    print("Enhancing practice files with complete content...")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Clone repository
    repo_dir = clone_repo()
    if not repo_dir:
        print("Failed to clone repository")
        return
    
    try:
        # Find all markdown files
        updated_count = 0
        skipped_count = 0
        
        categories = ['timezone', 'active_record', 'controllers', 'error_handling',
                     'code_organization', 'views', 'migrations', 'security',
                     'code_quality', 'performance', 'testing', 'routes', 'general']
        
        for category in categories:
            category_dir = os.path.join(base_dir, category)
            if not os.path.exists(category_dir):
                continue
            
            print(f"\nProcessing {category}...")
            for md_file in sorted(Path(category_dir).glob('*.md')):
                # Skip scripts and index
                if md_file.name in ['INDEX.md', 'README.md']:
                    continue
                
                print(f"  Enhancing: {md_file.name}")
                if enhance_existing_file(str(md_file), repo_dir):
                    updated_count += 1
                else:
                    skipped_count += 1
        
        print(f"\n\nUpdated {updated_count} files")
        print(f"Skipped {skipped_count} files")
        print("\nDone!")
        
    finally:
        # Clean up
        print(f"Cleaning up temporary directory...")
        shutil.rmtree(repo_dir, ignore_errors=True)

if __name__ == '__main__':
    main()
