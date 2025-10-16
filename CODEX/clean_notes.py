#!/usr/bin/env python3
"""
Clean notes.md by removing chat interface artifacts.
Keep only pure concept definitions with their structure.
"""

import re
from pathlib import Path


def clean_markdown(content: str) -> str:
    """Remove chat UI artifacts and conversational fluff."""
    
    # Remove chat header artifacts
    content = re.sub(r'^Skip to content\s*\n', '', content, flags=re.MULTILINE)
    content = re.sub(r'^Chat history\s*\n', '', content, flags=re.MULTILINE)
    
    # Remove "You said:" prompts and their content (until next section)
    content = re.sub(r'\nYou said:\s*\n[^\n<]*\n(?:Code Syntax[^\n]*\n)?', '\n\n', content)
    
    # Remove "Code Syntax for Entity and Morphism Distinctions said:" headers
    content = re.sub(r'Code Syntax for Entity and Morphism Distinctions said:\s*\n', '', content)
    
    # Remove "Thought for Xs" lines
    content = re.sub(r'Thought for \d+s\s*\n', '', content)
    
    # Remove conversational artifacts like "looks like you meant..."
    content = re.sub(r'^looks like you meant[^\n]*\n\n', '', content, flags=re.MULTILINE)
    
    # Remove excessive blank lines (more than 2 consecutive)
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    # Clean up leading/trailing whitespace
    content = content.strip()
    
    return content


def main():
    """Clean the notes.md file."""
    input_file = Path('/Users/gaia/EOS/CODEX/notes.md')
    output_file = Path('/Users/gaia/EOS/CODEX/notes_clean.md')
    backup_file = Path('/Users/gaia/EOS/CODEX/notes_backup.md')
    
    print(f"Reading {input_file}...")
    original_content = input_file.read_text(encoding='utf-8')
    original_lines = len(original_content.split('\n'))
    original_size = len(original_content)
    
    # Create backup
    print(f"Creating backup at {backup_file}...")
    backup_file.write_text(original_content, encoding='utf-8')
    
    # Clean content
    print("Cleaning content...")
    cleaned_content = clean_markdown(original_content)
    cleaned_lines = len(cleaned_content.split('\n'))
    cleaned_size = len(cleaned_content)
    
    # Write cleaned version
    print(f"Writing cleaned version to {output_file}...")
    output_file.write_text(cleaned_content, encoding='utf-8')
    
    # Stats
    lines_removed = original_lines - cleaned_lines
    bytes_removed = original_size - cleaned_size
    reduction_pct = (bytes_removed / original_size) * 100
    
    print(f"\n✅ Cleanup complete!")
    print(f"\nStatistics:")
    print(f"  Original: {original_lines:,} lines, {original_size:,} bytes")
    print(f"  Cleaned:  {cleaned_lines:,} lines, {cleaned_size:,} bytes")
    print(f"  Removed:  {lines_removed:,} lines, {bytes_removed:,} bytes ({reduction_pct:.1f}% reduction)")
    print(f"\n📄 Output: {output_file}")
    print(f"💾 Backup: {backup_file}")


if __name__ == '__main__':
    main()
