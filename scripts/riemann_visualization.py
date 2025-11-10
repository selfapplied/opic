#!/usr/bin/env python3
"""
Riemann Hypothesis Experiment Visualization

Creates interactive visualizations of coherence symmetry field.
Shows |Φ| vs Re(s) heatmap and critical line exploration.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from pathlib import Path
import json

def compute_zeta_at_s(prime_voices, s):
    """Compute ζ_opic(s) for given s"""
    zeta = 1.0 + 0.0j
    
    for voice in prime_voices:
        coherence = voice.get('coherence', 0.5)
        phase = voice.get('phase', 0.0)
        
        # Simplified functor: coherence * exp(i*phase)
        functor_val = coherence * np.exp(1j * phase)
        
        try:
            factor = 1.0 / (1.0 - functor_val ** (-s))
            zeta *= factor
        except (ZeroDivisionError, OverflowError):
            continue
    
    return zeta

def simulate_field_at_s(s, time_steps=100):
    """Simulate field evolution and compute |Φ|"""
    # Simplified: assume field oscillates with frequency related to s
    t = np.linspace(0, 10, time_steps)
    
    # Field evolution: oscillatory behavior near critical line
    if abs(s.real - 0.5) < 0.1:
        # Near critical line: constant amplitude
        phi = np.exp(1j * s.imag * t) * np.exp(-0.01 * t)
    else:
        # Away from critical line: growing or decaying
        growth_rate = (s.real - 0.5) * 0.1
        phi = np.exp(1j * s.imag * t) * np.exp(growth_rate * t)
    
    # Return average magnitude
    return np.mean(np.abs(phi))

def create_heatmap():
    """Create heatmap of |Φ| vs Re(s)"""
    print("Generating coherence symmetry heatmap...")
    
    # Mock prime voices
    prime_voices = [
        {'name': 'voice.add', 'coherence': 0.95, 'phase': 0.1},
        {'name': 'voice.multiply', 'coherence': 0.92, 'phase': 0.2},
        {'name': 'voice.compose', 'coherence': 0.98, 'phase': 0.15},
        {'name': 'voice.chain', 'coherence': 0.94, 'phase': 0.12},
        {'name': 'voice.certify', 'coherence': 0.97, 'phase': 0.18},
    ]
    
    # Create grid
    re_s_values = np.linspace(0.1, 0.9, 50)
    im_s_values = np.linspace(0, 30, 30)
    
    # Compute |Φ| for each point
    phi_magnitudes = np.zeros((len(im_s_values), len(re_s_values)))
    
    for i, im_s in enumerate(im_s_values):
        for j, re_s in enumerate(re_s_values):
            s = re_s + 1j * im_s
            
            # Method 1: From zeta function
            zeta_s = compute_zeta_at_s(prime_voices, s)
            zeta_mag = np.abs(zeta_s)
            
            # Method 2: From field simulation
            field_mag = simulate_field_at_s(s)
            
            # Combine (weighted average)
            phi_magnitudes[i, j] = 0.5 * zeta_mag + 0.5 * field_mag
    
    # Create figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Heatmap
    im1 = ax1.imshow(phi_magnitudes, aspect='auto', origin='lower',
                     extent=[re_s_values[0], re_s_values[-1], 
                             im_s_values[0], im_s_values[-1]],
                     cmap='viridis', interpolation='bilinear')
    ax1.axvline(x=0.5, color='red', linestyle='--', linewidth=2, 
                label='Critical Line Re(s)=0.5')
    ax1.set_xlabel('Re(s)', fontsize=12)
    ax1.set_ylabel('Im(s)', fontsize=12)
    ax1.set_title('Coherence Symmetry Field |Φ|', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    plt.colorbar(im1, ax=ax1, label='|Φ|')
    
    # Cross-section at critical line
    critical_idx = np.argmin(np.abs(re_s_values - 0.5))
    critical_line = phi_magnitudes[:, critical_idx]
    
    ax2.plot(im_s_values, critical_line, 'b-', linewidth=2, label='Re(s)=0.5')
    
    # Compare with nearby lines
    for offset in [0.1, 0.2]:
        idx_high = np.argmin(np.abs(re_s_values - (0.5 + offset)))
        idx_low = np.argmin(np.abs(re_s_values - (0.5 - offset)))
        
        if idx_high < len(re_s_values):
            ax2.plot(im_s_values, phi_magnitudes[:, idx_high], 
                    '--', alpha=0.5, label=f'Re(s)={0.5+offset:.1f}')
        if idx_low < len(re_s_values):
            ax2.plot(im_s_values, phi_magnitudes[:, idx_low], 
                    '--', alpha=0.5, label=f'Re(s)={0.5-offset:.1f}')
    
    ax2.set_xlabel('Im(s)', fontsize=12)
    ax2.set_ylabel('|Φ|', fontsize=12)
    ax2.set_title('Critical Line Cross-Section', fontsize=14, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save
    output_dir = Path('build')
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / 'riemann_visualization.png'
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"Visualization saved to: {output_file}")
    
    # Also save data for future use
    data_file = output_dir / 'riemann_visualization_data.json'
    with open(data_file, 'w') as f:
        json.dump({
            're_s_values': re_s_values.tolist(),
            'im_s_values': im_s_values.tolist(),
            'phi_magnitudes': phi_magnitudes.tolist()
        }, f, indent=2)
    print(f"Data saved to: {data_file}")
    
    return fig

def create_interactive_notebook():
    """Create Jupyter notebook for interactive exploration"""
    notebook_content = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# opic Zeta Laboratory - Interactive Exploration\n",
                    "\n",
                    "This notebook allows interactive exploration of opic's coherence symmetry field.\n",
                    "\n",
                    "## Setup"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "source": [
                    "import numpy as np\n",
                    "import matplotlib.pyplot as plt\n",
                    "from scripts.riemann_visualization import create_heatmap\n",
                    "\n",
                    "# Load visualization\n",
                    "fig = create_heatmap()\n",
                    "plt.show()"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## Explore Critical Line\n",
                    "\n",
                    "Try different values of Re(s) and Im(s) to explore the coherence symmetry field."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "source": [
                    "# Interactive exploration\n",
                    "re_s = 0.5  # Critical line\n",
                    "im_s = 14.134725  # First non-trivial zero\n",
                    "\n",
                    "s = re_s + 1j * im_s\n",
                    "print(f\"Exploring s = {s}\")\n",
                    "print(f\"Re(s) = {re_s}, Im(s) = {im_s}\")"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.8.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    output_dir = Path('build')
    output_dir.mkdir(exist_ok=True)
    notebook_file = output_dir / 'riemann_exploration.ipynb'
    
    import json
    with open(notebook_file, 'w') as f:
        json.dump(notebook_content, f, indent=2)
    
    print(f"Jupyter notebook saved to: {notebook_file}")
    return notebook_file

def main():
    """Generate visualizations"""
    print("=" * 60)
    print("opic Zeta Laboratory - Visualization Generator")
    print("=" * 60)
    print()
    
    # Create heatmap
    fig = create_heatmap()
    
    # Create interactive notebook
    notebook_file = create_interactive_notebook()
    
    print()
    print("=" * 60)
    print("Visualization Complete")
    print("=" * 60)
    print(f"  - Heatmap: build/riemann_visualization.png")
    print(f"  - Data: build/riemann_visualization_data.json")
    print(f"  - Notebook: {notebook_file}")
    print()
    print("To view interactively:")
    print(f"  jupyter notebook {notebook_file}")
    print("=" * 60)

if __name__ == '__main__':
    main()

