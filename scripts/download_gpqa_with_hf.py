#!/usr/bin/env python3
"""
Download GPQA using hf CLI authentication
"""

import subprocess
import json
import sys
from pathlib import Path

def main():
    print("=" * 60)
    print("Downloading GPQA Dataset")
    print("=" * 60)
    print()
    
    # Check authentication
    print("Checking authentication...")
    result = subprocess.run(["hf", "auth", "whoami"], capture_output=True, text=True)
    if result.returncode != 0:
        print("⚠ Not authenticated. Run: hf auth login")
        return
    
    username = result.stdout.strip().split(":")[-1].strip() if ":" in result.stdout else result.stdout.strip()
    print(f"✓ Authenticated as: {username}")
    print()
    
    print("Note: If you get 403 errors, you may need to:")
    print("  1. Visit https://huggingface.co/settings/tokens")
    print("  2. Edit your token")
    print("  3. Enable 'Read access to public gated repositories'")
    print()
    
    # Try to download using hf
    print("Attempting to download GPQA...")
    data_dir = Path("data/benchmarks")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Try using hf download
    result = subprocess.run([
        "hf", "download", 
        "Idavidrein/gpqa",
        "--repo-type", "dataset",
        "--local-dir", str(data_dir / "gpqa_raw")
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✓ Downloaded GPQA files")
        print("  Processing files...")
        # Process the downloaded files
        # (implementation depends on file format)
    else:
        print("⚠ Download failed:")
        print(result.stderr)
        print()
        print("Alternative: Use Python datasets library:")
        print("  pip3 install datasets")
        print("  python3 -c \"from datasets import load_dataset; ds = load_dataset('Idavidrein/gpqa'); print(ds)\"")

if __name__ == "__main__":
    main()

