#!/usr/bin/env python3
"""
Download BERT Training Data — Download Wikipedia and BooksCorpus
"""

import os
import sys
import subprocess
from pathlib import Path
import urllib.request
import json
from typing import Optional

def download_file(url: str, output_path: Path, description: str) -> bool:
    """Download a file with progress"""
    print(f"\nDownloading {description}...")
    print(f"  URL: {url}")
    print(f"  Output: {output_path}")
    
    try:
        # Use urllib with progress
        def show_progress(block_num, block_size, total_size):
            if total_size > 0:
                percent = min(100, (block_num * block_size * 100) // total_size)
                print(f"\r  Progress: {percent}%", end='', flush=True)
        
        urllib.request.urlretrieve(url, output_path, show_progress)
        print(f"\n✓ Downloaded: {output_path}")
        return True
    except Exception as e:
        print(f"\n⚠ Error downloading: {e}")
        return False

def download_wikipedia_sample():
    """Download a sample Wikipedia dump"""
    data_dir = Path(__file__).parent.parent / "data"
    data_dir.mkdir(exist_ok=True)
    
    output_file = data_dir / "wikipedia_sample.jsonl"
    
    # Use HuggingFace datasets to get Wikipedia sample
    print("=" * 60)
    print("Downloading Wikipedia Sample")
    print("=" * 60)
    print("\nUsing HuggingFace datasets library to get Wikipedia sample...")
    
    try:
        from datasets import load_dataset
        
        print("  Loading Wikipedia dataset from HuggingFace...")
        # Load a small sample (1000 articles)
        dataset = load_dataset("wikipedia", "20220301.en", split="train[:1000]")
        
        print(f"  Writing {len(dataset)} articles to {output_file}...")
        with open(output_file, 'w', encoding='utf-8') as f:
            for article in dataset:
                json.dump({
                    "title": article.get("title", ""),
                    "text": article.get("text", "")
                }, f, ensure_ascii=False)
                f.write('\n')
        
        print(f"✓ Saved {len(dataset)} Wikipedia articles to {output_file}")
        return True
        
    except ImportError:
        print("⚠ HuggingFace datasets not installed.")
        print("  Install with: pip install datasets")
        print("\n  Creating sample Wikipedia data manually...")
        
        # Create sample data
        sample_articles = [
            {
                "title": "Mathematics",
                "text": "Mathematics is the study of numbers, quantities, and shapes. It includes algebra, geometry, calculus, and many other branches. Mathematics is used in science, engineering, and many other fields."
            },
            {
                "title": "Physics",
                "text": "Physics is the natural science that studies matter, motion, and behavior through space and time. It includes mechanics, thermodynamics, quantum mechanics, and many other branches."
            },
            {
                "title": "Biology",
                "text": "Biology is the study of living organisms. It includes cell biology, genetics, evolution, ecology, and many other branches. Biology helps us understand life on Earth."
            },
            {
                "title": "Chemistry",
                "text": "Chemistry is the study of matter and its properties. It includes organic chemistry, inorganic chemistry, physical chemistry, and analytical chemistry."
            },
            {
                "title": "Computer Science",
                "text": "Computer science is the study of computation and information processing. It includes algorithms, data structures, programming languages, and artificial intelligence."
            },
        ]
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for article in sample_articles:
                json.dump(article, f, ensure_ascii=False)
                f.write('\n')
        
        print(f"✓ Created sample Wikipedia file with {len(sample_articles)} articles")
        return True
    except Exception as e:
        print(f"⚠ Error: {e}")
        return False

def download_books_corpus_sample():
    """Download or create BooksCorpus sample"""
    data_dir = Path(__file__).parent.parent / "data"
    data_dir.mkdir(exist_ok=True)
    
    output_file = data_dir / "books_sample.txt"
    
    print("\n" + "=" * 60)
    print("Creating BooksCorpus Sample")
    print("=" * 60)
    
    # Create sample book text
    sample_text = """
The Art of War by Sun Tzu

War is a matter of vital importance to the state. It is a matter of life and death, a road either to safety or to ruin. Hence it is a subject of inquiry which can on no account be neglected.

The art of war is governed by five constant factors. These are: the Moral Law, Heaven, Earth, the Commander, and Method and Discipline.

The Moral Law causes the people to be in complete accord with their ruler, so that they will follow him regardless of their lives.

Heaven signifies night and day, cold and heat, times and seasons.

Earth comprises distances, great and small; danger and security; open ground and narrow passes; the chances of life and death.

The Commander stands for the virtues of wisdom, sincerity, benevolence, courage, and strictness.

Method and Discipline are to be understood as the marshaling of the army in its proper subdivisions, the graduations of rank among the officers, the maintenance of roads by which supplies may reach the army, and the control of military expenditure.

These five heads should be familiar to every general. He who knows them will be victorious; he who knows them not will fail.

The Prince by Niccolò Machiavelli

It is better to be feared than loved, if you cannot be both. For men have less scruple in offending one who is beloved than one who is feared, for love is preserved by the link of obligation which, owing to the baseness of men, is broken at every opportunity for their advantage; but fear preserves you by a dread of punishment which never fails.

A prince should show himself a lover of merit, give preferment to the able, and honor those who excel in every art. He should encourage his citizens to practice their callings peaceably, both in commerce and agriculture, and in every other following, so that the one should not be deterred from improving his possessions for fear they should be taken away from him, and another from opening up trade for fear of taxes.

The prince who has more to fear from the people than from foreigners ought to build fortresses, but he who has more to fear from foreigners than from the people ought to leave them alone.

The Republic by Plato

Justice is giving each man his due. The just man is the one who does his own work and does not meddle with what is not his own.

The state is the individual writ large. As the individual has three parts—reason, spirit, and appetite—so the state has three classes—rulers, auxiliaries, and producers.

The philosopher-king is the ideal ruler, one who has knowledge of the Good and uses it to govern justly.

Education is the process of turning the soul toward the light, away from the shadows of the cave.

The unexamined life is not worth living. Philosophy begins in wonder.
""".strip()
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(sample_text)
    
    print(f"✓ Created sample BooksCorpus file: {output_file}")
    print(f"  Size: {len(sample_text)} characters")
    return True

def download_full_wikipedia():
    """Instructions for downloading full Wikipedia"""
    print("\n" + "=" * 60)
    print("Full Wikipedia Download Instructions")
    print("=" * 60)
    print("""
To download the full Wikipedia dump:

1. Visit: https://dumps.wikimedia.org/enwiki/latest/
2. Download: enwiki-latest-pages-articles.xml.bz2
3. Convert to JSON Lines format using wikiextractor:
   
   pip install wikiextractor
   wikiextractor enwiki-latest-pages-articles.xml.bz2 --json
   
4. The output will be in text/ directory
5. Concatenate JSON files:
   
   cat text/*/wiki_* > data/wikipedia.jsonl

Alternatively, use HuggingFace datasets:

  from datasets import load_dataset
  dataset = load_dataset("wikipedia", "20220301.en", split="train")
  # Save to JSON Lines format
""")

def download_full_books_corpus():
    """Instructions for downloading full BooksCorpus"""
    print("\n" + "=" * 60)
    print("Full BooksCorpus Download Instructions")
    print("=" * 60)
    print("""
To download the full BooksCorpus:

1. Visit: https://yknzhu.wixsite.com/mbweb
2. Request access to BooksCorpus dataset
3. Download the text files
4. Concatenate all book files:
   
   cat book*.txt > data/books.txt

Note: BooksCorpus access may require approval.
For research purposes, you can also use:
- Project Gutenberg texts
- Open Library texts
- Other public domain book collections
""")

def main():
    project_root = Path(__file__).parent.parent
    data_dir = project_root / "data"
    data_dir.mkdir(exist_ok=True)
    
    print("=" * 60)
    print("BERT Training Data Download")
    print("=" * 60)
    print("\nThis script downloads sample BERT training data.")
    print("For full datasets, see instructions below.\n")
    
    # Download samples
    wikipedia_ok = download_wikipedia_sample()
    books_ok = download_books_corpus_sample()
    
    if wikipedia_ok and books_ok:
        print("\n" + "=" * 60)
        print("✓ Sample Data Ready")
        print("=" * 60)
        print("\nSample files created:")
        print(f"  - {data_dir / 'wikipedia_sample.jsonl'}")
        print(f"  - {data_dir / 'books_sample.txt'}")
        print("\nYou can now run:")
        print("  python3 scripts/ingest_bert_data.py")
        print("\nOr rename files to:")
        print("  - data/wikipedia.jsonl")
        print("  - data/books.txt")
        print("  for full ingestion")
    
    # Show instructions for full downloads
    download_full_wikipedia()
    download_full_books_corpus()
    
    print("\n" + "=" * 60)
    print("Next Steps")
    print("=" * 60)
    print("""
1. For quick start: Use the sample files created above
2. For better results: Download full Wikipedia dump
3. For best results: Download full BooksCorpus + Wikipedia
4. Run ingestion: python3 scripts/ingest_bert_data.py
5. Run benchmarks: python3 scripts/benchmark_eval_real.py
""")

if __name__ == "__main__":
    main()

