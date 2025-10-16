#!/usr/bin/env python3
"""
Parse notes.md by conversation turns with EXACT content preservation.
No formatting changes - keep every blank line, every space exactly as original.
"""

import re
from pathlib import Path


def parse_exact_turns(content: str) -> str:
    """Parse conversation with zero content modification."""
    
    output = []
    
    # Add header
    output.append("# Concept Codex - Conversation Archive (Exact Preservation)")
    output.append("")
    output.append("**Entity/Morphism Notation:**")
    output.append("- `<entity>` = nouns, things that exist")
    output.append("- `[morphism]` = verbs, actions, transformations")
    output.append("")
    output.append("**Format:** Original content preserved exactly, organized by conversation turn.")
    output.append("")
    output.append("=" * 80)
    output.append("")
    
    # Split by turn boundaries but keep EVERYTHING in between
    # Pattern: find "You said:" or "Code Syntax..." lines
    lines = content.split('\n')
    
    turn_number = 0
    current_speaker = None
    current_content = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check for speaker changes
        if line.strip() == 'You said:':
            # Output previous turn if exists
            if current_content:
                output.extend(current_content)
                output.append("")
                output.append("-" * 80)
                output.append("")
            
            turn_number += 1
            current_speaker = 'User'
            current_content = [f"## TURN {turn_number} - USER", ""]
            current_content.append(line)  # Keep original line
            
        elif line.strip() == 'Code Syntax for Entity and Morphism Distinctions said:':
            # Don't output yet - continue accumulating user turn
            if current_speaker == 'User':
                current_content.append(line)
                current_content.append("")
                current_content.append(f"### ASSISTANT RESPONSE:")
                current_content.append("")
            current_speaker = 'Assistant'
            
        elif line.strip().startswith('Thought for '):
            # Keep these in content
            current_content.append(line)
            
        else:
            # Regular content line - keep exactly as is
            current_content.append(line)
        
        i += 1
    
    # Output final turn
    if current_content:
        output.extend(current_content)
    
    return '\n'.join(output)


def main():
    """Parse with exact preservation."""
    input_file = Path('/Users/gaia/EOS/CODEX/notes_backup.md')
    output_file = Path('/Users/gaia/EOS/CODEX/notes_exact_turns.md')
    
    print(f"Reading {input_file}...")
    content = input_file.read_text(encoding='utf-8')
    
    original_lines = len(content.split('\n'))
    original_chars = len(content)
    
    print("Parsing with exact content preservation...")
    parsed = parse_exact_turns(content)
    
    parsed_lines = len(parsed.split('\n'))
    parsed_chars = len(parsed)
    
    print(f"Writing to {output_file}...")
    output_file.write_text(parsed, encoding='utf-8')
    
    print(f"\n✅ Exact parsing complete!")
    print(f"\n📊 Statistics:")
    print(f"  Original: {original_lines:,} lines, {original_chars:,} chars")
    print(f"  Parsed:   {parsed_lines:,} lines, {parsed_chars:,} chars")
    print(f"  Added:    {parsed_lines - original_lines:,} lines (structure only)")
    print(f"\n📄 All content preserved: {output_file}")


if __name__ == '__main__':
    main()
