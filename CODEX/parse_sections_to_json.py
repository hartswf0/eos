#!/usr/bin/env python3
"""
Parse notes_by_turns.md into JSON organized by sections.
Extract: Definition, Key terms, Secondary expansions, Sitemap, Summary, 
         Checklist, Completion, Contrast set, Process schema, etc.
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional


def extract_section(content: str, section_name: str, stop_at: List[str]) -> Optional[str]:
    """Extract a specific section from content."""
    # Pattern: section name (with optional suffix like "(recursive...)") followed by content until next section
    pattern = rf'^{re.escape(section_name)}(?:\s*\([^)]+\))?\s*\n(.*?)(?=\n(?:{"|".join(re.escape(s) for s in stop_at)})|\Z)'
    match = re.search(pattern, content, re.DOTALL | re.MULTILINE)
    
    if match:
        text = match.group(1).strip()
        return text if text else None
    return None


def parse_concept_from_turn(turn_content: str) -> Optional[Dict[str, Any]]:
    """Parse a single concept from a turn's content."""
    
    # Extract concept name (line starting with <ConceptName>)
    concept_match = re.search(r'^<([^>]+)>\s*$', turn_content, re.MULTILINE)
    if not concept_match:
        return None
    
    concept_name = concept_match.group(1)
    concept_id = concept_name.lower().replace(' ', '_').replace('/', '_').replace('(', '').replace(')', '').replace('-', '_')
    
    # Define all possible sections and their stop markers
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
    
    # Extract each section
    concept_data = {
        'id': concept_id,
        'term': concept_name,
        'sections': {}
    }
    
    # Definition
    definition = extract_section(turn_content, 'Definition', sections_order[1:])
    if definition:
        concept_data['sections']['definition'] = definition
    
    # Key terms (main)
    key_terms = extract_section(turn_content, 'Key terms', sections_order[2:])
    if key_terms:
        concept_data['sections']['key_terms'] = key_terms
    
    # Key mechanics (alternative to key terms)
    key_mechanics = extract_section(turn_content, 'Key mechanics', sections_order[3:])
    if key_mechanics:
        concept_data['sections']['key_mechanics'] = key_mechanics
    
    # Secondary expansions
    secondary = extract_section(turn_content, 'Secondary expansions', sections_order[4:])
    if secondary:
        concept_data['sections']['secondary_expansions'] = secondary
    
    # Sitemap
    sitemap = extract_section(turn_content, 'Sitemap', sections_order[5:])
    if sitemap:
        concept_data['sections']['sitemap'] = sitemap
    
    # Summary
    summary = extract_section(turn_content, 'Summary', sections_order[6:])
    if summary:
        concept_data['sections']['summary'] = summary
    
    # One-line gist (alternative to summary)
    gist = extract_section(turn_content, 'One-line gist', sections_order[7:])
    if gist:
        concept_data['sections']['one_line_gist'] = gist
    
    # Checklist
    checklist = extract_section(turn_content, 'Checklist', sections_order[8:])
    if checklist:
        concept_data['sections']['checklist'] = checklist
    
    # Completion
    completion = extract_section(turn_content, 'Completion', sections_order[9:])
    if completion:
        concept_data['sections']['completion'] = completion
    
    # Contrast set
    contrast = extract_section(turn_content, 'Contrast set', sections_order[10:])
    if contrast:
        concept_data['sections']['contrast_set'] = contrast
    
    # Process schema
    process = extract_section(turn_content, 'Process schema', sections_order[11:])
    if process:
        concept_data['sections']['process_schema'] = process
    
    # Example
    example = extract_section(turn_content, 'Example', [])
    if example:
        concept_data['sections']['example'] = example
    
    return concept_data


def parse_all_turns(content: str) -> List[Dict[str, Any]]:
    """Parse all turns from the document."""
    
    concepts = []
    
    # Split by turn boundaries
    turn_pattern = r'## Turn \d+'
    turns = re.split(turn_pattern, content)
    
    for turn_text in turns[1:]:  # Skip header before first turn
        # Extract assistant response (after "### ASSISTANT RESPONSE:" or after user query)
        assistant_match = re.search(r'(?:\*\*Assistant Response:\*\*.*?\n\n)(.*?)(?=\n---|\Z)', turn_text, re.DOTALL)
        
        if assistant_match:
            response_content = assistant_match.group(1)
            
            # Try to parse concept from this response
            concept = parse_concept_from_turn(response_content)
            if concept and concept['sections']:
                concepts.append(concept)
    
    return concepts


def build_output_structure(concepts: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Build final JSON output structure."""
    
    # Categorize concepts
    categories = {
        'technical_philosophical': [],
        'aesthetic_perceptual': [],
        'literature_cultural': [],
        'ai_systems': [],
        'ekphrasis_modes': [],
        'ekphrasis_critical_stances': [],
        'media_relations': [],
        'semiotic_visual': [],
        'general': []
    }
    
    for concept in concepts:
        term = concept['term'].lower()
        
        if 'ekphrasis' in term or 'ekphrastic' in term:
            if any(word in term for word in ['hope', 'fear', 'indifference']):
                categories['ekphrasis_critical_stances'].append(concept['id'])
            else:
                categories['ekphrasis_modes'].append(concept['id'])
        elif any(word in term for word in ['imagetext', 'paragonal', 'mediamachia']):
            categories['media_relations'].append(concept['id'])
        elif any(word in term for word in ['llm', 'wizard', 'symbolic reasoning', 'prompting', 'apparatus theory']):
            categories['ai_systems'].append(concept['id'])
        elif any(word in term for word in ['apparatus', 'microcode', 'assembly', 'hypertext']):
            categories['technical_philosophical'].append(concept['id'])
        elif any(word in term for word in ['aura', 'uncanny']):
            categories['aesthetic_perceptual'].append(concept['id'])
        elif any(word in term for word in ['grimoire', 'screwtape', 'atlas']):
            categories['literature_cultural'].append(concept['id'])
        elif any(word in term for word in ['translation', 'intersemiotic', 'diagram']):
            categories['semiotic_visual'].append(concept['id'])
        else:
            categories['general'].append(concept['id'])
    
    # Remove empty categories
    taxonomy = {k: v for k, v in categories.items() if v}
    
    return {
        'meta': {
            'title': 'Code Syntax for Entity and Morphism Distinctions - Concept Codex',
            'description': 'Structured concept definitions organized by sections',
            'notation': {
                'entity': '<entity> = nouns, things that exist',
                'morphism': '[morphism] = verbs, actions, transformations'
            },
            'source': 'notes_by_turns.md',
            'total_concepts': len(concepts),
            'parser': 'parse_sections_to_json.py'
        },
        'concepts': concepts,
        'taxonomy': taxonomy
    }


def main():
    """Parse sections to JSON."""
    input_file = Path('/Users/gaia/EOS/CODEX/notes_by_turns.md')
    output_file = Path('/Users/gaia/EOS/CODEX/notes_structured.json')
    
    print(f"Reading {input_file}...")
    content = input_file.read_text(encoding='utf-8')
    
    print("Parsing concepts by sections...")
    concepts = parse_all_turns(content)
    
    print(f"Found {len(concepts)} concepts with structured sections")
    
    # Count sections
    section_stats = {}
    for concept in concepts:
        for section_name in concept['sections'].keys():
            section_stats[section_name] = section_stats.get(section_name, 0) + 1
    
    print("\nSections found:")
    for section, count in sorted(section_stats.items()):
        print(f"  - {section}: {count} concepts")
    
    print("\nBuilding output structure...")
    output = build_output_structure(concepts)
    
    print(f"Writing to {output_file}...")
    output_file.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding='utf-8')
    
    output_size = output_file.stat().st_size
    
    print(f"\n✅ Structured JSON created!")
    print(f"\n📊 Output:")
    print(f"  - {len(concepts)} concepts")
    print(f"  - {len(output['taxonomy'])} categories")
    print(f"  - {output_size:,} bytes")
    print(f"\n📄 Structured JSON: {output_file}")


if __name__ == '__main__':
    main()
