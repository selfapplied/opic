#!/usr/bin/env python3
"""
Parameter sweeps for the finite Adelic Bi-Laplacian prototype.

Sweeps:
- N_t ∈ {64, 100, 144, 196} with T = log 100, w_p = 1
- T ∈ {log 50, log 100, log 200} with N_t = 100, w_p = 1
- w ∈ {0.5, 1.0, 2.0} applied to both primes {2,3} with N_t = 100, T = log 100

Outputs:
- output/results/bi_laplacian_sweep.json (aggregated results)
- output/results/bi_laplacian_sweep_lambda1_vs_Nt.png
- output/results/bi_laplacian_sweep_topband_vs_Nt.png
- output/results/bi_laplacian_sweep_lambda1_vs_T.png
- output/results/bi_laplacian_sweep_topband_vs_T.png
- output/results/bi_laplacian_sweep_lambda1_vs_w.png
- output/results/bi_laplacian_sweep_topband_vs_w.png
"""

import json
import math
import os
from typing import Dict, List, Tuple

import numpy as np

# Local imports by path without packaging; mirror core logic from the single-run script
from scripts.bi_laplacian_sim import (
	build_periodic_circulant_laplacian,
	build_fractional_shift_matrix,
	build_hp_from_shift,
	compute_spectrum,
)


def ensure_output_dir() -> str:
	results_dir = os.path.join("output", "results")
	os.makedirs(results_dir, exist_ok=True)
	return results_dir


def construct_hamiltonian(
	num_points: int,
	T: float,
	primes: List[int],
	weights: Dict[int, float],
) -> Tuple[np.ndarray, Dict[int, np.ndarray], float, np.ndarray]:
	t_min, t_max = -T, T
	t_grid = np.linspace(t_min, t_max, num_points, endpoint=False)
	dt = (t_max - t_min) / num_points

	L_D = build_periodic_circulant_laplacian(num_points, dt).astype(complex)

	H_p_dict: Dict[int, np.ndarray] = {}
	for p in primes:
		log_p = math.log(p)
		alpha = log_p / dt
		S_p = build_fractional_shift_matrix(num_points, theta=alpha)
		H_p = build_hp_from_shift(S_p, log_p=log_p)
		H_p_dict[p] = H_p

	H_N = L_D.copy()
	for p in primes:
		w = weights.get(p, 1.0)
		H_N = H_N + w * H_p_dict[p]

	return H_N, H_p_dict, dt, t_grid


def run_single(num_points: int, T: float, w: float, L: int = 20) -> Dict[str, float]:
	primes = [2, 3]
	weights = {2: w, 3: w}
	H_N, _, dt, _ = construct_hamiltonian(
		num_points=num_points,
		T=T,
		primes=primes,
		weights=weights,
	)
	evals, _ = compute_spectrum(H_N, num_eigs=L)
	lambda0 = float(evals[0]) if len(evals) > 0 else float("nan")
	lambda1 = float(evals[1]) if len(evals) > 1 else float("nan")
	top_band = float(evals[L - 1]) if len(evals) >= L else float(evals[-1])
	return {
		"N_t": float(num_points),
		"T": float(T),
		"delta_t": float((2.0 * T) / num_points),
		"w": float(w),
		"lambda0": lambda0,
		"lambda1": lambda1,
		"top_band": top_band,
	}


def safe_plot(x: List[float], y: List[float], xlabel: str, ylabel: str, title: str, save_path: str) -> bool:
	try:
		import matplotlib.pyplot as plt  # type: ignore
	except Exception:
		return False
	plt.figure(figsize=(6, 4))
	plt.plot(x, y, marker="o")
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.title(title)
	plt.grid(True, alpha=0.3)
	plt.tight_layout()
	plt.savefig(save_path, dpi=150)
	plt.close()
	return True


def main() -> None:
	results_dir = ensure_output_dir()
	L = 20

	# Defaults
	default_T = math.log(100.0)
	default_Nt = 100
	default_w = 1.0

	# Sweeps
	Nt_list = [64, 100, 144, 196]
	T_list = [math.log(50.0), math.log(100.0), math.log(200.0)]
	w_list = [0.5, 1.0, 2.0]

	# 1) N_t sweep
	nt_results: List[Dict[str, float]] = []
	for Nt in Nt_list:
		nt_results.append(run_single(num_points=Nt, T=default_T, w=default_w, L=L))

	# 2) T sweep
	t_results: List[Dict[str, float]] = []
	for T in T_list:
		t_results.append(run_single(num_points=default_Nt, T=T, w=default_w, L=L))

	# 3) weight sweep
	w_results: List[Dict[str, float]] = []
	for w in w_list:
		w_results.append(run_single(num_points=default_Nt, T=default_T, w=w, L=L))

	# Save aggregated JSON
	aggregate = {
		"defaults": {"N_t": default_Nt, "T": default_T, "w": default_w, "L": L},
		"sweeps": {
			"N_t": nt_results,
			"T": t_results,
			"w": w_results,
		},
	}
	with open(os.path.join(results_dir, "bi_laplacian_sweep.json"), "w") as f:
		json.dump(aggregate, f, indent=2)

	# Plots
	# N_t
	x_nt = [r["N_t"] for r in nt_results]
	y_nt_l1 = [r["lambda1"] for r in nt_results]
	y_nt_top = [r["top_band"] for r in nt_results]
	safe_plot(x_nt, y_nt_l1, "N_t", "λ1", "λ1 vs N_t", os.path.join(results_dir, "bi_laplacian_sweep_lambda1_vs_Nt.png"))
	safe_plot(x_nt, y_nt_top, "N_t", "Top eigenvalue (≈ band edge)", "Top band vs N_t", os.path.join(results_dir, "bi_laplacian_sweep_topband_vs_Nt.png"))

	# T
	x_t = [r["T"] for r in t_results]
	y_t_l1 = [r["lambda1"] for r in t_results]
	y_t_top = [r["top_band"] for r in t_results]
	safe_plot(x_t, y_t_l1, "T", "λ1", "λ1 vs T", os.path.join(results_dir, "bi_laplacian_sweep_lambda1_vs_T.png"))
	safe_plot(x_t, y_t_top, "T", "Top eigenvalue (≈ band edge)", "Top band vs T", os.path.join(results_dir, "bi_laplacian_sweep_topband_vs_T.png"))

	# w
	x_w = [r["w"] for r in w_results]
	y_w_l1 = [r["lambda1"] for r in w_results]
	y_w_top = [r["top_band"] for r in w_results]
	safe_plot(x_w, y_w_l1, "w", "λ1", "λ1 vs weight", os.path.join(results_dir, "bi_laplacian_sweep_lambda1_vs_w.png"))
	safe_plot(x_w, y_w_top, "w", "Top eigenvalue (≈ band edge)", "Top band vs weight", os.path.join(results_dir, "bi_laplacian_sweep_topband_vs_w.png"))

	print("Wrote sweep results and plots to:", results_dir)


if __name__ == "__main__":
	main()


