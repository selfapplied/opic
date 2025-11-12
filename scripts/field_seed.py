#!/usr/bin/env python3
"""
Emit JSONL trace: {file, line, phi_entropy, phi_curvature, boundary_score}
Uses opic voices: corpus.read -> corpus.project -> trace output
Deterministic; ignores whitespace-only lines.
"""
import sys
import os
import json
from pathlib import Path
from collections import Counter
import math

# Import opic executor to use voices
sys.path.insert(0, str(Path(__file__).parent.parent))
from scripts.opic_executor import OpicExecutor

def shannon_entropy(s: str) -> float:
    if not s:
        return 0.0
    counts = Counter(s)
    n = len(s)
    ent = 0.0
    for c in counts.values():
        p = c / n
        ent -= p * math.log2(p)
    return ent

def curvature(line: str) -> float:
    # Use ordinal second-difference magnitude average
    xs = [ord(c) for c in line]
    if len(xs) < 3:
        return 0.0
    acc = 0.0
    cnt = 0
    for i in range(1, len(xs) - 1):
        sec = xs[i + 1] - 2 * xs[i] + xs[i - 1]
        acc += abs(sec)
        cnt += 1
    return acc / max(cnt, 1)

def boundary(prev_entropy: float, this_entropy: float, prev_score: float) -> float:
    # Smooth absolute entropy delta
    delta = abs(this_entropy - prev_entropy)
    # EWMA with alpha=0.3
    alpha = 0.3
    return (1 - alpha) * prev_score + alpha * delta

def iter_files(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip hidden and build/venv/node_modules
        if any(part.startswith('.') for part in Path(dirpath).parts):
            continue
        if any(seg in dirpath for seg in ("/.git", "/build", "/dist", "/node_modules", "/__pycache__")):
            continue
        for fn in filenames:
            p = Path(dirpath) / fn
            # Skip binaries
            try:
                text = p.read_text(encoding='utf-8', errors='ignore')
            except Exception:
                continue
            yield p, text

def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    out = sys.stdout
    
    # Try to use opic voices first
    executor = OpicExecutor(root)
    
    if "corpus.read" in executor.voices and "corpus.project" in executor.voices:
        # Use opic-native execution via voices
        files = []
        for p, text in iter_files(root):
            files.append({"path": str(p), "content": text})
        
        # Execute corpus.read -> corpus.project chain
        read_result = executor.execute_voice("corpus.read", {"path": root})
        if read_result:
            # Execute corpus.project with lines
            lines = []
            for p, text in iter_files(root):
                for idx, line in enumerate(text.splitlines(), start=1):
                    if line.strip():
                        lines.append({"file": str(p), "line": idx, "content": line})
            
            project_result = executor.execute_voice("corpus.project", {"lines": lines})
            if project_result and isinstance(project_result, list):
                # Voice returned traces directly
                for trace in project_result:
                    out.write(json.dumps(trace, ensure_ascii=False) + "\n")
                return
            elif project_result and isinstance(project_result, str):
                # Voice returned JSONL string
                for line in project_result.split('\n'):
                    if line.strip():
                        out.write(line + "\n")
                return
    
    # Fallback: direct Python computation (matches opic voice semantics)
    prev_ent_for_file = {}
    prev_bnd_for_file = {}

    for p, text in iter_files(root):
        prev_ent = 0.0
        prev_bnd = 0.0
        for idx, raw in enumerate(text.splitlines(), start=1):
            line = raw.rstrip("\n")
            if not line.strip():
                continue
            e = shannon_entropy(line)
            k = curvature(line)
            b = boundary(prev_ent, e, prev_bnd)
            obj = {
                "file": str(p),
                "line": idx,
                "phi_entropy": round(e, 6),
                "phi_curvature": round(k, 6),
                "boundary_score": round(b, 6),
            }
            out.write(json.dumps(obj, ensure_ascii=False) + "\n")
            prev_ent = e
            prev_bnd = b

if __name__ == "__main__":
    main()


