#!/usr/bin/env python3
"""
Organize straggler files from root directory
"""

from pathlib import Path
import sys

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "core"))

import importlib.util
executor_path = project_root / "core" / "opic_executor.py"
spec = importlib.util.spec_from_file_location("opic_executor", executor_path)
executor_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(executor_module)
OpicExecutor = executor_module.OpicExecutor

executor = OpicExecutor(project_root)

print("=== Organizing Straggler Files ===")
print("")

# Examples/entry points (should stay accessible)
examples_dir = project_root / "examples"
examples_dir.mkdir(exist_ok=True)

# Root .ops files that are examples/entry points
example_files = [
    ("getting_started.ops", "examples/getting_started.ops"),
    ("hello.ops", "examples/hello.ops"),
    ("art_gallery.ops", "examples/art_gallery.ops"),
    ("draw.ops", "examples/draw.ops"),
]

# System/application files
systems_dir = project_root / "systems"
systems_dir.mkdir(exist_ok=True)

system_files = [
    ("opic_help.ops", "systems/help/opic_help.ops"),
    ("wild_sort_service.ops", "systems/wild_sort_service.ops"),
    ("company_seed.ops", "systems/company_seed.ops"),
    ("whitepaper.ops", "systems/whitepaper.ops"),
    ("agspan_namespace.ops", "systems/agspan_namespace.ops"),
]

# Documentation files
docs_dir = project_root / "docs"
docs_dir.mkdir(exist_ok=True)

doc_files = [
    ("FILE_ORGANIZATION.md", "docs/FILE_ORGANIZATION.md"),
    ("ORGANIZATION_PLAN.md", "docs/ORGANIZATION_PLAN.md"),
    ("CONTRIBUTING.md", "docs/CONTRIBUTING.md"),
    # README.md stays in root
]

print("Moving example files...")
for source, dest in example_files:
    source_path = project_root / source
    if source_path.exists():
        dest_path = project_root / dest
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        result = executor._call_primitive("file.move", {"source": str(source_path), "dest": str(dest_path)})
        if result and not result.startswith("error"):
            print(f"  ✓ Moved {source} → {dest}")
        else:
            print(f"  ⚠ {result}")

print("")
print("Moving system files...")
for source, dest in system_files:
    source_path = project_root / source
    if source_path.exists():
        dest_path = project_root / dest
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        result = executor._call_primitive("file.move", {"source": str(source_path), "dest": str(dest_path)})
        if result and not result.startswith("error"):
            print(f"  ✓ Moved {source} → {dest}")
        else:
            print(f"  ⚠ {result}")

print("")
print("Moving documentation files...")
for source, dest in doc_files:
    source_path = project_root / source
    if source_path.exists():
        dest_path = project_root / dest
        result = executor._call_primitive("file.move", {"source": str(source_path), "dest": str(dest_path)})
        if result and not result.startswith("error"):
            print(f"  ✓ Moved {source} → {dest}")
        else:
            print(f"  ⚠ {result}")

print("")
print("✓ Straggler files organized!")

