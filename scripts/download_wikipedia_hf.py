#!/usr/bin/env python3
"""
Download Wikipedia using HuggingFace datasets
"""

import json
import sys
from pathlib import Path

def download_wikipedia_hf(num_articles: int = 10000):
    """Download Wikipedia articles using HuggingFace"""
    try:
        from datasets import load_dataset
    except ImportError:
        print("⚠ HuggingFace datasets not installed.")
        print("  Install with: pip3 install --user datasets")
        print("  Or use: python3 -m pip install --user datasets")
        print("\n  Using sample data instead...")
        return False
    
    data_dir = Path(__file__).parent.parent / "data"
    data_dir.mkdir(exist_ok=True)
    
    output_file = data_dir / "wikipedia.jsonl"
    
    print("=" * 60)
    print(f"Downloading {num_articles} Wikipedia Articles")
    print("=" * 60)
    print("\nThis may take a few minutes...")
    
    try:
        # Load Wikipedia dataset
        print("  Loading Wikipedia dataset from HuggingFace...")
        dataset = load_dataset("wikipedia", "20220301.en", split=f"train[:{num_articles}]")
        
        print(f"  Writing {len(dataset)} articles to {output_file}...")
        count = 0
        with open(output_file, 'w', encoding='utf-8') as f:
            for article in dataset:
                # Only include articles with substantial text
                text = article.get("text", "")
                if len(text) > 100:  # At least 100 characters
                    json.dump({
                        "title": article.get("title", ""),
                        "text": text
                    }, f, ensure_ascii=False)
                    f.write('\n')
                    count += 1
                    
                    if count % 1000 == 0:
                        print(f"    Written {count} articles...")
        
        print(f"\n✓ Saved {count} Wikipedia articles to {output_file}")
        print(f"  File size: {output_file.stat().st_size / 1024 / 1024:.1f} MB")
        return True
        
    except Exception as e:
        print(f"\n⚠ Error: {e}")
        print("\nFalling back to sample data...")
        return False

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--num", type=int, default=10000, help="Number of articles to download")
    args = parser.parse_args()
    
    download_wikipedia_hf(args.num)

