#!/usr/bin/env python3
"""
Execute OPIC Reorganization using OPIC primitives
This uses OPIC's own file operations to reorganize OPIC
"""

from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "scripts"))
sys.path.insert(0, str(project_root / "core"))

# Try new location first, then fallback
try:
    from core.opic_executor import OpicExecutor
except ImportError:
    try:
        from opic_executor import OpicExecutor
    except ImportError:
        import importlib.util
        executor_path = project_root / "core" / "opic_executor.py"
        if not executor_path.exists():
            executor_path = project_root / "scripts" / "opic_executor.py"
        spec = importlib.util.spec_from_file_location("opic_executor", executor_path)
        executor_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(executor_module)
        OpicExecutor = executor_module.OpicExecutor

def main():
    executor = OpicExecutor(project_root)
    
    print("=== OPIC Reorganization ===")
    print("Using OPIC primitives to reorganize OPIC")
    print("")
    
    # Step 1: Create directory structure
    print("Step 1: Creating directory structure...")
    dirs = [
        "core",
        "systems/00_core",
        "systems/01_ce1",
        "systems/02_runtime",
        "systems/03_flow",
        "systems/04_mode7",
        "systems/05_experiments",
        "docs/00_specification",
        "docs/01_theory",
        "docs/02_implementation",
        "docs/03_reference",
        "archive/python_experiments",
    ]
    
    for dir_path in dirs:
        result = executor._call_primitive("dir.create", {"path": dir_path})
        if result and not result.startswith("error"):
            print(f"  ✓ Created {dir_path}")
        elif result and result.startswith("error"):
            print(f"  ⚠ {result}")
    
    print("")
    
    # Step 2: Backup and move core files
    print("Step 2: Migrating core files...")
    core_files = [
        ("scripts/opic_executor.py", "core/opic_executor.py"),
        ("scripts/generate.py", "core/parser.py"),
    ]
    
    for source, dest in core_files:
        source_path = project_root / source
        if source_path.exists():
            # Backup first
            backup = executor._call_primitive("file.backup", {"source": str(source_path)})
            print(f"  ✓ Backed up {source}")
            
            # Move
            result = executor._call_primitive("file.move", {"source": str(source_path), "dest": str(project_root / dest)})
            if result and not result.startswith("error"):
                print(f"  ✓ Moved {source} → {dest}")
            else:
                print(f"  ⚠ {result}")
        else:
            print(f"  ⚠ Source not found: {source}")
    
    print("")
    
    # Step 3: Move core systems
    print("Step 3: Migrating core systems...")
    core_systems = [
        ("systems/opic_field_0.7.ops", "systems/00_core/opic_field_0.7.ops"),
        ("systems/opic_cosmogenesis.ops", "systems/00_core/opic_cosmogenesis.ops"),
        ("systems/opic_phase_flux.ops", "systems/00_core/opic_phase_flux.ops"),
        ("systems/opic_three_fluxes.ops", "systems/00_core/opic_three_fluxes.ops"),
        ("systems/opic_coherence_dance.ops", "systems/00_core/opic_coherence_dance.ops"),
    ]
    
    for source, dest in core_systems:
        source_path = project_root / source
        if source_path.exists():
            result = executor._call_primitive("file.move", {"source": str(source_path), "dest": str(project_root / dest)})
            if result and not result.startswith("error"):
                print(f"  ✓ Moved {source} → {dest}")
            else:
                print(f"  ⚠ {result}")
    
    print("")
    
    # Step 4: Move CE1 systems
    print("Step 4: Migrating CE1 systems...")
    ce1_systems = [
        ("systems/ce1_field_kernel.ops", "systems/01_ce1/ce1_field_kernel.ops"),
        ("systems/ce1_pascal_kernel.ops", "systems/01_ce1/ce1_pascal_kernel.ops"),
        ("systems/ce1_zeta_core.ops", "systems/01_ce1/ce1_zeta_core.ops"),
        ("systems/ce1_ethical_enforcement.ops", "systems/01_ce1/ce1_ethical_enforcement.ops"),
        ("systems/ce1_resonant_attention.ops", "systems/01_ce1/ce1_resonant_attention.ops"),
        ("systems/ce1_implementation_stack.ops", "systems/01_ce1/ce1_implementation_stack.ops"),
    ]
    
    for source, dest in ce1_systems:
        source_path = project_root / source
        if source_path.exists():
            result = executor._call_primitive("file.move", {"source": str(source_path), "dest": str(project_root / dest)})
            if result and not result.startswith("error"):
                print(f"  ✓ Moved {source} → {dest}")
    
    print("")
    
    # Step 5: Move runtime systems
    print("Step 5: Migrating runtime systems...")
    runtime_systems = [
        ("systems/zetacore_runtime.ops", "systems/02_runtime/zetacore_runtime.ops"),
        ("systems/sigmabody_interfaces.ops", "systems/02_runtime/sigmabody_interfaces.ops"),
        ("systems/signetwork_governance.ops", "systems/02_runtime/signetwork_governance.ops"),
    ]
    
    for source, dest in runtime_systems:
        source_path = project_root / source
        if source_path.exists():
            result = executor._call_primitive("file.move", {"source": str(source_path), "dest": str(project_root / dest)})
            if result and not result.startswith("error"):
                print(f"  ✓ Moved {source} → {dest}")
    
    print("")
    
    # Step 6: Move flow systems
    print("Step 6: Migrating flow systems...")
    flow_systems = [
        ("systems/flow3d_core.ops", "systems/03_flow/flow3d_core.ops"),
        ("systems/flow3d_mask.ops", "systems/03_flow/flow3d_mask.ops"),
        ("systems/flow3d_descent.ops", "systems/03_flow/flow3d_descent.ops"),
        ("systems/flow3d_benchmarks.ops", "systems/03_flow/flow3d_benchmarks.ops"),
        ("systems/flow3d_caba.ops", "systems/03_flow/flow3d_caba.ops"),
        ("systems/flow3d_main.ops", "systems/03_flow/flow3d_main.ops"),
    ]
    
    for source, dest in flow_systems:
        source_path = project_root / source
        if source_path.exists():
            result = executor._call_primitive("file.move", {"source": str(source_path), "dest": str(project_root / dest)})
            if result and not result.startswith("error"):
                print(f"  ✓ Moved {source} → {dest}")
    
    print("")
    
    # Step 7: Move Mode 7 systems
    print("Step 7: Migrating Mode 7 systems...")
    mode7_systems = [
        ("systems/opic_mode7_perspective.ops", "systems/04_mode7/opic_mode7_perspective.ops"),
        ("systems/opic_mode7_dashboard.ops", "systems/04_mode7/opic_mode7_dashboard.ops"),
        ("systems/opic_mode7_fusion.ops", "systems/04_mode7/opic_mode7_fusion.ops"),
        ("systems/opic_mode7_features.ops", "systems/04_mode7/opic_mode7_features.ops"),
        ("systems/opic_mode7_harvest.ops", "systems/04_mode7/opic_mode7_harvest.ops"),
        ("systems/opic_mode7_lab.ops", "systems/04_mode7/opic_mode7_lab.ops"),
    ]
    
    for source, dest in mode7_systems:
        source_path = project_root / source
        if source_path.exists():
            result = executor._call_primitive("file.move", {"source": str(source_path), "dest": str(project_root / dest)})
            if result and not result.startswith("error"):
                print(f"  ✓ Moved {source} → {dest}")
    
    print("")
    print("✓ Reorganization complete!")
    print("")
    print("Next steps:")
    print("1. Update include paths in .ops files")
    print("2. Archive Python experiments")
    print("3. Migrate documentation files")

if __name__ == "__main__":
    main()

