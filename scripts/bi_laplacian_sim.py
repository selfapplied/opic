#!/usr/bin/env python3
"""
Finite-dimensional prototype for the Adelic Bi-Laplacian (Bi-L-RH) experiment.

Constructs H_N = L_D + sum_p H_p on a 1D periodic grid in t ∈ [-T, T].
Outputs:
- output/results/bi_laplacian_sim.json: eigenvalues (first 20), λ1, and valuation energies
- output/results/bi_laplacian_psi1.png: plot of the first non-trivial eigenvector ψ1 (if matplotlib available)
"""

import json
import math
import os
from typing import Dict, List, Tuple

import numpy as np


def ensure_output_dirs() -> Tuple[str, str]:
	"""Ensure the output directories exist, return (results_json_path, psi1_png_path)."""
	results_dir = os.path.join("output", "results")
	os.makedirs(results_dir, exist_ok=True)
	return (
		os.path.join(results_dir, "bi_laplacian_sim.json"),
		os.path.join(results_dir, "bi_laplacian_psi1.png"),
	)


def build_periodic_circulant_laplacian(num_points: int, dt: float) -> np.ndarray:
	"""
	Discrete second derivative with periodic boundary conditions (circulant).
	Stencil: [-1, 2, -1] / dt^2 with wrap-around.
	"""
	if num_points < 3:
		raise ValueError("num_points must be >= 3 for a stable second-derivative stencil.")
	L = np.zeros((num_points, num_points), dtype=float)
	for i in range(num_points):
		L[i, i] = 2.0
		L[i, (i - 1) % num_points] = -1.0
		L[i, (i + 1) % num_points] = -1.0
	return L / (dt * dt)


def build_fractional_shift_matrix(num_points: int, theta: float) -> np.ndarray:
	"""
	Build the unitary fractional shift operator S acting on R^N (treated as C^N) with periodic BCs,
	via the Fourier diagonalization:
	  S = F^{-1} diag(exp(i * k * theta)) F
	where k ranges over the discrete frequency indices compatible with numpy's rfft/fft conventions.
	Notes:
	- theta is the shift in grid index units (i.e., shift = (Δt * log p) / Δt = log p / Δt).
	- We implement with the standard complex FFT basis to keep S unitary/Hermitian-compliant in H_p.
	"""
	# Construct Fourier matrix F and its inverse explicitly for clarity (O(N^2), fine for N=100)
	n = num_points
	k = np.arange(n)  # frequency indices (0..n-1) in DFT convention
	# DFT matrix F_{jk} = (1/√n) exp(-2πi jk / n)
	j = k[:, None]
	F = (1.0 / math.sqrt(n)) * np.exp(-2j * np.pi * j * k / n)
	FH = np.conjugate(F).T  # F^{-1} since F is unitary
	# Phase for shift theta in index units: multiplier exp(+2π i k theta / n) due to DFT convention
	phase = np.exp(+2j * np.pi * k * theta / n)
	D = np.diag(phase)
	S = FH @ D @ F
	return S


def build_hp_from_shift(S: np.ndarray, log_p: float) -> np.ndarray:
	"""
	H_p = (1 / (log p)^2) * (S - I)† (S - I)
	    = (1 / (log p)^2) * (2I - S - S†)
	This is Hermitian positive semi-definite when S is unitary.
	"""
	I = np.eye(S.shape[0], dtype=complex)
	return (2.0 * I - S - S.conj().T) / (log_p * log_p)


def construct_hamiltonian(
	num_points: int,
	T: float,
	primes: List[int],
	weights: Dict[int, float],
) -> Tuple[np.ndarray, Dict[int, np.ndarray], float, np.ndarray]:
	"""
	Construct H_N and component matrices:
	- L_D: periodic discrete Laplacian in t
	- H_p for each p in primes
	- H_N = L_D + sum_p w_p H_p
	Returns (H_N, {p: H_p}, dt, t_grid)
	"""
	t_min, t_max = -T, T
	# Uniform grid including periodic wrap conceptually; we store N points on [-T, T) effectively
	t_grid = np.linspace(t_min, t_max, num_points, endpoint=False)
	dt = (t_max - t_min) / num_points

	# Analytic term: L_D (real symmetric)
	L_D = build_periodic_circulant_laplacian(num_points, dt).astype(complex)

	# Non-archimedean terms via fractional shift S_p with shift size alpha_p = log(p)/dt (in index units)
	H_p_dict: Dict[int, np.ndarray] = {}
	for p in primes:
		log_p = math.log(p)
		alpha = log_p / dt  # fractional shift in index space
		S_p = build_fractional_shift_matrix(num_points, theta=alpha)
		H_p = build_hp_from_shift(S_p, log_p=log_p)
		H_p_dict[p] = H_p

	# Combine
	H_N = L_D.copy()
	for p in primes:
		w = weights.get(p, 1.0)
		H_N = H_N + w * H_p_dict[p]

	return H_N, H_p_dict, dt, t_grid


def compute_spectrum(H: np.ndarray, num_eigs: int = 20) -> Tuple[np.ndarray, np.ndarray]:
	"""
	Compute the lowest `num_eigs` eigenvalues and eigenvectors of Hermitian H.
	We use full dense eigh since N is small; values are sorted ascending.
	Returns (eigenvalues, eigenvectors) where columns of eigenvectors correspond to eigenvalues.
	"""
	# Convert to hermitian explicitly to avoid minor numerical asymmetries
	Hh = 0.5 * (H + H.conj().T)
	w, v = np.linalg.eigh(Hh)
	# Safety: numerical negatives near zero should be truncated to 0 for readability
	w = np.real(w)
	v = np.array(v, dtype=complex)
	idx = np.argsort(w)
	w = w[idx]
	v = v[:, idx]
	return w[:num_eigs], v[:, :num_eigs]


def valuation_energies(psi: np.ndarray, H_p_dict: Dict[int, np.ndarray]) -> Dict[int, float]:
	"""
	Compute ψ† H_p ψ for each prime p.
	Returns a dict p -> real energy.
	"""
	out: Dict[int, float] = {}
	psi = psi.reshape(-1, 1)
	for p, Hp in H_p_dict.items():
		val = np.real(np.conjugate(psi).T @ (Hp @ psi))
		out[p] = float(val[0, 0])
	return out


def try_plot_psi1(t_grid: np.ndarray, psi1: np.ndarray, save_path: str) -> bool:
	"""
	Best-effort plot of the first non-trivial eigenvector. Returns True if saved.
	"""
	try:
		import matplotlib.pyplot as plt  # type: ignore
	except Exception:
		return False
	plt.figure(figsize=(8, 4))
	plt.plot(t_grid, np.real(psi1), label="Re(ψ1)", lw=2)
	plt.plot(t_grid, np.imag(psi1), label="Im(ψ1)", lw=1.5, alpha=0.7)
	plt.xlabel("t")
	plt.ylabel("ψ1(t)")
	plt.title("First non-trivial eigenvector ψ1")
	plt.grid(True, alpha=0.3)
	plt.legend()
	plt.tight_layout()
	plt.savefig(save_path, dpi=150)
	plt.close()
	return True


def main() -> None:
	# Simulation specification
	primes = [2, 3]  # P_K = {2, 3}
	weights = {2: 1.0, 3: 1.0}
	N_t = 100
	T = math.log(100.0)
	L = 20  # number of eigenpairs to report

	results_json_path, psi1_png_path = ensure_output_dirs()

	# Construct Hamiltonian and components
	H_N, H_p_dict, dt, t_grid = construct_hamiltonian(
		num_points=N_t,
		T=T,
		primes=primes,
		weights=weights,
	)

	# Spectrum
	evals, evecs = compute_spectrum(H_N, num_eigs=L)

	# Identify λ0 and λ1
	lambda0 = float(evals[0]) if len(evals) > 0 else float("nan")
	lambda1 = float(evals[1]) if len(evals) > 1 else float("nan")

	# First non-trivial eigenvector ψ1
	psi1 = evecs[:, 1] if evecs.shape[1] > 1 else None

	# Valuation energies for ψ1
	val_energies = valuation_energies(psi1, H_p_dict) if psi1 is not None else {p: float("nan") for p in primes}

	# Plot ψ1 if available
	plot_saved = False
	if psi1 is not None:
		plot_saved = try_plot_psi1(t_grid, psi1, psi1_png_path)

	# Prepare JSON result
	result = {
		"spec": {
			"primes": primes,
			"weights": weights,
			"N_t": N_t,
			"T": T,
			"delta_t": dt,
			"description": "H_N = L_D + sum_p w_p H_p with periodic BCs; H_p = (S_p - I)†(S_p - I)/(log p)^2",
		},
		"eigenvalues_first_20": [float(x) for x in evals.tolist()],
		"lambda0": lambda0,
		"lambda1": lambda1,
		"valuation_energies_psi1": {str(p): v for p, v in val_energies.items()},
		"psi1_plot_saved": plot_saved,
		"psi1_plot_path": psi1_png_path if plot_saved else None,
	}

	with open(results_json_path, "w") as f:
		json.dump(result, f, indent=2)

	print(f"Wrote eigen results to: {results_json_path}")
	if plot_saved:
		print(f"Wrote ψ1 plot to: {psi1_png_path}")
	else:
		print("matplotlib not available; skipped ψ1 plot.")


if __name__ == "__main__":
	main()


