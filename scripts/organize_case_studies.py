#!/usr/bin/env python3
"""
Organize OPIC repository into coherent case studies.

This script follows CURSOR_ORGANIZE_PROMPT.md to:
1. Create archive structure
2. Create case study directories
3. Copy core pattern files
4. Copy domain lens files
5. Move everything else to archive
6. Create minimal active structure
"""

import os
import shutil
from pathlib import Path
from typing import List, Tuple

# Base directory
BASE_DIR = Path(__file__).parent.parent

# File mappings: (source, destination)
CORE_PATTERNS = {
    "1.1_cosmology": [
        ("systems/zeta/zeta_cosmological_correspondence.ops", "case_studies/core/cosmology/"),
        ("systems/cosmology/cosmological_extended.ops", "case_studies/core/cosmology/"),
        ("docs/cosmological_validation.md", "case_studies/core/cosmology/"),
    ],
    "1.2_reasoning": [
        ("systems/reasoning.ops", "case_studies/core/reasoning/"),
        ("systems/explain.ops", "case_studies/core/reasoning/"),
        ("action/tests/explanation_plan.ops", "case_studies/core/reasoning/"),
        ("action/tests/self_explanation.ops", "case_studies/core/reasoning/"),
    ],
    "1.3_tests": [
        ("action/tests/scoring.ops", "case_studies/core/tests/"),
        ("action/tests/self.ops", "case_studies/core/tests/"),
        ("action/tests/executor_flow.ops", "case_studies/core/tests/"),
    ],
    "1.4_compression": [
        ("systems/critical_geometry_codec.ops", "case_studies/core/compression/"),
        ("systems/compression/compression.ops", "case_studies/core/compression/"),
        ("systems/zeta/zeta_compression.ops", "case_studies/core/compression/"),
    ],
    "1.5_emergent": [
        ("systems/actor_coupled_modeling.ops", "case_studies/core/emergent/"),
    ],
    "1.6_learn": [
        ("systems/solve/solve_simple.ops", "case_studies/core/learn/"),
        ("systems/solve/example.ops", "case_studies/core/learn/"),
    ],
}

DOMAIN_LENSES = {
    "2.1_biology": [
        ("systems/fields/biology_field.ops", "case_studies/domains/biology/"),
        ("docs/biology_field_equations.md", "case_studies/domains/biology/"),
    ],
    "2.2_ml": [
        ("action/ml/ml.ops", "case_studies/domains/ml/"),
        ("action/ml/gann.ops", "case_studies/domains/ml/"),
        ("action/ml/generate.ops", "case_studies/domains/ml/"),
        ("action/ml/train.ops", "case_studies/domains/ml/"),
        ("action/ml/attention.ops", "case_studies/domains/ml/"),
    ],
    "2.3_protocols": [
        ("systems/protocol/peer.ops", "case_studies/domains/protocols/"),
        ("systems/protocol/certificate.ops", "case_studies/domains/protocols/"),
        ("systems/protocol/consensus.ops", "case_studies/domains/protocols/"),
        ("systems/protocol/governance.ops", "case_studies/domains/protocols/"),
    ],
    "2.4_medicine": [
        ("systems/fields/biology_field.ops", "case_studies/domains/medicine/"),
    ],
}

# Directories to archive (everything except what we're keeping)
ARCHIVE_DIRS = [
    "systems",
    "action",
    "docs",
    "build",
    "resources",
]

# Files to keep in root
KEEP_IN_ROOT = [
    "core",
    "systems/solve",  # Keep solve system
    "systems/grammar",  # Keep grammar infrastructure (just consolidated!)
    "systems/registry",  # Keep registry infrastructure (status, filter, translation)
    "systems/opic_core",  # Keep executor implementation
    "case_studies.md",
    "README.md",
    "REFACTOR_PLAN.md",
    "CURSOR_ORGANIZE_PROMPT.md",
    "scripts",
    "opic",
    "Makefile",
    "LICENSE",
    "self.ops",
]


def create_directories():
    """Create archive and case study directory structures."""
    print("Creating directory structures...")
    
    # Archive structure
    archive_dirs = [
        "archive/systems",
        "archive/action",
        "archive/docs",
        "archive/build",
        "archive/resources",
    ]
    
    # Case study structure
    case_study_dirs = [
        "case_studies/core/cosmology",
        "case_studies/core/reasoning",
        "case_studies/core/tests",
        "case_studies/core/compression",
        "case_studies/core/emergent",
        "case_studies/core/learn",
        "case_studies/core/emit",
        "case_studies/domains/biology",
        "case_studies/domains/ml",
        "case_studies/domains/protocols",
        "case_studies/domains/medicine",
    ]
    
    for dir_path in archive_dirs + case_study_dirs:
        full_path = BASE_DIR / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"  Created: {dir_path}")


def copy_files(file_mappings: List[Tuple[str, str]], category: str):
    """Copy files to case study directories."""
    print(f"\nCopying {category} files...")
    
    copied_files = []
    missing_files = []
    
    for source, dest_dir in file_mappings:
        source_path = BASE_DIR / source
        dest_path = BASE_DIR / dest_dir
        
        if source_path.exists():
            dest_path.mkdir(parents=True, exist_ok=True)
            dest_file = dest_path / source_path.name
            
            # Handle duplicate names (e.g., biology_field.ops in both biology and medicine)
            if dest_file.exists() and source_path != dest_file:
                # Add category prefix
                dest_file = dest_path / f"{category}_{source_path.name}"
            
            shutil.copy2(source_path, dest_file)
            copied_files.append((source, str(dest_file.relative_to(BASE_DIR))))
            print(f"  ✓ {source} → {dest_file.relative_to(BASE_DIR)}")
        else:
            missing_files.append(source)
            print(f"  ✗ Missing: {source}")
    
    return copied_files, missing_files


def get_files_to_archive():
    """Get list of files that should be archived (everything except what we're keeping)."""
    files_to_archive = []
    
    # Track files we're keeping
    kept_files = set()
    
    # Add core pattern files
    for mappings in CORE_PATTERNS.values():
        for source, _ in mappings:
            kept_files.add(BASE_DIR / source)
    
    # Add domain lens files
    for mappings in DOMAIN_LENSES.values():
        for source, _ in mappings:
            kept_files.add(BASE_DIR / source)
    
    # Add root files to keep
    for item in KEEP_IN_ROOT:
        item_path = BASE_DIR / item
        if item_path.exists():
            if item_path.is_file():
                kept_files.add(item_path)
            else:
                # Directory - add all files in it
                for file_path in item_path.rglob("*"):
                    if file_path.is_file():
                        kept_files.add(file_path)
    
    # Find files to archive
    for archive_dir in ARCHIVE_DIRS:
        archive_path = BASE_DIR / archive_dir
        if archive_path.exists():
            for file_path in archive_path.rglob("*"):
                if file_path.is_file() and file_path not in kept_files:
                    files_to_archive.append(file_path)
    
    return files_to_archive, kept_files


def archive_files(dry_run: bool = True):
    """Move files to archive (dry run by default)."""
    files_to_archive, kept_files = get_files_to_archive()
    
    print(f"\n{'[DRY RUN] ' if dry_run else ''}Archiving files...")
    print(f"Found {len(files_to_archive)} files to archive")
    print(f"Keeping {len(kept_files)} files")
    
    if dry_run:
        print("\nFiles that would be archived (first 20):")
        for file_path in files_to_archive[:20]:
            rel_path = file_path.relative_to(BASE_DIR)
            archive_dest = BASE_DIR / "archive" / rel_path
            print(f"  {rel_path} → archive/{rel_path}")
        if len(files_to_archive) > 20:
            print(f"  ... and {len(files_to_archive) - 20} more")
    else:
        # Actually move files
        moved = 0
        for file_path in files_to_archive:
            rel_path = file_path.relative_to(BASE_DIR)
            archive_dest = BASE_DIR / "archive" / rel_path
            archive_dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(file_path), str(archive_dest))
            moved += 1
            if moved % 100 == 0:
                print(f"  Moved {moved} files...")
        print(f"  ✓ Moved {moved} files to archive")


def create_readme_files():
    """Create README.md files in each case study directory."""
    print("\nCreating README files...")
    
    readme_template = """# {title}

{description}

## What It Demonstrates

{demonstrates}

## Key Files

{files}

## How to Run Examples

{run_instructions}

## Connection to Other Case Studies

{connections}
"""
    
    # This would be populated from case_studies.md
    # For now, create placeholder READMEs
    case_study_dirs = [
        ("case_studies/core/cosmology", "Cosmology - Predictive Models"),
        ("case_studies/core/reasoning", "Reasoning - Natural Language"),
        ("case_studies/core/tests", "Tests as Proofs"),
        ("case_studies/core/compression", "Compression Solver"),
        ("case_studies/core/emergent", "Emergent Behaviors"),
        ("case_studies/core/learn", "Fun Learning Curve"),
        ("case_studies/core/emit", "Emit to Runtime"),
        ("case_studies/domains/biology", "Biology as Field Equations"),
        ("case_studies/domains/ml", "Machine Learning as Compositional Fields"),
        ("case_studies/domains/protocols", "Internet Protocols as Value Fields"),
        ("case_studies/domains/medicine", "Medicine & Healthcare as Field Coherence"),
    ]
    
    for dir_path, title in case_study_dirs:
        readme_path = BASE_DIR / dir_path / "README.md"
        if not readme_path.exists():
            with open(readme_path, "w") as f:
                f.write(f"# {title}\n\n")
                f.write("See `case_studies.md` for full documentation.\n")
            print(f"  Created: {readme_path.relative_to(BASE_DIR)}")


def main():
    """Main organization function."""
    print("=" * 70)
    print("OPIC Case Studies Organization")
    print("=" * 70)
    
    # Step 1: Create directories
    create_directories()
    
    # Step 2: Copy core pattern files
    all_copied = []
    all_missing = []
    
    for category, mappings in CORE_PATTERNS.items():
        copied, missing = copy_files(mappings, category)
        all_copied.extend(copied)
        all_missing.extend(missing)
    
    # Step 3: Copy domain lens files
    for category, mappings in DOMAIN_LENSES.items():
        copied, missing = copy_files(mappings, category)
        all_copied.extend(copied)
        all_missing.extend(missing)
    
    # Step 4: Create README files
    create_readme_files()
    
    # Step 5: Archive files (dry run)
    archive_files(dry_run=True)
    
    # Summary
    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)
    print(f"✓ Copied {len(all_copied)} files")
    if all_missing:
        print(f"✗ Missing {len(all_missing)} files:")
        for missing in all_missing[:10]:
            print(f"    - {missing}")
        if len(all_missing) > 10:
            print(f"    ... and {len(all_missing) - 10} more")
    
    print("\n⚠️  This was a DRY RUN for archiving.")
    print("   Review the output above, then run with --execute to actually archive files.")
    print("\nNext steps:")
    print("  1. Review copied files")
    print("  2. Fix any missing file paths")
    print("  3. Run: python scripts/organize_case_studies.py --execute")


if __name__ == "__main__":
    import sys
    
    if "--execute" in sys.argv:
        print("⚠️  EXECUTING ACTUAL FILE MOVES")
        print("   This will move files to archive. Press Ctrl+C to cancel...")
        import time
        time.sleep(3)
        
        # Re-run with actual archiving
        create_directories()
        
        all_copied = []
        all_missing = []
        
        for category, mappings in CORE_PATTERNS.items():
            copied, missing = copy_files(mappings, category)
            all_copied.extend(copied)
            all_missing.extend(missing)
        
        for category, mappings in DOMAIN_LENSES.items():
            copied, missing = copy_files(mappings, category)
            all_copied.extend(copied)
            all_missing.extend(missing)
        
        create_readme_files()
        archive_files(dry_run=False)
        
        print("\n✓ Organization complete!")
    else:
        main()

