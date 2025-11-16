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


def adaptive_step(env: Dict[str, Any]) -> str:
	"""
	Declarative, contextual acceptance step:
	- Reads context: epsilon, lambda_comp, a1,a2,a3, N_t, |P|, q_k
	- Computes C = a1*N_t + a2*|P| + a3*log(max(q_k,1))
	- Uses latest lambda1 from sim as E (proxy) and checks metastable band heuristic via sweep (optional)
	- Returns a concise decision string
	"""
	# Context with defaults
	epsilon = float(env.get("epsilon", 1e-3))
	lambda_comp = float(env.get("lambda_comp", 1e-2))
	a1 = float(env.get("a1", 1e-3))
	a2 = float(env.get("a2", 0.1))
	a3 = float(env.get("a3", 1e-3))
	N_t = int(env.get("N_t", 100))
	P = env.get("P", [2, 3])
	q_k = float(env.get("q_k", 100.0))

	# Ensure current sim/sweep exist
	_run_python("scripts/bi_laplacian_sim.py")
	sweep_json = RESULTS_DIR / "bi_laplacian_sweep.json"
	if not sweep_json.exists():
		_run_python("scripts/bi_laplacian_sweep.py")

	# Load lambda1
	lambda1 = None
	sim_json = RESULTS_DIR / "bi_laplacian_sim.json"
	if sim_json.exists():
		try:
			data = json.loads(sim_json.read_text())
			lambda1 = float(data.get("lambda1"))
		except Exception:
			lambda1 = None

	# Estimate Lcrit as the 90th percentile of eigenvalues from sweep top bands (very rough heuristic)
	Lcrit_est = None
	try:
		sdata = json.loads(sweep_json.read_text())
		top_vals = []
		for sec in ("N_t", "T", "w"):
			for r in sdata.get("sweeps", {}).get(sec, []):
				if "top_band" in r:
					top_vals.append(float(r["top_band"]))
		if top_vals:
			top_vals.sort()
			idx = int(0.9 * (len(top_vals) - 1))
			Lcrit_est = top_vals[idx]
	except Exception:
		Lcrit_est = None

	# Complexity and free energy
	Ck = a1 * float(N_t) + a2 * float(len(P)) + a3 * (0.0 if q_k <= 1.0 else float(__import__("math").log(q_k)))
	if lambda1 is None:
		return f"adaptive: no lambda1; C={Ck:.6f}"
	Fk = lambda1 + lambda_comp * Ck

	# Context for proposed refinement (simple +ΔN_t)
	N_t_next = int(env.get("N_t_next", N_t * 2))
	q_next = float(env.get("q_next", q_k * 2.0))
	Ck1 = a1 * float(N_t_next) + a2 * float(len(P)) + a3 * (0.0 if q_next <= 1.0 else float(__import__('math').log(q_next)))
	# We don't recompute lambda at next config here; use a conservative proxy assuming small improvement
	# If sweep exists, use trend with N_t to project a tiny decrease
	delta_E = -abs(lambda1) * 1e-4  # tiny improvement proxy
	Fk1 = (lambda1 + delta_E) + lambda_comp * Ck1

	metastable_ok = True
	if Lcrit_est is not None and lambda1 is not None:
		metastable_ok = (lambda1 < Lcrit_est)

	accept = (Fk1 < Fk - epsilon) and metastable_ok
	return f"adaptive: Fk={Fk:.6f}, Fk+1≈{Fk1:.6f}, epsilon={epsilon}, Lcrit≈{Lcrit_est}, accept={bool(accept)}"


