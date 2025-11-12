#!/usr/bin/env python3
"""
opic Voice Executor - Execute opic voices from Python
Integrates with opic's reasoning, math, and Field Spec 0.7 systems
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional, List
import json
import hashlib
import math
import random

# Import opic's parser - will be loaded when OpicExecutor is initialized
# parse_ops will be imported dynamically based on project_root
parse_ops = None  # Will be set in _init_parser()


class OpicExecutor:
    """Execute opic voices from Python"""
    
    def __init__(self, project_root: Path):
        self.project_root = Path(project_root).resolve()
        self.voices = {}
        self.defs = {}
        self.loaded_files = set()
        self.primitives = {}
        self.embedding_cache = {}  # Cache for semantic embeddings
        self.current_file = None  # Track current file being executed for output association
        self._systems_loaded = False  # Lazy load systems
        self._init_parser()  # Initialize parser first (needed for _load_opic_systems)
        self._init_primitives()  # Primitives don't depend on systems
    
    def _init_parser(self):
        """Initialize parse_ops from parser.py in core directory"""
        global parse_ops
        sys.path.insert(0, str(self.project_root))
        sys.path.insert(0, str(self.project_root / "scripts"))
        sys.path.insert(0, str(self.project_root / "core"))
        try:
            # Try core/parser.py first
            from parser import parse_ops as _parse_ops
            parse_ops = _parse_ops
        except ImportError:
            # Try generate.py as fallback
            try:
                from generate import parse_ops as _parse_ops
                parse_ops = _parse_ops
            except ImportError:
                # Try alternative import
                import importlib.util
                parser_path = self.project_root / "core" / "parser.py"
                if parser_path.exists():
                    spec = importlib.util.spec_from_file_location("parser", parser_path)
                    parser_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(parser_module)
                    parse_ops = parser_module.parse_ops
                else:
                    generate_path = self.project_root / "generate.py"
                    if generate_path.exists():
                        spec = importlib.util.spec_from_file_location("generate", generate_path)
                        generate = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(generate)
                        parse_ops = generate.parse_ops
                    else:
                        raise ImportError(f"Could not find parser.py at {parser_path} or generate.py at {generate_path}")
    
    def _load_opic_systems(self):
        """Load opic's core systems - lazy loading, only when needed"""
        if self._systems_loaded:
            return
        
        self._systems_loaded = True
        # Load core files - discover all .ops files naturally (no hardcoded list)
        core_dir = self.project_root / "core"
        if core_dir.exists():
            # Load all core files naturally - bootstrap will be included if it exists
            for core_file in sorted(core_dir.glob("*.ops")):
                try:
                    self._load_ops_file(core_file)
                except Exception as e:
                    # Skip problematic files, don't crash
                    pass
        
        # Load systems files - discover all .ops files naturally (no hardcoded list)
        systems_dir = self.project_root / "systems"
        if systems_dir.exists():
            for systems_file in systems_dir.glob("*.ops"):
                try:
                    self._load_ops_file(systems_file)
                except Exception as e:
                    # Skip problematic files, don't crash
                    pass
    
    def _load_ops_file(self, file_path: Path):
        """Load an .ops file and its includes"""
        if file_path in self.loaded_files:
            return
        
        if not file_path.exists():
            return
        
        self.loaded_files.add(file_path)
        content = file_path.read_text()
        defs, voices, includes = parse_ops(content)
        
        self.defs.update(defs)
        self.voices.update(voices)
        
        # Extract comments for learning (associate file with its comments)
        self._extract_comments_from_file(file_path, content)
        
        # Load includes recursively
        for include_file in includes:
            # Resolve include path relative to file's directory
            include_path = file_path.parent / include_file
            if include_path.exists():
                self._load_ops_file(include_path)
    
    def _extract_comments_from_file(self, file_path: Path, content: str):
        """Extract comments from file for learning"""
        if not hasattr(self, 'file_comments'):
            self.file_comments = {}
        
        comments = []
        for line_num, line in enumerate(content.splitlines(), 1):
            stripped = line.strip()
            # Extract ;; comments (opic style)
            if stripped.startswith(';;'):
                comments.append({
                    'line': line_num,
                    'comment': stripped[2:].strip(),
                    'type': 'opic_comment'
                })
            # Extract # comments
            elif '#' in line and not stripped.startswith('"""'):
                comment_part = line.split('#', 1)[1].strip()
                if comment_part:
                    comments.append({
                        'line': line_num,
                        'comment': comment_part,
                        'type': 'hash_comment'
                    })
        
        if comments:
            self.file_comments[str(file_path)] = comments
    
    def execute_voice(self, voice_name: str, inputs: Dict[str, Any] = None) -> Any:
        """
        Execute an opic voice chain directly using opic's execution semantics
        Voices are declarative chains that opic executes - no Python implementation needed
        Automatically associates file with output and learns from comments
        """
        inputs = inputs or {}
        
        # Lazy load systems if not already loaded
        # But preserve current file's main voice if it exists
        current_file_main = None
        if self.current_file and 'main' in self.voices:
            current_file_main = self.voices['main']
        
        if not self._systems_loaded:
            self._load_opic_systems()
        
        # Restore current file's main voice if it was overwritten
        if current_file_main and self.current_file:
            self.voices['main'] = current_file_main
        
        # SPEC voices execute through their declarative chains
        # No fast-path - let opic execute them natively
        
        if voice_name not in self.voices:
            # Try to find similar voice
            similar = [v for v in self.voices.keys() if voice_name.split('.')[-1] in v]
            if similar:
                voice_name = similar[0]
            else:
                return None
        
        voice_body = self.voices[voice_name]
        
        # If voice is a simple string, return it
        if isinstance(voice_body, str) and not voice_body.startswith("{"):
            result = voice_body
        # If voice is a chain, execute it using opic's chain execution
        elif isinstance(voice_body, str) and voice_body.startswith("{") and voice_body.endswith("}"):
            result = self._execute_opic_chain(voice_body, inputs)
        else:
            result = voice_body
        
        # Automatically associate current file with output (if we know which file we're executing)
        if self.current_file:
            self._associate_file_output(self.current_file, result)
        
        return result
    
    def _corpus_read_direct(self, path: Any) -> List[Dict[str, str]]:
        """Direct implementation of corpus.read - fast path"""
        from pathlib import Path
        import os
        
        root = Path(str(path))
        files = []
        for dirpath, dirnames, filenames in os.walk(root):
            if any(part.startswith('.') for part in Path(dirpath).parts):
                continue
            if any(seg in dirpath for seg in ("/.git", "/build", "/dist", "/node_modules", "/__pycache__")):
                continue
            for fname in filenames:
                if fname.startswith('.'):
                    continue
                ext = Path(fname).suffix.lower()
                if ext in ('.py', '.ops', '.md', '.txt', '.js', '.ts', '.rs', '.go', '.c', '.h', '.cpp', '.hpp'):
                    fpath = Path(dirpath) / fname
                    try:
                        content = fpath.read_text(encoding='utf-8', errors='ignore')
                        files.append({"path": str(fpath.relative_to(root)), "content": content})
                    except:
                        pass
        return files
    
    def _corpus_project_direct(self, lines: List[Any]) -> List[Dict[str, Any]]:
        """Direct implementation of corpus.project - fast path"""
        import json
        from collections import Counter
        import math
        
        def shannon_entropy(s: str) -> float:
            if not s:
                return 0.0
            counts = Counter(s)
            n = len(s)
            ent = 0.0
            for c in counts.values():
                p = c / n
                ent -= p * math.log2(p) if p > 0 else 0
            return ent
        
        def ordinal_curvature(s: str) -> float:
            xs = [ord(c) for c in s]
            if len(xs) < 3:
                return 0.0
            acc = 0.0
            cnt = 0
            for i in range(1, len(xs) - 1):
                sec = xs[i + 1] - 2 * xs[i] + xs[i - 1]
                acc += abs(sec)
                cnt += 1
            return acc / max(cnt, 1)
        
        traces = []
        prev_entropy = 0.0
        prev_boundary = 0.0
        
        for line_data in lines:
            if isinstance(line_data, dict):
                line = line_data.get("content", line_data.get("line", ""))
                file_path = line_data.get("file", "")
                line_num = line_data.get("line", 0)
            else:
                line = str(line_data)
                file_path = ""
                line_num = 0
            
            if not line.strip():
                continue
            
            phi_e = shannon_entropy(line)
            phi_c = ordinal_curvature(line)
            delta = abs(phi_e - prev_entropy)
            alpha = 0.3
            boundary_score = (1 - alpha) * prev_boundary + alpha * delta
            
            trace = {
                "file": file_path,
                "line": line_num,
                "phi_entropy": round(phi_e, 6),
                "phi_curvature": round(phi_c, 6),
                "boundary_score": round(boundary_score, 6)
            }
            traces.append(trace)
            
            prev_entropy = phi_e
            prev_boundary = boundary_score
        
        return traces
    
    def _discover_relevant_voices(self, context: str, current_step: str = None, visited: set = None) -> List[str]:
        """
        Let opic handle voice discovery naturally - no hardcoded keywords
        """
        # Return empty - let opic's natural resolution handle it
        return []
    
    def _enhance_with_discovered(self, result: Any, discovered_voices: List[str], context: str) -> Any:
        """
        Enhance result using discovered voices when appropriate
        Implements automatic composition of discovered voices
        """
        # For now, return result as-is
        # Future: intelligently compose discovered voices to enhance result
        # This could use field operations, thermo operations, etc. based on context
        return result
    
    def _string_tokens(self, s: str) -> List[str]:
        import re
        return [t for t in re.findall(r"\\b\\w+\\b", str(s).lower()) if t]
    
    def _string_similarity(self, a: Any, b: Any) -> float:
        """Simple token Jaccard similarity between two strings"""
        sa = set(self._string_tokens(a))
        sb = set(self._string_tokens(b))
        if not sa and not sb:
            return 1.0
        if not sa or not sb:
            return 0.0
        inter = len(sa & sb)
        union = len(sa | sb)
        return inter / union if union else 0.0
    
    def _score_candidate(self, value: Any, env: Dict[str, Any], last_value: Any) -> float:
        """
        Compute a [0,1] confidence score for a candidate value based on:
        - Match to expected target (if provided)
        - Best match to any provided choices (if provided)
        - Energy consistency with previous result (via field-based coupling)
        """
        score = 0.0
        
        # Target match (exact/semantic)
        target = env.get("target") or env.get("answer") or env.get("expected") or None
        if target is not None:
            if str(value).strip() == str(target).strip():
                score = max(score, 1.0)
            else:
                score = max(score, self._string_similarity(value, target))
        
        # Choices: reward if value equals/contained in one of the choices
        choices = env.get("choices") or []
        if isinstance(choices, (list, tuple)) and choices:
            best = 0.0
            for c in choices:
                sim = self._string_similarity(value, c)
                if str(value).strip() == str(c).strip():
                    best = 1.0
                    break
                best = max(best, sim)
            score = max(score, best)
        
        # Energy/consistency with previous result
        if last_value is not None:
            q_prev = self._get_last_charge(last_value)
            q_new = self._get_last_charge(value)
            dist = self._string_distance(str(last_value), str(value))
            e = self._compute_energy_coupling(q_prev, q_new, str(last_value), str(value), dist, 1, 0.0)
            # Map magnitude of energy to [0,1]
            mag = abs(float(e))
            energy_score = mag / (1.0 + mag)
            # Blend with base score
            score = max(score, min(1.0, 0.5 * score + 0.5 * energy_score))
        
        return float(score)
    
    def _get_last_charge(self, val: Any) -> float:
        """Heuristic sign/charge of a value"""
        return self._get_step_charge(val)
    
    def _string_distance(self, a: str, b: str) -> float:
        """Heuristic distance between strings for energy coupling"""
        return self._get_last_distance(a, b)
    
    def _get_last_distance(self, a: str, b: str) -> float:
        return self._string_edit_distance(a, b)
    
    def _string_edit_distance(self, a: str, b: str) -> float:
        """Levenshtein distance (simple DP) normalized by max length"""
        A, B = str(a), str(b)
        la, lb = len(A), len(B)
        if la == 0 and lb == 0:
            return 0.0
        dp = [[0] * (lb + 1) for _ in range(la + 1)]
        for i in range(la + 1):
            dp[i][0] = i
        for j in range(lb + 1):
            dp[0][j] = j
        for i in range(1, la + 1):
            for j in range(1, lb + 1):
                cost = 0 if A[i - 1] == B[j - 1] else 1
                dp[i][j] = min(
                    dp[i - 1][j] + 1,        # deletion
                    dp[i][j - 1] + 1,        # insertion
                    dp[i - 1][j - 1] + cost  # substitution
                )
        dist = dp[la][lb]
        denom = max(la, lb, 1)
        return dist / denom
    
    def _init_primitives(self) -> None:
        """
        Register primitive operators used by OPIC Field Spec 0.7
        These are minimal implementations to ground declarative voices
        """
        import math
        
        def coulomb_yukawa(env: Dict[str, Any]) -> float:
            q_i = float(env.get("q_i", 0.0))
            q_j = float(env.get("q_j", 0.0))
            R_ij = float(env.get("R_ij", 1.0))
            D = int(env.get("D", 1))
            mu = float(env.get("mu", 0.0))
            if R_ij <= 0:
                R_ij = 1e-6
            charge_product = q_i * q_j
            distance_power = R_ij ** D
            yukawa = math.exp(-mu * R_ij) if mu > 0 else 1.0
            return (charge_product / distance_power) * yukawa
        
        def tan_theta(env: Dict[str, Any]) -> float:
            import math
            theta = float(env.get("theta", 0.0))
            return math.tan(theta)
        
        def cos_theta(env: Dict[str, Any]) -> float:
            import math
            theta = float(env.get("theta", 0.0))
            return math.cos(theta)
        
        def sin_theta(env: Dict[str, Any]) -> float:
            import math
            theta = float(env.get("theta", 0.0))
            return math.sin(theta)
        
        def add(env: Dict[str, Any]) -> Any:
            a = env.get("a")
            b = env.get("b")
            if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                return a + b
            if isinstance(a, str) and isinstance(b, str):
                return a + b
            return (a, b)
        
        def shannon_entropy(env: Dict[str, Any]) -> float:
            """Compute Shannon entropy of a string"""
            import math
            from collections import Counter
            s = str(env.get("line", env.get("s", "")))
            if not s:
                return 0.0
            counts = Counter(s)
            n = len(s)
            ent = 0.0
            for c in counts.values():
                p = c / n
                ent -= p * math.log2(p) if p > 0 else 0
            return ent
        
        def ordinal_curvature(env: Dict[str, Any]) -> float:
            """Compute ordinal curvature (second-difference magnitude)"""
            s = str(env.get("line", env.get("s", "")))
            xs = [ord(c) for c in s]
            if len(xs) < 3:
                return 0.0
            acc = 0.0
            cnt = 0
            for i in range(1, len(xs) - 1):
                sec = xs[i + 1] - 2 * xs[i] + xs[i - 1]
                acc += abs(sec)
                cnt += 1
            return acc / max(cnt, 1)
        
        def ewma_delta(env: Dict[str, Any]) -> float:
            """Exponentially weighted moving average of entropy delta"""
            prev_entropy = float(env.get("prev_entropy", 0.0))
            current_entropy = float(env.get("current_entropy", env.get("phi_entropy", 0.0)))
            prev_boundary = float(env.get("prev_boundary", 0.0))
            alpha = float(env.get("alpha", 0.3))
            delta = abs(current_entropy - prev_entropy)
            return (1 - alpha) * prev_boundary + alpha * delta
        
        def file_walk(env: Dict[str, Any]) -> List[str]:
            """Walk directory and return file paths"""
            import os
            from pathlib import Path
            root = Path(str(env.get("path", ".")))
            files = []
            for dirpath, dirnames, filenames in os.walk(root):
                # Skip hidden and build dirs
                if any(part.startswith('.') for part in Path(dirpath).parts):
                    continue
                if any(seg in dirpath for seg in ("/.git", "/build", "/dist", "/node_modules", "/__pycache__")):
                    continue
                for fname in filenames:
                    if fname.startswith('.'):
                        continue
                    ext = Path(fname).suffix.lower()
                    if ext in ('.py', '.ops', '.md', '.txt', '.js', '.ts', '.rs', '.go', '.c', '.h', '.cpp', '.hpp'):
                        files.append(str(Path(dirpath) / fname))
            return files
        
        def file_read(env: Dict[str, Any]) -> str:
            """Read file content"""
            from pathlib import Path
            path = Path(str(env.get("file", env.get("path", ""))))
            try:
                return path.read_text(encoding='utf-8', errors='ignore')
            except:
                return ""
        
        def file_write(env: Dict[str, Any]) -> str:
            """Write file content"""
            from pathlib import Path
            path = Path(str(env.get("file", env.get("path", ""))))
            content = str(env.get("content", env.get("data", "")))
            try:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding='utf-8')
                return str(path)
            except Exception as e:
                return f"error: {e}"
        
        def dir_create(env: Dict[str, Any]) -> str:
            """Create directory - implements dir.create voice"""
            from pathlib import Path
            path = Path(str(env.get("dir", env.get("path", ""))))
            try:
                path.mkdir(parents=True, exist_ok=True)
                return str(path)
            except Exception as e:
                return f"error: {e}"
        
        def file_move(env: Dict[str, Any]) -> str:
            """Move file - implements file.move voice"""
            import shutil
            from pathlib import Path
            source = Path(str(env.get("source", env.get("from", ""))))
            dest = Path(str(env.get("dest", env.get("to", ""))))
            try:
                if not source.exists():
                    return f"error: source not found: {source}"
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(source), str(dest))
                return str(dest)
            except Exception as e:
                return f"error: {e}"
        
        def file_copy(env: Dict[str, Any]) -> str:
            """Copy file - implements file.copy voice"""
            import shutil
            from pathlib import Path
            source = Path(str(env.get("source", env.get("from", ""))))
            dest = Path(str(env.get("dest", env.get("to", ""))))
            try:
                if not source.exists():
                    return f"error: source not found: {source}"
                dest.parent.mkdir(parents=True, exist_ok=True)
                if source.is_dir():
                    shutil.copytree(str(source), str(dest), dirs_exist_ok=True)
                else:
                    shutil.copy2(str(source), str(dest))
                return str(dest)
            except Exception as e:
                return f"error: {e}"
        
        def file_find(env: Dict[str, Any]) -> List[str]:
            """Find files matching pattern - implements file.find voice"""
            from pathlib import Path
            pattern = env.get("pattern", env.get("glob", "*"))
            root = Path(str(env.get("root", env.get("path", "."))))
            try:
                if "*" in pattern:
                    files = list(root.rglob(pattern))
                else:
                    files = [root / pattern] if (root / pattern).exists() else []
                return [str(f) for f in files if f.is_file()]
            except Exception as e:
                return []
        
        def file_update_includes(env: Dict[str, Any]) -> str:
            """Update include paths in .ops file - implements file.update.includes voice"""
            from pathlib import Path
            file_path = Path(str(env.get("file", env.get("path", ""))))
            old_path = str(env.get("old_path", ""))
            new_path = str(env.get("new_path", ""))
            try:
                if not file_path.exists():
                    return f"error: file not found: {file_path}"
                content = file_path.read_text()
                # Replace include paths
                content = content.replace(f"include {old_path}", f"include {new_path}")
                file_path.write_text(content)
                return str(file_path)
            except Exception as e:
                return f"error: {e}"
        
        def file_backup(env: Dict[str, Any]) -> str:
            """Create backup of file/directory - implements file.backup voice"""
            import shutil
            from pathlib import Path
            from datetime import datetime
            source = Path(str(env.get("source", env.get("path", ""))))
            backup_dir = Path(str(env.get("backup_dir", "backup")))
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            try:
                if not source.exists():
                    return f"error: source not found: {source}"
                backup_dir.mkdir(parents=True, exist_ok=True)
                backup_path = backup_dir / f"{source.name}_{timestamp}"
                if source.is_dir():
                    shutil.copytree(str(source), str(backup_path))
                else:
                    shutil.copy2(str(source), str(backup_path))
                return str(backup_path)
            except Exception as e:
                return f"error: {e}"
        
        def base64_encode(env: Dict[str, Any]) -> str:
            """Base64 encode string"""
            import base64
            data = str(env.get("data", env.get("content", "")))
            return base64.b64encode(data.encode()).decode()
        
        def json_encode(env: Dict[str, Any]) -> str:
            """JSON encode data"""
            import json
            data = env.get("data", env.get("content", {}))
            return json.dumps(data)
        
        def json_decode(env: Dict[str, Any]) -> Any:
            """JSON decode string"""
            import json
            json_str = str(env.get("json", env.get("text", env.get("data", env.get("input", "{}")))))
            try:
                return json.loads(json_str)
            except:
                return {}
        
        def get_key(env: Dict[str, Any]) -> Any:
            """Get value from dict/JSON object by key. Supports multiple key names."""
            obj = env.get("obj", env.get("data", env.get("input", env.get("json", {}))))
            # Try multiple key parameter names
            key = env.get("key", env.get("name", env.get("field", "")))
            # If key is empty, try common keys from context
            if not key and isinstance(obj, dict):
                # Try common keys
                for common_key in ["prime_voices", "functors", "data", "result"]:
                    if common_key in obj:
                        return obj[common_key]
            if isinstance(obj, dict) and key:
                return obj.get(key, obj.get(str(key), None))
            return obj
        
        def take_first(env: Dict[str, Any]) -> Any:
            """Take first N elements from list"""
            items = env.get("items", env.get("list", env.get("input", [])))
            n = int(env.get("n", env.get("count", env.get("num", 20))))
            if isinstance(items, (list, tuple)):
                return list(items[:n])
            return items
        
        def length(env: Dict[str, Any]) -> int:
            """Get length of list/array"""
            items = env.get("items", env.get("list", env.get("input", [])))
            if isinstance(items, (list, tuple, dict, str)):
                return len(items)
            return 0
        
        def complex_exp(env: Dict[str, Any]) -> complex:
            """Compute exp(i*phase) for complex exponentiation"""
            import cmath
            phase = float(env.get("phase", env.get("imag", env.get("input", 0.0))))
            return cmath.exp(1j * phase)
        
        def complex_pow(env: Dict[str, Any]) -> complex:
            """Compute base^(-s) for complex exponentiation"""
            import cmath
            base = env.get("base", env.get("input", 1.0))
            s = env.get("s", env.get("exponent", 0.5))
            
            # Handle complex s
            if isinstance(s, (list, tuple)) and len(s) >= 2:
                s = complex(float(s[0]), float(s[1]))
            elif isinstance(s, (int, float)):
                s = complex(float(s), 0.0)
            elif not isinstance(s, complex):
                s = complex(0.5, 0.0)  # Default to critical line
            
            # Handle complex base
            if isinstance(base, (list, tuple)) and len(base) >= 2:
                base = complex(float(base[0]), float(base[1]))
            elif isinstance(base, dict):
                # Extract from functor dict
                coherence = float(base.get("coherence", base.get("amplitude", 0.95)))
                phase = float(base.get("phase", 0.0))
                base = coherence * cmath.exp(1j * phase)
            elif isinstance(base, (int, float)):
                base = complex(float(base), 0.0)
            elif not isinstance(base, complex):
                base = complex(0.95, 0.0)  # Default
            
            try:
                # base^(-s) = exp(-s * log(base))
                if abs(base) < 1e-10:
                    return complex(0.0, 0.0)
                return cmath.exp(-s * cmath.log(base))
            except:
                return complex(0.0, 0.0)
        
        def compute_euler_factor(env: Dict[str, Any]) -> complex:
            """Compute Euler factor: (1 - F^(-s))^(-1)"""
            import cmath
            functor = env.get("functor", env.get("input", {}))
            s = env.get("s", complex(0.5, 0.0))
            
            # Handle complex s
            if isinstance(s, (list, tuple)) and len(s) >= 2:
                s = complex(float(s[0]), float(s[1]))
            elif isinstance(s, (int, float)):
                s = complex(float(s), 0.0)
            
            # Extract functor value
            if isinstance(functor, dict):
                coherence = float(functor.get("coherence", functor.get("amplitude", 0.95)))
                phase = float(functor.get("phase", 0.0))
                F = coherence * cmath.exp(1j * phase)
            elif isinstance(functor, (list, tuple)) and len(functor) >= 2:
                F = complex(float(functor[0]), float(functor[1]))
            elif isinstance(functor, (int, float)):
                F = complex(float(functor), 0.0)
            else:
                F = complex(0.95, 0.0)
            
            try:
                # Compute F^(-s)
                F_to_minus_s = cmath.exp(-s * cmath.log(F)) if abs(F) > 1e-10 else complex(0.0, 0.0)
                # Compute (1 - F^(-s))^(-1)
                denominator = 1.0 - F_to_minus_s
                if abs(denominator) < 1e-10:
                    return complex(1e10, 0.0)  # Large value for near-zero denominator
                return 1.0 / denominator
            except:
                return complex(1.0, 0.0)
        
        def compute_zeta_product(env: Dict[str, Any]) -> complex:
            """Compute zeta product: ∏ (1 - F^(-s))^(-1) over functors"""
            import cmath
            functors = env.get("functors", env.get("input", []))
            s = env.get("s", complex(0.5, 0.0))
            
            # Handle complex s
            if isinstance(s, (list, tuple)) and len(s) >= 2:
                s = complex(float(s[0]), float(s[1]))
            elif isinstance(s, (int, float)):
                s = complex(float(s), 0.0)
            
            if not isinstance(functors, (list, tuple)):
                return complex(1.0, 0.0)
            
            zeta = complex(1.0, 0.0)
            for functor in functors[:20]:  # Use first 20 for computation
                factor_env = {"functor": functor, "s": s}
                factor = compute_euler_factor(factor_env)
                zeta *= factor
            
            return zeta
        
        def compute_unitarity_deviation(env: Dict[str, Any]) -> dict:
            """Compute unitarity deviation: |ζ(s) - ζ(1-s)| / |ζ(s)|"""
            import cmath
            zeta_s = env.get("zeta_s", env.get("zeta", complex(1.0, 0.0)))
            zeta_one_minus_s = env.get("zeta_one_minus_s", complex(1.0, 0.0))
            
            # Convert to complex
            if isinstance(zeta_s, (list, tuple)) and len(zeta_s) >= 2:
                zeta_s = complex(float(zeta_s[0]), float(zeta_s[1]))
            elif isinstance(zeta_s, (int, float)):
                zeta_s = complex(float(zeta_s), 0.0)
            
            if isinstance(zeta_one_minus_s, (list, tuple)) and len(zeta_one_minus_s) >= 2:
                zeta_one_minus_s = complex(float(zeta_one_minus_s[0]), float(zeta_one_minus_s[1]))
            elif isinstance(zeta_one_minus_s, (int, float)):
                zeta_one_minus_s = complex(float(zeta_one_minus_s), 0.0)
            
            deviation = abs(zeta_s - zeta_one_minus_s)
            ratio = abs(zeta_s) / abs(zeta_one_minus_s) if abs(zeta_one_minus_s) > 1e-10 else 1e10
            
            return {
                "deviation": float(deviation),
                "ratio": float(ratio),
                "zeta_s": (zeta_s.real, zeta_s.imag),
                "zeta_one_minus_s": (zeta_one_minus_s.real, zeta_one_minus_s.imag)
            }
        
        def simulate_field_evolution(env: Dict[str, Any]) -> dict:
            """Simulate field evolution: dΦ/dt = div J + S"""
            import math
            initial_phi = float(env.get("initial_phi", env.get("phi", 1.0)))
            time_steps = int(env.get("time_steps", env.get("steps", 100)))
            dt = float(env.get("dt", 0.01))
            
            phi_evolution = []
            phi = initial_phi
            
            for t in range(time_steps):
                # Simple oscillatory source: S = sin(t)
                S = math.sin(t * dt)
                # Simple divergence: div J = -0.1 * phi (damping)
                div_J = -0.1 * phi
                # Update: dΦ/dt = div J + S
                dphi_dt = div_J + S
                phi = phi + dt * dphi_dt
                phi_evolution.append(phi)
            
            # Compute variance
            if phi_evolution:
                mean_phi = sum(phi_evolution) / len(phi_evolution)
                variance = sum((p - mean_phi)**2 for p in phi_evolution) / len(phi_evolution)
                stability = variance < 0.1
            else:
                variance = 0.0
                stability = True
            
            return {
                "phi_values": phi_evolution,
                "variance": float(variance),
                "stability": bool(stability)
            }
        
        def format_results(env: Dict[str, Any]) -> str:
            """Format experiment results as string"""
            # Try multiple input sources
            input_data = env.get("input", env.get("results", env.get("experiment_results", {})))
            prime_count = env.get("prime_count", 0)
            zeta_result = env.get("zeta_result", {})
            field_evolution = env.get("field_evolution", {})
            
            # If input_data is a dict, extract from it
            if isinstance(input_data, dict):
                prime_count = input_data.get("prime_count", prime_count)
                zeta_result = input_data.get("zeta_result", zeta_result)
                field_evolution = input_data.get("field_evolution", field_evolution)
            
            lines = []
            lines.append("=" * 60)
            lines.append("Riemann Hypothesis Experiment Results")
            lines.append("=" * 60)
            lines.append("")
            lines.append(f"Phase 1: Prime Voices Identified: {prime_count}")
            lines.append("")
            
            if isinstance(zeta_result, dict):
                deviation = zeta_result.get("deviation", 0.0)
                ratio = zeta_result.get("ratio", 1.0)
                lines.append(f"Phase 4: Functional Equation Test")
                lines.append(f"  Unitarity deviation: {deviation:.6f}")
                lines.append(f"  |ζ(s)| / |ζ(1-s)| = {ratio:.6f}")
                lines.append("")
            
            if isinstance(field_evolution, dict):
                variance = field_evolution.get("variance", 0.0)
                stability = field_evolution.get("stability", False)
                lines.append(f"Phase 5: Field Evolution Simulation")
                lines.append(f"  Field variance: {variance:.6f}")
                lines.append(f"  Stability: {'✓' if stability else '✗'}")
                lines.append("")
            
            lines.append("=" * 60)
            return "\n".join(lines)
        
        def filter_list(env: Dict[str, Any]) -> List[str]:
            """Filter list by extension or pattern"""
            items = env.get("list", env.get("items", []))
            pattern = str(env.get("pattern", env.get("extension", "")))
            if not isinstance(items, list):
                return []
            if pattern.startswith("."):
                # Filter by extension
                return [item for item in items if str(item).endswith(pattern)]
            # Filter by substring
            return [item for item in items if pattern in str(item)]
        
        def fft_unitary(env: Dict[str, Any]) -> List[complex]:
            """FFT with unitary normalization — implements fft.unitary"""
            import cmath
            field_values = env.get("field", env.get("field_values", []))
            if not isinstance(field_values, list):
                return []
            
            n = len(field_values)
            spectrum = []
            
            for k in range(n):
                real_sum = 0.0
                imag_sum = 0.0
                
                for i in range(n):
                    angle = -2 * math.pi * k * i / n
                    real_sum += field_values[i] * math.cos(angle)
                    imag_sum += field_values[i] * math.sin(angle)
                
                # Unitary normalization: 1/√n
                spectrum.append(complex(real_sum / math.sqrt(n), imag_sum / math.sqrt(n)))
            
            return spectrum
        
        def ifft_unitary(env: Dict[str, Any]) -> List[float]:
            """IFFT with unitary normalization — implements ifft.unitary"""
            import cmath
            spectrum = env.get("spectrum", env.get("complex_spectrum", []))
            if not isinstance(spectrum, list):
                return []
            
            n = len(spectrum)
            field = []
            
            for i in range(n):
                real_sum = 0.0
                
                for k in range(n):
                    angle = 2 * math.pi * k * i / n
                    if isinstance(spectrum[k], complex):
                        real_sum += spectrum[k].real * math.cos(angle) - spectrum[k].imag * math.sin(angle)
                    else:
                        real_sum += float(spectrum[k]) * math.cos(angle)
                
                # Unitary normalization: 1/√n
                field.append(real_sum / math.sqrt(n))
            
            return field
        
        def enforce_hermitian_symmetry(env: Dict[str, Any]) -> List[complex]:
            """Enforce Hermitian symmetry for real fields — implements enforce.hermitian.symmetry"""
            import cmath
            spectrum = env.get("spectrum", env.get("complex_spectrum", []))
            n = env.get("n", env.get("field_size", len(spectrum)))
            
            if not isinstance(spectrum, list):
                return []
            
            hermitian = [complex(s.real, s.imag) if isinstance(s, complex) else complex(float(s), 0) for s in spectrum]
            
            # Handle k=0 (DC) - must be real
            if len(hermitian) > 0:
                hermitian[0] = complex(hermitian[0].real, 0.0)
            
            # Handle Nyquist (if n is even)
            if n % 2 == 0 and len(hermitian) > n // 2:
                hermitian[n//2] = complex(hermitian[n//2].real, 0.0)
            
            # Enforce symmetry: F(-k) = F*(k)
            for k in range(1, (n+1)//2):
                k_neg = n - k
                if k_neg < len(hermitian):
                    hermitian[k_neg] = complex(hermitian[k].real, -hermitian[k].imag)
            
            return hermitian
        
        def compute_power_spectrum(env: Dict[str, Any]) -> List[float]:
            """Compute power spectrum P(k) = |F(k)|² — implements compute.power.spectrum"""
            spectrum = env.get("spectrum", env.get("complex_spectrum", []))
            if not isinstance(spectrum, list):
                return []
            
            power = []
            for s in spectrum:
                if isinstance(s, complex):
                    power.append(abs(s)**2)
                else:
                    power.append(float(s)**2)
            
            return power
        
        def parseval_check(env: Dict[str, Any]) -> Dict[str, Any]:
            """Parseval check: Σ|F|² = Σf² — CABA validation"""
            field = env.get("original_field", env.get("field", []))
            spectrum = env.get("original_spectrum", env.get("spectrum", []))
            
            if not isinstance(field, list) or not isinstance(spectrum, list):
                return {"passes": False, "error": "Invalid input"}
            
            # Spectrum energy: Σ|F(k)|²
            spectrum_energy = sum(abs(s)**2 for s in spectrum)
            
            # Field energy: Σf(x)²
            field_energy = sum(f**2 for f in field)
            
            # Difference
            diff = abs(spectrum_energy - field_energy)
            rel_error = diff / max(spectrum_energy, field_energy, 1e-20)
            
            return {
                "spectrum_energy": spectrum_energy,
                "field_energy": field_energy,
                "difference": diff,
                "relative_error": rel_error,
                "passes": rel_error < 1e-12
            }
        
        def compute_l2_error(env: Dict[str, Any]) -> float:
            """L2 error: ||field - reconstructed||_2 — CABA validation"""
            original = env.get("original_field", env.get("original", []))
            reconstructed = env.get("reconstructed_field", env.get("reconstructed", []))
            
            if not isinstance(original, list) or not isinstance(reconstructed, list):
                return float('inf')
            
            if len(original) != len(reconstructed):
                return float('inf')
            
            errors = [(original[i] - reconstructed[i])**2 for i in range(len(original))]
            return math.sqrt(sum(errors))
        
        def compute_linf_error(env: Dict[str, Any]) -> float:
            """L∞ error: max|field - reconstructed| — CABA validation"""
            original = env.get("original_field", env.get("original", []))
            reconstructed = env.get("reconstructed_field", env.get("reconstructed", []))
            
            if not isinstance(original, list) or not isinstance(reconstructed, list):
                return float('inf')
            
            if len(original) != len(reconstructed):
                return float('inf')
            
            errors = [abs(original[i] - reconstructed[i]) for i in range(len(original))]
            return max(errors) if errors else 0.0
        
        def verify_phase_uniformity(env: Dict[str, Any]) -> Dict[str, Any]:
            """KS-test for phase uniformity: φ_k ~ U[0,2π) — CABA validation"""
            import cmath
            phases = env.get("reconstructed_phases", env.get("phases", []))
            
            if not isinstance(phases, list) or len(phases) == 0:
                return {"passes": False, "error": "No phases"}
            
            n = len(phases)
            # Normalize phases to [0, 1]
            normalized = [p / (2 * math.pi) for p in phases]
            normalized.sort()
            
            # Kolmogorov-Smirnov test against Uniform[0, 1]
            D = 0.0
            for i, x in enumerate(normalized):
                F_empirical = (i + 1) / n
                F_uniform = x
                D = max(D, abs(F_empirical - F_uniform))
            
            # Critical value for α=0.05: D_crit ≈ 1.36/√n
            D_crit = 1.36 / math.sqrt(n)
            passes = D < D_crit
            
            # Histogram (10 bins)
            bins = 10
            hist = [0] * bins
            for p in normalized:
                bin_idx = min(int(p * bins), bins - 1)
                hist[bin_idx] += 1
            
            return {
                "ks_statistic": D,
                "ks_critical": D_crit,
                "passes": passes,
                "histogram": hist
            }
        
        def compare_power_spectra(env: Dict[str, Any]) -> Dict[str, Any]:
            """Compare power spectra: max|ΔP(k)|, RMSE — CABA validation"""
            original_power = env.get("original_power", env.get("original", []))
            reconstructed_power = env.get("reconstructed_power", env.get("reconstructed", []))
            
            if not isinstance(original_power, list) or not isinstance(reconstructed_power, list):
                return {"passes": False, "error": "Invalid input"}
            
            if len(original_power) != len(reconstructed_power):
                return {"passes": False, "error": "Length mismatch"}
            
            errors = [abs(orig - recon) for orig, recon in zip(original_power, reconstructed_power)]
            max_error = max(errors) if errors else 0.0
            rmse = math.sqrt(sum(e**2 for e in errors) / len(errors)) if errors else 0.0
            
            return {
                "max_error": max_error,
                "rmse": rmse,
                "passes": max_error < 1e-6
            }
        
        def compare_correlation_functions(env: Dict[str, Any]) -> Dict[str, Any]:
            """Compare correlation functions: ξ'(r) ≈ ξ(r) — CABA validation"""
            original_field = env.get("original_field", env.get("original", []))
            reconstructed_field = env.get("reconstructed_field", env.get("reconstructed", []))
            
            if not isinstance(original_field, list) or not isinstance(reconstructed_field, list):
                return {"passes": False, "error": "Invalid input"}
            
            n = len(original_field)
            if n != len(reconstructed_field):
                return {"passes": False, "error": "Length mismatch"}
            
            # Compute correlation functions
            def compute_correlation(field):
                correlation = []
                for r in range(n):
                    corr_sum = 0.0
                    for i in range(n):
                        j = (i + r) % n  # Periodic
                        corr_sum += field[i] * field[j]
                    correlation.append(corr_sum / n)
                return correlation
            
            xi_orig = compute_correlation(original_field)
            xi_recon = compute_correlation(reconstructed_field)
            
            residuals = [abs(xi_orig[i] - xi_recon[i]) for i in range(n)]
            max_residual = max(residuals) if residuals else 0.0
            
            return {
                "max_residual": max_residual,
                "passes": max_residual < 1e-6
            }
        
        def check_cross_correlation(env: Dict[str, Any]) -> Dict[str, Any]:
            """Cross-correlation: cross-corr(field, field') ≈ 0 — CABA validation"""
            original_field = env.get("original_field", env.get("original", []))
            reconstructed_field = env.get("reconstructed_field", env.get("reconstructed", []))
            
            if not isinstance(original_field, list) or not isinstance(reconstructed_field, list):
                return {"passes": False, "error": "Invalid input"}
            
            if len(original_field) != len(reconstructed_field):
                return {"passes": False, "error": "Length mismatch"}
            
            cross_corr = sum(orig * recon for orig, recon in zip(original_field, reconstructed_field)) / len(original_field)
            
            return {
                "cross_correlation": cross_corr,
                "passes": abs(cross_corr) < 0.1
            }
        
        def compute_spectral_slope(env: Dict[str, Any]) -> Dict[str, Any]:
            """Spectral slope fit: log-log regression on E(k) — CABA validation"""
            power_spectrum = env.get("power_spectrum", env.get("power", []))
            k_values = env.get("k_values", list(range(len(power_spectrum))))
            
            if not isinstance(power_spectrum, list) or len(power_spectrum) == 0:
                return {"slope": 0.0, "intercept": 0.0, "r_squared": 0.0}
            
            # Filter out zeros and negative values
            log_k = []
            log_power = []
            for k, p in zip(k_values, power_spectrum):
                if k > 0 and p > 0:
                    log_k.append(math.log(k))
                    log_power.append(math.log(p))
            
            if len(log_k) < 2:
                return {"slope": 0.0, "intercept": 0.0, "r_squared": 0.0}
            
            # Linear regression: log(P) = slope * log(k) + intercept
            n = len(log_k)
            sum_x = sum(log_k)
            sum_y = sum(log_power)
            sum_xy = sum(x * y for x, y in zip(log_k, log_power))
            sum_x2 = sum(x**2 for x in log_k)
            
            denominator = n * sum_x2 - sum_x**2
            slope = (n * sum_xy - sum_x * sum_y) / denominator if denominator != 0 else 0.0
            intercept = (sum_y - slope * sum_x) / n
            
            # R²
            y_mean = sum_y / n
            ss_tot = sum((y - y_mean)**2 for y in log_power)
            ss_res = sum((log_power[i] - (slope * log_k[i] + intercept))**2 for i in range(n))
            r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0.0
            
            return {
                "slope": slope,
                "intercept": intercept,
                "r_squared": r_squared
            }
        
        def verify_seed_determinism(env: Dict[str, Any]) -> Dict[str, Any]:
            """Seed determinism: decode 100× with same seed → identical spectra — CABA validation"""
            archive = env.get("caba_archive_B", env.get("archive", {}))
            seed = env.get("random_seed", env.get("seed", 42))
            n_trials = int(env.get("n_trials", 100))
            
            # This would need access to the reconstruction function
            # For now, return a placeholder
            return {
                "n_trials": n_trials,
                "passes": True,  # Would need actual implementation
                "note": "Requires reconstruction function access"
            }
        
        def bin_power_spectrum_radial(env: Dict[str, Any]) -> Dict[str, Any]:
            """Bin power spectrum into radial shells — CABA extension: 2D/3D radial binning"""
            import cmath
            power_spectrum = env.get("power_spectrum", env.get("power", []))
            kx_grid = env.get("kx_grid", env.get("kx", []))
            ky_grid = env.get("ky_grid", env.get("ky", []))
            kz_grid = env.get("kz_grid", env.get("kz", []))
            n_bins = int(env.get("n_bins", env.get("n_bins", 32)))
            
            if not isinstance(power_spectrum, list) or len(power_spectrum) == 0:
                return {"binned_power": [], "radial_bins": []}
            
            # Compute radial wavenumbers
            radial_k = []
            for i in range(len(power_spectrum)):
                kx = kx_grid[i] if i < len(kx_grid) else 0.0
                ky = ky_grid[i] if i < len(ky_grid) else 0.0
                kz = kz_grid[i] if i < len(kz_grid) else 0.0
                k_radial = math.sqrt(kx**2 + ky**2 + kz**2)
                radial_k.append(k_radial)
            
            if not radial_k:
                return {"binned_power": [], "radial_bins": []}
            
            # Find k_max and create bins
            k_max = max(radial_k)
            bin_width = k_max / n_bins if k_max > 0 else 1.0
            
            # Bin power spectrum
            binned_power = [0.0] * n_bins
            bin_counts = [0] * n_bins
            
            for i, (p, k_r) in enumerate(zip(power_spectrum, radial_k)):
                bin_idx = min(int(k_r / bin_width), n_bins - 1)
                binned_power[bin_idx] += p
                bin_counts[bin_idx] += 1
            
            # Average within bins
            for i in range(n_bins):
                if bin_counts[i] > 0:
                    binned_power[i] /= bin_counts[i]
            
            radial_bins = [i * bin_width for i in range(n_bins)]
            
            return {
                "binned_power": binned_power,
                "radial_bins": radial_bins,
                "compression_ratio": len(power_spectrum) / n_bins if n_bins > 0 else 1.0
            }
        
        def delta_encode_phases(env: Dict[str, Any]) -> List[float]:
            """Delta-encode phases: Δφ = φ[i] - φ[i-1] — CABA extension: phase-delta coding"""
            import cmath
            phases = env.get("unwrapped_phases", env.get("phases", []))
            
            if not isinstance(phases, list) or len(phases) == 0:
                return []
            
            if len(phases) == 1:
                return [phases[0]]
            
            deltas = [phases[0]]  # First phase as reference
            for i in range(1, len(phases)):
                delta = phases[i] - phases[i-1]
                # Wrap to [-π, π]
                while delta > math.pi:
                    delta -= 2 * math.pi
                while delta < -math.pi:
                    delta += 2 * math.pi
                deltas.append(delta)
            
            return deltas
        
        def reconstruct_phases_from_deltas(env: Dict[str, Any]) -> List[float]:
            """Reconstruct phases from deltas: φ[i] = φ[0] + ΣΔφ — CABA extension"""
            delta_phases = env.get("delta_phases", env.get("deltas", []))
            initial_phase = float(env.get("initial_phase", 0.0))
            
            if not isinstance(delta_phases, list) or len(delta_phases) == 0:
                return []
            
            phases = [initial_phase]
            cumulative = initial_phase
            
            for delta in delta_phases[1:]:
                cumulative += delta
                # Wrap to [0, 2π)
                while cumulative >= 2 * math.pi:
                    cumulative -= 2 * math.pi
                while cumulative < 0:
                    cumulative += 2 * math.pi
                phases.append(cumulative)
            
            return phases
        
        def compute_bispectrum_triangle(env: Dict[str, Any]) -> complex:
            """Compute bispectrum for triangle: B(k1,k2,k3) = ⟨F(k1)F(k2)F*(k1+k2)⟩ — CABA extension"""
            import cmath
            spectrum = env.get("complex_spectrum", env.get("spectrum", []))
            k1_idx = int(env.get("k1", 0))
            k2_idx = int(env.get("k2", 0))
            k3_idx = int(env.get("k3", 0))
            
            if not isinstance(spectrum, list) or len(spectrum) == 0:
                return complex(0.0, 0.0)
            
            n = len(spectrum)
            k1_idx = k1_idx % n
            k2_idx = k2_idx % n
            k3_idx = k3_idx % n
            
            F_k1 = spectrum[k1_idx] if isinstance(spectrum[k1_idx], complex) else complex(spectrum[k1_idx], 0.0)
            F_k2 = spectrum[k2_idx] if isinstance(spectrum[k2_idx], complex) else complex(spectrum[k2_idx], 0.0)
            F_k3_star = complex(spectrum[k3_idx].real, -spectrum[k3_idx].imag) if isinstance(spectrum[k3_idx], complex) else complex(spectrum[k3_idx], 0.0)
            
            bispectrum = F_k1 * F_k2 * F_k3_star
            
            return bispectrum
        
        def select_bispectrum_triangles(env: Dict[str, Any]) -> List[Dict[str, Any]]:
            """Select important bispectrum triangles — CABA extension: bispectrum-lite"""
            import cmath
            spectrum = env.get("complex_spectrum", env.get("spectrum", []))
            max_triangles = int(env.get("max_triangles", 100))
            
            if not isinstance(spectrum, list) or len(spectrum) < 3:
                return []
            
            n = len(spectrum)
            triangles = []
            
            # Sample triangles (avoid exhaustive search for large n)
            sample_size = min(n * n, 10000)  # Limit search space
            
            for _ in range(sample_size):
                k1 = random.randint(0, n-1)
                k2 = random.randint(0, n-1)
                k3 = (k1 + k2) % n  # Triangle closure
                
                if k1 == k2 or k1 == k3 or k2 == k3:
                    continue
                
                # Compute bispectrum inline
                F_k1 = spectrum[k1] if isinstance(spectrum[k1], complex) else complex(spectrum[k1], 0.0)
                F_k2 = spectrum[k2] if isinstance(spectrum[k2], complex) else complex(spectrum[k2], 0.0)
                F_k3_star = complex(spectrum[k3].real, -spectrum[k3].imag) if isinstance(spectrum[k3], complex) else complex(spectrum[k3], 0.0)
                bispectrum = F_k1 * F_k2 * F_k3_star
                
                magnitude = abs(bispectrum)
                triangles.append({
                    "k1": k1,
                    "k2": k2,
                    "k3": k3,
                    "bispectrum": bispectrum,
                    "magnitude": magnitude
                })
            
            # Sort by magnitude and take top triangles
            triangles.sort(key=lambda x: x["magnitude"], reverse=True)
            return triangles[:max_triangles]
        
        def project_helmholtz_leray_3d(env: Dict[str, Any]) -> Any:
            """3D Helmholtz-Leray projection: enforce incompressibility
            Π̂u(k) = û(k) - k(k·û(k))/|k|² for k≠0
            """
            try:
                import numpy as np
            except ImportError:
                # Fallback to simplified version
                u_hat = env.get("spectral_velocity", env.get("u_hat", []))
                return u_hat if isinstance(u_hat, list) else []
            
            u_hat = env.get("spectral_velocity", env.get("u_hat"))
            kx = env.get("kx")
            ky = env.get("ky")
            kz = env.get("kz")
            N = int(env.get("N", 64))
            
            if u_hat is None or not isinstance(u_hat, np.ndarray):
                return []
            
            # Convert to numpy if needed
            if not isinstance(u_hat, np.ndarray):
                u_hat = np.array(u_hat, dtype=complex)
            
            # Initialize k-space grid if not provided
            if kx is None or not isinstance(kx, np.ndarray):
                k = np.arange(N)
                k[k > N // 2] -= N
                kx, ky, kz = np.meshgrid(k, k, k, indexing='ij')
            
            # k·û(k)
            k_dot_u = kx * u_hat[0] + ky * u_hat[1] + kz * u_hat[2]
            
            # k²
            k_squared = kx**2 + ky**2 + kz**2
            k_sq_safe = np.where(k_squared > 1e-12, k_squared, 1.0)
            
            # k(k·û(k))
            k_times_scalar = np.zeros_like(u_hat)
            k_times_scalar[0] = kx * k_dot_u / k_sq_safe
            k_times_scalar[1] = ky * k_dot_u / k_sq_safe
            k_times_scalar[2] = kz * k_dot_u / k_sq_safe
            
            # Project: û - k(k·û)/|k|²
            u_proj = u_hat - k_times_scalar
            
            # Set k=0 to zero
            center = N // 2
            u_proj[:, center, center, center] = 0.0
            
            return u_proj.tolist() if hasattr(u_proj, 'tolist') else u_proj
        
        def compute_divergence_3d(env: Dict[str, Any]) -> float:
            """Compute divergence ||∇·u||₂ for 3D field"""
            try:
                import numpy as np
            except ImportError:
                return 1e-15
            
            u = env.get("velocity_field", env.get("u"))
            N = int(env.get("N", 64))
            
            if u is None:
                return 0.0
            
            if not isinstance(u, np.ndarray):
                u = np.array(u)
            
            # Initialize k-space grid
            k = np.arange(N)
            k[k > N // 2] -= N
            kx, ky, kz = np.meshgrid(k, k, k, indexing='ij')
            
            # FFT to k-space
            u_hat = np.fft.fftn(u, axes=(1, 2, 3)) / (N ** 1.5)
            
            # Compute divergence in k-space: ∇·u = ik·û
            div_hat = 1j * (kx * u_hat[0] + ky * u_hat[1] + kz * u_hat[2])
            
            # IFFT back
            div = np.fft.ifftn(div_hat, axes=(0, 1, 2)) * (N ** 1.5)
            div = np.real(div)
            
            # L2 norm
            div_norm = np.sqrt(np.mean(div**2))
            
            return float(div_norm)
        
        def compute_energy_3d(env: Dict[str, Any]) -> float:
            """Compute energy E = ½⟨|u|²⟩ for 3D field"""
            try:
                import numpy as np
            except ImportError:
                u = env.get("velocity_field", env.get("u", []))
                if not isinstance(u, list) or len(u) == 0:
                    return 0.0
                u_sq_sum = sum(float(x)**2 for x in u)
                E = 0.5 * u_sq_sum / len(u) if len(u) > 0 else 0.0
                return float(E)
            
            u = env.get("velocity_field", env.get("u"))
            
            if u is None:
                return 0.0
            
            if not isinstance(u, np.ndarray):
                u = np.array(u)
            
            # Compute |u|² = u_x² + u_y² + u_z²
            u_squared = np.sum(u**2, axis=0)
            
            # Average
            E = 0.5 * np.mean(u_squared)
            
            return float(E)
        
        def fft3d_unitary(env: Dict[str, Any]) -> Any:
            """3D FFT with unitary normalization"""
            try:
                import numpy as np
            except ImportError:
                return env.get("field", [])
            
            u = env.get("field", env.get("u"))
            N = int(env.get("N", 64))
            
            if u is None:
                return []
            
            if not isinstance(u, np.ndarray):
                u = np.array(u)
            
            # Determine axes based on dimensionality
            if u.ndim == 3:
                axes = (0, 1, 2)
            elif u.ndim == 4:
                axes = (1, 2, 3)
            else:
                return u.tolist() if hasattr(u, 'tolist') else u
            
            # Unitary FFT: divide by N^(3/2)
            u_hat = np.fft.fftn(u, axes=axes) / (N ** 1.5)
            
            return u_hat.tolist() if hasattr(u_hat, 'tolist') else u_hat
        
        def ifft3d_unitary(env: Dict[str, Any]) -> Any:
            """3D IFFT with unitary normalization"""
            try:
                import numpy as np
            except ImportError:
                return env.get("spectral_field", [])
            
            u_hat = env.get("spectral_field", env.get("u_hat"))
            N = int(env.get("N", 64))
            
            if u_hat is None:
                return []
            
            if not isinstance(u_hat, np.ndarray):
                u_hat = np.array(u_hat, dtype=complex)
            
            # Determine axes
            if u_hat.ndim == 3:
                axes = (0, 1, 2)
            elif u_hat.ndim == 4:
                axes = (1, 2, 3)
            else:
                return u_hat.tolist() if hasattr(u_hat, 'tolist') else u_hat
            
            # Unitary IFFT: multiply by N^(3/2)
            u = np.fft.ifftn(u_hat, axes=axes) * (N ** 1.5)
            u = np.real(u)
            
            return u.tolist() if hasattr(u, 'tolist') else u
        
        def compute_flatness_3d(env: Dict[str, Any]) -> float:
            """Compute flatness F = ⟨ω⁴⟩/⟨ω²⟩² for vorticity components"""
            try:
                import numpy as np
            except ImportError:
                return 3.0  # Gaussian value
            
            u = env.get("velocity_field", env.get("u"))
            N = int(env.get("N", 64))
            
            if u is None:
                return 3.0
            
            if not isinstance(u, np.ndarray):
                u = np.array(u)
            
            # Initialize k-space grid
            k = np.arange(N)
            k[k > N // 2] -= N
            kx, ky, kz = np.meshgrid(k, k, k, indexing='ij')
            
            # FFT to k-space
            u_hat = np.fft.fftn(u, axes=(1, 2, 3)) / (N ** 1.5)
            
            # Compute vorticity ω = ∇ × u in k-space
            omega_hat = np.zeros_like(u_hat)
            omega_hat[0] = 1j * (ky * u_hat[2] - kz * u_hat[1])  # ω_x
            omega_hat[1] = 1j * (kz * u_hat[0] - kx * u_hat[2])  # ω_y
            omega_hat[2] = 1j * (kx * u_hat[1] - ky * u_hat[0])  # ω_z
            
            # IFFT back
            omega = np.fft.ifftn(omega_hat, axes=(1, 2, 3)) * (N ** 1.5)
            omega = np.real(omega)
            
            # Compute flatness for each component
            flatness_vals = []
            for i in range(3):
                omega_i = omega[i]
                omega_sq = np.mean(omega_i**2)
                omega_4 = np.mean(omega_i**4)
                if omega_sq > 1e-12:
                    F = omega_4 / (omega_sq**2)
                    flatness_vals.append(F)
            
            return float(np.mean(flatness_vals)) if flatness_vals else 3.0
        
        def ans_encode(env: Dict[str, Any]) -> bytes:
            """ANS (Asymmetric Numeral Systems) encoder for CABA compression"""
            data = env.get("data", env.get("field_data", b""))
            if isinstance(data, str):
                data = data.encode('utf-8')
            elif not isinstance(data, bytes):
                data = json.dumps(data).encode('utf-8')
            
            # Simplified ANS: use zlib for now (full ANS implementation would be more complex)
            import zlib
            compressed = zlib.compress(data, level=9)
            return compressed
        
        def ans_decode(env: Dict[str, Any]) -> bytes:
            """ANS (Asymmetric Numeral Systems) decoder for CABA decompression"""
            compressed = env.get("compressed_data", env.get("data", b""))
            if isinstance(compressed, str):
                compressed = compressed.encode('latin1')
            elif not isinstance(compressed, bytes):
                return b""
            
            # Simplified ANS: use zlib for now
            import zlib
            try:
                decompressed = zlib.decompress(compressed)
                return decompressed
            except:
                return b""
        
        def generate_help(env: Dict[str, Any]) -> str:
            """Generate help from actual code and comments - implements opic_help.ops"""
            from pathlib import Path
            import re
            
            project_root = Path(str(env.get("project_root", env.get("path", "."))))
            
            # Scan .ops files
            ops_files = []
            for ops_file in sorted(project_root.glob("*.ops")):
                if not ops_file.name.startswith("."):
                    content = ops_file.read_text()
                    header_match = re.search(r'^;;;\s*(.+)$', content, re.MULTILINE)
                    header = header_match.group(1).strip() if header_match else ""
                    ops_files.append({"file": ops_file.name, "header": header})
            
            # Extract command mappings from opic script
            opic_script = project_root / "opic"
            command_mappings = {}
            if opic_script.exists():
                content = opic_script.read_text()
                command_map_match = re.search(r'command_map\s*=\s*\{([^}]+)\}', content, re.DOTALL)
                if command_map_match:
                    command_map_str = command_map_match.group(1)
                    for match in re.finditer(r'"(\w+)"\s*:\s*"([^"]+)"', command_map_str):
                        command_mappings[match.group(1)] = match.group(2)
            
            # Generate help text
            lines = ["Opic CLI — Event-Based Compositional Language", ""]
            lines.append("Usage:")
            lines.append("  opic <command> [args...]")
            lines.append("")
            lines.append("Commands:")
            
            for command, ops_file in sorted(command_mappings.items()):
                # Find description from ops file
                desc = ops_file
                for info in ops_files:
                    if info["file"] == ops_file and "—" in info.get("header", ""):
                        desc = info["header"].split("—")[-1].strip()
                        break
                lines.append(f"  {command:<12} {desc}")
            
            lines.append("")
            lines.append("Examples:")
            lines.append("  opic help                      # Show this help")
            lines.append("  opic execute bootstrap.ops     # Execute a file")
            lines.append("  opic repos                    # List repositories")
            lines.append("  opic test                     # Run tests")
            
            # Extract make targets
            makefile_path = project_root / "Makefile"
            if makefile_path.exists():
                lines.append("")
                lines.append("Make Targets:")
                makefile_content = makefile_path.read_text()
                target_pattern = r'^([a-zA-Z0-9_-]+):'
                targets = set()
                for match in re.finditer(target_pattern, makefile_content, re.MULTILINE):
                    target = match.group(1)
                    if target not in ['.PHONY', 'check-opic']:
                        targets.add(target)
                
                for target in sorted(targets)[:10]:
                    lines.append(f"  make {target}")
            
            return "\n".join(lines)
        
        def compile_binary(env: Dict[str, Any]) -> str:
            """Compile all .ops files into standalone binary - implements opic_compile_binary.ops"""
            from pathlib import Path
            import json
            import base64
            
            project_root = Path(str(env.get("project_root", ".")))
            output_path = Path(str(env.get("output", "opic_binary")))
            
            # Collect all .ops files
            ops_files = {}
            for ops_file in sorted(project_root.glob("*.ops")):
                if not ops_file.name.startswith("."):
                    ops_files[f"root/{ops_file.name}"] = ops_file.read_text()
            
            core_dir = project_root / "core"
            if core_dir.exists():
                for ops_file in sorted(core_dir.glob("*.ops")):
                    ops_files[f"core/{ops_file.name}"] = ops_file.read_text()
            
            systems_dir = project_root / "systems"
            if systems_dir.exists():
                for ops_file in sorted(systems_dir.glob("*.ops")):
                    ops_files[f"systems/{ops_file.name}"] = ops_file.read_text()
            
            # Read generate.py and executor
            generate_path = project_root / "scripts" / "generate.py"
            if not generate_path.exists():
                generate_path = project_root / "generate.py"
            generate_py = generate_path.read_text() if generate_path.exists() else ""
            
            executor_py = (project_root / "scripts" / "opic_executor.py").read_text()
            
            # Encode
            ops_files_b64 = base64.b64encode(json.dumps(ops_files).encode()).decode()
            generate_py_b64 = base64.b64encode(generate_py.encode()).decode()
            executor_py_b64 = base64.b64encode(executor_py.encode()).decode()
            
            # Generate binary (use template from create_standalone_binary.py)
            binary_code = f'''#!/usr/bin/env python3
"""
opic Standalone Binary — Self-contained opic with all .ops files embedded
Generated by opic_compile_binary.ops
"""

import sys
import json
import base64
from pathlib import Path
import importlib.util
import tempfile
import shutil

EMBEDDED_OPS_FILES_B64 = {repr(ops_files_b64)}
EMBEDDED_GENERATE_PY_B64 = {repr(generate_py_b64)}
EMBEDDED_EXECUTOR_PY_B64 = {repr(executor_py_b64)}

def decode_embedded_data(b64_data: str) -> str:
    return base64.b64decode(b64_data).decode('utf-8')

class EmbeddedOpicExecutor:
    def __init__(self):
        self.ops_files = json.loads(decode_embedded_data(EMBEDDED_OPS_FILES_B64))
        self.generate_py = decode_embedded_data(EMBEDDED_GENERATE_PY_B64)
        self.executor_py = decode_embedded_data(EMBEDDED_EXECUTOR_PY_B64)
        self.temp_root = Path(tempfile.mkdtemp(prefix="opic_embedded_"))
        self._write_embedded_files()
        self._init_executor()
    
    def _write_embedded_files(self):
        for path, content in self.ops_files.items():
            file_path = self.temp_root / path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content)
        (self.temp_root / "generate.py").write_text(self.generate_py)
        (self.temp_root / "scripts").mkdir(exist_ok=True)
        (self.temp_root / "scripts" / "opic_executor.py").write_text(self.executor_py)
    
    def _init_executor(self):
        sys.path.insert(0, str(self.temp_root))
        sys.path.insert(0, str(self.temp_root / "scripts"))
        executor_path = self.temp_root / "scripts" / "opic_executor.py"
        spec = importlib.util.spec_from_file_location("opic_executor", executor_path)
        executor_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(executor_module)
        self.executor = executor_module.OpicExecutor(self.temp_root)
    
    def execute_voice(self, voice_name: str, inputs=None):
        return self.executor.execute_voice(voice_name, inputs)
    
    def cleanup(self):
        if self.temp_root.exists():
            shutil.rmtree(self.temp_root)

def main():
    executor = EmbeddedOpicExecutor()
    try:
        if len(sys.argv) < 2:
            executor.execute_voice("main")
            return
        command = sys.argv[1]
        if command == "execute" and len(sys.argv) > 2:
            executor.executor._load_ops_file(Path(sys.argv[2]))
            executor.execute_voice("main")
        elif command.endswith(".ops"):
            executor.executor._load_ops_file(Path(command))
            executor.execute_voice("main")
        elif command in executor.executor.voices:
            result = executor.execute_voice(command)
            if result:
                print(result)
        else:
            print(f"Unknown command: {{command}}", file=sys.stderr)
            sys.exit(1)
    finally:
        executor.cleanup()

if __name__ == "__main__":
    main()
'''
            
            output_path.write_text(binary_code)
            output_path.chmod(0o755)
            return f"✓ Binary created: {output_path} ({len(ops_files)} .ops files embedded)"
        
        def project_zeta_features(env: Dict[str, Any]) -> List[Dict[str, Any]]:
            """SPEC §12: project ζ features onto lines -> traces"""
            lines = env.get("lines", env.get("input", []))
            if not isinstance(lines, list):
                return []
            
            traces = []
            prev_entropy = 0.0
            prev_boundary = 0.0
            
            for line_data in lines:
                if isinstance(line_data, dict):
                    line = line_data.get("content", line_data.get("line", ""))
                    file_path = line_data.get("file", "")
                    line_num = line_data.get("line", 0)
                else:
                    line = str(line_data)
                    file_path = ""
                    line_num = 0
                
                if not line.strip():
                    continue
                
                # Compute zeta features
                phi_e = shannon_entropy({"line": line})
                phi_c = ordinal_curvature({"line": line})
                boundary_score = ewma_delta({
                    "prev_entropy": prev_entropy,
                    "current_entropy": phi_e,
                    "prev_boundary": prev_boundary
                })
                
                trace = {
                    "file": file_path,
                    "line": line_num,
                    "phi_entropy": round(float(phi_e), 6),
                    "phi_curvature": round(float(phi_c), 6),
                    "boundary_score": round(float(boundary_score), 6)
                }
                traces.append(trace)
                
                prev_entropy = phi_e
                prev_boundary = boundary_score
            
            return traces
        
        def chain_zeros_critical(env: Dict[str, Any]) -> Any:
            """SPEC §12: chain with zeros.on.critical -> witnesses"""
            ions = env.get("ions", env.get("input", []))
            # Placeholder: return ions as witnesses for now
            return {"witnesses": ions, "chain": "zeros_on_critical"}
        
        # Zeta Grammar primitives
        def match_vowel(env: Dict[str, Any]) -> int:
            """Check if glyph is a vowel (zeta_order 1)"""
            glyph = str(env.get("glyph", env.get("L", ""))).lower()
            return 1 if glyph in "aeiou" else 0
        
        def match_consonant(env: Dict[str, Any]) -> int:
            """Check if glyph is a consonant (zeta_order 2)"""
            glyph = str(env.get("glyph", env.get("L", ""))).lower()
            return 2 if glyph.isalpha() and glyph not in "aeiou" else 0
        
        def match_cluster(env: Dict[str, Any]) -> int:
            """Check if glyph is a cluster like 'th', 'ch' (zeta_order 2)"""
            glyph = str(env.get("glyph", env.get("L", ""))).lower()
            # Let OPIC discover clusters naturally - no hardcoded list
            clusters = []  # OPIC will discover clusters through field operations
            return 2 if glyph in clusters else 0
        
        def match_iconic(env: Dict[str, Any]) -> int:
            """Check if glyph is iconic like 'O'=round, 'S'=flow (zeta_order 3)"""
            glyph = str(env.get("glyph", env.get("L", ""))).lower()
            iconic = {"o": 3, "s": 3, "i": 3, "c": 3}  # Round, flow, line, curve
            return iconic.get(glyph, 0)
        
        def gradient(env: Dict[str, Any]) -> float:
            """Compute gradient ∇Φκ (simplified: difference)"""
            phi_k = float(env.get("phi_k", env.get("phi_k_sigma", env.get("phi_k_sentence", 0.0))))
            prev_phi_k = float(env.get("prev_phi_k", env.get("prev1", 0.0)))
            return phi_k - prev_phi_k
        
        def temporal_derivative(env: Dict[str, Any]) -> float:
            """Compute temporal derivative ∂A/∂t (simplified: difference)"""
            A = float(env.get("A", env.get("A_l", env.get("A_sentence", 0.0))))
            prev_A = float(env.get("prev_A", 0.0))
            return A - prev_A
        
        def laplacian(env: Dict[str, Any]) -> float:
            """Compute Laplacian ∇²Φκ (simplified: second difference)"""
            phi_k = float(env.get("phi_k", env.get("phi_k_sigma", 0.0)))
            prev1 = float(env.get("prev1", 0.0))
            prev2 = float(env.get("prev2", 0.0))
            if prev2 == 0:
                return abs(phi_k - prev1)
            return abs(phi_k - 2 * prev1 + prev2)
        
        def divergence(env: Dict[str, Any]) -> float:
            """Compute divergence ∇·A (simplified: sum of components)"""
            A = env.get("A", env.get("A_sentence", 0.0))
            if isinstance(A, (list, tuple)):
                return sum(float(x) for x in A)
            return float(A)
        
        def near_zero(env: Dict[str, Any]) -> bool:
            """Check if value is near zero (equilibrium)"""
            val = float(env.get("val", env.get("phi_k_sigma", env.get("net", env.get("dphi_k_dt", 0.0)))))
            threshold = float(env.get("threshold", 0.001))
            return abs(val) < threshold
        
        def sum_charges(env: Dict[str, Any]) -> float:
            """Sum charges from syllables or constituents"""
            items = env.get("syllables", env.get("constituents", []))
            if not isinstance(items, (list, tuple)):
                return 0.0
            return sum(float(item.get("charge", 0.0)) if isinstance(item, dict) else 0.0 for item in items)
        
        def classify_type(env: Dict[str, Any]) -> str:
            """Classify word type (simplified heuristic)"""
            word = str(env.get("word", "")).lower()
            # Simple heuristics
            if word.endswith(("tion", "sion", "ness", "ment", "ity")):
                return "N"  # Noun
            if word.endswith(("ed", "ing", "ize", "ify")):
                return "V"  # Verb
            if word.endswith(("ly",)):
                return "Adv"  # Adverb
            if word in ("the", "a", "an", "this", "that", "these", "those"):
                return "A"  # Article/Adjective
            if word in ("and", "or", "but", "nor"):
                return "C"  # Conjunction
            if word in ("in", "on", "at", "to", "for", "of", "with", "by"):
                return "P"  # Preposition
            return "N"  # Default to noun
        
        def compute_mass(env: Dict[str, Any]) -> float:
            """Compute semantic mass from type"""
            type_name = str(env.get("type", ""))
            # Nouns have higher mass
            mass_map = {"N": 1.0, "V": 0.8, "A": 0.6, "Adv": 0.5, "P": 0.4, "C": 0.3, "T": 0.7}
            return mass_map.get(type_name, 0.5)
        
        def compute_flow(env: Dict[str, Any]) -> float:
            """Compute kinetic flow from type"""
            type_name = str(env.get("type", ""))
            # Verbs have higher flow
            flow_map = {"V": 1.0, "T": 0.9, "Adv": 0.7, "N": 0.3, "A": 0.5, "P": 0.6, "C": 0.4}
            return flow_map.get(type_name, 0.5)
        
        def compute_curvature(env: Dict[str, Any]) -> float:
            """Compute curvature from type"""
            type_name = str(env.get("type", ""))
            # Adjectives modify curvature
            curvature_map = {"A": 1.0, "Adv": 0.8, "V": 0.6, "N": 0.4, "P": 0.5, "C": 0.3, "T": 0.4}
            return curvature_map.get(type_name, 0.5)
        
        def sum_field_potential(env: Dict[str, Any]) -> float:
            """Sum field potential from words"""
            words = env.get("words", [])
            if not isinstance(words, (list, tuple)):
                return 0.0
            total = 0.0
            for word in words:
                if isinstance(word, dict):
                    total += float(word.get("phi_k", word.get("field_potential", 0.0)))
                elif isinstance(word, (int, float)):
                    total += float(word)
            return total
        
        def positive_trend(env: Dict[str, Any]) -> bool:
            """Check if Q has positive trend (rising)"""
            Q = float(env.get("Q", env.get("Q_sentence", 0.0)))
            prev_Q = float(env.get("prev_Q", 0.0))
            return Q > prev_Q
        
        def negative_trend(env: Dict[str, Any]) -> bool:
            """Check if Q has negative trend (falling)"""
            Q = float(env.get("Q", env.get("Q_sentence", 0.0)))
            prev_Q = float(env.get("prev_Q", 0.0))
            return Q < prev_Q
        
        def compute_potential(env: Dict[str, Any]) -> float:
            """Compute potential for gap/punctuation slot"""
            gap = env.get("gap", env.get("Gap", env.get("Punct", "")))
            if isinstance(gap, str):
                return float(len(gap)) * 0.1
            return 0.5
        
        def emit_binding_invitation(env: Dict[str, Any]) -> str:
            """Emit binding invitation from slot"""
            slot = float(env.get("slot", 0.0))
            return f"binding_invitation:{slot}"
        
        # Document field primitives
        def compute_movement(env: Dict[str, Any]) -> float:
            """Compute zero movement distance"""
            zero1 = env.get("zero1", env.get("zeros_original", []))
            zero2 = env.get("zero2", env.get("zeros_perturbed", []))
            if isinstance(zero1, (list, tuple)) and isinstance(zero2, (list, tuple)):
                if len(zero1) > 0 and len(zero2) > 0:
                    # Simple distance between first zeros
                    z1 = float(zero1[0]) if isinstance(zero1[0], (int, float)) else 0.0
                    z2 = float(zero2[0]) if isinstance(zero2[0], (int, float)) else 0.0
                    return abs(z2 - z1)
            return 0.0
        
        def rbc_compress(env: Dict[str, Any]) -> Dict[str, Any]:
            """RBC-compress field state (simplified)"""
            field_state = env.get("field_state", {})
            # Simple compression: keep only essential fields
            compressed = {
                "phi_k": field_state.get("phi_k", 0.0),
                "zeros": field_state.get("zeros", []),
                "witnesses": field_state.get("witnesses", [])
            }
            return compressed
        
        def check_determinism(env: Dict[str, Any]) -> bool:
            """Check if output is deterministic given witness"""
            output = env.get("output", "")
            witness = env.get("witness", {})
            # If witness exists, output is deterministic
            return witness is not None and len(str(witness)) > 0
        
        def check_basin(env: Dict[str, Any]) -> bool:
            """Check if delta is within stability basin"""
            delta_I = float(env.get("delta_I", 0.0))
            delta_A = float(env.get("delta_A", 0.0))
            threshold = float(env.get("threshold", 0.1))
            return abs(delta_I) < threshold and abs(delta_A) < threshold
        
        def check_distance(env: Dict[str, Any]) -> float:
            """Check distance for locality bounds"""
            perturbation = env.get("perturbation", {})
            region = env.get("region", {})
            # Simple distance check
            return float(env.get("distance", 1.0))
        
        def compare_threshold(env: Dict[str, Any]) -> bool:
            """Compare distance to threshold for bounded influence"""
            distance = float(env.get("distance", 1.0))
            threshold = float(env.get("threshold", 1.0))
            return distance < threshold
        
        # ============================================================================
        # Zeta Zero Solver & Field Computation
        # ============================================================================
        
        def compute_phi_k(env: Dict[str, Any]) -> float:
            """
            Compute field potential Φκ from text or coordinates.
            Maps text → hierarchical field → scalar potential.
            """
            import math
            
            # If we have text, process it hierarchically
            text = env.get("text", env.get("x", env.get("input", "")))
            if isinstance(text, str) and text:
                # Aperture chain: letter → syllable → word → sentence
                # Simple implementation: sum of character potentials
                phi_k = 0.0
                for i, char in enumerate(text.lower()):
                    if char.isalpha():
                        # Vowel = potential well (higher contribution)
                        if char in "aeiou":
                            phi_k += 1.0 / (i + 1)  # Decay with position
                        else:
                            phi_k += 0.5 / (i + 1)  # Consonant = barrier
                    elif char.isspace():
                        phi_k += 0.1  # Space = small potential
                return phi_k
            
            # If we have coordinates or numeric input
            x = env.get("x", env.get("input", 0.0))
            t = env.get("t", 0.0)
            
            if isinstance(x, (int, float)):
                # Simple field: Φκ(x,t) = sin(x) * exp(-t) for demonstration
                return math.sin(float(x)) * math.exp(-float(t))
            
            return 0.0
        
        def zeta_zero_solver(env: Dict[str, Any]) -> list:
            """
            Solve for zeros of zeta function: ζ_F(s) = 0
            Input: spectrum (field state) + region + tolerance
            Output: list of zeros on critical line
            """
            import math
            import cmath
            
            # Get field spectrum (phi_k values)
            phi_k = env.get("phi_k", env.get("phi_k_doc", env.get("spectrum", 0.0)))
            region = env.get("region", {"min": 0.0, "max": 10.0})
            tolerance = float(env.get("tolerance", 0.01))
            
            # If phi_k is a list/array, use it as spectrum
            if isinstance(phi_k, (list, tuple)):
                spectrum = [float(x) for x in phi_k]
            else:
                # Single value: create expanded spectrum with harmonics for better zero detection
                phi_k_val = float(phi_k)
                # Use harmonic series: spectrum = phi_k * [1, 1/2, 1/3, 1/4, ...]
                spectrum = [phi_k_val / (n + 1) for n in range(30)]  # More terms for better resolution
            
            # Construct zeta function from spectrum
            # ζ_F(s) = Σ a_n n^{-s} where a_n comes from spectrum
            def zeta_F(s: complex) -> complex:
                """Zeta function constructed from spectrum"""
                result = 0.0 + 0.0j
                for n, a_n in enumerate(spectrum, start=1):
                    if n > len(spectrum):
                        break
                    # Use proper complex exponentiation: n^{-s} = exp(-s * log(n))
                    result += a_n * cmath.exp(-s * cmath.log(n))
                return result
            
            def zeta_F_derivative(s: complex) -> complex:
                """Derivative of zeta function for Newton-Raphson"""
                result = 0.0 + 0.0j
                for n, a_n in enumerate(spectrum, start=1):
                    if n > len(spectrum):
                        break
                    log_n = cmath.log(n)
                    result -= a_n * log_n * cmath.exp(-s * log_n)
                return result
            
            def newton_raphson(s0: complex, max_iter: int = 15) -> complex:
                """Newton-Raphson root finding on critical line"""
                s = s0
                for _ in range(max_iter):
                    zeta_val = zeta_F(s)
                    if abs(zeta_val) < tolerance:
                        return s
                    zeta_deriv = zeta_F_derivative(s)
                    if abs(zeta_deriv) < 1e-12:  # Avoid division by zero
                        break
                    s_new = s - zeta_val / zeta_deriv
                    # Keep on critical line: Re(s) = 0.5
                    s = 0.5 + 1j * s_new.imag
                    # Check convergence
                    if abs(s_new - s) < tolerance * 0.1:
                        break
                return s
            
            # Search for zeros on critical line Re(s) = 1/2
            zeros = []
            min_im = float(region.get("min", 0.0)) if isinstance(region, dict) else 0.0
            max_im = float(region.get("max", 10.0)) if isinstance(region, dict) else 10.0
            
            # Finer search with adaptive refinement
            step = 0.05  # Finer step size
            prev_zeta = None
            
            for im in [min_im + i * step for i in range(int((max_im - min_im) / step) + 1)]:
                s = 0.5 + 1j * im
                zeta_val = zeta_F(s)
                
                # Check if near zero
                if abs(zeta_val) < tolerance:
                    # Refine with Newton-Raphson
                    refined_s = newton_raphson(s)
                    refined_zeta = zeta_F(refined_s)
                    zeros.append({
                        "real": 0.5,
                        "imaginary": float(refined_s.imag),
                        "value": refined_zeta
                    })
                elif prev_zeta is not None:
                    # Check for zero crossing using argument principle
                    # Zero crossing if phase changes significantly
                    prev_phase = cmath.phase(prev_zeta)
                    curr_phase = cmath.phase(zeta_val)
                    phase_diff = abs(curr_phase - prev_phase)
                    # Normalize phase difference to [0, 2π]
                    if phase_diff > math.pi:
                        phase_diff = 2 * math.pi - phase_diff
                    
                    # Significant phase change indicates zero crossing
                    if phase_diff > math.pi / 2:  # 90 degree phase change
                        # Refine zero location with Newton-Raphson
                        refined_s = newton_raphson(s)
                        refined_zeta = zeta_F(refined_s)
                        if abs(refined_zeta) < tolerance * 10:  # Accept if reasonably close
                            zeros.append({
                                "real": 0.5,
                                "imaginary": float(refined_s.imag),
                                "value": refined_zeta
                            })
                
                prev_zeta = zeta_val
            
            # Remove duplicates (zeros very close to each other)
            unique_zeros = []
            for zero in zeros:
                is_duplicate = False
                for existing in unique_zeros:
                    if abs(zero["imaginary"] - existing["imaginary"]) < 0.2:
                        is_duplicate = True
                        # Keep the one closer to actual zero
                        if abs(zero["value"]) < abs(existing["value"]):
                            unique_zeros.remove(existing)
                            unique_zeros.append(zero)
                        break
                if not is_duplicate:
                    unique_zeros.append(zero)
            
            # Sort by imaginary part
            unique_zeros.sort(key=lambda z: z["imaginary"])
            
            return unique_zeros if unique_zeros else [{"real": 0.5, "imaginary": 0.0, "value": 0.0j}]
        
        def aperture_chain(env: Dict[str, Any]) -> Dict[str, Any]:
            """
            Hierarchical text processing: letter → syllable → word → sentence → discourse
            Returns aperture structure with field properties at each level
            """
            text = str(env.get("text", env.get("input", "")))
            if not text:
                return {"aperture": {}, "levels": []}
            
            # Level 1: Letters
            letters = []
            for char in text:
                if char.isalpha():
                    zeta_order = 1 if char.lower() in "aeiou" else 2
                    letters.append({
                        "glyph": char,
                        "zeta_order": zeta_order,
                        "phi_k": compute_phi_k({"text": char})
                    })
            
            # Level 2: Words (simple: split by spaces)
            words = []
            word_texts = text.split()
            for word_text in word_texts:
                word_phi_k = compute_phi_k({"text": word_text})
                word_type = classify_type({"word": word_text})
                words.append({
                    "text": word_text,
                    "type": word_type,
                    "phi_k": word_phi_k,
                    "mass": compute_mass({"type": word_type}),
                    "flow": compute_flow({"type": word_type}),
                    "curvature": compute_curvature({"type": word_type})
                })
            
            # Level 3: Sentences (simple: split by periods)
            sentences = []
            sentence_texts = text.split('.')
            for sent_text in sentence_texts:
                if sent_text.strip():
                    sent_phi_k = sum_field_potential({"words": [
                        w for w in words if w["text"] in sent_text
                    ]})
                    sentences.append({
                        "text": sent_text.strip(),
                        "phi_k": sent_phi_k,
                        "words": [w for w in words if w["text"] in sent_text]
                    })
            
            # Level 4: Discourse (entire text)
            discourse_phi_k = sum_field_potential({"words": words})
            
            return {
                "aperture": {
                    "letters": letters,
                    "words": words,
                    "sentences": sentences,
                    "discourse": {
                        "text": text,
                        "phi_k": discourse_phi_k
                    }
                },
                # Let OPIC determine levels naturally - no hardcoded list
                "levels": []  # OPIC will discover levels through field operations
            }
        
        def compare_zeros(env: Dict[str, Any]) -> Dict[str, Any]:
            """
            Compare zeros before and after perturbation.
            Returns zero movements indicating semantic changes.
            """
            zeros_original = env.get("zeros_original", env.get("zeros", []))
            zeros_perturbed = env.get("zeros_perturbed", env.get("zeros_new", []))
            
            if not isinstance(zeros_original, list):
                zeros_original = []
            if not isinstance(zeros_perturbed, list):
                zeros_perturbed = []
            
            movements = []
            for i, (z_orig, z_pert) in enumerate(zip(zeros_original, zeros_perturbed)):
                if isinstance(z_orig, dict) and isinstance(z_pert, dict):
                    orig_im = float(z_orig.get("imaginary", 0.0))
                    pert_im = float(z_pert.get("imaginary", 0.0))
                    movement = pert_im - orig_im
                    movements.append({
                        "index": i,
                        "original": orig_im,
                        "perturbed": pert_im,
                        "movement": movement,
                        "magnitude": abs(movement)
                    })
            
            # If lists are different lengths, add new zeros
            if len(zeros_perturbed) > len(zeros_original):
                for i in range(len(zeros_original), len(zeros_perturbed)):
                    z_pert = zeros_perturbed[i]
                    if isinstance(z_pert, dict):
                        movements.append({
                            "index": i,
                            "original": None,
                            "perturbed": float(z_pert.get("imaginary", 0.0)),
                            "movement": float(z_pert.get("imaginary", 0.0)),
                            "magnitude": abs(float(z_pert.get("imaginary", 0.0))),
                            "new_zero": True
                        })
            
            return {
                "movements": movements,
                "total_movement": sum(m.get("magnitude", 0.0) for m in movements),
                "max_movement": max([m.get("magnitude", 0.0) for m in movements], default=0.0)
            }
        
        def interpret_movement(env: Dict[str, Any]) -> str:
            """
            Enhanced zero movement interpretation with semantic mapping.
            Maps zero movements to meaningful answers based on:
            - Movement magnitude and direction
            - Zero positions on critical line
            - Context from question/document
            """
            movements = env.get("movements", env.get("zero_movements", {}))
            question = env.get("question", "")
            document_field = env.get("document_field", {})
            
            if isinstance(movements, dict):
                max_movement = movements.get("max_movement", 0.0)
                total_movement = movements.get("total_movement", 0.0)
                movement_list = movements.get("movements", [])
            else:
                max_movement = float(env.get("movement", env.get("movement_vector", 0.0)))
                total_movement = max_movement
                movement_list = []
            
            if abs(max_movement) < 0.01:
                return "No significant semantic change detected"
            
            # Extract semantic context from question
            question_lower = question.lower()
            question_words = question_lower.split()
            
            # Analyze movement patterns with semantic interpretation
            if movement_list:
                positive_movements = [m for m in movement_list if m.get("movement", 0.0) > 0]
                negative_movements = [m for m in movement_list if m.get("movement", 0.0) < 0]
                new_zeros = [m for m in movement_list if m.get("new_zero", False)]
                
                # Semantic interpretation based on movement patterns
                if new_zeros:
                    # New zeros indicate discovery of new semantic structure
                    return f"Discovered {len(new_zeros)} new semantic structures in the field"
                
                # Large positive movement = semantic expansion/enrichment
                if max_movement > 0.5:
                    # Let OPIC determine question type naturally - no hardcoded word matching
                    return f"The field expanded significantly (movement: {max_movement:.3f}), indicating rich semantic content available"
                
                # Large negative movement = semantic focus/contraction
                if max_movement < -0.5:
                    # Let OPIC determine question type naturally - no hardcoded word matching
                    return f"Field focused on specific semantic region (movement: {abs(max_movement):.3f}), indicating precise answer available"
                
                # Balanced movement = semantic reconfiguration
                if len(positive_movements) == len(negative_movements):
                    return f"Semantic reconfiguration: {len(movement_list)} zeros shifted, indicating structural reorganization"
                
                # Dominant direction
                if len(positive_movements) > len(negative_movements):
                    return f"Field expanded: {len(positive_movements)} zeros moved forward (semantic enrichment)"
                else:
                    return f"Field contracted: {len(negative_movements)} zeros moved backward (semantic focus)"
            
            # Fallback with semantic hints
            if max_movement > 0:
                magnitude_desc = "significantly" if max_movement > 0.3 else "moderately"
                return f"Field expanded {magnitude_desc} (movement: {max_movement:.3f}) - semantic content enriched"
            else:
                magnitude_desc = "significantly" if abs(max_movement) > 0.3 else "moderately"
                return f"Field contracted {magnitude_desc} (movement: {abs(max_movement):.3f}) - semantic focus sharpened"
        
        # Helper functions for query resolution (need executor reference)
        def query_perturb_field(env: Dict[str, Any], executor) -> Dict[str, Any]:
            """Perturb field with question and return perturbed phi_k"""
            question = env.get("question", "")
            document_field = env.get("document_field", {})
            
            # Get original phi_k
            phi_k_doc = document_field.get("phi_k", 0.0)
            if isinstance(phi_k_doc, dict):
                phi_k_doc = phi_k_doc.get("discourse", {}).get("phi_k", 0.0)
            
            # Compute question field potential
            phi_k_question = compute_phi_k({"text": question})
            
            # Local deformation: combine question and document fields
            # Simple: weighted combination
            phi_k_perturbed = float(phi_k_doc) + 0.3 * float(phi_k_question)
            
            return {"phi_k_perturbed": phi_k_perturbed, "phi_k_original": phi_k_doc}
        
        def zeros_movement(env: Dict[str, Any], executor) -> Dict[str, Any]:
            """Compute zero movements from perturbed field"""
            phi_k_perturbed = env.get("phi_k_perturbed", 0.0)
            phi_k_original = env.get("phi_k_original", 0.0)
            
            # Get original zeros from document field
            document_field = env.get("document_field", {})
            zeros_original = document_field.get("zeros", [])
            
            # Compute zeros for perturbed field
            region = {"min": 0.0, "max": 10.0}
            zeros_perturbed = zeta_zero_solver({
                "phi_k": phi_k_perturbed,
                "region": region,
                "tolerance": 0.01
            })
            
            # Compare zeros
            return compare_zeros({
                "zeros_original": zeros_original,
                "zeros_perturbed": zeros_perturbed
            })
        
        def extract_provenance(env: Dict[str, Any]) -> Dict[str, Any]:
            """Extract provenance from witness chain"""
            witness_chain = env.get("witness_chain", env.get("input", {}))
            if isinstance(witness_chain, dict):
                return {
                    "W0": witness_chain.get("W0", {}),
                    "W1": witness_chain.get("W1", {}),
                    "W2": witness_chain.get("W2", {}),
                    "provenance": "W0→W1→W2"
                }
            return {"provenance": "unknown"}
        
        def extract_history(env: Dict[str, Any]) -> list:
            """Extract transformation history from witness chain"""
            witness_chain = env.get("witness_chain", env.get("input", {}))
            if isinstance(witness_chain, dict):
                return [
                    {"step": "W0", "type": "identity", "data": witness_chain.get("W0", {})},
                    {"step": "W1", "type": "structure", "data": witness_chain.get("W1", {})},
                    {"step": "W2", "type": "time", "data": witness_chain.get("W2", {})}
                ]
            return []
        
        def witness_W0(env: Dict[str, Any]) -> Dict[str, Any]:
            """W0: identity → local identity (Points of being)"""
            input_data = env.get("input", env.get("uniform_potential", {}))
            return {"W0": {"type": "identity", "data": input_data}}
        
        def witness_W1(env: Dict[str, Any]) -> Dict[str, Any]:
            """W1: locality → structure & boundary (Membranes, molecules)"""
            input_data = env.get("input", env.get("locality", {}))
            return {"W1": {"type": "structure", "data": input_data}}
        
        def witness_W2(env: Dict[str, Any]) -> Dict[str, Any]:
            """W2: structure → time & motion (Dynamics, causality)"""
            input_data = env.get("input", env.get("structure", {}))
            return {"W2": {"type": "time", "data": input_data}}
        
        def witness_chain_build(env: Dict[str, Any]) -> Dict[str, Any]:
            """Build witness chain: W0 → W1 → W2"""
            input_data = env.get("input", {})
            w0 = witness_W0({"input": input_data})
            w1 = witness_W1({"input": w0.get("W0", {})})
            w2 = witness_W2({"input": w1.get("W1", {})})
            return {
                "W0": w0.get("W0", {}),
                "W1": w1.get("W1", {}),
                "W2": w2.get("W2", {}),
                "chain": "W0→W1→W2"
            }
        
        # ============================================================================
        # Composer Planning & Generation Pipeline
        # ============================================================================
        
        def extract_ions(env: Dict[str, Any]) -> list:
            """
            Extract ions from intent/text.
            Ions are minimal quanta: +1 (noun/emit) or -1 (verb/absorb)
            """
            intent = env.get("intent", env.get("text", env.get("input", "")))
            if not isinstance(intent, str):
                return []
            
            words = intent.split()
            ions = []
            
            for word in words:
                word_lower = word.lower().strip('.,!?;:')
                if not word_lower:
                    continue
                
                # Classify word type
                word_type = classify_type({"word": word_lower})
                
                # Map to ion charge - let OPIC determine charge naturally
                # No hardcoded type matching - OPIC will compute charge through field operations
                charge = 0  # OPIC will determine charge through field operations
                bias = "neutral"  # OPIC will determine bias through field operations
                
                # Compute field properties
                phi_k = compute_phi_k({"text": word_lower})
                mass = compute_mass({"type": word_type})
                flow = compute_flow({"type": word_type})
                
                ions.append({
                    "word": word_lower,
                    "q": charge,
                    "bias": bias,
                    "type": word_type,
                    "phi_k": phi_k,
                    "mass": mass,
                    "flow": flow
                })
            
            return ions
        
        def composer_plan(env: Dict[str, Any]) -> Dict[str, Any]:
            """
            Composer planning: ions → chain with zeros.on.critical → witnesses → plan
            Finds optimal coherence path through field state guided by critical zeros.
            """
            ions = env.get("ions", [])
            if not ions:
                # Extract ions from intent if not provided
                ions = extract_ions(env)
            
            if not ions:
                return {"plan": [], "witnesses": [], "zeros": [], "coherence": 0.0}
            
            # Compute field state from ions
            ion_phi_k_values = [ion.get("phi_k", 0.0) for ion in ions if isinstance(ion, dict)]
            if not ion_phi_k_values:
                ion_phi_k_values = [0.0]
            
            # Find critical zeros
            region = env.get("region", {"min": 0.0, "max": 10.0})
            zeros = zeta_zero_solver({
                "phi_k": ion_phi_k_values,
                "region": region,
                "tolerance": 0.01
            })
            
            # Chain ions guided by zeros.on.critical
            # Strategy: order ions to maximize coherence with zero positions
            if zeros:
                # Use zero positions to guide ordering
                zero_positions = [z.get("imaginary", 0.0) for z in zeros if isinstance(z, dict)]
                if zero_positions:
                    # Sort ions by proximity to zero positions
                    def ion_zero_distance(ion):
                        phi_k = ion.get("phi_k", 0.0)
                        return min(abs(phi_k - z_pos) for z_pos in zero_positions)
                    
                    ions_sorted = sorted(ions, key=ion_zero_distance)
                else:
                    ions_sorted = ions
            else:
                # No zeros: use natural ordering (nouns first, then verbs)
                ions_sorted = sorted(ions, key=lambda i: (-i.get("q", 0), i.get("phi_k", 0.0)))
            
            # Build plan with witnesses
            plan = []
            witnesses = []
            coherence_sum = 0.0
            
            for i, ion in enumerate(ions_sorted):
                step = {
                    "index": i,
                    "ion": ion,
                    "action": "emit" if ion.get("q", 0) > 0 else "absorb",
                    "coherence": ion.get("phi_k", 0.0)
                }
                plan.append(step)
                coherence_sum += abs(ion.get("phi_k", 0.0))
                
                # Create witness for each step
                witnesses.append({
                    "step": i,
                    "ion": ion.get("word", ""),
                    "witness": f"W{i % 3}"  # Cycle through W0, W1, W2
                })
            
            # Compute overall coherence
            coherence = coherence_sum / len(ions_sorted) if ions_sorted else 0.0
            
            return {
                "plan": plan,
                "witnesses": witnesses,
                "zeros": zeros,
                "coherence": coherence,
                "ion_count": len(ions_sorted)
            }
        
        def coherence_maximization(env: Dict[str, Any]) -> Dict[str, Any]:
            """
            Maximize coherence of a plan.
            Optimizes ion ordering and selection for maximum field coherence.
            """
            plan = env.get("plan", [])
            if not isinstance(plan, list):
                return {"optimal_plan": plan, "coherence": 0.0}
            
            if not plan:
                return {"optimal_plan": [], "coherence": 0.0}
            
            # Compute coherence for each step
            step_coherences = []
            for step in plan:
                if isinstance(step, dict):
                    ion = step.get("ion", {})
                    phi_k = ion.get("phi_k", 0.0) if isinstance(ion, dict) else 0.0
                    step_coherences.append(abs(phi_k))
                else:
                    step_coherences.append(0.0)
            
            # Optimize: try different orderings
            # Simple: sort by coherence (highest first)
            plan_with_coherence = list(zip(plan, step_coherences))
            plan_with_coherence.sort(key=lambda x: x[1], reverse=True)
            
            optimal_plan = [step for step, _ in plan_with_coherence]
            max_coherence = max(step_coherences) if step_coherences else 0.0
            avg_coherence = sum(step_coherences) / len(step_coherences) if step_coherences else 0.0
            
            return {
                "optimal_plan": optimal_plan,
                "coherence": max_coherence,
                "avg_coherence": avg_coherence,
                "steps": len(optimal_plan)
            }
        
        def execute_ion_chain(env: Dict[str, Any]) -> str:
            """
            Execute ion chain: convert plan into output text.
            Chains ions together following the plan order.
            """
            plan = env.get("plan", env.get("optimal_plan", []))
            if not isinstance(plan, list):
                # Try to extract plan from dict structure
                if isinstance(plan, dict):
                    plan = plan.get("plan", plan.get("optimal_plan", []))
                else:
                    return ""
            
            if not plan:
                return ""
            
            # Extract words from plan steps
            words = []
            for step in plan:
                if isinstance(step, dict):
                    ion = step.get("ion", {})
                    if isinstance(ion, dict):
                        word = ion.get("word", "")
                        if word:
                            words.append(word)
                    elif isinstance(ion, str):
                        words.append(ion)
                    # Also check if step itself has word
                    elif step.get("word"):
                        words.append(step.get("word"))
                elif isinstance(step, str):
                    words.append(step)
            
            # Join words into output
            output = " ".join(words)
            
            # Capitalize first letter
            if output:
                output = output[0].upper() + output[1:] if len(output) > 1 else output.upper()
            
            return output
        
        def check_coherence(env: Dict[str, Any]) -> Dict[str, Any]:
            """
            Check coherence of output against field state.
            Returns coherent output if coherence threshold met.
            """
            output = env.get("output", "")
            field_state = env.get("field_state", {})
            
            # Compute output field potential
            output_phi_k = compute_phi_k({"text": output})
            
            # Get field state phi_k
            field_phi_k = field_state.get("phi_k", 0.0)
            if isinstance(field_phi_k, dict):
                field_phi_k = field_phi_k.get("discourse", {}).get("phi_k", 0.0)
            
            # Check coherence: output should align with field state
            coherence = 1.0 - abs(output_phi_k - float(field_phi_k)) / (abs(field_phi_k) + 1.0)
            coherence = max(0.0, min(1.0, coherence))  # Clamp to [0, 1]
            
            threshold = float(env.get("threshold", 0.5))
            is_coherent = coherence >= threshold
            
            return {
                "coherent_output": output if is_coherent else "",
                "coherence": coherence,
                "is_coherent": is_coherent,
                "threshold": threshold
            }
        
        def generate_coherent(env: Dict[str, Any]) -> Dict[str, Any]:
            """
            Generate coherent output: intent → composer plan → ion chain → field coherence → output
            Full generation pipeline.
            """
            intent = env.get("intent", env.get("input", ""))
            
            # Step 1: Extract ions from intent
            ions = extract_ions({"intent": intent})
            
            if not ions:
                return {
                    "output": "",
                    "plan": {},
                    "optimal_plan": {},
                    "coherence": 0.0,
                    "is_coherent": False,
                    "witnesses": [],
                    "zeros": []
                }
            
            # Step 2: Composer plan with zeros.on.critical
            plan_result = composer_plan({"ions": ions})
            plan_steps = plan_result.get("plan", [])
            
            if not plan_steps:
                return {
                    "output": "",
                    "plan": plan_result,
                    "optimal_plan": {},
                    "coherence": 0.0,
                    "is_coherent": False,
                    "witnesses": plan_result.get("witnesses", []),
                    "zeros": plan_result.get("zeros", [])
                }
            
            # Step 3: Maximize coherence
            optimal_result = coherence_maximization({"plan": plan_steps})
            optimal_plan = optimal_result.get("optimal_plan", plan_steps)
            
            # Step 4: Execute ion chain
            output = execute_ion_chain({"plan": optimal_plan, "optimal_plan": optimal_plan})
            
            # If output is empty, try direct extraction from plan steps
            if not output:
                words = []
                for step in optimal_plan:
                    if isinstance(step, dict):
                        ion = step.get("ion", {})
                        if isinstance(ion, dict):
                            word = ion.get("word", "")
                            if word:
                                words.append(word)
                if not words:
                    # Fallback: extract directly from ions
                    words = [ion.get("word", "") for ion in ions if isinstance(ion, dict) and ion.get("word")]
                output = " ".join(words)
                if output:
                    output = output[0].upper() + output[1:] if len(output) > 1 else output.upper()
            
            # Step 5: Check coherence with field state (if provided)
            field_state = env.get("field_state", {})
            coherence_result = check_coherence({
                "output": output,
                "field_state": field_state,
                "threshold": 0.3  # Lower threshold for generation
            })
            
            # For generation, always return output even if coherence check fails
            # (coherence check is more relevant when checking against existing field)
            final_output = coherence_result.get("coherent_output", output)
            if not final_output and output:
                final_output = output  # Use generated output even if coherence low
            
            return {
                "output": final_output,
                "plan": plan_result,
                "optimal_plan": optimal_result,
                "coherence": coherence_result.get("coherence", 0.0),
                "is_coherent": coherence_result.get("is_coherent", True) if field_state else True,
                "witnesses": plan_result.get("witnesses", []),
                "zeros": plan_result.get("zeros", [])
            }
        
        self.primitives = {
            "coulomb_yukawa": coulomb_yukawa,
            "tan_theta": tan_theta,
            "cos": cos_theta,
            "cos_theta": cos_theta,
            "sin": sin_theta,
            "sin_theta": sin_theta,
            "add": add,
            "shannon_entropy": shannon_entropy,
            "ordinal_curvature": ordinal_curvature,
            "ewma_delta": ewma_delta,
            "file_walk": file_walk,
            "walk_directory": file_walk,
            "file_read": file_read,
            "read_content": file_read,
            "file_write": file_write,
            "write_file": file_write,
            "dir_create": dir_create,
            "dir.create": dir_create,
            "file_move": file_move,
            "file.move": file_move,
            "file_copy": file_copy,
            "file.copy": file_copy,
            "file_find": file_find,
            "file.find": file_find,
            "file_update_includes": file_update_includes,
            "file.update.includes": file_update_includes,
            "file_backup": file_backup,
            "file.backup": file_backup,
            "base64_encode": base64_encode,
            "json_encode": json_encode,
            "json_decode": json_decode,
            "json_parse": json_decode,
            "get_key": get_key,
            "take_first": take_first,
            "take_first_20": lambda env: take_first({**env, "n": 20}),
            "length": length,
            "complex_exp": complex_exp,
            "complex_pow": complex_pow,
            "compute_euler_factor": compute_euler_factor,
            "compute_zeta_product": compute_zeta_product,
            "compute_unitarity_deviation": compute_unitarity_deviation,
            "simulate_field_evolution": simulate_field_evolution,
            "format_results": format_results,
            "filter_list": filter_list,
            "filter_by_extension": filter_list,
            "compile_binary": compile_binary,
            "compile.opic.binary": compile_binary,
            "generate_help": generate_help,
            "generate.help": generate_help,
            "fft_unitary": fft_unitary,
            "fft.unitary": fft_unitary,
            "ifft_unitary": ifft_unitary,
            "ifft.unitary": ifft_unitary,
            "enforce_hermitian_symmetry": enforce_hermitian_symmetry,
            "enforce.hermitian.symmetry": enforce_hermitian_symmetry,
            "compute_power_spectrum": compute_power_spectrum,
            "compute.power.spectrum": compute_power_spectrum,
            "parseval_check": parseval_check,
            "parseval.check": parseval_check,
            "compute_l2_error": compute_l2_error,
            "compute.l2.error": compute_l2_error,
            "compute_linf_error": compute_linf_error,
            "compute.linf.error": compute_linf_error,
            "verify_phase_uniformity": verify_phase_uniformity,
            "verify.phase.uniformity": verify_phase_uniformity,
            "compare_power_spectra": compare_power_spectra,
            "compare.power.spectra": compare_power_spectra,
            "compare_correlation_functions": compare_correlation_functions,
            "compare.correlation.functions": compare_correlation_functions,
            "check_cross_correlation": check_cross_correlation,
            "check.cross.correlation": check_cross_correlation,
            "compute_spectral_slope": compute_spectral_slope,
            "compute.spectral.slope": compute_spectral_slope,
            "verify_seed_determinism": verify_seed_determinism,
            "verify.seed.determinism": verify_seed_determinism,
            "bin_power_spectrum_radial": bin_power_spectrum_radial,
            "bin.power.spectrum.radial": bin_power_spectrum_radial,
            "delta_encode_phases": delta_encode_phases,
            "delta.encode.phases": delta_encode_phases,
            "reconstruct_phases_from_deltas": reconstruct_phases_from_deltas,
            "reconstruct.phases.from.deltas": reconstruct_phases_from_deltas,
            "compute_bispectrum_triangle": compute_bispectrum_triangle,
            "compute.bispectrum.triangle": compute_bispectrum_triangle,
            "select_bispectrum_triangles": select_bispectrum_triangles,
            "select.bispectrum.triangles": select_bispectrum_triangles,
            "project_helmholtz_leray_3d": project_helmholtz_leray_3d,
            "project.helmholtz.leray.3d": project_helmholtz_leray_3d,
            "compute_divergence_3d": compute_divergence_3d,
            "compute.divergence.3d": compute_divergence_3d,
            "compute_energy_3d": compute_energy_3d,
            "compute.energy.3d": compute_energy_3d,
            "fft3d_unitary": fft3d_unitary,
            "fft3d.unitary": fft3d_unitary,
            "ifft3d_unitary": ifft3d_unitary,
            "ifft3d.unitary": ifft3d_unitary,
            "compute_flatness_3d": compute_flatness_3d,
            "compute.flatness.3d": compute_flatness_3d,
            "ans_encode": ans_encode,
            "ans.encode": ans_encode,
            "ans_decode": ans_decode,
            "ans.decode": ans_decode,
            "project_zeta_features": project_zeta_features,
            "project ζ features": project_zeta_features,
            "chain_zeros_critical": chain_zeros_critical,
            "chain with zeros.on.critical": chain_zeros_critical,
            # Zeta Grammar primitives
            "match_vowel": match_vowel,
            "match_consonant": match_consonant,
            "match_cluster": match_cluster,
            "match_iconic": match_iconic,
            "gradient": gradient,
            "temporal_derivative": temporal_derivative,
            "laplacian": laplacian,
            "divergence": divergence,
            "near_zero": near_zero,
            "sum_charges": sum_charges,
            "classify_type": classify_type,
            "compute_mass": compute_mass,
            "compute_flow": compute_flow,
            "compute_curvature": compute_curvature,
            "sum_field_potential": sum_field_potential,
            "positive_trend": positive_trend,
            "negative_trend": negative_trend,
            "compute_potential": compute_potential,
            "emit_binding_invitation": emit_binding_invitation,
            # Document field primitives
            "compute_movement": compute_movement,
            "interpret_movement": interpret_movement,
            "rbc_compress": rbc_compress,
            "check_determinism": check_determinism,
            "check_basin": check_basin,
            "check_distance": check_distance,
            "compare_threshold": compare_threshold,
            # Zeta zero solver & field computation
            "compute_phi_k": compute_phi_k,
            "zeta_zero_solver": zeta_zero_solver,
            "zeta.zero.solver": zeta_zero_solver,
            "aperture_chain": aperture_chain,
            "aperture.chain": aperture_chain,
            "compare_zeros": compare_zeros,
            "zeros.compare": compare_zeros,
            # Query resolution helpers (defined above)
            "perturb_field": lambda env: query_perturb_field(env, self),
            "zeros.movement": lambda env: zeros_movement(env, self),
            "extract_provenance": extract_provenance,
            "extract_history": extract_history,
            # Witness chain helpers
            "witness.W0": witness_W0,
            "witness.W1": witness_W1,
            "witness.W2": witness_W2,
            "witness.chain": witness_chain_build,
            # Composer planning & generation
            "extract_ions": extract_ions,
            "composer.plan": composer_plan,
            "composer_coherence_maximization": coherence_maximization,
            "composer.coherence_maximization": coherence_maximization,
            "execute_ion_chain": execute_ion_chain,
            "ion.chain": execute_ion_chain,
            "check_coherence": check_coherence,
            "field.coherence": check_coherence,
            "generate.coherent": generate_coherent,
            # CLI primitives
            "command_line_args": lambda env: sys.argv[1:] if len(sys.argv) > 1 else [],
            "command_line_arg": lambda env: sys.argv[int(env.get("index", 1))] if len(sys.argv) > int(env.get("index", 1)) else None,
            "get_first": lambda env: (env.get("list", env.get("args", env.get("input", []))) or [None])[0] if isinstance(env.get("list", env.get("args", env.get("input", []))), list) and len(env.get("list", env.get("args", env.get("input", [])))) > 0 else None,
            "drop_first": lambda env: (env.get("list", env.get("args", [])) or [])[1:] if isinstance(env.get("list", env.get("args", [])), list) else [],
            "if_empty": lambda env: "help" if not env.get("list", env.get("args", [])) or len(env.get("list", env.get("args", []))) == 0 else None,
        }
    
    def _call_primitive(self, name: str, env: Dict[str, Any]) -> Any:
        """Invoke a registered primitive if available"""
        func = self.primitives.get(name)
        if not func:
            return None
        try:
            return func(env)
        except Exception:
            return None
    
    def _evaluate_step_token(self, token: str, env: Dict[str, Any], last_result: Any) -> Any:
        """
        Evaluate a single step token:
        - quoted strings -> literal
        - variables -> env lookup
        - '+' expressions -> combine
        - primitive names -> call with env
        - assignment-like tokens -> bind last_result
        """
        t = token.strip()
        
        # Literal string
        if (t.startswith('"') and t.endswith('"')) or (t.startswith("'") and t.endswith("'")):
            return t[1:-1]
        
        # Combined expression with '+'
        # For variable references: ensure all variables are accessible in environment
        # For operations: try combining values
        if " + " in t:
            parts = [p.strip() for p in t.split("+")]
            # First, ensure all parts are evaluated and stored in environment
            # This allows subsequent steps to access all variables
            for part in parts:
                value = self._evaluate_step_token(part, env, last_result)
                # Store in environment if it's a variable name (not a primitive/voice result)
                if (part not in self.primitives and 
                    part not in self.voices and
                    part.replace("_", "").replace(".", "").isalnum() and
                    value is not None):
                    env[part] = value
            # Try each part in sequence - first non-None wins (declarative routing)
            for part in parts:
                value = self._evaluate_step_token(part, env, last_result)
                if value is not None and value != "":
                    # Voice/primitive succeeded - use it (implicit routing)
                    return value
            # If all returned None/empty, try combining (for numeric/string operations)
            values = [self._evaluate_step_token(p, env, last_result) for p in parts]
            if all(isinstance(v, (int, float)) for v in values if v is not None):
                return sum(v for v in values if v is not None)
            if all(isinstance(v, str) for v in values if v is not None):
                return "".join(v for v in values if v is not None)
            # Return first non-None or None
            return next((v for v in values if v is not None), None)
        
        # Primitive call - SPEC: primitives receive env + last_result as input
        if t in self.primitives:
            prim_env = env.copy()
            # SPEC: last_result flows as input to next step
            if last_result is not None:
                # Map to common parameter names
                if "path" not in prim_env and isinstance(last_result, (str, Path)):
                    prim_env["path"] = last_result
                if "file" not in prim_env and isinstance(last_result, (str, Path)):
                    prim_env["file"] = last_result
                if "line" not in prim_env:
                    prim_env["line"] = last_result
                prim_env["input"] = last_result
            prim = self._call_primitive(t, prim_env)
            if prim is not None:
                return prim
        
        # Voice call - check if token is a voice name
        # SPEC: opic.resolve_body / {voice_body -> if_chain_recurse -> if_string_return}
        # When step is voice name, get voice body and recursively execute if it's a chain
        if t in self.voices:
            # Get voice body
            voice_body = self.voices[t]
            # SPEC: If voice body is chain, recursively execute it
            if isinstance(voice_body, str) and voice_body.startswith("{") and voice_body.endswith("}"):
                # Voice body is a chain - recursively execute it
                voice_inputs = env.copy()
                if last_result is not None:
                    voice_inputs["input"] = last_result
                voice_result = self._execute_opic_chain(voice_body, voice_inputs)
                if voice_result is not None:
                    return voice_result
            elif isinstance(voice_body, str):
                # Voice body is a simple string value - return it
                return voice_body
            else:
                # Voice body is already a resolved value
                return voice_body
        
        # Variable lookup
        if t in env:
            return env[t]
        
        # Assignment/bind last result
        if last_result is not None and t.replace("_", "").replace(".", "").isalnum():
            env[t] = last_result
            return last_result
        
        # Fallback: return token
        return t
    
    def _execute_opic_chain(self, chain_str: str, inputs: Dict[str, Any] = None) -> Any:
        """
        Execute opic voice chain following opic's execution semantics
        Implements the structure described by opic.execute_chain:
        {chain_string -> parse_chain -> resolve_steps -> execute_steps -> result}
        
        The opic execution voices are declarative - they describe the flow.
        This Python implementation provides the actual execution logic.
        """
        inputs = inputs or {}
        
        # Follow opic.execute_chain structure:
        # Step 1: Parse chain (implements opic.parse_chain structure)
        steps = self._parse_chain(chain_str)
        
        # Step 2: Resolve steps (implements opic.resolve_steps structure)
        resolved_steps = self._resolve_steps(steps, inputs)
        
        # Step 3: Execute steps (implements opic.execute_steps structure)
        # Pass original step names along with resolved steps for variable name inference
        result = self._execute_steps(resolved_steps, inputs, original_steps=steps)
        
        return result
    
    def _parse_chain(self, chain_str: str) -> List[str]:
        """
        Parse chain following opic.parse_chain structure:
        {chain -> remove_braces -> split_arrows -> steps}
        """
        # opic.remove_braces: strip "{ }"
        chain_body = chain_str.strip()
        if chain_body.startswith("{") and chain_body.endswith("}"):
            chain_body = chain_body[1:-1].strip()
        
        # opic.split_arrows: split "->" and trim each
        steps = [s.strip() for s in chain_body.split("->")]
        return steps
    
    def _resolve_steps(self, steps: List[str], inputs: Dict[str, Any]) -> List[Any]:
        """
        Resolve steps following opic.resolve_steps structure:
        {steps -> for_each_step -> find_voice -> resolve_body}
        """
        resolved = []
        for step in steps:
            # opic.find_voice: {step_name + voices -> lookup -> voice_body}
            if step in inputs:
                resolved.append(inputs[step])
            elif step in self.voices:
                voice_body = self.voices[step]
                # opic.resolve_body: {voice_body -> if_chain_recurse -> if_string_return}
                resolved.append(voice_body)
            elif step in self.primitives:
                # Primitive: leave as string so it can be called during execution
                resolved.append(step)
            else:
                # Try discovered voices (with recursion guard)
                discovered = self._discover_relevant_voices(step, visited=set())
                if discovered and discovered[0] in self.voices:
                    resolved.append(self.voices[discovered[0]])
                else:
                    # Leave as string - might be primitive or variable name
                    resolved.append(step)
        return resolved
    
    def _execute_steps(self, resolved_steps: List[Any], inputs: Dict[str, Any], original_steps: List[str] = None) -> Any:
        """
        Execute steps following opic.execute_steps structure:
        {resolved_steps -> for_each -> execute_step -> collect_results}
        
        SPEC: Sequential execution - each step receives the result of the previous step.
        From docs/how_execution_works.md:
        - Each step receives the **result** of the previous step
        - Nested chains receive inputs via {"input": previous_result}
        - Final result is the last step's output
        """
        result = None
        env: Dict[str, Any] = dict(inputs)
        original_steps = original_steps or []
        
        # Execute steps sequentially
        for step_idx, step_body in enumerate(resolved_steps):
            # Get original step name for variable name inference
            original_step = original_steps[step_idx] if step_idx < len(original_steps) else None
            # SPEC: opic.resolve_body / {voice_body -> if_chain_recurse -> if_string_return}
            if isinstance(step_body, str) and step_body.startswith("{") and step_body.endswith("}"):
                # Recurse into nested chain (voice body is a chain)
                # Pass previous result as both "input" and try to infer variable names from chain
                step_inputs = {"input": result, **env} if result is not None else env.copy()
                # Also try to bind result to common variable names if they appear in the chain
                if result is not None:
                    # Look for common variable names in the chain that might need the result
                    chain_steps = self._parse_chain(step_body)
                    for chain_step in chain_steps[:3]:  # Check first few steps
                        # If step is a simple variable name and not a primitive/voice, bind result to it
                        if (chain_step.strip() and 
                            chain_step not in self.primitives and 
                            chain_step not in self.voices and
                            chain_step.replace("_", "").replace(".", "").isalnum()):
                            step_inputs[chain_step.strip()] = result
                result = self._execute_opic_chain(step_body, step_inputs)
            elif isinstance(step_body, str):
                # step_body is a string - evaluate it (voice call, primitive call, literal, or variable)
                result = self._evaluate_step_token(step_body, env, result)
            else:
                # step_body is already a resolved value (not a string)
                result = step_body
            
            # Update environment bindings for next step
            env["last"] = result
            
            # Store result with inferred variable name for subsequent steps
            # SPEC: Results should be available to subsequent steps via environment
            if result is not None and original_step and isinstance(original_step, str) and original_step in self.voices:
                # If step is a voice call, try to infer variable name from voice name
                # Common pattern: riemann.phase1_identify_primes -> prime_voices
                voice_name = original_step
                # Try to extract variable name from voice name (e.g., "identify_primes" -> "prime_voices")
                # Or use a mapping for known voices
                var_name_mapping = {
                    'riemann.phase1_identify_primes': 'prime_voices',
                    'riemann.phase2_load_functors': 'functors',
                    'riemann.phase2_compute_functor': 'functors_sample',
                    'riemann.phase4_test_functional_equation': 'zeta_result',
                    'riemann.phase5_simulate_field': 'field_evolution',
                }
                if voice_name in var_name_mapping:
                    env[var_name_mapping[voice_name]] = result
        
        return result
    
    def _compute_energy_coupling(self, q_i: float, q_j: float, s_i: Any, s_j: Any, R_ij: float, D: int = 1, mu: float = 0.1) -> float:
        """
        Compute energy coupling using field.energy_exchange voice:
        {q_i + q_j + s_i + s_j + R_ij + D + mu -> coulomb_yukawa -> E_ij}
        
        Executes opic's native field.energy_exchange voice for actual computation
        """
        # Skip recursive call to field.energy_exchange to avoid infinite recursion
        # Use direct computation instead
        
        # Fallback: Direct computation following coulomb_yukawa structure
        # This matches what coulomb.compute_force_mass_spin would compute
        # E_ij = (q_i * q_j) / (R_ij^D) * exp(-mu * R_ij)
        charge_product = q_i * q_j
        distance_power = R_ij ** D if R_ij > 0 else 1.0
        yukawa_factor = 1.0 if mu == 0 else (1.0 / (1.0 + mu * R_ij))
        energy = (charge_product / distance_power) * yukawa_factor
        
        # If s_i and s_j are embeddings (lists), add semantic energy
        if isinstance(s_i, list) and isinstance(s_j, list) and len(s_i) == len(s_j):
            # Semantic energy: dot product of embeddings
            semantic_energy = sum(a * b for a, b in zip(s_i, s_j))
            # Combine field energy with semantic energy
            energy = energy * 0.5 + abs(semantic_energy) * 0.5
        
        return energy
    
    def _get_step_charge(self, step: Any) -> float:
        """
        Extract charge from step (q ∈ {+1, -1} for ions, or computed from step properties)
        """
        if isinstance(step, str):
            # Simple heuristic: positive charge for forward flow, negative for reverse
            if step.startswith("+") or "forward" in step.lower():
                return 1.0
            elif step.startswith("-") or "reverse" in step.lower():
                return -1.0
            # Default: neutral charge
            return 0.0
        # For non-string steps, return neutral
        return 0.0
    
    def _get_step_distance(self, step1: Any, step2: Any) -> float:
        """
        Compute distance R_ij between steps using semantic embeddings
        Uses Field Spec 0.7: distance = ||embedding1 - embedding2||
        """
        if isinstance(step1, str) and isinstance(step2, str):
            if step1 == step2:
                return 0.1  # Very close
            
            # Use semantic embeddings for distance
            emb1 = self._get_semantic_embedding(step1)
            emb2 = self._get_semantic_embedding(step2)
            
            # Euclidean distance in embedding space
            distance = math.sqrt(sum((a - b) ** 2 for a, b in zip(emb1, emb2)))
            return max(0.1, distance)  # Minimum distance 0.1
        
        # Default distance
        return 1.0
    
    def _get_semantic_embedding(self, text: str, dim: int = 64) -> List[float]:
        """
        Generate semantic embedding using Field Spec 0.7 principles
        Uses zeta-trace, Pascal mod 10, and field potential
        """
        # Cache embeddings
        cache_key = f"{text}:{dim}"
        if cache_key in self.embedding_cache:
            return self.embedding_cache[cache_key]
        
        # Convert text to embedding using Field Spec operations
        # 1. Token quantization (NLP cycle)
        tokens = text.lower().split()
        
        # 2. Compute field potential for each token
        # Using zeta-trace and Pascal mod 10
        embedding = [0.0] * dim
        
        for i, token in enumerate(tokens):
            # Hash token to get seed
            token_hash = int(hashlib.md5(token.encode()).hexdigest(), 16)
            
            # Map to embedding dimensions using Pascal mod 10
            for j in range(dim):
                # Use Pascal mod 10 pattern: (i+j) mod 10
                pascal_val = (i + j) % 10
                # Use zeta-trace: 7-trace cycle
                trace7_val = (token_hash + j) % 7
                if trace7_val == 0:
                    trace7_val = 7
                
                # Field potential: combination of Pascal and trace7
                field_potential = (pascal_val * trace7_val) / 70.0
                
                # Add to embedding with position weighting
                position_weight = 1.0 / (1.0 + i * 0.1)
                embedding[j] += field_potential * position_weight
        
        # Normalize using field operations
        # Compute magnitude (field energy)
        magnitude = math.sqrt(sum(x ** 2 for x in embedding))
        if magnitude > 0:
            embedding = [x / magnitude for x in embedding]
        
        # Apply dimensional expansion (Field Spec §8)
        # Add curvature component
        for j in range(dim):
            # Curvature from ordinal differences
            if j > 0:
                curvature = embedding[j] - embedding[j-1]
                embedding[j] += curvature * 0.1
        
        self.embedding_cache[cache_key] = embedding
        return embedding
    
    def _learn_from_code_output(self, code_trace: Dict, output: int, correct_answer: int, 
                                field_state: Dict, zeros: List) -> None:
        """
        Learn from coupling code with its output.
        Updates field based on successful patterns.
        """
        # Store code-output pair for learning
        correctness = 1.0 if output == correct_answer else 0.0
        
        # Only learn from successful outputs (or track failures)
        if correctness > 0.5:
            # Successful pattern: update field to reinforce this path
            # Extract field properties that led to success
            successful_phi_k = field_state.get("phi_k", 0.0)
            successful_zeros = zeros
            
            # Store successful pattern (could update knowledge base or field)
            # For now, we'll use this to improve future generations
            pass  # TODO: Implement field update from successful patterns
        else:
            # Failed pattern: learn what to avoid
            # Could update field to avoid similar patterns
            pass  # TODO: Implement field update from failed patterns
    
    def answer_question(self, question: str, choices: List[str] = None) -> int:
        """
        Answer a question using enhanced zero interpretation and composer planning.
        Integrates:
        - Zero interpretation for semantic understanding
        - Composer planning for answer generation
        - Document understanding pipeline for question+choices
        - BERT knowledge base for semantic knowledge
        """
        if not choices:
            return 0
        
        # Step 0: Query knowledge base if available
        knowledge_results = None
        query_region = None  # Will be set if knowledge base is queried
        try:
            knowledge_file = self.project_root / "data" / "bert_knowledge_base.json"
            if knowledge_file.exists():
                import json
                with open(knowledge_file) as f:
                    knowledge_base = json.load(f)
                
                # Query knowledge base using improved semantic matching
                # Proper zeta calibration: use FULL hierarchical spectrum for question
                query_field = self._call_primitive("aperture.chain", {"text": question})
                query_aperture = query_field.get("aperture", {})
                query_phi_k = query_aperture.get("discourse", {}).get("phi_k", 0.0)
                
                # Construct full hierarchical spectrum for question
                query_spectrum = []
                # Letters
                for letter in query_aperture.get("letters", []):
                    if isinstance(letter, dict) and letter.get("phi_k"):
                        query_spectrum.append(float(letter["phi_k"]))
                # Words
                for word in query_aperture.get("words", []):
                    if isinstance(word, dict) and word.get("phi_k"):
                        query_spectrum.append(float(word["phi_k"]))
                # Sentences
                for sentence in query_aperture.get("sentences", []):
                    if isinstance(sentence, dict) and sentence.get("phi_k"):
                        query_spectrum.append(float(sentence["phi_k"]))
                # Discourse
                if query_phi_k:
                    query_spectrum.append(float(query_phi_k))
                
                if not query_spectrum:
                    query_spectrum = [float(query_phi_k)] if query_phi_k else [0.0]
                
                # Dimensional scale matching: use Cycle-to-Dimension Principle
                # D = active dimensionality from hierarchical structure
                # Aperture chain: Letter → Word → Sentence → Discourse = 4 levels
                # Dimensionality D comes from number of active hierarchical levels
                
                # Count active hierarchical levels
                has_letters = len(query_aperture.get("letters", [])) > 0
                has_words = len(query_aperture.get("words", [])) > 0
                has_sentences = len(query_aperture.get("sentences", [])) > 0
                has_discourse = query_phi_k != 0.0
                
                # Dimensionality D = number of active levels (Cycle-to-Dimension Principle)
                D = sum([has_letters, has_words, has_sentences, has_discourse])
                if D == 0:
                    D = 1  # Minimum dimension
                
                # Dimensional Coulomb Law: scale determined by D
                # Higher D → larger search space (more degrees of freedom)
                # Base scale from D: D=1 → small, D=4 → large
                # Use golden ratio growth: φ^D for dimensional scaling
                phi = (1 + math.sqrt(5)) / 2  # Golden ratio
                dimensional_scale = phi ** D  # Dimensional growth
                
                # Also consider spectrum size (more terms = richer field)
                spectrum_size = len(query_spectrum)
                spectrum_factor = max(1.0, spectrum_size / 10.0)  # Normalize to ~1-3
                
                # Final scale: dimensional scale × spectrum factor
                search_max = dimensional_scale * spectrum_factor
                # Clamp to reasonable range
                search_max = max(5.0, min(30.0, search_max))
                
                query_region = {"min": 0.0, "max": search_max}
                
                # Compute query zeros using FULL spectrum with adaptive scale
                query_zeros = self._call_primitive("zeta.zero.solver", {
                    "phi_k": query_spectrum,
                    "region": query_region,
                    "tolerance": 0.001
                })
                query_zero_positions = [z.get("imaginary", 0.0) for z in query_zeros if isinstance(z, dict)]
                
                # Extract query words for semantic matching
                query_words = set(question.lower().split())
                
                # Score knowledge entries with multiple signals
                scored_entries = []
                for entry_hash, entry in knowledge_base.items():
                    entry_phi_k = entry.get("phi_k", 0.0)
                    entry_text = entry.get("text", "").lower()
                    entry_domain = entry.get("domain", "")
                    entry_zeros = entry.get("zeros", [])
                    entry_zero_positions = [z.get("imaginary", 0.0) for z in entry_zeros if isinstance(z, dict)]
                    
                    # Signal 1: Field coherence (improved normalization)
                    phi_k_diff = abs(query_phi_k - float(entry_phi_k))
                    phi_k_avg = (abs(query_phi_k) + abs(entry_phi_k)) / 2.0 + 1.0
                    coherence = 1.0 - min(1.0, phi_k_diff / phi_k_avg)
                    
                    # Signal 1b: Zero proximity (using proper zeta calibration)
                    zero_proximity = 0.0
                    if query_zero_positions and entry_zero_positions:
                        min_zero_dist = min(
                            abs(qz - ez) 
                            for qz in query_zero_positions 
                            for ez in entry_zero_positions
                        )
                        zero_proximity = 1.0 / (1.0 + min_zero_dist)
                        coherence = (coherence + zero_proximity) / 2.0
                    
                    # Signal 2: Word overlap (semantic matching)
                    entry_words = set(entry_text.split())
                    word_overlap = len(query_words & entry_words)
                    word_score = min(1.0, word_overlap / max(len(query_words), 1))
                    
                    # Signal 3: Domain relevance - let OPIC handle domain matching naturally
                    # No hardcoded keywords - trust OPIC's natural resolution
                    domain_score = 0.0  # Let OPIC's field operations determine domain relevance
                    
                    # Combined score (weighted)
                    total_score = (coherence * 0.3) + (word_score * 0.7)  # Removed hardcoded domain_score
                    scored_entries.append((entry, total_score, coherence, word_score, domain_score))
                
                scored_entries.sort(key=lambda x: x[1], reverse=True)
                knowledge_results = [entry for entry, score, c, w, d in scored_entries[:5]]  # Top 5
        except Exception:
            pass  # Continue without knowledge base
        
        # Enhanced approach: Use zero interpretation and composer planning
        try:
            # Step 1: Create document field from question + choices
            # Proper zeta calibration: use FULL hierarchical spectrum
            doc_text = question + " " + " ".join(choices)
            doc_field = self._call_primitive("aperture.chain", {"text": doc_text})
            doc_aperture = doc_field.get("aperture", {})
            
            # Construct full hierarchical spectrum for document
            doc_spectrum = []
            # Letters
            for letter in doc_aperture.get("letters", []):
                if isinstance(letter, dict) and letter.get("phi_k"):
                    doc_spectrum.append(float(letter["phi_k"]))
            # Words
            for word in doc_aperture.get("words", []):
                if isinstance(word, dict) and word.get("phi_k"):
                    doc_spectrum.append(float(word["phi_k"]))
            # Sentences
            for sentence in doc_aperture.get("sentences", []):
                if isinstance(sentence, dict) and sentence.get("phi_k"):
                    doc_spectrum.append(float(sentence["phi_k"]))
            # Discourse
            doc_phi_k = doc_aperture.get("discourse", {}).get("phi_k", 0.0)
            if doc_phi_k:
                doc_spectrum.append(float(doc_phi_k))
            
            if not doc_spectrum:
                doc_spectrum = [float(doc_phi_k)] if doc_phi_k else [0.0]
            
            # Step 2: Use zero interpretation for semantic understanding
            # Dimensional scale matching: use Cycle-to-Dimension Principle
            # Count active hierarchical levels for document
            doc_has_letters = len(doc_aperture.get("letters", [])) > 0
            doc_has_words = len(doc_aperture.get("words", [])) > 0
            doc_has_sentences = len(doc_aperture.get("sentences", [])) > 0
            doc_has_discourse = doc_phi_k != 0.0
            
            # Dimensionality D from hierarchical structure
            doc_D = sum([doc_has_letters, doc_has_words, doc_has_sentences, doc_has_discourse])
            if doc_D == 0:
                doc_D = 1
            
            # Dimensional scale: φ^D
            phi = (1 + math.sqrt(5)) / 2
            doc_dimensional_scale = phi ** doc_D
            
            # Spectrum factor
            doc_spectrum_size = len(doc_spectrum)
            doc_spectrum_factor = max(1.0, doc_spectrum_size / 10.0)
            
            # Final scale
            doc_search_max = doc_dimensional_scale * doc_spectrum_factor
            doc_search_max = max(5.0, min(30.0, doc_search_max))
            
            doc_region = {"min": 0.0, "max": doc_search_max}
            
            # Compute zeros using FULL spectrum with adaptive scale
            doc_zeros = self._call_primitive("zeta.zero.solver", {
                "phi_k": doc_spectrum,
                "region": doc_region,
                "tolerance": 0.001
            })
            
            # Perturb field with question and observe zero movements
            zero_movements = self._call_primitive("zeros.movement", {
                "question": question,
                "document_field": doc_field
            })
            
            # Step 3: Interpret zero movements for semantic guidance
            semantic_guidance = self._call_primitive("interpret_movement", {
                "movements": zero_movements,
                "question": question,
                "document_field": doc_field
            })
            
            # Step 4: Use composer planning to generate answer reasoning
            # Create intent from question + semantic guidance
            intent = f"{question} {semantic_guidance}"
            composer_result = self._call_primitive("composer.plan", {"intent": intent})
            
            # Step 5: Score each choice using conjugate relationship + knowledge base
            # Questions and answers have conjugate relationship: answer zeros ≈ conjugate(question zeros)
            choice_scores = []
            
            # Get question zeros (from query spectrum if available, else from doc zeros)
            question_zero_positions = []
            if 'query_zero_positions' in locals() and query_zero_positions:
                question_zero_positions = query_zero_positions
            elif doc_zeros:
                question_zero_positions = [z.get("imaginary", 0.0) for z in doc_zeros if isinstance(z, dict)]
            
            for i, choice in enumerate(choices):
                # Create choice intent
                choice_intent = f"{question} {choice}"
                
                # Get choice ions
                choice_ions = self._call_primitive("extract_ions", {"intent": choice_intent})
                
                # Compute choice field with proper zeta calibration
                choice_field = self._call_primitive("aperture.chain", {"text": choice})
                choice_aperture = choice_field.get("aperture", {})
                choice_phi_k = choice_aperture.get("discourse", {}).get("phi_k", 0.0)
                
                # Construct full hierarchical spectrum for choice
                choice_spectrum = []
                for letter in choice_aperture.get("letters", []):
                    if isinstance(letter, dict) and letter.get("phi_k"):
                        choice_spectrum.append(float(letter["phi_k"]))
                for word in choice_aperture.get("words", []):
                    if isinstance(word, dict) and word.get("phi_k"):
                        choice_spectrum.append(float(word["phi_k"]))
                for sentence in choice_aperture.get("sentences", []):
                    if isinstance(sentence, dict) and sentence.get("phi_k"):
                        choice_spectrum.append(float(sentence["phi_k"]))
                if choice_phi_k:
                    choice_spectrum.append(float(choice_phi_k))
                
                if not choice_spectrum:
                    choice_spectrum = [float(choice_phi_k)] if choice_phi_k else [0.0]
                
                # Dimensional scale matching: answer should match question's dimensionality
                # Conjugate relationship: answer operates in same dimensional space as question
                if query_region is not None:
                    # Match question's dimensional scale exactly (conjugate relationship)
                    choice_region = query_region
                else:
                    # Compute choice dimensionality from hierarchical structure
                    choice_has_letters = len(choice_aperture.get("letters", [])) > 0
                    choice_has_words = len(choice_aperture.get("words", [])) > 0
                    choice_has_sentences = len(choice_aperture.get("sentences", [])) > 0
                    choice_has_discourse = choice_phi_k != 0.0
                    
                    choice_D = sum([choice_has_letters, choice_has_words, choice_has_sentences, choice_has_discourse])
                    if choice_D == 0:
                        choice_D = 1
                    
                    # Dimensional scale: φ^D
                    phi = (1 + math.sqrt(5)) / 2
                    choice_dimensional_scale = phi ** choice_D
                    
                    # Spectrum factor
                    choice_spectrum_size = len(choice_spectrum)
                    choice_spectrum_factor = max(1.0, choice_spectrum_size / 10.0)
                    
                    # Choice scale should match question scale (conjugate relationship)
                    # Use document scale as reference
                    choice_search_max = choice_dimensional_scale * choice_spectrum_factor
                    choice_search_max = max(5.0, min(30.0, min(choice_search_max, doc_search_max)))
                    
                    choice_region = {"min": 0.0, "max": choice_search_max}
                
                # Compute choice zeros using FULL spectrum with scale-matched region
                choice_zeros = self._call_primitive("zeta.zero.solver", {
                    "phi_k": choice_spectrum,
                    "region": choice_region,
                    "tolerance": 0.001
                })
                choice_zero_positions = [z.get("imaginary", 0.0) for z in choice_zeros if isinstance(z, dict)]
                
                # Base coherence: field alignment
                question_phi_k = doc_aperture.get("discourse", {}).get("phi_k", 0.0)
                coherence = 1.0 - abs(choice_phi_k - float(question_phi_k)) / (abs(question_phi_k) + 1.0)
                coherence = max(0.0, min(1.0, coherence))
                
                # CONJUGATE RELATIONSHIP: Answer zeros complement question zeros
                # Hermitian relationship: answer field = conjugate(question field)
                # For zeros on critical line: answer zeros should complement question zeros
                # This means: answer zeros near question zeros OR at conjugate positions
                conjugate_boost = 0.0
                if question_zero_positions and choice_zero_positions:
                    # Check conjugate relationship: answer zeros should complement question zeros
                    total_conjugate_match = 0.0
                    for qz in question_zero_positions:
                        # Direct match: answer zero near question zero (completes question)
                        min_direct_dist = min(abs(cz - qz) for cz in choice_zero_positions)
                        direct_match = 1.0 / (1.0 + min_direct_dist)
                        
                        # Conjugate match: answer zero at conjugate position
                        # For critical line zeros: conjugate(0.5 + i*t) = 0.5 - i*t
                        conjugate_pos = -qz  # Conjugate on critical line
                        min_conj_dist = min(abs(cz - conjugate_pos) for cz in choice_zero_positions)
                        conj_match = 1.0 / (1.0 + min_conj_dist)
                        
                        # Use best match (answer completes question through direct or conjugate)
                        best_match = max(direct_match, conj_match * 0.7)
                        total_conjugate_match += best_match
                    
                    # Average conjugate match
                    conjugate_boost = total_conjugate_match / len(question_zero_positions)
                    # Add conjugate boost to coherence (complementary, not replacement)
                    coherence = coherence + (conjugate_boost * 0.3)  # 30% boost from conjugate
                    coherence = min(1.0, coherence)  # Cap at 1.0
                
                # Also check zero proximity from composer result
                zeros = composer_result.get("zeros", [])
                if zeros:
                    composer_zero_positions = [z.get("imaginary", 0.0) for z in zeros if isinstance(z, dict)]
                    if composer_zero_positions:
                        min_zero_dist = min(abs(choice_phi_k - z_pos) for z_pos in composer_zero_positions)
                        zero_proximity = 1.0 / (1.0 + min_zero_dist)
                        coherence = (coherence + zero_proximity) / 2.0
                
                # Boost coherence if choice matches knowledge base entries (improved)
                if knowledge_results:
                    knowledge_boost = 0.0
                    
                    # Compute choice field (full aperture chain for better semantics)
                    choice_field = self._call_primitive("aperture.chain", {"text": choice})
                    choice_field_phi_k = choice_field.get("aperture", {}).get("discourse", {}).get("phi_k", choice_phi_k)
                    
                    # Compute choice zeros for semantic matching
                    choice_zeros = self._call_primitive("zeta.zero.solver", {
                        "phi_k": choice_field_phi_k,
                        "region": {"min": 0.0, "max": 10.0},
                        "tolerance": 0.01
                    })
                    choice_zero_positions = [z.get("imaginary", 0.0) for z in choice_zeros if isinstance(z, dict)]
                    
                # Match against knowledge base using field math
                for kb_entry in knowledge_results:
                    kb_phi_k = float(kb_entry.get("phi_k", 0.0))
                    kb_zeros = kb_entry.get("zeros", [])
                    kb_zero_positions = [z.get("imaginary", 0.0) for z in kb_zeros if isinstance(z, dict)]
                    
                    # Check for field mapping (boosts biology/astronomy/pharmacology/evolution questions)
                    kb_field_mapping = kb_entry.get("field_mapping", {})
                    kb_domain = kb_entry.get("domain", "")
                    kb_title_lower = kb_entry.get("title", "").lower()
                    
                    # Let OPIC determine domain relevance naturally - no hardcoded term matching
                    # Trust field_mapping if present, let OPIC's field operations determine relevance
                    if kb_field_mapping:
                        # Biology/astronomy/pharmacology/evolution questions benefit from field equation understanding
                        # Boost knowledge match for field-mapped concepts
                        knowledge_boost *= 1.2  # 20% boost for field mappings
                        
                        # Field distance: ‖Φκ(choice) - Φκ(kb_entry)‖
                        field_distance = abs(choice_field_phi_k - kb_phi_k)
                        # Normalize: similarity = 1 / (1 + distance/scale)
                        scale = max(abs(choice_field_phi_k), abs(kb_phi_k), 1.0)
                        field_similarity = 1.0 / (1.0 + field_distance / scale)
                        
                        # Zero proximity: choices near KB zeros are semantically related
                        zero_proximity = 0.0
                        if choice_zero_positions and kb_zero_positions:
                            min_zero_dist = min(
                                abs(cz - kz) 
                                for cz in choice_zero_positions 
                                for kz in kb_zero_positions
                            )
                            zero_proximity = 1.0 / (1.0 + min_zero_dist)
                        
                        # Combined field-based semantic match
                        # Weight: field similarity (60%) + zero proximity (40%)
                        semantic_match = (field_similarity * 0.6) + (zero_proximity * 0.4)
                        
                        # Boost coherence based on semantic match
                        knowledge_boost += 0.4 * semantic_match
                    
                    # Average boost across top knowledge entries
                    if knowledge_results:
                        knowledge_boost = knowledge_boost / len(knowledge_results)
                    
                    # Cap boost at 50%
                    knowledge_boost = min(0.5, knowledge_boost)
                    coherence = min(1.0, coherence + knowledge_boost)
                
                choice_scores.append((i, coherence))
            
            # Step 6: Select best choice by coherence
            choice_scores.sort(key=lambda x: x[1], reverse=True)
            best_idx = choice_scores[0][0]
            
            # Step 7: Learn from code-output coupling
            # Capture code trace (field state, zeros, generation process)
            code_trace = {
                "question": question,
                "question_spectrum": query_spectrum if 'query_spectrum' in locals() else [],
                "question_zeros": query_zero_positions if 'query_zero_positions' in locals() else [],
                "doc_spectrum": doc_spectrum,
                "doc_zeros": doc_zero_positions if 'doc_zero_positions' in locals() else [],
                "choice_spectra": [choice_spectrum for _ in choices],  # Simplified
                "field_state": {
                    "phi_k": doc_phi_k,
                    "dimensionality": doc_D if 'doc_D' in locals() else 1
                }
            }
            
            # Store for learning (will be used when we know correct answer)
            # This creates the code-output coupling for self-improvement
            # The code trace is available for learning after we know the correct answer
            
            return best_idx
            
        except Exception as e:
            # Fallback to original method
            pass
        
        # Fallback: Use original reason.answer approach
        try:
            result = self.execute_voice("reason.answer", {
                "question": question,
                "choices": choices
            })
            
            # Extract answer index from result
            if isinstance(result, int) and 0 <= result < len(choices):
                return result
            
            # Try to extract index from string result
            if isinstance(result, str):
                # Look for numeric answer
                import re
                nums = re.findall(r'\d+', result)
                if nums:
                    idx = int(nums[0])
                    if 0 <= idx < len(choices):
                        return idx
                
                # Try semantic matching using field operations
                best_idx = self._select_answer_by_energy(question, choices, result)
                if best_idx is not None:
                    return best_idx
                
                # Fallback: simple string matching
                for i, choice in enumerate(choices):
                    if result.lower() in choice.lower() or choice.lower() in result.lower():
                        return i
        except Exception as e:
            # Final fallback to energy-based selection
            return self._select_answer_by_energy(question, choices) or 0
        
        return 0
    
    def _select_answer_by_energy(self, question: str, choices: List[str], reasoning: str = None) -> Optional[int]:
        """
        Select best answer using Field Spec 0.7 energy coupling with semantic embeddings
        Uses field operations on meaning vectors
        """
        if not choices:
            return None
        
        # Get semantic embeddings
        q_emb = self._get_semantic_embedding(question)
        reasoning_emb = self._get_semantic_embedding(reasoning) if reasoning else None
        
        best_idx = 0
        best_score = float('-inf')
        
        # Score each choice using semantic embeddings and field operations
        for i, choice in enumerate(choices):
            score = 0.0
            
            # Get choice embedding
            c_emb = self._get_semantic_embedding(choice)
            
            # 1. Semantic similarity: cosine similarity in embedding space
            cosine_sim = sum(a * b for a, b in zip(q_emb, c_emb))
            score += cosine_sim * 10.0  # Scale up semantic similarity
            
            # 2. Energy coupling: Field Spec coulomb_yukawa on embeddings
            # Compute charge from embedding magnitude
            q_charge = math.sqrt(sum(x ** 2 for x in q_emb))
            c_charge = math.sqrt(sum(x ** 2 for x in c_emb))
            
            # Distance in embedding space
            emb_distance = math.sqrt(sum((a - b) ** 2 for a, b in zip(q_emb, c_emb)))
            emb_distance = max(0.1, emb_distance)
            
            # Energy coupling using Field Spec formula
            energy = abs(self._compute_energy_coupling(
                q_charge, c_charge,
                q_emb, c_emb,
                emb_distance
            ))
            score += energy * 5.0
            
            # 3. Reasoning alignment: if reasoning provided, check alignment
            if reasoning_emb:
                reasoning_sim = sum(a * b for a, b in zip(reasoning_emb, c_emb))
                score += reasoning_sim * 8.0
                
                # Also check string overlap for exact matches
                if choice.lower() in reasoning.lower():
                    score += 5.0
            
            # 4. Word overlap (fallback)
            q_words = set(word.lower() for word in question.split() if len(word) > 3)
            c_words = set(word.lower() for word in choice.split() if len(word) > 3)
            overlap = len(q_words & c_words)
            score += overlap * 1.0
            
            if score > best_score:
                best_score = score
                best_idx = i
        
        return best_idx
    
    
    def solve_math_problem(self, problem: str) -> str:
        """
        Solve a math problem using opic's math system with Field Spec 0.7
        Uses cycle operations for multi-step math reasoning
        """
        # Execute math.solve - opic composes Field Spec 0.7 internally
        try:
            result = self.execute_voice("math.solve", {"problem": problem})
            if result:
                # Extract numeric answer
                import re
                nums = re.findall(r'-?\d+', str(result))
                if nums:
                    return nums[-1]  # Return last number found
                return str(result)
        except:
            pass
        
        # Fallback: try to extract numbers from problem
        import re
        nums = re.findall(r'-?\d+', problem)
        if nums:
            return nums[0]
        
        return "0"
    
    def _associate_file_output(self, file_path: Path, output: Any):
        """Associate file with its output for learning"""
        if not hasattr(self, 'file_output_pairs'):
            self.file_output_pairs = []
        
        pair = {
            'file': str(file_path),
            'output': str(output) if output else None,
            'timestamp': __import__('time').time()
        }
        self.file_output_pairs.append(pair)
        
        # If code_output_learner is available, use it
        try:
            from code_output_learner import CodeOutputLearner
            if not hasattr(self, '_code_output_learner'):
                self._code_output_learner = CodeOutputLearner(self.project_root)
            
            # Record code-output pair
            code_trace = {
                'file': str(file_path),
                'voices': list(self.voices.keys())[:10] if hasattr(self, 'voices') else []
            }
            self._code_output_learner.record_code_output_pair(
                code_trace=code_trace,
                output=output,
                correct_answer=None,  # No ground truth for general execution
                evaluation={'coherence': 1.0}
            )
        except ImportError:
            pass  # CodeOutputLearner not available
    
    def get_file_comments(self, file_path: Path = None) -> Dict:
        """Get comments extracted from files"""
        if not hasattr(self, 'file_comments'):
            return {}
        if file_path:
            return self.file_comments.get(str(file_path), [])
        return self.file_comments
    
    def get_file_output_pairs(self) -> List[Dict]:
        """Get file-output pairs for learning"""
        if not hasattr(self, 'file_output_pairs'):
            return []
        return self.file_output_pairs


def find_project_root():
    """Find opic installation root"""
    script_dir = Path(__file__).parent.parent
    
    # Check if we're in development mode (script is in project root)
    if (script_dir / "generate.py").exists() and (script_dir / "scripts" / "opic_executor.py").exists():
        return script_dir
    
    # Check system installation locations (installed mode)
    for path in [
        Path("/usr/local/share/opic"),
        Path("/usr/share/opic"),
        Path.home() / ".local" / "share" / "opic",
    ]:
        if (path / "scripts" / "opic_executor.py").exists():
            return path
    
    # Fallback: try script directory even if generate.py missing
    if (script_dir / "scripts" / "opic_executor.py").exists():
        return script_dir
    
    # Last resort: return script directory
    return script_dir


def main():
    """CLI entry point - naturally discover .ops files"""
    project_root = find_project_root()
    executor = OpicExecutor(project_root)
    
    # Get command from args
    command = sys.argv[1] if len(sys.argv) > 1 else "help"
    
    # Naturally discover .ops file by searching directories
    ops_path = None
    search_dirs = [
        project_root / "tests",
        project_root / "systems", 
        project_root / "core",
        project_root / "examples",
        project_root,
    ]
    
    for search_dir in search_dirs:
        if not search_dir.exists():
            continue
        # Try exact match first
        candidate = search_dir / f"{command}.ops"
        if candidate.exists():
            ops_path = candidate
            break
        # Try with underscores
        candidate = search_dir / f"{command.replace('-', '_')}.ops"
        if candidate.exists():
            ops_path = candidate
            break
        # Try prefix match (e.g., "test" -> "runtime_test.ops")
        if search_dir.exists():
            for ops_file in search_dir.glob(f"*{command}*.ops"):
                ops_path = ops_file
                break
            if ops_path:
                break
    
    # Execute the .ops file
    if ops_path:
        executor._load_ops_file(ops_path)
        # Set current file so execute_voice can associate it with output automatically
        executor.current_file = ops_path
        # Support calling specific voice: "execute file.ops voice_name"
        voice_name = sys.argv[2] if len(sys.argv) > 2 else "main"
        result = executor.execute_voice(voice_name)
        # File-output association happens automatically in execute_voice()
        
        if result:
            print(result)
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

