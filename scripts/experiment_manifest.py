#!/usr/bin/env python3
"""
Experiment Manifest Generator
Freeze manifest.json per experiment: code commit, config, seeds, hashes, wall-clock time
"""

import json
import hashlib
import subprocess
import time
import platform
from pathlib import Path
from typing import Dict, Any

def get_git_commit() -> str:
    """Get current git commit hash"""
    try:
        result = subprocess.run(['git', 'rev-parse', 'HEAD'], 
                              capture_output=True, text=True, cwd=Path.cwd())
        return result.stdout.strip()
    except:
        return "unknown"

def compute_file_hash(file_path: Path) -> str:
    """Compute SHA-256 hash of file"""
    if not file_path.exists():
        return "missing"
    with open(file_path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def generate_manifest(experiment_name: str, config: Dict, seeds: List[int], 
                     input_files: List[str], output_files: List[str]) -> Dict:
    """Generate experiment manifest"""
    
    manifest = {
        "experiment": experiment_name,
        "timestamp": time.time(),
        "iso_timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "git_commit": get_git_commit(),
        "hardware": {
            "platform": platform.platform(),
            "processor": platform.processor(),
            "machine": platform.machine()
        },
        "config": config,
        "seeds": seeds,
        "input_files": {},
        "output_files": {},
        "wall_clock_time": None  # Set after experiment
    }
    
    # Hash input files
    for file_path in input_files:
        path = Path(file_path)
        manifest["input_files"][str(path)] = compute_file_hash(path)
    
    # Hash output files (after creation)
    for file_path in output_files:
        path = Path(file_path)
        if path.exists():
            manifest["output_files"][str(path)] = compute_file_hash(path)
    
    return manifest

def save_manifest(manifest: Dict, output_path: Path):
    """Save manifest to file"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(manifest, f, indent=2)

def main():
    """Example usage"""
    manifest = generate_manifest(
        experiment_name="fingerprint_persistence_ab",
        config={"N": 64, "primorial": 2310, "n_steps": 100},
        seeds=[42, 123, 456, 789, 1000],
        input_files=["systems/flow3d_core.ops", "systems/flow3d_mask.ops"],
        output_files=["results/fingerprint_persistence_ab.json"]
    )
    
    output_path = Path('results/manifests/fingerprint_persistence_ab_manifest.json')
    save_manifest(manifest, output_path)
    print(f"✓ Manifest saved to {output_path}")

if __name__ == "__main__":
    main()

