#!/usr/bin/env python3
"""
Generate Help — Derive help from actual .ops files, comments, and code
"""

import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple

def parse_ops_file(file_path: Path) -> Dict:
    """Parse .ops file and extract help information"""
    content = file_path.read_text()
    
    # Extract header comment (;;; line)
    header_match = re.search(r'^;;;\s*(.+)$', content, re.MULTILINE)
    header = header_match.group(1).strip() if header_match else ""
    
    # Extract all comments
    comments = []
    for line in content.splitlines():
        line = line.strip()
        if line.startswith(';;'):
            comment = line[2:].strip()
            if comment and not comment.startswith(';'):  # Skip ;;;
                comments.append(comment)
    
    # Extract voice definitions
    voices = []
    voice_pattern = r'voice\s+(\S+)\s*/\s*(.+)$'
    for match in re.finditer(voice_pattern, content, re.MULTILINE):
        voice_name = match.group(1)
        voice_body = match.group(2).strip()
        voices.append({
            "name": voice_name,
            "body": voice_body[:100] + "..." if len(voice_body) > 100 else voice_body
        })
    
    # Extract target definitions
    targets = []
    target_pattern = r'target\s+(\S+)\s*/\s*"(.+)"'
    for match in re.finditer(target_pattern, content, re.MULTILINE):
        targets.append({
            "name": match.group(1),
            "description": match.group(2)
        })
    
    return {
        "file": file_path.name,
        "path": str(file_path),
        "header": header,
        "comments": comments,
        "voices": voices,
        "targets": targets
    }

def scan_ops_files(project_root: Path) -> List[Dict]:
    """Scan all .ops files in project"""
    ops_files = []
    
    # Root .ops files
    for ops_file in sorted(project_root.glob("*.ops")):
        if not ops_file.name.startswith("."):
            ops_files.append(parse_ops_file(ops_file))
    
    # Core .ops files
    core_dir = project_root / "core"
    if core_dir.exists():
        for ops_file in sorted(core_dir.glob("*.ops")):
            ops_files.append(parse_ops_file(ops_file))
    
    # Systems .ops files
    systems_dir = project_root / "systems"
    if systems_dir.exists():
        for ops_file in sorted(systems_dir.glob("*.ops")):
            ops_files.append(parse_ops_file(ops_file))
    
    return ops_files

def extract_command_mappings(opic_script: Path) -> Dict[str, str]:
    """Extract command mappings from opic script"""
    content = opic_script.read_text()
    
    # Find command_map dictionary
    command_map_match = re.search(r'command_map\s*=\s*\{([^}]+)\}', content, re.DOTALL)
    if not command_map_match:
        return {}
    
    command_map_str = command_map_match.group(1)
    
    # Extract individual mappings
    mappings = {}
    for match in re.finditer(r'"(\w+)"\s*:\s*"([^"]+)"', command_map_str):
        command = match.group(1)
        ops_file = match.group(2)
        mappings[command] = ops_file
    
    return mappings

def generate_help_text(ops_files: List[Dict], command_mappings: Dict[str, str], project_root: Path) -> str:
    """Generate help text from parsed information"""
    lines = []
    lines.append("Opic CLI — Event-Based Compositional Language")
    lines.append("")
    lines.append("Usage:")
    lines.append("  opic <command> [args...]")
    lines.append("")
    
    # Commands section
    lines.append("Commands:")
    for command, ops_file in sorted(command_mappings.items()):
        # Find the ops file to get its description
        ops_info = None
        for info in ops_files:
            if info["file"] == ops_file:
                ops_info = info
                break
        
        if ops_info:
            desc = ops_info.get("header", "").split("—")[-1].strip() if "—" in ops_info.get("header", "") else ops_file
            lines.append(f"  {command:<12} {desc}")
        else:
            lines.append(f"  {command:<12} Execute {ops_file}")
    
    lines.append("")
    
    # Key .ops files section
    lines.append("Key .ops Files:")
    key_files = [
        ("bootstrap.ops", "Bring opic up"),
        ("opic_help.ops", "Show help"),
        ("repos.ops", "List repositories"),
        ("runtime_test.ops", "Run tests"),
    ]
    
    for file_name, description in key_files:
        # Find actual description from parsed files
        for info in ops_files:
            if info["file"] == file_name:
                header = info.get("header", "")
                if "—" in header:
                    description = header.split("—")[-1].strip()
                else:
                    description = description
                lines.append(f"  {file_name:<20} {description}")
                break
    
    lines.append("")
    
    # Examples section
    lines.append("Examples:")
    lines.append("  opic help                      # Show this help")
    lines.append("  opic execute bootstrap.ops     # Execute a file")
    lines.append("  opic repos                    # List repositories")
    lines.append("  opic test                     # Run tests")
    lines.append("")
    
    # Make targets section
    makefile_path = project_root / "Makefile"
    if makefile_path.exists():
        lines.append("Make Targets:")
        makefile_content = makefile_path.read_text()
        # Extract make targets (simplified)
        target_pattern = r'^([a-zA-Z0-9_-]+):'
        targets = []
        for match in re.finditer(target_pattern, makefile_content, re.MULTILINE):
            target = match.group(1)
            if target not in ['.PHONY', 'check-opic']:
                targets.append(target)
        
        for target in sorted(set(targets))[:10]:  # Limit to first 10
            lines.append(f"  make {target}")
        lines.append("")
    
    return "\n".join(lines)

def main():
    """Generate help from codebase"""
    project_root = Path(__file__).parent.parent
    
    # Scan .ops files
    ops_files = scan_ops_files(project_root)
    
    # Extract command mappings
    opic_script = project_root / "opic"
    command_mappings = extract_command_mappings(opic_script) if opic_script.exists() else {}
    
    # Generate help
    help_text = generate_help_text(ops_files, command_mappings, project_root)
    
    print(help_text)

if __name__ == "__main__":
    main()

