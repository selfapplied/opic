#!/usr/bin/env python3
"""
Phase 1: Prime Voice Identification

Identifies indecomposable (prime) voices in the opic codebase.
A voice is prime if it cannot be decomposed into simpler voices.
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict

def find_all_ops_files(root_dir):
    """Find all .ops files in the codebase"""
    ops_files = []
    for root, dirs, files in os.walk(root_dir):
        # Skip certain directories
        dirs[:] = [d for d in dirs if d not in ['build', '.git', '__pycache__', 'node_modules']]
        
        for file in files:
            if file.endswith('.ops'):
                ops_files.append(Path(root) / file)
    
    return ops_files

def parse_voice(line):
    """Parse a voice definition from a line"""
    # Match: voice name / {chain}
    match = re.match(r'voice\s+([\w.]+)\s*/\s*\{([^}]+)\}', line)
    if match:
        name = match.group(1)
        body = match.group(2).strip()
        return {'name': name, 'body': body, 'line': line.strip()}
    return None

def parse_all_voices(ops_files):
    """Parse all voices from all .ops files"""
    all_voices = {}
    voice_locations = {}
    
    for ops_file in ops_files:
        try:
            with open(ops_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            for i, line in enumerate(lines, 1):
                # Skip comments
                if line.strip().startswith(';;') or line.strip().startswith('#'):
                    continue
                
                voice = parse_voice(line)
                if voice:
                    name = voice['name']
                    all_voices[name] = voice
                    voice_locations[name] = {
                        'file': str(ops_file.relative_to(Path.cwd())),
                        'line': i
                    }
        except Exception as e:
            print(f"Warning: Could not parse {ops_file}: {e}")
    
    return all_voices, voice_locations

def extract_voice_names_from_chain(chain_body):
    """Extract voice names referenced in a chain"""
    # Split by -> and extract voice names
    steps = [s.strip() for s in chain_body.split('->')]
    voice_names = []
    
    for step in steps:
        # Remove any operators or modifiers
        step = re.sub(r'[+\-*/()]', ' ', step)
        # Extract potential voice names (alphanumeric with dots)
        parts = re.findall(r'\b[\w.]+\b', step)
        voice_names.extend(parts)
    
    return voice_names

def check_decomposability(voice_name, voice_body, all_voices):
    """Check if a voice can be decomposed into other voices"""
    # Extract voices referenced in this voice's chain
    referenced_voices = extract_voice_names_from_chain(voice_body)
    
    # Filter to only voices that actually exist
    existing_referenced = [v for v in referenced_voices if v in all_voices]
    
    # A voice is decomposable if:
    # 1. It references other voices (not just primitives)
    # 2. Those voices are not just simple operations
    
    # Simple operations (not decomposable in our sense)
    simple_ops = {'add', 'subtract', 'multiply', 'divide', 'equals', 'plus', 'minus', 
                  'times', 'divide', 'and', 'or', 'not', 'if', 'then', 'else'}
    
    # Filter out simple operations
    meaningful_referenced = [v for v in existing_referenced 
                           if not any(op in v.lower() for op in simple_ops)]
    
    # If voice references other meaningful voices, it might be decomposable
    # But we need to check if those voices themselves are simpler
    
    # For now, heuristic:
    # - If voice has a simple body (just one step), it's likely prime
    # - If voice chains multiple other voices, it might be decomposable
    
    steps = [s.strip() for s in voice_body.split('->')]
    
    # Very simple voices (single operation) are prime
    if len(steps) <= 1:
        return False  # Not decomposable = prime
    
    # If it references other voices, check if those are simpler
    if meaningful_referenced:
        # Check if referenced voices are simpler (shorter chains)
        referenced_complexity = []
        for ref_name in meaningful_referenced:
            if ref_name in all_voices:
                ref_body = all_voices[ref_name]['body']
                ref_steps = len([s.strip() for s in ref_body.split('->')])
                referenced_complexity.append((ref_name, ref_steps))
        
        # If all referenced voices are simpler (shorter), this voice is decomposable
        current_complexity = len(steps)
        if referenced_complexity:
            min_ref_complexity = min(c for _, c in referenced_complexity)
            if min_ref_complexity < current_complexity:
                return True  # Decomposable
    
    # Default: not decomposable (prime)
    return False

def identify_prime_voices(all_voices):
    """Identify prime (indecomposable) voices"""
    prime_voices = []
    decomposable_voices = []
    
    for name, voice in all_voices.items():
        is_decomposable = check_decomposability(name, voice['body'], all_voices)
        
        voice_info = {
            'name': name,
            'body': voice['body'],
            'is_decomposable': is_decomposable,
            'is_prime': not is_decomposable
        }
        
        if is_decomposable:
            decomposable_voices.append(voice_info)
        else:
            prime_voices.append(voice_info)
    
    return prime_voices, decomposable_voices

def main():
    """Run Phase 1: Prime Voice Identification"""
    print("=" * 60)
    print("Phase 1: Prime Voice Identification")
    print("=" * 60)
    print()
    
    # Find all .ops files
    root_dir = Path.cwd()
    print(f"Scanning {root_dir} for .ops files...")
    ops_files = find_all_ops_files(root_dir)
    print(f"Found {len(ops_files)} .ops files")
    print()
    
    # Parse all voices
    print("Parsing voices...")
    all_voices, voice_locations = parse_all_voices(ops_files)
    print(f"Found {len(all_voices)} voices")
    print()
    
    # Identify prime voices
    print("Identifying prime voices...")
    prime_voices, decomposable_voices = identify_prime_voices(all_voices)
    
    print(f"Prime voices: {len(prime_voices)}")
    print(f"Decomposable voices: {len(decomposable_voices)}")
    print()
    
    # Show sample prime voices
    print("Sample Prime Voices (first 10):")
    print("-" * 60)
    for voice in prime_voices[:10]:
        print(f"  {voice['name']}")
        print(f"    Body: {voice['body'][:80]}...")
        print()
    
    # Save results
    results = {
        'total_voices': len(all_voices),
        'prime_voices_count': len(prime_voices),
        'decomposable_voices_count': len(decomposable_voices),
        'prime_voices': prime_voices,
        'decomposable_voices': decomposable_voices[:20],  # Sample
        'voice_locations': {k: v for k, v in list(voice_locations.items())[:50]}  # Sample
    }
    
    output_dir = Path('build')
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / 'phase1_prime_voices.json'
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to: {output_file}")
    print()
    print("=" * 60)
    print("Phase 1 Complete")
    print("=" * 60)
    print(f"✓ Found {len(prime_voices)} prime voices")
    print(f"✓ Results saved to {output_file}")
    print()
    print("Next: Phase 2 - Compute Functor ℱ(v) for prime voices")
    
    return results

if __name__ == '__main__':
    main()

