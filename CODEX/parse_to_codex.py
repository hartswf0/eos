#!/usr/bin/env python3
"""
Parser to convert various text formats into codex JSON with media support.
Supports YouTube videos and image URLs.
"""

import json
import re
import sys
from datetime import datetime

def slugify(text):
    """Convert text to URL-friendly slug."""
    slug = text.lower()
    slug = re.sub(r'[^a-z0-9]+', '_', slug)
    slug = slug.strip('_')
    return slug

def parse_concept_block(block):
    """Parse a concept block into structured JSON."""
    lines = block.strip().split('\n')
    
    concept = {
        'id': '',
        'term': '',
        'sections': {}
    }
    
    current_section = None
    current_content = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Detect term (first line or line starting with ##)
        if not concept['term']:
            if line.startswith('##'):
                concept['term'] = line.lstrip('#').strip()
            else:
                concept['term'] = line
            concept['id'] = slugify(concept['term'])
            continue
        
        # Detect sections
        section_match = re.match(r'^([A-Z][a-z\s]+):\s*(.*)$', line)
        if section_match:
            # Save previous section
            if current_section and current_content:
                content = ' '.join(current_content).strip()
                if current_section in ['key_terms', 'secondary_expansions', 'sitemap', 'checklist', 'recurring_motifs']:
                    concept['sections'][current_section] = current_content
                else:
                    concept['sections'][current_section] = content
            
            # Start new section
            current_section = slugify(section_match.group(1))
            content_start = section_match.group(2).strip()
            current_content = [content_start] if content_start else []
        
        # Check for list items (for array sections)
        elif line.startswith('-') or line.startswith('•'):
            item = line.lstrip('-•').strip()
            if current_section:
                current_content.append(item)
        
        # Check for YouTube URLs
        elif 'youtube.com' in line or 'youtu.be' in line:
            youtube_match = re.search(r'(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]+)', line)
            if youtube_match:
                video_id = youtube_match.group(1)
                if 'media' not in concept['sections']:
                    concept['sections']['media'] = []
                concept['sections']['media'].append({
                    'type': 'youtube',
                    'id': video_id,
                    'url': f'https://www.youtube.com/watch?v={video_id}'
                })
        
        # Check for image URLs
        elif re.search(r'\.(jpg|jpeg|png|gif|webp|svg)(?:\?|$)', line.lower()):
            img_match = re.search(r'(https?://[^\s]+\.(?:jpg|jpeg|png|gif|webp|svg)(?:\?[^\s]*)?)', line, re.IGNORECASE)
            if img_match:
                img_url = img_match.group(1)
                if 'media' not in concept['sections']:
                    concept['sections']['media'] = []
                concept['sections']['media'].append({
                    'type': 'image',
                    'url': img_url
                })
        
        # Regular content
        else:
            if current_section:
                current_content.append(line)
    
    # Save last section
    if current_section and current_content:
        content = ' '.join(current_content).strip()
        if current_section in ['key_terms', 'secondary_expansions', 'sitemap', 'checklist', 'recurring_motifs']:
            concept['sections'][current_section] = current_content
        else:
            concept['sections'][current_section] = content
    
    return concept if concept['term'] else None

def parse_text_to_codex(text):
    """Parse text input into codex JSON format."""
    # Split by double newlines or concept markers
    blocks = re.split(r'\n\s*\n+|\n(?=##\s)', text)
    
    concepts = []
    for block in blocks:
        if not block.strip():
            continue
        
        concept = parse_concept_block(block)
        if concept and concept['term']:
            concepts.append(concept)
    
    # Build final JSON
    codex = {
        'meta': {
            'title': 'Parsed Concept Codex',
            'description': 'Concepts parsed with media support',
            'notation': {
                'entity': '<entity> = nouns, things that exist',
                'morphism': '[morphism] = verbs, actions, transformations'
            },
            'source': 'manual_parse',
            'total_concepts': len(concepts),
            'parser': 'parse_to_codex.py',
            'created': datetime.now().isoformat(),
            'features': ['youtube_embeds', 'image_urls']
        },
        'concepts': concepts
    }
    
    return codex

def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        # Read from file
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        # Read from stdin
        print("Paste your concept data (Ctrl+D when done):")
        text = sys.stdin.read()
    
    codex = parse_text_to_codex(text)
    
    # Output filename
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'parsed_codex.json'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(codex, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Parsed {codex['meta']['total_concepts']} concepts")
    print(f"✓ Output: {output_file}")
    
    # Show media count
    media_count = sum(1 for c in codex['concepts'] if 'media' in c['sections'])
    if media_count > 0:
        print(f"✓ {media_count} concepts with media")

if __name__ == '__main__':
    main()
