#!/usr/bin/env python3
"""Export PyTorch tensors (embeddings) for direct use in opic"""

import json
import numpy as np
from pathlib import Path
import sys

def export_bert_embeddings():
    """Export BERT embeddings as numpy arrays for opic"""
    try:
        from transformers import BertTokenizer, BertModel
        import torch
    except ImportError:
        print("⚠ transformers/torch not available")
        return
    
    project_root = Path(__file__).parent
    data_file = project_root / "voice_training_data.json"
    
    if not data_file.exists():
        print(f"Error: {data_file} not found")
        return
    
    print("Loading training data...")
    with open(data_file) as f:
        training_data = json.load(f)
    
    pairs = training_data.get('pairs', [])
    
    print("Loading BERT model...")
    bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    bert_model = BertModel.from_pretrained('bert-base-uncased')
    bert_model.eval()
    
    print("Computing embeddings...")
    embeddings_data = []
    
    for i, pair in enumerate(pairs):
        train_input = ' '.join(pair.get('input', [])) if isinstance(pair.get('input'), list) else str(pair.get('input', ''))
        train_target_list = pair.get('target', [])
        train_target = ' '.join(train_target_list) if isinstance(train_target_list, list) else str(train_target_list)
        
        if train_input:
            try:
                train_inputs = bert_tokenizer(train_input, return_tensors='pt', padding=True, truncation=True, max_length=128)
                with torch.no_grad():
                    train_outputs = bert_model(**train_inputs)
                    train_embedding = train_outputs.last_hidden_state.mean(dim=1)
                
                # Convert tensor to numpy array
                embedding_np = train_embedding.cpu().numpy().flatten().tolist()
                
                embeddings_data.append({
                    'input': train_input,
                    'target': train_target,
                    'target_tokens': train_target_list if isinstance(train_target_list, list) else train_target.split(),
                    'embedding': embedding_np,
                    'embedding_dim': len(embedding_np)
                })
                
                if (i + 1) % 100 == 0:
                    print(f"  Processed {i + 1}/{len(pairs)} pairs")
            except Exception as e:
                print(f"  Error processing pair {i}: {e}")
                continue
    
    # Save embeddings as JSON (numpy arrays as lists)
    output_file = project_root / "opic_embeddings.json"
    with open(output_file, 'w') as f:
        json.dump({
            'embeddings': embeddings_data,
            'total_points': len(embeddings_data),
            'embedding_dim': embeddings_data[0]['embedding_dim'] if embeddings_data else 768,
            'model': 'bert-base-uncased'
        }, f, indent=2)
    
    print(f"\n✓ Exported {len(embeddings_data)} embeddings to {output_file}")
    print(f"  Embedding dimension: {embeddings_data[0]['embedding_dim'] if embeddings_data else 768}")
    
    # Also save as numpy format for direct loading
    if embeddings_data:
        embeddings_array = np.array([e['embedding'] for e in embeddings_data])
        np_file = project_root / "opic_embeddings.npy"
        np.save(np_file, embeddings_array)
        print(f"✓ Saved numpy array to {np_file}")
        
        # Save metadata separately
        metadata = {
            'inputs': [e['input'] for e in embeddings_data],
            'targets': [e['target'] for e in embeddings_data],
            'target_tokens': [e['target_tokens'] for e in embeddings_data]
        }
        metadata_file = project_root / "opic_embeddings_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"✓ Saved metadata to {metadata_file}")

if __name__ == "__main__":
    export_bert_embeddings()

