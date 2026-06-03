#!/usr/bin/env python3
"""
Script to update INDEX.md with all practices found in the repository.
"""

import os
import re
from pathlib import Path

def extract_title_from_markdown(file_path):
    """Extract title from markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            # Remove # markdown header
            if first_line.startswith('#'):
                title = first_line[1:].strip()
                return title
            return None
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def get_all_practices():
    """Get all practices organized by category."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    practices = {}
    
    categories = [
        'timezone', 'active_record', 'controllers', 'error_handling',
        'code_organization', 'views', 'migrations', 'security',
        'code_quality', 'performance', 'testing', 'routes', 'general'
    ]
    
    for category in categories:
        category_dir = os.path.join(base_dir, category)
        if not os.path.exists(category_dir):
            continue
        
        practices[category] = []
        for md_file in sorted(Path(category_dir).glob('*.md')):
            # Skip duplicates and alternatives
            if 'duplicate' in md_file.name or 'alternative' in md_file.name:
                continue
            
            title = extract_title_from_markdown(str(md_file))
            if title:
                relative_path = os.path.join(category, md_file.name)
                practices[category].append({
                    'title': title,
                    'path': relative_path
                })
    
    return practices

def generate_index_md(practices):
    """Generate INDEX.md content."""
    content = """# Rails Best Practices Index

Complete index of all Rails best practices from [rails-bestpractices.com](https://rails-bestpractices.com/).

"""
    
    # Category display names
    category_names = {
        'timezone': 'Timezone',
        'active_record': 'ActiveRecord',
        'controllers': 'Controllers',
        'error_handling': 'Error Handling',
        'code_organization': 'Code Organization',
        'views': 'Views',
        'migrations': 'Migrations',
        'security': 'Security',
        'code_quality': 'Code Quality',
        'performance': 'Performance',
        'testing': 'Testing',
        'routes': 'Routes',
        'general': 'General'
    }
    
    for category in ['timezone', 'active_record', 'controllers', 'error_handling',
                     'code_organization', 'views', 'migrations', 'security',
                     'code_quality', 'performance', 'testing', 'routes', 'general']:
        if category not in practices or not practices[category]:
            continue
        
        content += f"## {category_names.get(category, category.title())}\n\n"
        
        for practice in practices[category]:
            # Convert path to markdown link format
            path_link = practice['path'].replace('\\', '/')
            content += f"- [{practice['title']}]({path_link})\n"
        
        content += "\n"
    
    content += """## Source

All practices are sourced from [rails-bestpractices.com](https://rails-bestpractices.com/).

## How to Use

1. **For Development**: Reference practices when writing code
2. **For Code Review**: Check code against these practices
3. **For CI/CD**: Integrate checks into your pipeline
4. **For Team**: Use as coding standards

## Contributing

When adding new practices:
1. Create a markdown file in the appropriate category
2. Include: title, description, examples, and source link
3. Update this index
4. Follow the existing format

"""
    
    return content

def main():
    """Main function."""
    print("Updating INDEX.md...")
    
    practices = get_all_practices()
    
    # Count total
    total = sum(len(p) for p in practices.values())
    print(f"Found {total} practices across {len([c for c in practices if practices[c]])} categories")
    
    # Generate index
    index_content = generate_index_md(practices)
    
    # Write to file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    index_path = os.path.join(base_dir, 'INDEX.md')
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"Updated {index_path}")
    print("Done!")

if __name__ == '__main__':
    main()
