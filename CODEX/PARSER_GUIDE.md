# Codex Parser Guide

Convert your text data into codex JSON format with YouTube and image support.

## Data Format

Your input can use this flexible format:

```
## Concept Name

Definition: Your definition with <entities> and [morphisms]

Key terms:
- <entity>: explanation
- [morphism]: explanation

Summary: One-line summary

https://www.youtube.com/watch?v=VIDEO_ID
https://example.com/image.jpg


## Another Concept

Definition: More text...
```

## Usage

### Option 1: From a file
```bash
python3 parse_to_codex.py input.txt output.json
```

### Option 2: Paste directly
```bash
python3 parse_to_codex.py
# Paste your text, then press Ctrl+D
```

### Option 3: Pipe input
```bash
cat data.txt | python3 parse_to_codex.py > codex.json
```

## Supported Formats

### Sections
The parser recognizes these section headers:
- `Definition:` - Main concept definition
- `Key terms:` - List of related terms (array)
- `Summary:` - One-line summary
- `Secondary expansions:` - Additional terms (array)
- `Sitemap:` - Related concepts (array)
- `Checklist:` - Verification items (array)

### Media

**YouTube Videos:**
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`

**Images:**
- Any URL ending in: `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`, `.svg`

### Markup
- `<entity>` - Nouns, things that exist
- `[morphism]` - Verbs, actions, transformations
- `{alternative}` - Alternative phrasings

## Example Input

```
## Symbolic Reasoning

Definition: <Symbolic Reasoning> is a [cognitive process] where <abstract symbols> 
[represent] <concepts> and [logic rules] [manipulate] them to [derive] new <knowledge>.

Key terms:
- <abstract symbols>: representations that [stand for] <concepts>
- [manipulate]: [transform] or [combine] according to <rules>

Summary: Using symbols and logic to reason about concepts

https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://example.com/diagram.png


## Machine Learning

Definition: <Machine Learning> is the [process] by which <algorithms> [learn] 
<patterns> from <data> without explicit [programming].

Summary: Algorithms that learn from data
```

## Example Output

The parser creates JSON like:

```json
{
  "meta": {
    "title": "Parsed Concept Codex",
    "total_concepts": 2,
    "features": ["youtube_embeds", "image_urls"]
  },
  "concepts": [
    {
      "id": "symbolic_reasoning",
      "term": "Symbolic Reasoning",
      "sections": {
        "definition": "...",
        "key_terms": ["...", "..."],
        "summary": "...",
        "media": [
          {
            "type": "youtube",
            "id": "dQw4w9WgXcQ",
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
          },
          {
            "type": "image",
            "url": "https://example.com/diagram.png"
          }
        ]
      }
    }
  ]
}
```

## View in Hypertext Browser

1. Parse your data: `python3 parse_to_codex.py input.txt my_codex.json`
2. Open `codex_hypertext.html` in browser
3. Update the fetch URL to point to your JSON:
   ```javascript
   const response = await fetch('my_codex.json');
   ```

The hypertext viewer will automatically render:
- ✅ YouTube embeds (16:9 responsive)
- ✅ Images (clickable to open full size)
- ✅ All hyperlinked entities and morphisms
- ✅ Collection/export functionality

## Tips

- **Be consistent** with markup: use `<>` for nouns, `[]` for verbs
- **One concept per block** separated by blank lines or `##` headers
- **Media URLs** can appear anywhere in the block
- **Lists** use `-` or `•` for bullet points
- **Sections** are automatically detected by the colon pattern

## Ready to parse?

Just give me your data and I'll convert it to codex JSON! 📝✨
