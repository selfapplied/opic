#!/usr/bin/env python3
"""Opic code generation — Metal and Swift"""

from pathlib import Path
import re

def parse_ops(text):
    """Parse .ops file - implements opic.parse_ops voice from opic_parse.ops"""
    defs, voices, includes = {}, {}, []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line or line.startswith(";"):
            i += 1
            continue
        if line.startswith("include "):
            # Implements opic.extract_include_files voice
            include_file = line[8:].strip()
            includes.append(include_file)
            i += 1
            continue
        elif line.startswith("def "):
            # Implements opic.parse_def voice
            parts = line[4:].split()
            name = parts[0]
            defs[name] = {}
            i += 1
            continue
        elif line.startswith("voice "):
            # Implements opic.parse_voice voice - handle multi-line chains
            l, _, r = line.partition("/")
            name = l.split()[1].strip()
            body = r.strip().strip('" ')
            
            # If body starts with '{', check if it's a single-line or multi-line chain
            if body.startswith("{"):
                # Check if braces are balanced on this line (single-line chain)
                brace_count = body.count("{") - body.count("}")
                if brace_count == 0:
                    # Single-line chain, use as-is
                    voices[name] = body.strip().strip('" ')
                    i += 1
                    continue
                else:
                    # Multi-line chain, collect until braces balance
                    chain_lines = [body]
                    i += 1
                    max_iterations = min(len(lines) - i + 10, 200)  # Safety limit
                    iterations = 0
                    # Continue reading until braces balance
                    while i < len(lines) and brace_count > 0 and iterations < max_iterations:
                        iterations += 1
                        next_line = lines[i] if i < len(lines) else ""
                        chain_lines.append(next_line)
                        brace_count += next_line.count("{") - next_line.count("}")
                        i += 1
                        if brace_count <= 0:
                            break  # Found closing brace, exit immediately
                    voices[name] = " ".join(chain_lines).strip().strip('" ')
                    continue  # i already points to next line after closing brace
            else:
                voices[name] = body.strip().strip('" ')
                i += 1
                continue
        i += 1  # Fallback increment (shouldn't be reached, but safety)
    return defs, voices, includes
