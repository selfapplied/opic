#!/usr/bin/env python3
"""
Ingest BERT Training Data — Large-scale ingestion of BooksCorpus + Wikipedia
Populates ζ-field knowledge base with semantic knowledge from BERT training data
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional
import time

sys.path.insert(0, str(Path(__file__).parent))
from bert_knowledge_ingest import BertKnowledgeIngester

def ingest_wikipedia_dump(wikipedia_file: Path, ingester: BertKnowledgeIngester, max_articles: int = 1000):
    """Ingest Wikipedia dump file"""
    if not wikipedia_file.exists():
        print(f"⚠ Wikipedia file not found: {wikipedia_file}")
        return 0
    
    print(f"Loading Wikipedia dump: {wikipedia_file}")
    
    count = 0
    try:
        # Try JSON Lines format
        with open(wikipedia_file, 'r', encoding='utf-8') as f:
            for line in f:
                if count >= max_articles:
                    break
                
                try:
                    article = json.loads(line)
                    title = article.get('title', '')
                    text = article.get('text', '')
                    
                    if text and len(text) > 50:
                        ingester.ingest_wikipedia_chunk(title, text)
                        count += 1
                        
                        if count % 100 == 0:
                            print(f"  Ingested {count} articles...")
                except json.JSONDecodeError:
                    continue
    except Exception as e:
        print(f"⚠ Error reading Wikipedia file: {e}")
        print("  Expected format: JSON Lines (one JSON object per line)")
    
    return count

def ingest_books_corpus(books_file: Path, ingester: BertKnowledgeIngester, max_chunks: int = 1000):
    """Ingest BooksCorpus text file"""
    if not books_file.exists():
        print(f"⚠ Books file not found: {books_file}")
        return 0
    
    print(f"Loading BooksCorpus: {books_file}")
    
    count = 0
    chunk_size = 500  # Characters per chunk
    
    try:
        with open(books_file, 'r', encoding='utf-8') as f:
            current_chunk = ""
            for line in f:
                if count >= max_chunks:
                    break
                
                current_chunk += line
                
                if len(current_chunk) >= chunk_size:
                    ingester.ingest_book_chunk(current_chunk)
                    count += 1
                    current_chunk = ""
                    
                    if count % 100 == 0:
                        print(f"  Ingested {count} chunks...")
            
            # Process remaining chunk
            if current_chunk and count < max_chunks:
                ingester.ingest_book_chunk(current_chunk)
                count += 1
    except Exception as e:
        print(f"⚠ Error reading books file: {e}")
    
    return count

def main():
    project_root = Path(__file__).parent.parent
    ingester = BertKnowledgeIngester(project_root)
    
    # Try to load existing knowledge base
    knowledge_file = project_root / "data" / "bert_knowledge_base.json"
    if knowledge_file.exists():
        print(f"Loading existing knowledge base...")
        ingester.load_knowledge_base(knowledge_file)
        print(f"  Loaded {len(ingester.knowledge_base)} entries")
    
    print("\n" + "=" * 60)
    print("BERT Training Data Ingestion")
    print("=" * 60)
    print("\nThis script ingests BERT training data (BooksCorpus + Wikipedia)")
    print("into the ζ-field knowledge base.")
    print("\nTo use:")
    print("  1. Download Wikipedia dump (JSON Lines format)")
    print("  2. Download BooksCorpus text file")
    print("  3. Place files in data/ directory")
    print("  4. Run this script")
    print()
    
    # Check for data files
    data_dir = project_root / "data"
    wikipedia_file = data_dir / "wikipedia.jsonl"
    books_file = data_dir / "books.txt"
    
    total_ingested = 0
    
    # Ingest Wikipedia if available
    if wikipedia_file.exists():
        print("=" * 60)
        print("Ingesting Wikipedia")
        print("=" * 60)
        count = ingest_wikipedia_dump(wikipedia_file, ingester, max_articles=1000)
        total_ingested += count
        print(f"✓ Ingested {count} Wikipedia articles")
    else:
        print(f"⚠ Wikipedia file not found: {wikipedia_file}")
        print("  Download from: https://dumps.wikimedia.org/")
        print("  Format: JSON Lines with 'title' and 'text' fields")
    
    # Ingest BooksCorpus if available
    if books_file.exists():
        print("\n" + "=" * 60)
        print("Ingesting BooksCorpus")
        print("=" * 60)
        count = ingest_books_corpus(books_file, ingester, max_chunks=1000)
        total_ingested += count
        print(f"✓ Ingested {count} book chunks")
    else:
        print(f"\n⚠ BooksCorpus file not found: {books_file}")
        print("  Download from: https://yknzhu.wixsite.com/mbweb")
        print("  Format: Plain text, one book per file or concatenated")
    
    # Save knowledge base
    if total_ingested > 0:
        print("\n" + "=" * 60)
        print("Saving Knowledge Base")
        print("=" * 60)
        ingester.save_knowledge_base(knowledge_file)
        print(f"\n✓ Total entries in knowledge base: {len(ingester.knowledge_base)}")
        print(f"✓ Knowledge base saved to: {knowledge_file}")
        print("\nThe knowledge base is now integrated into benchmark answering.")
    else:
        print("\n⚠ No data ingested. Please provide Wikipedia and/or BooksCorpus files.")
        print("\nFor now, using sample knowledge base with 5 entries.")

if __name__ == "__main__":
    main()

