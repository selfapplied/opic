#!/usr/bin/env python3
"""
Render a simple radial bloom SVG from JSONL traces.
Input: path to data/field_traces.jsonl
Output: SVG to stdout
"""
import sys
import json
from math import cos, sin, pi

def load_traces(path):
    traces = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            traces.append(obj)
    return traces

def normalize(values):
    if not values:
        return [0.0]
    mn = min(values)
    mx = max(values)
    if mx - mn < 1e-9:
        return [0.5 for _ in values]
    return [(v - mn) / (mx - mn) for v in values]

def main():
    if len(sys.argv) < 2:
        print("Usage: bloom_svg.py path/to/field_traces.jsonl", file=sys.stderr)
        sys.exit(1)
    path = sys.argv[1]
    traces = load_traces(path)
    if not traces:
        print("<svg xmlns='http://www.w3.org/2000/svg' width='800' height='800'/>")
        return
    # Use entropy as radius, boundary as stroke alpha, group by file to color
    ent = [t.get("phi_entropy", 0.0) for t in traces]
    bnd = [t.get("boundary_score", 0.0) for t in traces]
    ent_n = normalize(ent)
    bnd_n = normalize(bnd)
    # Simple palette
    files = list({t["file"] for t in traces})
    file_to_hue = {f: (i * 137) % 360 for i, f in enumerate(files)}
    cx = cy = 400
    R = 360
    N = len(traces)
    print(f"<svg xmlns='http://www.w3.org/2000/svg' width='800' height='800' viewBox='0 0 800 800'>")
    print(f"  <rect x='0' y='0' width='800' height='800' fill='white'/>")
    print(f"  <g transform='translate({cx},{cy})'>")
    for i, t in enumerate(traces):
        theta = 2 * pi * (i / N)
        radius = 40 + ent_n[i] * R
        x = radius * cos(theta)
        y = radius * sin(theta)
        hue = file_to_hue.get(t["file"], 200)
        alpha = 0.2 + 0.8 * bnd_n[i]
        stroke = f"hsla({hue},60%,45%,{alpha:.3f})"
        print(f"    <line x1='0' y1='0' x2='{x:.2f}' y2='{y:.2f}' stroke='{stroke}' stroke-width='1'/>")
    print("  </g>")
    print("</svg>")

if __name__ == "__main__":
    main()


