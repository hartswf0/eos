#!/usr/bin/env python3
"""
Extract MULVEY_CODEX and FILM_CODEX from codex-uni.html
and save as JSON files for codex_universal.html
"""
import re
import json

# Read the HTML file
with open('codex-uni.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract MULVEY_CODEX
mulvey_match = re.search(r'const MULVEY_CODEX = ({.*?});', content, re.DOTALL)
if mulvey_match:
    mulvey_js = mulvey_match.group(1)
    # Convert JS object notation to JSON
    # This is a simple conversion - might need manual tweaking for complex cases
    mulvey_js = re.sub(r"(\w+):", r'"\1":', mulvey_js)  # Add quotes to keys
    mulvey_js = re.sub(r"'", r'"', mulvey_js)  # Replace single quotes with double
    
    try:
        mulvey_data = eval(mulvey_js)  # Using eval since it's our own controlled data
        with open('mulvey_codex.json', 'w', encoding='utf-8') as f:
            json.dump(mulvey_data, f, indent=2, ensure_ascii=False)
        print("✓ Created mulvey_codex.json")
    except Exception as e:
        print(f"Error parsing MULVEY_CODEX: {e}")
        # Fallback: save raw extracted JS
        with open('mulvey_codex_raw.js', 'w') as f:
            f.write(mulvey_js)
        print("  Saved raw JS to mulvey_codex_raw.js for manual conversion")

# Extract FILM_CODEX  
film_match = re.search(r'const FILM_CODEX = ({.*?});', content, re.DOTALL)
if film_match:
    film_js = film_match.group(1)
    # Convert JS object notation to JSON
    film_js = re.sub(r"(\w+):", r'"\1":', film_js)
    film_js = re.sub(r"'", r'"', film_js)
    
    try:
        film_data = eval(film_js)
        with open('film_gaze_codex.json', 'w', encoding='utf-8') as f:
            json.dump(film_data, f, indent=2, ensure_ascii=False)
        print("✓ Created film_gaze_codex.json")
    except Exception as e:
        print(f"Error parsing FILM_CODEX: {e}")
        with open('film_codex_raw.js', 'w') as f:
            f.write(film_js)
        print("  Saved raw JS to film_codex_raw.js for manual conversion")

print("\nNext steps:")
print("1. Verify the JSON files are valid")
print("2. Load them in codex_universal.html using the dropdown")
