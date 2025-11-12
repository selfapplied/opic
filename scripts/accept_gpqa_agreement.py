#!/usr/bin/env python3
"""
Accept GPQA dataset agreement and download
"""

import sys
from pathlib import Path

def main():
    print("=" * 60)
    print("GPQA Dataset Agreement Acceptance")
    print("=" * 60)
    print()
    print("GPQA is a gated dataset that requires:")
    print("  1. Accepting the dataset agreement on HuggingFace")
    print("  2. Authenticating with your HuggingFace account")
    print()
    print("Steps:")
    print("  1. Visit: https://huggingface.co/datasets/Idavidrein/gpqa")
    print("  2. Click 'Agree and access repository'")
    print("  3. Log in or create a HuggingFace account if needed")
    print("  4. Accept the terms")
    print()
    print("Then authenticate from command line:")
    print("  huggingface-cli login")
    print()
    print("Or use Python:")
    print("  python3 -c \"from huggingface_hub import login; login()\"")
    print()
    
    # Try to check if already logged in
    try:
        from huggingface_hub import whoami
        user = whoami()
        print(f"✓ Already authenticated as: {user.get('name', 'Unknown')}")
        print()
        print("Attempting to download GPQA...")
        
        from datasets import load_dataset
        try:
            dataset = load_dataset("Idavidrein/gpqa")
            print("✓ Successfully loaded GPQA dataset!")
            
            # Save it
            project_root = Path(__file__).parent.parent
            data_dir = project_root / "data" / "benchmarks"
            data_dir.mkdir(parents=True, exist_ok=True)
            
            gpqa_data = []
            # Handle DatasetDict
            if hasattr(dataset, 'keys'):
                for split_name in dataset.keys():
                    split_data = dataset[split_name]
                    for item in split_data:
                        question = item.get("question", item.get("Question", item.get("text", "")))
                        choices = item.get("choices", item.get("Choices", item.get("options", [])))
                        answer = item.get("answer", item.get("Answer", item.get("correct_answer", 0)))
                        
                        if isinstance(answer, str) and answer.isalpha():
                            answer = ord(answer.upper()) - ord('A')
                        elif isinstance(answer, str) and answer.isdigit():
                            answer = int(answer)
                        
                        gpqa_data.append({
                            "question": question,
                            "choices": choices if isinstance(choices, list) else list(choices.values()) if isinstance(choices, dict) else [],
                            "answer": answer if isinstance(answer, int) else 0
                        })
            else:
                for item in dataset:
                    question = item.get("question", item.get("Question", item.get("text", "")))
                    choices = item.get("choices", item.get("Choices", item.get("options", [])))
                    answer = item.get("answer", item.get("Answer", item.get("correct_answer", 0)))
                    
                    if isinstance(answer, str) and answer.isalpha():
                        answer = ord(answer.upper()) - ord('A')
                    elif isinstance(answer, str) and answer.isdigit():
                        answer = int(answer)
                    
                    gpqa_data.append({
                        "question": question,
                        "choices": choices if isinstance(choices, list) else list(choices.values()) if isinstance(choices, dict) else [],
                        "answer": answer if isinstance(answer, int) else 0
                    })
            
            gpqa_file = data_dir / "gpqa.json"
            import json
            with open(gpqa_file, 'w') as f:
                json.dump(gpqa_data, f, indent=2)
            
            print(f"✓ Saved {len(gpqa_data)} GPQA questions to {gpqa_file}")
            
        except Exception as e:
            print(f"⚠ Error loading dataset: {e}")
            print("  Make sure you've accepted the agreement at:")
            print("  https://huggingface.co/datasets/Idavidrein/gpqa")
            
    except Exception as e:
        print("⚠ Not authenticated or error checking authentication")
        print(f"  Error: {e}")
        print()
        print("To authenticate, run:")
        print("  huggingface-cli login")
        print()
        print("Or visit: https://huggingface.co/datasets/Idavidrein/gpqa")
        print("and accept the agreement, then authenticate.")

if __name__ == "__main__":
    main()

