#!/usr/bin/env python3
"""
Build energy decomposition tables for the first k modes, for k in {3, 5, 6}.

Configuration:
- primes P = {2, 3}
- weights w_p = 1
- N_t = 100
- T = log(100)

Outputs:
- output/results/bi_l_modes_table.json  (structured data)
- output/results/bi_l_modes_table.csv   (CSV)
- output/results/bi_l_modes_table.md    (Markdown table)
"""

import csv
import json
import math
import os
from typing import Dict, List, Tuple

import numpy as np

# Reuse construction and eigensolver from the single-run and sweep logic
try:
	from bi_laplacian_sim import (
		build_periodic_circulant_laplacian,
		build_fractional_shift_matrix,
		build_hp_from_shift,
		compute_spectrum,
	)
except Exception:
	import sys
	sys.path.append(os.path.dirname(__file__))
	from bi_laplacian_sim import (
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
) -> Tuple[np.ndarray, Dict[int, np.ndarray], float, np.ndarray, np.ndarray]:
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

	return H_N, H_p_dict, dt, t_grid, L_D


def valuation_energies(psi: np.ndarray, H_p_dict: Dict[int, np.ndarray]) -> Dict[int, float]:
	out: Dict[int, float] = {}
	psi = psi.reshape(-1, 1)
	for p, Hp in H_p_dict.items():
		val = np.real(np.conjugate(psi).T @ (Hp @ psi))
		out[p] = float(val[0, 0])
	return out


def build_tables(k_values: List[int]) -> Dict:
	# Fixed config
	primes = [2, 3]
	weights = {2: 1.0, 3: 1.0}
	N_t = 100
	T = math.log(100.0)
	L = max(k_values)

	# Build H and spectrum
	H_N, H_p_dict, dt, t_grid, L_D = construct_hamiltonian(
		num_points=N_t, T=T, primes=primes, weights=weights
	)
	evals, evecs = compute_spectrum(H_N, num_eigs=L)

	# Collect rows per mode index n for n=0..L-1
	mode_rows: List[Dict] = []
	for n in range(L):
		lambda_n = float(evals[n])
		psi_n = evecs[:, n]
		vals = valuation_energies(psi_n, H_p_dict)
		E_val_sum = sum(vals.values())
		E_inf = float(lambda_n - E_val_sum)
		mode_rows.append({
			"n": n,
			"lambda": lambda_n,
			"E_inf": E_inf,
			**{f"E_{p}": vals[p] for p in primes},
		})

	# Prepare tables for requested k values
	tables = {}
	for k in k_values:
		tables[str(k)] = mode_rows[:k]

	return {
		"spec": {
			"primes": primes,
			"weights": weights,
			"N_t": N_t,
			"T": T,
			"delta_t": (2.0 * T) / N_t,
			"description": "Energy decomposition per mode: lambda_n, E_inf, E_2, E_3",
		},
		"k_values": k_values,
		"tables": tables,
	}


def write_csv(path: str, rows: List[Dict]) -> None:
	if not rows:
		with open(path, "w") as f:
			f.write("")
		return
	fieldnames = list(rows[0].keys())
	with open(path, "w", newline="") as f:
		writer = csv.DictWriter(f, fieldnames=fieldnames)
		writer.writeheader()
		for r in rows:
			writer.writerow(r)


def write_md_table(path: str, title: str, rows: List[Dict]) -> None:
	if not rows:
		with open(path, "w") as f:
			f.write(f"{title}\n\n(empty)\n")
		return
	cols = list(rows[0].keys())
	with open(path, "w") as f:
		f.write(f"{title}\n\n")
		# Header
		f.write("| " + " | ".join(cols) + " |\n")
		f.write("| " + " | ".join(["---"] * len(cols)) + " |\n")
		# Rows
		for r in rows:
			f.write("| " + " | ".join(f"{r[c]}" for c in cols) + " |\n")


def main() -> None:
	results_dir = ensure_output_dir()
	result = build_tables([3, 5, 6])

	# Write JSON
	json_path = os.path.join(results_dir, "bi_l_modes_table.json")
	with open(json_path, "w") as f:
		json.dump(result, f, indent=2)

	# Write CSV/MD for each k
	for k_str, rows in result["tables"].items():
		k = int(k_str)
		csv_path = os.path.join(results_dir, f"bi_l_modes_table_k{k}.csv")
		md_path = os.path.join(results_dir, f"bi_l_modes_table_k{k}.md")
		write_csv(csv_path, rows)
		write_md_table(md_path, f"Bi-Laplacian mode energies for k={k}", rows)

	print("Wrote tables to:", results_dir)


if __name__ == "__main__":
	main()


