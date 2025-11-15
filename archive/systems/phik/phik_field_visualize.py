#!.venv/bin/python
"""
phik_field_visualize.py — Visualization engine for Φκ-field

Generates SVG or PNG visualizations of the stabilizing field.
"""

import sys
import os

# Ensure we can import required modules
try:
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap
except ImportError as e:
    print(f"Error: Required module not found: {e}", file=sys.stderr)
    print("Install with: pip install numpy matplotlib", file=sys.stderr)
    sys.exit(1)

# Import phik_field_python (adjust path if needed)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from phik_field_python import PhikFieldBuilder, PhikField


class PhikFieldVisualizer:
    """Visualization engine for Φκ-field"""
    
    def __init__(self, field: PhikField, builder: PhikFieldBuilder):
        self.field = field
        self.builder = builder
    
    def visualize_field(self, output_path: str = 'phik_field.png', format: str = 'png'):
        """Generate complete field visualization"""
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle('Stabilizing Φκ-Field', fontsize=16)
        
        # 1. Intensity I
        im1 = axes[0, 0].imshow(self.field.I, cmap='gray', origin='lower')
        axes[0, 0].set_title('Intensity I(x)')
        axes[0, 0].axis('off')
        plt.colorbar(im1, ax=axes[0, 0])
        
        # 2. Alignment A (as vector field)
        A_gx, A_gy = self.builder.compute_alignment(self.field.Phi_kappa)
        axes[0, 1].quiver(
            A_gx[::4, ::4], A_gy[::4, ::4],
            scale=20, color='blue', alpha=0.6
        )
        axes[0, 1].set_title('Alignment A(x) = ∇Φκ')
        axes[0, 1].axis('off')
        
        # 3. Gradient magnitude α
        im3 = axes[0, 2].imshow(self.field.alpha, cmap='hot', origin='lower')
        axes[0, 2].set_title('Gradient Magnitude α(x)')
        axes[0, 2].axis('off')
        plt.colorbar(im3, ax=axes[0, 2])
        
        # 4. Φκ field (main potential)
        im4 = axes[1, 0].imshow(self.field.Phi_kappa, cmap='viridis', origin='lower')
        axes[1, 0].set_title('Φκ Field (Potential)')
        axes[1, 0].plot(self.field.x_0[1], self.field.x_0[0], 'r*', markersize=15, label='x₀')
        axes[1, 0].legend()
        axes[1, 0].axis('off')
        plt.colorbar(im4, ax=axes[1, 0])
        
        # 5. Charge Q (divergence)
        Q = self.builder.compute_charge(self.field.Phi_kappa)
        im5 = axes[1, 1].imshow(Q, cmap='RdBu', origin='lower', vmin=-Q.max(), vmax=Q.max())
        axes[1, 1].set_title('Charge Q(x) = ∇²Φκ')
        axes[1, 1].axis('off')
        plt.colorbar(im5, ax=axes[1, 1])
        
        # 6. Stability indicators
        A = self.builder.compute_alignment(self.field.Phi_kappa)
        K = self.builder.compute_kinetics(self.field.Phi_kappa, None)
        M = self.builder.compute_momentum(A, None)
        stability = self.builder.check_stability(M, K, Q, epsilon=1e-6)
        
        axes[1, 2].axis('off')
        axes[1, 2].text(0.1, 0.8, 'Stability Status:', fontsize=12, weight='bold', transform=axes[1, 2].transAxes)
        axes[1, 2].text(0.1, 0.6, f"Momentum: {'✓' if stability['momentum_stable'] else '✗'}", 
                       fontsize=10, transform=axes[1, 2].transAxes)
        axes[1, 2].text(0.1, 0.4, f"Kinetics: {'✓' if stability['kinetics_stable'] else '✗'}", 
                       fontsize=10, transform=axes[1, 2].transAxes)
        axes[1, 2].text(0.1, 0.2, f"Charge: {'✓' if stability['charge_stable'] else '✗'}", 
                       fontsize=10, transform=axes[1, 2].transAxes)
        axes[1, 2].text(0.1, 0.0, f"Overall: {'STABLE' if stability['is_stable'] else 'UNSTABLE'}", 
                       fontsize=12, weight='bold', 
                       color='green' if stability['is_stable'] else 'red',
                       transform=axes[1, 2].transAxes)
        
        plt.tight_layout()
        
        if format == 'svg':
            plt.savefig(output_path.replace('.png', '.svg'), format='svg', dpi=150)
        else:
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
        
        print(f"Visualization saved to {output_path}")
        plt.close()
    
    def visualize_evolution(self, iterations: int = 10, output_dir: str = 'evolution'):
        """Visualize field evolution over time"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        I = self.field.I.copy()
        Phi_kappa = self.field.Phi_kappa.copy()
        Phi_kappa_prev = None
        A_prev = None
        
        for t in range(iterations):
            # Compute flows
            A = self.builder.compute_alignment(Phi_kappa)
            Q = self.builder.compute_charge(Phi_kappa)
            K = self.builder.compute_kinetics(Phi_kappa, Phi_kappa_prev)
            M = self.builder.compute_momentum(A, A_prev)
            
            # Check stability
            stability = self.builder.check_stability(M, K, Q)
            
            # Visualize current state
            fig, axes = plt.subplots(1, 2, figsize=(12, 5))
            
            axes[0].imshow(Phi_kappa, cmap='viridis', origin='lower')
            axes[0].set_title(f'Φκ Field (t={t})')
            axes[0].axis('off')
            
            axes[1].imshow(Q, cmap='RdBu', origin='lower', vmin=-Q.max(), vmax=Q.max())
            axes[1].set_title(f'Charge Q (t={t})')
            axes[1].axis('off')
            
            plt.suptitle(f'Stable: {stability["is_stable"]}', fontsize=14)
            plt.tight_layout()
            plt.savefig(f'{output_dir}/step_{t:03d}.png', dpi=100)
            plt.close()
            
            # Evolve
            I = self.builder.evolve(I, Phi_kappa, Q, eta=0.01)
            Phi_kappa_prev = Phi_kappa
            Phi_kappa = self.builder.compute_field(I, A[0], self.field.alpha, self.field.x_0, self.field.kappa)
            A_prev = A
        
        print(f"Evolution visualization saved to {output_dir}/")


if __name__ == '__main__':
    # Build field
    builder = PhikFieldBuilder(H=128, W=128)
    field = builder.build_field()
    
    # Visualize
    visualizer = PhikFieldVisualizer(field, builder)
    visualizer.visualize_field('phik_field.png')
    
    # Evolve and visualize
    visualizer.visualize_evolution(iterations=20)

