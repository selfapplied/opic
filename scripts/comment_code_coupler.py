#!/usr/bin/env python3
"""
Comment-Code Coupler — Couple comments with neighboring code for learning
Comments describe code → learn from comment-code pairs
"""

import re
import ast
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import json

sys.path.insert(0, str(Path(__file__).parent))
from opic_executor import OpicExecutor

class CommentCodeCoupler:
    """
    Couple comments with neighboring code for learning.
    Comments describe what code does → learn from comment-code pairs.
    """
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.opic = OpicExecutor(project_root)
        self.comment_code_pairs = []
        
    def extract_comments_from_file(self, file_path: Path) -> List[Dict]:
        """
        Extract comments and their neighboring code from a file.
        
        Args:
            file_path: Path to code file
        
        Returns:
            List of comment-code pairs
        """
        if not file_path.exists():
            return []
        
        try:
            content = file_path.read_text()
        except:
            return []
        
        pairs = []
        
        # Python files: extract docstrings and comments
        if file_path.suffix == '.py':
            pairs.extend(self._extract_python_comments(content, file_path))
        
        # OPIC files: extract ;; comments
        elif file_path.suffix == '.ops':
            pairs.extend(self._extract_opic_comments(content, file_path))
        
        # General: extract # comments (works for many languages)
        pairs.extend(self._extract_hash_comments(content, file_path))
        
        return pairs
    
    def _extract_python_comments(self, content: str, file_path: Path) -> List[Dict]:
        """Extract Python docstrings and comments"""
        pairs = []
        
        try:
            tree = ast.parse(content)
            
            # Extract docstrings
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
                    docstring = ast.get_docstring(node)
                    if docstring:
                        # Get code context
                        code_lines = content.split('\n')
                        if hasattr(node, 'lineno'):
                            start_line = node.lineno - 1
                            end_line = node.end_lineno if hasattr(node, 'end_lineno') else start_line + 10
                            code_context = '\n'.join(code_lines[start_line:end_line])
                            
                            pairs.append({
                                "comment": docstring,
                                "code": code_context,
                                "type": "docstring",
                                "file": str(file_path),
                                "line": node.lineno
                            })
        except:
            pass
        
        return pairs
    
    def _extract_opic_comments(self, content: str, file_path: Path) -> List[Dict]:
        """Extract OPIC ;; comments"""
        pairs = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            # OPIC comments start with ;;
            if ';;' in line:
                comment = line.split(';;', 1)[1].strip()
                if comment:
                    # Get neighboring code (next few lines)
                    code_context = '\n'.join(lines[max(0, i-2):min(len(lines), i+5)])
                    
                    pairs.append({
                        "comment": comment,
                        "code": code_context,
                        "type": "inline",
                        "file": str(file_path),
                        "line": i + 1
                    })
        
        return pairs
    
    def _extract_hash_comments(self, content: str, file_path: Path) -> List[Dict]:
        """Extract # comments (works for many languages)"""
        pairs = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            # Comments start with #
            if '#' in line and not line.strip().startswith('#'):
                # Inline comment
                parts = line.split('#', 1)
                if len(parts) == 2:
                    code_part = parts[0].strip()
                    comment = parts[1].strip()
                    
                    if comment and code_part:
                        pairs.append({
                            "comment": comment,
                            "code": code_part,
                            "type": "inline",
                            "file": str(file_path),
                            "line": i + 1
                        })
            elif line.strip().startswith('#'):
                # Block comment
                comment = line.strip('#').strip()
                if comment:
                    # Get neighboring code
                    code_context = '\n'.join(lines[max(0, i-3):min(len(lines), i+3)])
                    
                    pairs.append({
                        "comment": comment,
                        "code": code_context,
                        "type": "block",
                        "file": str(file_path),
                        "line": i + 1
                    })
        
        return pairs
    
    def compute_field_properties(self, comment_code_pair: Dict) -> Dict:
        """
        Compute field properties for comment-code pair.
        
        Args:
            comment_code_pair: Comment-code pair dict
        
        Returns:
            Pair with field properties
        """
        comment = comment_code_pair.get("comment", "")
        code = comment_code_pair.get("code", "")
        
        # Map comment to field
        comment_field = self.opic._call_primitive("aperture.chain", {"text": comment})
        comment_aperture = comment_field.get("aperture", {})
        comment_phi_k = comment_aperture.get("discourse", {}).get("phi_k", 0.0)
        
        # Map code to field
        code_field = self.opic._call_primitive("aperture.chain", {"text": code})
        code_aperture = code_field.get("aperture", {})
        code_phi_k = code_aperture.get("discourse", {}).get("phi_k", 0.0)
        
        # Construct spectra
        comment_spectrum = []
        for word in comment_aperture.get("words", []):
            if isinstance(word, dict) and word.get("phi_k"):
                comment_spectrum.append(float(word["phi_k"]))
        if comment_phi_k:
            comment_spectrum.append(float(comment_phi_k))
        
        code_spectrum = []
        for word in code_aperture.get("words", []):
            if isinstance(word, dict) and word.get("phi_k"):
                code_spectrum.append(float(word["phi_k"]))
        if code_phi_k:
            code_spectrum.append(float(code_phi_k))
        
        # Compute zeros
        comment_zeros = []
        if comment_spectrum:
            comment_zeros = self.opic._call_primitive("zeta.zero.solver", {
                "phi_k": comment_spectrum,
                "region": {"min": 0.0, "max": 10.0},
                "tolerance": 0.01
            })
        
        code_zeros = []
        if code_spectrum:
            code_zeros = self.opic._call_primitive("zeta.zero.solver", {
                "phi_k": code_spectrum,
                "region": {"min": 0.0, "max": 10.0},
                "tolerance": 0.01
            })
        
        # Compute alignment (field distance)
        field_distance = abs(comment_phi_k - code_phi_k)
        scale = max(abs(comment_phi_k), abs(code_phi_k), 1.0)
        alignment = 1.0 / (1.0 + field_distance / scale)
        
        # Compute coherence (how well comment describes code)
        coherence = alignment
        
        return {
            **comment_code_pair,
            "comment_field": {
                "phi_k": comment_phi_k,
                "spectrum": comment_spectrum,
                "zeros": comment_zeros
            },
            "code_field": {
                "phi_k": code_phi_k,
                "spectrum": code_spectrum,
                "zeros": code_zeros
            },
            "alignment": alignment,
            "coherence": coherence
        }
    
    def learn_from_pairs(self, pairs: List[Dict]) -> Dict:
        """
        Learn from comment-code pairs.
        
        Args:
            pairs: List of comment-code pairs with field properties
        
        Returns:
            Learning analysis
        """
        if not pairs:
            return {}
        
        # Filter high-coherence pairs (good comment-code alignment)
        threshold = 0.5
        coherent_pairs = [p for p in pairs if p.get("coherence", 0.0) > threshold]
        
        # Analyze patterns
        avg_coherence = sum(p.get("coherence", 0.0) for p in pairs) / len(pairs) if pairs else 0.0
        avg_alignment = sum(p.get("alignment", 0.0) for p in pairs) / len(pairs) if pairs else 0.0
        
        # Extract successful patterns
        successful_patterns = {
            "high_coherence_pairs": len(coherent_pairs),
            "avg_coherence": avg_coherence,
            "avg_alignment": avg_alignment,
            "comment_types": {}
        }
        
        # Group by comment type
        for pair in pairs:
            comment_type = pair.get("type", "unknown")
            if comment_type not in successful_patterns["comment_types"]:
                successful_patterns["comment_types"][comment_type] = {
                    "count": 0,
                    "avg_coherence": 0.0
                }
            successful_patterns["comment_types"][comment_type]["count"] += 1
        
        return {
            "total_pairs": len(pairs),
            "coherent_pairs": len(coherent_pairs),
            "coherence_rate": len(coherent_pairs) / len(pairs) if pairs else 0.0,
            "successful_patterns": successful_patterns
        }
    
    def process_codebase(self, directory: Path) -> List[Dict]:
        """
        Process entire codebase to extract comment-code pairs.
        
        Args:
            directory: Root directory to process
        
        Returns:
            List of comment-code pairs with field properties
        """
        pairs = []
        
        # Find code files
        code_extensions = ['.py', '.ops', '.js', '.ts', '.java', '.cpp', '.c', '.h']
        
        for ext in code_extensions:
            for file_path in directory.rglob(f'*{ext}'):
                if 'node_modules' in str(file_path) or '__pycache__' in str(file_path):
                    continue
                
                file_pairs = self.extract_comments_from_file(file_path)
                pairs.extend(file_pairs)
        
        # Compute field properties for each pair
        processed_pairs = []
        for pair in pairs:
            try:
                processed_pair = self.compute_field_properties(pair)
                processed_pairs.append(processed_pair)
            except Exception as e:
                pass  # Skip pairs that fail
        
        return processed_pairs
    
    def save_learning_data(self, pairs: List[Dict], output_file: Path):
        """Save comment-code pairs for learning"""
        # Clean pairs for JSON serialization
        clean_pairs = []
        for pair in pairs:
            clean_pair = {
                "comment": pair.get("comment", ""),
                "code": pair.get("code", "")[:500],  # Limit code length
                "type": pair.get("type", "unknown"),
                "file": pair.get("file", ""),
                "line": pair.get("line", 0),
                "alignment": float(pair.get("alignment", 0.0)),
                "coherence": float(pair.get("coherence", 0.0)),
                "comment_phi_k": float(pair.get("comment_field", {}).get("phi_k", 0.0)),
                "code_phi_k": float(pair.get("code_field", {}).get("phi_k", 0.0))
            }
            clean_pairs.append(clean_pair)
        
        data = {
            "comment_code_pairs": clean_pairs[:1000],  # Limit to 1000 pairs
            "analysis": self.learn_from_pairs(pairs)
        }
        
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✓ Saved {len(clean_pairs)} comment-code pairs to {output_file}")

def main():
    """Test comment-code coupler"""
    project_root = Path(__file__).parent.parent
    coupler = CommentCodeCoupler(project_root)
    
    print("=" * 70)
    print("Comment-Code Coupler")
    print("=" * 70)
    print("\nExtracting comment-code pairs from codebase...")
    
    # Process scripts directory
    scripts_dir = project_root / "scripts"
    pairs = coupler.process_codebase(scripts_dir)
    
    print(f"\n✓ Extracted {len(pairs)} comment-code pairs")
    
    # Learn from pairs
    learning = coupler.learn_from_pairs(pairs)
    print(f"\nLearning Analysis:")
    print(f"  Total pairs: {learning.get('total_pairs', 0)}")
    print(f"  Coherent pairs: {learning.get('coherent_pairs', 0)}")
    print(f"  Coherence rate: {learning.get('coherence_rate', 0.0):.1%}")
    
    # Show examples
    if pairs:
        print(f"\nExample pairs:")
        for i, pair in enumerate(pairs[:3]):
            print(f"\n  Pair {i+1}:")
            print(f"    Comment: {pair.get('comment', '')[:80]}...")
            print(f"    Code: {pair.get('code', '')[:80]}...")
            print(f"    Coherence: {pair.get('coherence', 0.0):.2f}")
    
    # Save learning data
    output_file = project_root / "data" / "comment_code_learning.json"
    output_file.parent.mkdir(exist_ok=True)
    coupler.save_learning_data(pairs, output_file)
    
    print("\n✓ Comment-code coupling complete")
    print("\nThis system learns from coupling comments with neighboring code,")
    print("creating a self-improving understanding of code semantics.")

if __name__ == "__main__":
    main()

