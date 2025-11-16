"""
OPIC extensions for Bi-Laplacian experiments.
These functions are callable from .ops via the $module.func$ extension bridge.
"""

import json
import os
import subprocess
from pathlib import Path
from typing import Any, Dict

PROJECT_ROOT = Path(__file__).resolve().parents[2]
VENV_PY = PROJECT_ROOT / ".venv" / "bin" / "python"
RESULTS_DIR = PROJECT_ROOT / "output" / "results"


def _ensure_dirs() -> None:
	RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def _run_python(script_rel: str, args: list[str] | None = None, env_extra: Dict[str, str] | None = None) -> str:
	"""
	Run a repository python script inside .venv if present; otherwise fall back to system python.
	Returns stdout+stderr for logging in OPIC.
	"""
	python_bin = VENVPY if (VENV_PY.exists()) else "python3"
	script_path = PROJECT_ROOT / script_rel
	cmd = [str(python_bin), str(script_path)]
	if args:
		cmd.extend(args)
	env = os.environ.copy()
	env["MPLBACKEND"] = "Agg"
	env["MPLCONFIGDIR"] = str(RESULTS_DIR / "mpl")
	if env_extra:
		env.update(env_extra)
	_ensure_dirs()
	(RESULTS_DIR / "mpl").mkdir(parents=True, exist_ok=True)
	proc = subprocess.run(cmd, cwd=str(PROJECT_ROOT), env=env, capture_output=True, text=True)
	return (proc.stdout or "") + (proc.stderr or "")


def run_sim(env: Dict[str, Any]) -> str:
	"""
	Run the single simulation and return a short report with λ1 and paths.
	"""
	log = _run_python("scripts/bi_laplacian_sim.py")
	json_path = RESULTS_DIR / "bi_laplacian_sim.json"
	lambda1 = None
	if json_path.exists():
		try:
			data = json.loads(json_path.read_text())
			lambda1 = data.get("lambda1")
		except Exception:
			pass
	return f"sim done; lambda1={lambda1}; json={json_path}"


def run_sweep(env: Dict[str, Any]) -> str:
	"""
	Run parameter sweeps and return the aggregate file path.
	"""
	log = _run_python("scripts/bi_laplacian_sweep.py")
	json_path = RESULTS_DIR / "bi_laplacian_sweep.json"
	return f"sweep done; json={json_path}"


def run_modes_table(env: Dict[str, Any]) -> str:
	"""
	Run tables for k in {3,5,6} including invariance norms; return paths.
	"""
	log = _run_python("scripts/bi_laplacian_modes_table.py")
	base = "output/results/bi_l_modes_table"
	return "tables done; " + ", ".join([
		f"{base}.json",
		f"{base}_k3.csv",
		f"{base}_k5.csv",
		f"{base}_k6.csv",
	])


