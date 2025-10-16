#!/usr/bin/env node
/**
 * Extract MULVEY_CODEX and FILM_CODEX from codex-uni.html
 * and save as JSON files for codex_universal.html
 */
const fs = require('fs');

// Read the HTML file
const content = fs.readFileSync('codex-uni.html', 'utf8');

// Extract the script content
const scriptMatch = content.match(/<script>([\s\S]*?)<\/script>/);
if (!scriptMatch) {
  console.error('Could not find script tag');
  process.exit(1);
}

const scriptContent = scriptMatch[1];

// Execute the script in a sandbox to get the data
const MULVEY_CODEX = {};
const FILM_CODEX = {};

try {
  // Use eval to execute the const declarations
  eval(scriptContent.match(/const MULVEY_CODEX = \{[\s\S]*?\n  \};/)[0]);
  eval(scriptContent.match(/const FILM_CODEX = \{[\s\S]*?\n  \};/)[0]);
  
  // Save as JSON
  fs.writeFileSync('mulvey_codex.json', JSON.stringify(MULVEY_CODEX, null, 2));
  console.log('✓ Created mulvey_codex.json');
  
  fs.writeFileSync('film_gaze_codex.json', JSON.stringify(FILM_CODEX, null, 2));
  console.log('✓ Created film_gaze_codex.json');
  
  console.log('\nNext steps:');
  console.log('1. These JSON files are now ready for codex_universal.html');
  console.log('2. Select them from the dropdown to load');
  
} catch (error) {
  console.error('Error extracting data:', error.message);
  process.exit(1);
}
