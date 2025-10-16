#!/usr/bin/env python3
"""
Distill notes.md to pure concept definitions.
SUBTRACTIVE: Keep only <Concept>, Definition, Key terms, Summary.
Remove: chat artifacts, sitemaps, secondary expansions, completions, checklists.
"""

import re
from pathlib import Path


def extract_essential_concepts(content: str) -> str:
    """Extract only the essential parts of each concept."""
    
    distilled = []
    
    # Find all concepts: <Name>\nDefinition\n...
    pattern = r'<([A-Z][^>]+?)>\s*\n(?:Definition|Definition \(full code syntax\))\s*\n(.*?)(?=\n<[A-Z][^>]+?>\s*\n(?:Definition|Definition \(full code syntax\))|\Z)'
    
    matches = re.finditer(pattern, content, re.DOTALL | re.MULTILINE)
    
    for match in matches:
        concept_name = match.group(1).strip()
        concept_body = match.group(2)
        
        # Extract definition (stop at first section break)
        def_match = re.search(
            r'^(.+?)(?=\n\n(?:Key terms|Key mechanics|Sitemap|Summary|One-line gist|Secondary expansions|Process schema|Contrast set|Checklist)|\Z)',
            concept_body,
            re.DOTALL | re.MULTILINE
        )
        definition = def_match.group(1).strip() if def_match else ""
        definition = re.sub(r'\s+', ' ', definition)  # Normalize whitespace
        
        # Extract key terms section (keep raw)
        key_terms_match = re.search(
            r'(?:Key terms|Key mechanics).*?\n(.*?)(?=\n\n(?:Sitemap|Summary|One-line gist|Secondary expansions|Process schema|Contrast set|Checklist)|\Z)',
            concept_body,
            re.DOTALL | re.MULTILINE
        )
        key_terms = key_terms_match.group(1).strip() if key_terms_match else ""
        
        # Extract summary (prefer "One-line gist", fallback to "Summary")
        summary_match = re.search(r'One-line gist\s*\n(.+?)(?=\n\n|\Z)', concept_body, re.DOTALL)
        if not summary_match:
            summary_match = re.search(r'Summary\s*\n(.+?)(?=\n\n|\Z)', concept_body, re.DOTALL)
        summary = summary_match.group(1).strip() if summary_match else ""
        summary = re.sub(r'\s+', ' ', summary)
        
        # Build distilled concept
        if definition:
            concept_text = f"<{concept_name}>\n\n"
            concept_text += f"Definition\n{definition}\n\n"
            
            if key_terms:
                concept_text += f"Key terms\n{key_terms}\n\n"
            
            if summary:
                concept_text += f"Summary\n{summary}\n"
            
            distilled.append(concept_text)
    
    return "\n---\n\n".join(distilled)


def main():
    """Distill notes.md to essentials only."""
    input_file = Path('/Users/gaia/EOS/CODEX/notes.md')
    output_file = Path('/Users/gaia/EOS/CODEX/notes_distilled.md')
    
    print(f"Reading {input_file}...")
    original_content = input_file.read_text(encoding='utf-8')
    original_lines = len(original_content.split('\n'))
    original_size = len(original_content)
    
    # Distill to essentials
    print("Distilling to essential definitions only...")
    distilled_content = extract_essential_concepts(original_content)
    distilled_lines = len(distilled_content.split('\n'))
    distilled_size = len(distilled_content)
    
    # Write distilled version
    print(f"Writing distilled version to {output_file}...")
    output_file.write_text(distilled_content, encoding='utf-8')
    
    # Count concepts
    concept_count = distilled_content.count('\n---\n') + 1
    
    # Stats
    lines_removed = original_lines - distilled_lines
    bytes_removed = original_size - distilled_size
    reduction_pct = (bytes_removed / original_size) * 100
    
    print(f"\n✅ Distillation complete!")
    print(f"\n📊 Statistics:")
    print(f"  Original:  {original_lines:,} lines, {original_size:,} bytes")
    print(f"  Distilled: {distilled_lines:,} lines, {distilled_size:,} bytes")
    print(f"  Removed:   {lines_removed:,} lines, {bytes_removed:,} bytes ({reduction_pct:.1f}% reduction)")
    print(f"  Concepts:  {concept_count}")
    print(f"\n📄 Pure concept definitions: {output_file}")


if __name__ == '__main__':
    main()
