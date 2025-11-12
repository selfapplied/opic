#!/usr/bin/env python3
"""
OPIC Reorganization Script
Moves files into systematic structure, archives Python experiments
"""

from pathlib import Path
import shutil
import json
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent

# New structure
NEW_STRUCTURE = {
    "core/": [
        "scripts/opic_executor.py",
        "scripts/generate.py",  # parser
    ],
    "systems/00_core/": [
        "systems/opic_field_0.7.ops",
        "systems/opic_cosmogenesis.ops",
        "systems/opic_phase_flux.ops",
        "systems/opic_three_fluxes.ops",
        "systems/opic_coherence_dance.ops",
    ],
    "systems/01_ce1/": [
        "systems/ce1_*.ops",
    ],
    "systems/02_runtime/": [
        "systems/zetacore_runtime.ops",
        "systems/sigmabody_interfaces.ops",
        "systems/signetwork_governance.ops",
    ],
    "systems/03_flow/": [
        "systems/flow3d_*.ops",
        "systems/ns_3d_flow*.ops",
    ],
    "systems/04_mode7/": [
        "systems/opic_mode7_*.ops",
    ],
    "systems/05_experiments/": [
        "systems/ops_*.ops",
    ],
    "docs/00_specification/": [
        "docs/ce1_*.md",
        "docs/zetacore_*.md",
        "docs/sigma*.md",
        "docs/opic_*.md",
        "docs/collective_*.md",
        "docs/metafield_*.md",
        "docs/mathematical_*.md",
        "docs/philosophical_*.md",
        "docs/meta_reflection_*.md",
        "docs/opic_complete_specification_index.md",
        "docs/opic_final_synthesis.md",
    ],
    "docs/01_theory/": [
        "docs/opic_cosmogenesis.md",
        "docs/mathematical_proof_annex.md",
        "docs/philosophical_synthesis.md",
        "docs/opic_phase_flux_insight.md",
    ],
    "docs/02_implementation/": [
        "docs/opic_engineering_spec.md",
        "docs/developer_experiments_handbook.md",
        "docs/reorganization_plan.md",
    ],
    "archive/python_experiments/": [
        "scripts/*_experiment.py",
        "scripts/*_test.py",
        "scripts/*_mapper.py",
        "scripts/*_benchmark.py",
        "scripts/*_visualization.py",
    ],
}

def find_files(pattern: str, base: Path) -> list:
    """Find files matching pattern"""
    if "*" in pattern:
        # Glob pattern
        return list(base.glob(pattern))
    else:
        # Exact file
        path = base / pattern
        return [path] if path.exists() else []

def create_structure():
    """Create new directory structure"""
    for dir_path in NEW_STRUCTURE.keys():
        full_path = PROJECT_ROOT / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created {dir_path}")

def move_files():
    """Move files to new locations"""
    moved = []
    skipped = []
    
    for dest_dir, patterns in NEW_STRUCTURE.items():
        dest_path = PROJECT_ROOT / dest_dir
        
        for pattern in patterns:
            files = find_files(pattern, PROJECT_ROOT)
            
            for src_file in files:
                if not src_file.exists():
                    skipped.append((pattern, "not found"))
                    continue
                
                # Skip if already in destination
                if dest_path in src_file.parents:
                    skipped.append((src_file, "already in destination"))
                    continue
                
                dest_file = dest_path / src_file.name
                
                # Handle conflicts
                if dest_file.exists():
                    # Add parent directory name to avoid conflicts
                    dest_file = dest_path / f"{src_file.parent.name}_{src_file.name}"
                
                try:
                    shutil.move(str(src_file), str(dest_file))
                    moved.append((src_file, dest_file))
                    print(f"✓ Moved {src_file.relative_to(PROJECT_ROOT)} → {dest_file.relative_to(PROJECT_ROOT)}")
                except Exception as e:
                    skipped.append((src_file, str(e)))
    
    return moved, skipped

def generate_report(moved, skipped):
    """Generate migration report"""
    report = {
        "timestamp": datetime.now().isoformat(),
        "moved": len(moved),
        "skipped": len(skipped),
        "files_moved": [str(dest.relative_to(PROJECT_ROOT)) for src, dest in moved],
        "files_skipped": [str(f) for f, reason in skipped],
    }
    
    report_path = PROJECT_ROOT / "docs" / "reorganization_report.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n✓ Report saved to {report_path.relative_to(PROJECT_ROOT)}")
    print(f"  Moved: {len(moved)} files")
    print(f"  Skipped: {len(skipped)} files")

def main():
    """Main reorganization"""
    print("OPIC Reorganization")
    print("=" * 50)
    
    # Create structure
    print("\n1. Creating directory structure...")
    create_structure()
    
    # Move files
    print("\n2. Moving files...")
    moved, skipped = move_files()
    
    # Generate report
    print("\n3. Generating report...")
    generate_report(moved, skipped)
    
    print("\n" + "=" * 50)
    print("Reorganization complete!")
    print("\nNext steps:")
    print("1. Review moved files")
    print("2. Update includes in .ops files")
    print("3. Update Makefile paths")
    print("4. Test system")

if __name__ == "__main__":
    main()

