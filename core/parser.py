#!/usr/bin/env python3
"""Opic code generation — Metal and Swift"""

from pathlib import Path
import re

def parse_ops(text, file_path=None):
    """Parse .ops file - uses OPIC expansion system (core/expansions.ops)
    Each line type is an expansion rule: def, voice, include, comment, empty.
    Expansion rules are defined declaratively in OPIC using matchers.
    Also builds semantic boundary matrix for symbol extraction and type filtering."""
    defs, voices, includes = {}, {}, []
    lines = text.splitlines()
    
    # Build semantic boundary matrix: [line, char, type, content, position]
    # Each row represents a significant semantic change (boundary condition)
    boundary_matrix = []
    
    # Build expansion map for symbols (directory -> files, file -> itself)
    # Expansion logic defined in core/expansions.ops: expansion.directory_to_files, expansion.file_to_self
    expansions = {}  # symbol -> (path, origin_dir)
    if file_path and file_path.parent.exists():
        bases = [file_path.parent]
        if file_path.parent.parent.exists():
            bases.append(file_path.parent.parent)
        for base in bases:
            try:
                for item in base.iterdir():
                    if item.is_dir() and not item.name.startswith('.'):
                        # expansion.directory_to_files: directory expands to its files
                        try:
                            for file_item in item.iterdir():
                                if file_item.suffix == '.ops' and file_item.is_file():
                                    symbol = file_item.stem
                                    expansions[symbol] = (file_item, item.name)
                        except (PermissionError, OSError):
                            pass
                    elif item.suffix == '.ops' and item.is_file():
                        # expansion.file_to_self: file expands to itself
                        symbol = item.stem
                        if symbol not in expansions:
                            expansions[symbol] = (item, base.name if base != file_path.parent else '.')
            except (PermissionError, OSError):
                pass
    
    # Collect symbols used in code (they're lambdas)
    symbols = set()
    builtin = {'opic', 'true', 'false', 'null', 'result', 'input', 'output', 'env', 'context', 'if', 'then', 'else'}
    
    for line in lines:
        if line.strip().startswith(";"):
            continue
        for ns, _ in re.findall(r'\b([a-zA-Z0-9_]+)\.([a-zA-Z0-9_]+)\b', line):
            if ns not in builtin:
                symbols.add(ns)
        for ns in re.findall(r'\{([a-zA-Z0-9_]+)\s*->', line):
            if ns not in builtin:
                symbols.add(ns)
    
    # Expand symbols using expansion.match
    for symbol in symbols:
        if symbol in expansions:
            path, origin = expansions[symbol]
            try:
                includes.append(str(path.relative_to(file_path.parent)))
            except ValueError:
                includes.append(f"{origin}/{path.name}" if origin != '.' else path.name)
        else:
            # expansion.resolve_string: symbol resolves to itself, but try to find file
            if file_path and file_path.parent.exists():
                bases = [file_path.parent]
                if file_path.parent.parent.exists():
                    bases.append(file_path.parent.parent)
                for base in bases:
                    ops_file = base / f"{symbol}.ops"
                    if ops_file.exists() and ops_file.is_file():
                        try:
                            includes.append(str(ops_file.relative_to(file_path.parent)))
                        except ValueError:
                            includes.append(ops_file.name)
                        break
    
    # Parse lines using expansion rules (each line type is an expansion)
    # expansion.parse_line applies expansion rules: expansion.def_expansion, expansion.voice_expansion, etc.
    # Also build semantic boundary matrix: track line, char, type, content, position
    for line_num, line in enumerate(lines, 1):
        stripped = line.strip()
        char_offset = len(line) - len(line.lstrip())
        
        if not stripped or stripped.startswith(";"):
            # expansion.comment_expansion, expansion.empty_expansion: skip
            if stripped.startswith(";"):
                boundary_matrix.append([line_num, char_offset, "comment", stripped, (line_num, char_offset)])
            continue
        elif stripped.startswith("include "):
            # expansion.include_expansion: include line expands to include path
            inc = stripped[8:].strip()
            boundary_matrix.append([line_num, char_offset, "include", inc, (line_num, char_offset)])
            if inc not in includes:
                includes.append(inc)
        elif stripped.startswith("def "):
            # expansion.def_expansion: def line expands to definition object
            parts = stripped[4:].split()
            def_name = parts[0] if parts else ""
            boundary_matrix.append([line_num, char_offset, "def_start", def_name, (line_num, char_offset)])
            defs[def_name] = {}
        elif stripped.startswith("voice "):
            # expansion.voice_expansion: voice line expands to voice object
            l, _, r = line.partition("/")
            name = l.split()[1].strip()
            body = r.strip().strip('" ')
            boundary_matrix.append([line_num, char_offset, "voice_start", name, (line_num, char_offset)])
            
            if body.startswith("{"):
                brace_count = body.count("{") - body.count("}")
                if brace_count == 0:
                    voices[name] = body.strip().strip('" ')
                else:
                    # Multi-line chain
                    chain_lines = [body]
                    i = lines.index(line) + 1
                    iterations = 0
                    while i < len(lines) and brace_count > 0 and iterations < 200:
                        iterations += 1
                        next_line = lines[i]
                        chain_lines.append(next_line)
                        brace_count += next_line.count("{") - next_line.count("}")
                        i += 1
                        if brace_count <= 0:
                            break
                    voices[name] = " ".join(chain_lines).strip().strip('" ')
            else:
                voices[name] = body.strip().strip('" ')
        
        # Track namespace usage (namespace.voice pattern)
        for ns_match in re.finditer(r'\b([a-zA-Z0-9_]+)\.([a-zA-Z0-9_]+)\b', line):
            ns_start = ns_match.start()
            namespace = ns_match.group(1)
            if namespace not in builtin:
                boundary_matrix.append([line_num, ns_start, "namespace", namespace, (line_num, ns_start)])
    
    # Extract symbol list from boundary matrix for expansion operations
    # Can use expansion.create_symbol_list, expansion.batch_expand, etc.
    symbol_list = list(set([row[3] for row in boundary_matrix if row[2] in ["def_start", "voice_start", "namespace"]]))
    
    return defs, voices, includes, boundary_matrix, symbol_list
