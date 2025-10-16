#!/usr/bin/env python3
"""
Parse notes.md and extract all concept definitions into structured JSON.
Handles the entity/morphism notation (<entity> and [morphism] syntax).
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional


def slugify(text: str) -> str:
    """Convert concept name to JSON-friendly ID."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '_', text)
    return text


def extract_key_terms(text: str) -> Dict[str, str]:
    """Extract key term definitions from the Key terms section."""
    key_terms = {}
    
    # Pattern: <term> or [term]: definition
    pattern = r'^(?:<([^>]+)>|\[([^\]]+)\]):\s*(.+)$'
    
    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        match = re.match(pattern, line)
        if match:
            entity_term = match.group(1)
            morphism_term = match.group(2)
            definition = match.group(3)
            
            term_name = entity_term if entity_term else morphism_term
            if term_name:
                key = slugify(term_name)
                key_terms[key] = definition
    
    return key_terms


def categorize_concept(term: str, definition: str) -> str:
    """Infer category based on term and definition content."""
    term_lower = term.lower()
    def_lower = definition.lower()
    
    if 'ekphrasis' in term_lower or 'ekphrastic' in term_lower:
        if any(word in term_lower for word in ['hope', 'fear', 'indifference']):
            return 'ekphrasis_critical_stances'
        return 'ekphrasis_modes'
    
    if any(word in term_lower for word in ['imagetext', 'paragonal', 'mediamachia']):
        return 'media_relations'
    
    if any(word in term_lower for word in ['prompt', 'llm', 'symbolic reasoning', 'wizard-npc']):
        return 'ai_systems'
    
    if any(word in term_lower for word in ['apparatus', 'microcode', 'assembly', 'hypertext', 'instruction']):
        return 'technical_philosophical'
    
    if any(word in term_lower for word in ['aura', 'uncanny', 'affective']):
        return 'aesthetic_perceptual'
    
    if any(word in term_lower for word in ['grimoire', 'screwtape', 'atlas shrugged', 'book', 'novel']):
        return 'literature_cultural'
    
    if any(word in term_lower for word in ['translation', 'intersemiotic', 'diagram']):
        return 'semiotic_visual'
    
    return 'general'


def extract_concepts(md_content: str) -> List[Dict[str, Any]]:
    """Parse the entire markdown file and extract all concepts."""
    concepts_dict = {}  # Use dict for deduplication by ID
    
    # Pattern 1: Look for <ConceptName> followed by "Definition"
    # More flexible to handle variations in whitespace and formatting
    concept_pattern = r'<([A-Z][^>]+?)>\s*\n(?:Definition|Definition \(full code syntax\))\s*\n(.*?)(?=\n<[A-Z][^>]+?>\s*\n(?:Definition|Definition \(full code syntax\))|\nYou said:|\Z)'
    
    matches = re.finditer(concept_pattern, md_content, re.DOTALL | re.MULTILINE)
    
    for match in matches:
        concept_header = match.group(1).strip()
        content = match.group(2)
        
        concept_id = slugify(concept_header)
        
        # Skip if we've already parsed a more complete version
        if concept_id in concepts_dict and concepts_dict[concept_id].get('summary'):
            # Only replace if new version has more content
            if 'Summary' not in content and 'One-line gist' not in content:
                continue
        
        # Extract definition (first line/paragraph after "Definition")
        # Stop at Key terms, Sitemap, Summary, or One-line gist
        def_match = re.search(r'^(.+?)(?=\n\n(?:Key terms|Key mechanics|Sitemap|Summary|One-line gist|Process schema)|\Z)', 
                             content, re.DOTALL | re.MULTILINE)
        definition = def_match.group(1).strip() if def_match else ""
        
        # Clean up definition
        definition = re.sub(r'\s+', ' ', definition)
        
        # Extract key terms
        key_terms_match = re.search(r'(?:Key terms|Key mechanics).*?\n(.*?)(?=\n\n(?:Sitemap|Summary|One-line gist|Process schema|Contrast set)|\Z)', 
                                    content, re.DOTALL | re.MULTILINE)
        key_terms_text = key_terms_match.group(1) if key_terms_match else ""
        key_terms = extract_key_terms(key_terms_text)
        
        # Extract summary - try "Summary" or "One-line gist"
        summary_match = re.search(r'(?:Summary|One-line gist)\s*\n(.+?)(?=\n\n|\Z)', content, re.DOTALL | re.MULTILINE)
        summary = summary_match.group(1).strip() if summary_match else ""
        summary = re.sub(r'\s+', ' ', summary)
        
        # Extract examples if present
        example_match = re.search(r'(?:Example|Completion)[s]?[:\s]+(.*?)(?=\n\n(?:[A-Z]|<)|\Z)', content, re.DOTALL | re.MULTILINE)
        example = example_match.group(1).strip() if example_match else None
        if example:
            example = re.sub(r'\s+', ' ', example)[:500]  # Truncate long examples
        
        # Extract contrast set if present
        contrast_match = re.search(r'Contrast set\s*\n(.*?)(?=\n\n(?:Process schema|Sitemap|Example)|\Z)', content, re.DOTALL | re.MULTILINE)
        contrasts = None
        if contrast_match:
            contrast_text = contrast_match.group(1)
            contrasts = [line.strip() for line in contrast_text.split('\n') if line.strip() and line.strip().startswith('<')]
        
        if definition:  # Only add if we found a definition
            concept = {
                "id": concept_id,
                "term": concept_header,
                "definition": definition,
                "key_terms": key_terms,
                "summary": summary,
                "category": categorize_concept(concept_header, definition)
            }
            
            if example:
                concept["example"] = example
            
            if contrasts:
                concept["contrasts"] = contrasts
            
            # Store in dict (automatically handles duplicates)
            concepts_dict[concept_id] = concept
    
    return list(concepts_dict.values())


def build_taxonomy(concepts: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    """Build taxonomy from categorized concepts."""
    taxonomy = {}
    
    for concept in concepts:
        category = concept['category']
        if category not in taxonomy:
            taxonomy[category] = []
        taxonomy[category].append(concept['id'])
    
    return taxonomy


def build_relationships(concepts: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Infer relationships between concepts."""
    relationships = {}
    concept_ids = {c['id'] for c in concepts}
    
    # Ekphrasis family
    ekphrasis_modes = [c['id'] for c in concepts if 'ekphrasis' in c['id'] and 
                      'ekphrastic' not in c['id'] and c['id'] != 'ekphrasis']
    ekphrasis_stances = [c['id'] for c in concepts if 'ekphrastic_' in c['id']]
    
    if ekphrasis_modes or ekphrasis_stances:
        relationships['ekphrasis_family'] = {
            'root': 'ekphrasis' if 'ekphrasis' in concept_ids else None,
            'specialized_modes': sorted(set(ekphrasis_modes)),  # Deduplicate
            'critical_positions': sorted(set(ekphrasis_stances))
        }
    
    # Word-image relations (only include concepts that actually exist)
    word_image_map = {
        'separation': 'ekphrastic_indifference',
        'bridging': 'ekphrastic_hope',
        'containment': 'ekphrastic_fear',
        'synthesis': 'imagetext',
        'negotiation': 'paragonal_struggle'
    }
    
    word_image_relations = {k: v for k, v in word_image_map.items() if v in concept_ids}
    if word_image_relations:
        relationships['word_image_relations'] = word_image_relations
    
    return relationships


def main():
    """Main parser function."""
    input_file = Path('/Users/gaia/EOS/CODEX/notes.md')
    output_file = Path('/Users/gaia/EOS/CODEX/notes.json')
    
    # Read markdown file
    print(f"Reading {input_file}...")
    md_content = input_file.read_text(encoding='utf-8')
    
    # Extract all concepts
    print("Parsing concepts...")
    concepts = extract_concepts(md_content)
    print(f"Found {len(concepts)} concepts")
    
    # Build taxonomy and relationships
    taxonomy = build_taxonomy(concepts)
    relationships = build_relationships(concepts)
    
    # Build output structure
    output = {
        "meta": {
            "title": "Code Syntax for Entity and Morphism Distinctions - Concept Codex",
            "description": "Normalized knowledge base of philosophical and technical concepts with entity/morphism syntax notation",
            "notation": {
                "entity": "Marked with angle brackets: <entity>",
                "morphism": "Marked with square brackets: [action]",
                "syntax_convention": "Entities are nouns/things and exist; Morphisms are verbs/processes/transformations"
            },
            "source_file": str(input_file),
            "total_concepts": len(concepts),
            "generated_by": "parse_notes.py",
            "parser_version": "1.0"
        },
        "concepts": concepts,
        "taxonomy": taxonomy,
        "relationships": relationships
    }
    
    # Write JSON output
    print(f"Writing to {output_file}...")
    output_file.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding='utf-8')
    
    print(f"\n✅ Successfully parsed {len(concepts)} concepts")
    print(f"\nCategories found:")
    for category, concept_ids in taxonomy.items():
        print(f"  - {category}: {len(concept_ids)} concepts")
    
    print(f"\n📄 Output written to: {output_file}")


if __name__ == '__main__':
    main()
