#!/usr/bin/env python3
"""
Parse notes_by_turns.md into well-formatted JSON with line breaks.
Break sections into arrays of paragraphs/items for readability.
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional


def parse_into_items(text: str) -> List[str]:
    """Split text into individual items/paragraphs."""
    # Split by double newlines (paragraph breaks)
    items = [item.strip() for item in text.split('\n\n') if item.strip()]
    return items


def extract_section(content: str, section_name: str, stop_at: List[str]) -> Optional[str]:
    """Extract a specific section from content."""
    # Pattern: section name (with optional suffix) followed by content until next section
    pattern = rf'^{re.escape(section_name)}(?:\s*\([^)]+\))?\s*\n(.*?)(?=\n(?:{"|".join(re.escape(s) for s in stop_at)})|\Z)'
    match = re.search(pattern, content, re.DOTALL | re.MULTILINE)
    
    if match:
        text = match.group(1).strip()
        return text if text else None
    return None


def parse_concept_from_turn(turn_content: str) -> Optional[Dict[str, Any]]:
    """Parse a single concept from a turn's content."""
    
    # Extract concept name
    concept_match = re.search(r'^<([^>]+)>\s*$', turn_content, re.MULTILINE)
    if not concept_match:
        return None
    
    concept_name = concept_match.group(1)
    concept_id = concept_name.lower().replace(' ', '_').replace('/', '_').replace('(', '').replace(')', '').replace('-', '_').replace(',', '').replace(':', '')
    
    # Define all possible sections
    sections_order = [
        'Definition',
        'Key terms',
        'Key mechanics',
        'Secondary expansions',
        'Sitemap',
        'Summary',
        'One-line gist',
        'Checklist',
        'Completion',
        'Contrast set',
        'Process schema',
        'Example',
        'Recurring motifs'
    ]
    
    concept_data = {
        'id': concept_id,
        'term': concept_name,
        'sections': {}
    }
    
    # Definition (single text)
    definition = extract_section(turn_content, 'Definition', sections_order[1:])
    if definition:
        concept_data['sections']['definition'] = definition
    
    # Key terms (array of term definitions)
    key_terms = extract_section(turn_content, 'Key terms', sections_order[2:])
    if key_terms:
        concept_data['sections']['key_terms'] = parse_into_items(key_terms)
    
    # Key mechanics (array)
    key_mechanics = extract_section(turn_content, 'Key mechanics', sections_order[3:])
    if key_mechanics:
        concept_data['sections']['key_mechanics'] = parse_into_items(key_mechanics)
    
    # Secondary expansions (array)
    secondary = extract_section(turn_content, 'Secondary expansions', sections_order[4:])
    if secondary:
        concept_data['sections']['secondary_expansions'] = parse_into_items(secondary)
    
    # Sitemap (break into lines for readability)
    sitemap = extract_section(turn_content, 'Sitemap', sections_order[5:])
    if sitemap:
        # Split by newlines to make it an array of lines
        sitemap_lines = [line for line in sitemap.split('\n') if line.strip()]
        concept_data['sections']['sitemap'] = sitemap_lines
    
    # Summary (single text)
    summary = extract_section(turn_content, 'Summary', sections_order[6:])
    if summary:
        concept_data['sections']['summary'] = summary
    
    # One-line gist (single text)
    gist = extract_section(turn_content, 'One-line gist', sections_order[7:])
    if gist:
        concept_data['sections']['one_line_gist'] = gist
    
    # Checklist (array)
    checklist = extract_section(turn_content, 'Checklist', sections_order[8:])
    if checklist:
        concept_data['sections']['checklist'] = parse_into_items(checklist)
    
    # Completion (single text or array if multiple completions)
    completion = extract_section(turn_content, 'Completion', sections_order[9:])
    if completion:
        # Check if it has multiple completions
        if '\n\n' in completion and len(completion) > 200:
            concept_data['sections']['completion'] = parse_into_items(completion)
        else:
            concept_data['sections']['completion'] = completion
    
    # Contrast set (array)
    contrast = extract_section(turn_content, 'Contrast set', sections_order[10:])
    if contrast:
        concept_data['sections']['contrast_set'] = parse_into_items(contrast)
    
    # Process schema (break into lines for readability)
    process = extract_section(turn_content, 'Process schema', sections_order[11:])
    if process:
        # Split by newlines to preserve tree structure but make readable
        process_lines = [line for line in process.split('\n') if line.strip()]
        concept_data['sections']['process_schema'] = process_lines
    
    # Example (single text)
    example = extract_section(turn_content, 'Example', [])
    if example:
        concept_data['sections']['example'] = example
    
    # Recurring motifs (array)
    motifs = extract_section(turn_content, 'Recurring motifs', [])
    if motifs:
        concept_data['sections']['recurring_motifs'] = parse_into_items(motifs)
    
    return concept_data


def parse_all_turns(content: str) -> List[Dict[str, Any]]:
    """Parse all turns from the document."""
    
    concepts = []
    
    # Split by turn boundaries
    turn_pattern = r'## Turn \d+'
    turns = re.split(turn_pattern, content)
    
    for turn_text in turns[1:]:  # Skip header
        # Extract assistant response
        assistant_match = re.search(r'(?:\*\*Assistant Response:\*\*.*?\n\n)(.*?)(?=\n---|\Z)', turn_text, re.DOTALL)
        
        if assistant_match:
            response_content = assistant_match.group(1)
            concept = parse_concept_from_turn(response_content)
            if concept and concept['sections']:
                concepts.append(concept)
    
    return concepts


def categorize_concept(term: str) -> str:
    """Categorize concept by term."""
    term_lower = term.lower()
    
    if 'ekphrasis' in term_lower or 'ekphrastic' in term_lower:
        if any(word in term_lower for word in ['hope', 'fear', 'indifference']):
            return 'ekphrasis_critical_stances'
        return 'ekphrasis_modes'
    elif any(word in term_lower for word in ['imagetext', 'paragonal', 'mediamachia']):
        return 'media_relations'
    elif any(word in term_lower for word in ['llm', 'wizard', 'symbolic reasoning', 'prompting', 'apparatus theory', 'attention']):
        return 'ai_systems'
    elif any(word in term_lower for word in ['apparatus', 'microcode', 'assembly', 'hypertext']):
        return 'technical_philosophical'
    elif any(word in term_lower for word in ['aura', 'uncanny']):
        return 'aesthetic_perceptual'
    elif any(word in term_lower for word in ['grimoire', 'screwtape', 'atlas']):
        return 'literature_cultural'
    elif any(word in term_lower for word in ['translation', 'intersemiotic', 'diagram']):
        return 'semiotic_visual'
    else:
        return 'general'


def build_output_structure(concepts: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Build final JSON output structure."""
    
    # Build taxonomy
    taxonomy = {}
    for concept in concepts:
        category = categorize_concept(concept['term'])
        if category not in taxonomy:
            taxonomy[category] = []
        taxonomy[category].append(concept['id'])
    
    return {
        'meta': {
            'title': 'Code Syntax for Entity and Morphism Distinctions - Concept Codex',
            'description': 'Structured concept definitions with readable formatting',
            'notation': {
                'entity': '<entity> = nouns, things that exist',
                'morphism': '[morphism] = verbs, actions, transformations'
            },
            'source': 'notes_by_turns.md',
            'total_concepts': len(concepts),
            'parser': 'parse_sections_formatted.py',
            'formatting': 'Sections broken into arrays for readability'
        },
        'concepts': concepts,
        'taxonomy': taxonomy
    }


def main():
    """Parse sections to formatted JSON."""
    input_file = Path('/Users/gaia/EOS/CODEX/notes_by_turns.md')
    output_file = Path('/Users/gaia/EOS/CODEX/notes_formatted.json')
    
    print(f"Reading {input_file}...")
    content = input_file.read_text(encoding='utf-8')
    
    print("Parsing concepts with formatted sections...")
    concepts = parse_all_turns(content)
    
    print(f"Found {len(concepts)} concepts")
    
    # Count sections
    section_stats = {}
    for concept in concepts:
        for section_name in concept['sections'].keys():
            section_stats[section_name] = section_stats.get(section_name, 0) + 1
    
    print("\nSections parsed:")
    for section, count in sorted(section_stats.items()):
        print(f"  - {section}: {count} concepts")
    
    print("\nBuilding formatted output...")
    output = build_output_structure(concepts)
    
    print(f"Writing to {output_file}...")
    output_file.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding='utf-8')
    
    output_size = output_file.stat().st_size
    
    print(f"\n✅ Formatted JSON created!")
    print(f"\n📊 Output:")
    print(f"  - {len(concepts)} concepts")
    print(f"  - {len(output['taxonomy'])} categories")
    print(f"  - {output_size:,} bytes")
    print(f"  - Sections broken into arrays for readability")
    print(f"\n📄 Formatted JSON: {output_file}")


if __name__ == '__main__':
    main()
