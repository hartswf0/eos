#!/usr/bin/env python3
"""
Parse notes.md by conversation turns.
Organize by speaker: "You said:" vs "Code Syntax for Entity and Morphism Distinctions said:"
Collect everything within each turn into structured sections.
"""

import re
from pathlib import Path
from typing import List, Dict, Any


def parse_conversation_turns(content: str) -> List[Dict[str, Any]]:
    """Parse the conversation into structured turns."""
    
    turns = []
    
    # Split by turn markers
    # Pattern: "You said:" or "Code Syntax for Entity and Morphism Distinctions said:"
    turn_pattern = r'((?:You said:|Code Syntax for Entity and Morphism Distinctions said:).*?)(?=(?:You said:|Code Syntax for Entity and Morphism Distinctions said:)|\Z)'
    
    matches = re.finditer(turn_pattern, content, re.DOTALL)
    
    for match in matches:
        turn_text = match.group(1).strip()
        
        # Identify speaker
        if turn_text.startswith('You said:'):
            speaker = 'User'
            # Extract user query (first non-empty line after "You said:")
            query_match = re.search(r'You said:\s*\n(.+?)(?:\n|$)', turn_text)
            query = query_match.group(1).strip() if query_match else ""
            
            turn = {
                'speaker': speaker,
                'query': query,
                'full_content': turn_text
            }
            
        elif turn_text.startswith('Code Syntax'):
            speaker = 'Assistant'
            
            # Check for "Thought for Xs"
            thought_match = re.search(r'Thought for (\d+)s', turn_text)
            thought_duration = thought_match.group(1) if thought_match else None
            
            # Extract concept name if present (line starting with <Something>)
            concept_match = re.search(r'\n<([^>]+)>\s*\n', turn_text)
            concept_name = concept_match.group(1) if concept_match else None
            
            # Check if it has a Definition section
            has_definition = 'Definition' in turn_text
            
            # Check for various sections
            has_key_terms = bool(re.search(r'Key terms', turn_text, re.IGNORECASE))
            has_sitemap = 'Sitemap' in turn_text
            has_summary = 'Summary' in turn_text or 'One-line gist' in turn_text
            has_contrast = 'Contrast set' in turn_text
            has_process = 'Process schema' in turn_text
            has_example = 'Example' in turn_text or 'Completion' in turn_text
            
            turn = {
                'speaker': speaker,
                'thought_duration': thought_duration,
                'concept_name': concept_name,
                'has_definition': has_definition,
                'has_key_terms': has_key_terms,
                'has_sitemap': has_sitemap,
                'has_summary': has_summary,
                'has_contrast': has_contrast,
                'has_process': has_process,
                'has_example': has_example,
                'full_content': turn_text
            }
        else:
            # Header content before first turn
            turn = {
                'speaker': 'Header',
                'full_content': turn_text
            }
        
        if turn_text:  # Only add non-empty turns
            turns.append(turn)
    
    return turns


def format_turns_as_markdown(turns: List[Dict[str, Any]]) -> str:
    """Format parsed turns into clean markdown."""
    
    output_lines = []
    
    # Add header
    output_lines.append("# Concept Codex - Conversation Archive")
    output_lines.append("")
    output_lines.append("**Entity/Morphism Notation:**")
    output_lines.append("- `<entity>` = nouns, things that exist")
    output_lines.append("- `[morphism]` = verbs, actions, transformations")
    output_lines.append("")
    output_lines.append("---")
    output_lines.append("")
    
    turn_number = 0
    
    for turn in turns:
        speaker = turn.get('speaker', 'Unknown')
        
        if speaker == 'Header':
            # Skip header content
            continue
        
        elif speaker == 'User':
            turn_number += 1
            query = turn.get('query', '')
            
            output_lines.append(f"## Turn {turn_number}")
            output_lines.append("")
            output_lines.append(f"**User Query:** {query}")
            output_lines.append("")
        
        elif speaker == 'Assistant':
            thought = turn.get('thought_duration')
            concept = turn.get('concept_name')
            
            # Add metadata about this response
            metadata = []
            if thought:
                metadata.append(f"Thought: {thought}s")
            if concept:
                metadata.append(f"Concept: `<{concept}>`")
            
            sections = []
            if turn.get('has_definition'):
                sections.append("Definition")
            if turn.get('has_key_terms'):
                sections.append("Key terms")
            if turn.get('has_sitemap'):
                sections.append("Sitemap")
            if turn.get('has_summary'):
                sections.append("Summary")
            if turn.get('has_contrast'):
                sections.append("Contrast set")
            if turn.get('has_process'):
                sections.append("Process schema")
            if turn.get('has_example'):
                sections.append("Example")
            
            if sections:
                metadata.append(f"Sections: {', '.join(sections)}")
            
            if metadata:
                output_lines.append(f"**Assistant Response:** {' | '.join(metadata)}")
                output_lines.append("")
            
            # Add the full content (cleaned up)
            content = turn.get('full_content', '')
            # Remove the speaker line
            content = re.sub(r'^Code Syntax for Entity and Morphism Distinctions said:\s*\n', '', content)
            # Remove "Thought for Xs" line
            content = re.sub(r'^Thought for \d+s\s*\n', '', content, flags=re.MULTILINE)
            
            output_lines.append(content.strip())
            output_lines.append("")
            output_lines.append("---")
            output_lines.append("")
    
    return "\n".join(output_lines)


def main():
    """Parse conversation by turns."""
    input_file = Path('/Users/gaia/EOS/CODEX/notes.md')
    output_file = Path('/Users/gaia/EOS/CODEX/notes_by_turns.md')
    
    print(f"Reading {input_file}...")
    content = input_file.read_text(encoding='utf-8')
    
    print("Parsing conversation turns...")
    turns = parse_conversation_turns(content)
    
    # Count stats
    user_turns = sum(1 for t in turns if t.get('speaker') == 'User')
    assistant_turns = sum(1 for t in turns if t.get('speaker') == 'Assistant')
    concepts_defined = sum(1 for t in turns if t.get('speaker') == 'Assistant' and t.get('concept_name'))
    
    print(f"Found {len(turns)} total turns:")
    print(f"  - User queries: {user_turns}")
    print(f"  - Assistant responses: {assistant_turns}")
    print(f"  - Concepts defined: {concepts_defined}")
    
    print("\nFormatting as structured markdown...")
    formatted = format_turns_as_markdown(turns)
    
    print(f"Writing to {output_file}...")
    output_file.write_text(formatted, encoding='utf-8')
    
    output_lines = len(formatted.split('\n'))
    output_size = len(formatted)
    
    print(f"\n✅ Conversation parsed by turns!")
    print(f"\n📊 Output:")
    print(f"  - {output_lines:,} lines")
    print(f"  - {output_size:,} bytes")
    print(f"  - {user_turns} conversations")
    print(f"  - {concepts_defined} concepts defined")
    print(f"\n📄 Structured conversation: {output_file}")


if __name__ == '__main__':
    main()
