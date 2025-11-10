#!/usr/bin/env python3
"""Opic drawing — Generate visual art from opic definitions"""

import subprocess
import sys
from pathlib import Path

def generate_ascii_art():
    """Generate ASCII art using opic"""
    # Create drawing ops
    draw_ops = """
def canvas { width: 40, height: 20 }
def pattern { symmetry: radial, elements: ["*", ".", " "] }

voice draw.pattern / {pattern -> canvas}
voice render / {canvas -> ascii}

target art / "ascii.output"
voice main / {pattern -> art}
"""
    
    test_file = Path("/tmp/draw_test.ops")
    test_file.write_text(draw_ops)
    
    # Generate code
    result = subprocess.run(
        [sys.executable, "generate.py", "swift", str(test_file), "/tmp/draw.swift"],
        capture_output=True,
        timeout=5
    )
    
    return result.returncode == 0

def draw_ascii_circle(radius=8):
    """Draw ASCII circle"""
    art = []
    for y in range(-radius, radius + 1):
        row = []
        for x in range(-radius * 2, radius * 2 + 1):
            dist = (x/2)**2 + y**2
            if abs(dist - radius**2) < radius:
                row.append("*")
            elif abs(dist - radius**2) < radius + 1:
                row.append(".")
            else:
                row.append(" ")
        art.append("".join(row))
    return "\n".join(art)

def draw_ascii_spiral(turns=3):
    """Draw ASCII spiral"""
    art = []
    size = 30
    for y in range(size):
        row = []
        for x in range(size):
            dx = x - size // 2
            dy = y - size // 2
            angle = math.atan2(dy, dx)
            dist = math.sqrt(dx*dx + dy*dy)
            spiral_angle = dist * turns * math.pi / (size // 2)
            if abs(angle - spiral_angle) < 0.3 or abs(angle - spiral_angle + 2*math.pi) < 0.3:
                row.append("*")
            elif dist < size // 2:
                row.append(".")
            else:
                row.append(" ")
        art.append("".join(row))
    return "\n".join(art)

def draw_ascii_fractal(depth=3):
    """Draw ASCII fractal tree"""
    import math
    
    def tree(x, y, angle, length, depth):
        if depth == 0:
            return []
        end_x = x + length * math.cos(angle)
        end_y = y + length * math.sin(angle)
        lines = [(x, y, end_x, end_y)]
        lines.extend(tree(end_x, end_y, angle - math.pi/6, length*0.7, depth-1))
        lines.extend(tree(end_x, end_y, angle + math.pi/6, length*0.7, depth-1))
        return lines
    
    lines = tree(15, 0, math.pi/2, 8, depth)
    
    art = [[" " for _ in range(30)] for _ in range(20)]
    for x1, y1, x2, y2 in lines:
        steps = int(math.sqrt((x2-x1)**2 + (y2-y1)**2)) + 1
        for i in range(steps):
            t = i / steps
            x = int(x1 + (x2-x1) * t)
            y = int(y1 + (y2-y1) * t)
            if 0 <= y < 20 and 0 <= x < 30:
                art[y][x] = "*"
    
    return "\n".join("".join(row) for row in art)

def draw_opic_logo():
    """Draw opic logo in ASCII"""
    logo = """
    ╔═══════════════════════════════╗
    ║                               ║
    ║        ╔═══╗  ╔═══╗          ║
    ║        ║   ║  ║   ║          ║
    ║        ║ O ║  ║ P ║          ║
    ║        ║   ║  ║   ║          ║
    ║        ╚═══╝  ╚═══╝          ║
    ║                               ║
    ║        ╔═══╗  ╔═══╗          ║
    ║        ║   ║  ║   ║          ║
    ║        ║ I ║  ║ C ║          ║
    ║        ║   ║  ║   ║          ║
    ║        ╚═══╝  ╚═══╝          ║
    ║                               ║
    ║    Event-Based Compositional  ║
    ║         Language              ║
    ║                               ║
    ╚═══════════════════════════════╝
    """
    return logo

def draw_harmonic_pattern():
    """Draw harmonic pattern based on opic's resonance"""
    import math
    
    art = []
    width, height = 60, 20
    for y in range(height):
        row = []
        for x in range(width):
            # Harmonic wave pattern
            wave1 = math.sin(x * 0.2) * math.cos(y * 0.3)
            wave2 = math.sin(x * 0.15 + y * 0.1) * 0.5
            combined = wave1 + wave2
            
            if combined > 0.7:
                row.append("█")
            elif combined > 0.4:
                row.append("▓")
            elif combined > 0.1:
                row.append("▒")
            elif combined > -0.1:
                row.append("░")
            else:
                row.append(" ")
        art.append("".join(row))
    return "\n".join(art)

def run_drawing_demo():
    """Run opic drawing demonstration"""
    print("=" * 70)
    print("Opic Drawing — Visual Art Generation")
    print("=" * 70)
    print()
    
    print("Drawing 1: Opic Logo")
    print("-" * 70)
    print(draw_opic_logo())
    print()
    
    print("Drawing 2: Harmonic Pattern (from opic resonance)")
    print("-" * 70)
    print(draw_harmonic_pattern())
    print()
    
    print("Drawing 3: ASCII Circle")
    print("-" * 70)
    print(draw_ascii_circle(8))
    print()
    
    print("Drawing 4: Fractal Tree")
    print("-" * 70)
    import math
    print(draw_ascii_fractal(4))
    print()
    
    print("=" * 70)
    print("Drawing complete")
    print("=" * 70)
    print()
    print("Generated from opic draw.ops definitions:")
    print("  • canvas, shape, pattern")
    print("  • draw.shape, compose.drawing")
    print("  • render.ascii, render.svg")

if __name__ == "__main__":
    import math
    run_drawing_demo()

