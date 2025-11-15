# ZetaCore: Topological Map UI Sketch

## Overview

ZetaCore is an interactive visualization tool for exploring the topological and spectral structure of OPIC voice compositions. It provides a real-time map of the field geometry, showing how voices are embedded, how chains flow, and how invariants are preserved during composition.

## Core Visualization: The Topological Map

### Layout

```
┌─────────────────────────────────────────────────────────────┐
│  ZetaCore - OPIC Field Geometry Explorer          [_][□][×] │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────────────────────────┐  ┌───────────────┐ │
│  │                                     │  │  Invariants   │ │
│  │                                     │  │               │ │
│  │         TOPOLOGICAL MAP             │  │  Energy: ████ │ │
│  │                                     │  │  Coherence:██ │ │
│  │    ○ ──→ ○ ──→ ○                   │  │  Momentum: ██ │ │
│  │   voice1  voice2  voice3           │  │               │ │
│  │                                     │  │  ┌─────────┐  │ │
│  │    ○                                │  │  │ Prime   │  │ │
│  │   ╱ ╲                               │  │  │ Voices: │  │ │
│  │  ○   ○                              │  │  │   42    │  │ │
│  │  voice4 voice5                      │  │  └─────────┘  │ │
│  │                                     │  │               │ │
│  └─────────────────────────────────────┘  └───────────────┘ │
│                                                               │
│  ┌─────────────────────────────────────┐  ┌───────────────┐ │
│  │  Critical Line Projection           │  │  Chain Flow   │ │
│  │                                     │  │               │ │
│  │   Re(s) = 1/2                       │  │  step1 → ...  │ │
│  │     │                               │  │  step2 → ...  │ │
│  │  ───┼───  ×  ×    ×     ×           │  │  step3 → ...  │ │
│  │     │                               │  │               │ │
│  │     └────────────────── Im(s)       │  │  Converged: ✓ │ │
│  │                                     │  │               │ │
│  └─────────────────────────────────────┘  └───────────────┘ │
│                                                               │
│  [Load .ops] [Export Geometry] [Settings]    Status: Ready  │
└─────────────────────────────────────────────────────────────┘
```

## Components

### 1. Main Topological Map (Top Left)

**Purpose:** Visualize the field geometry where voices are embedded as nodes and chains as edges.

**Visual Elements:**
- **Nodes (○):** Individual voices, sized by complexity
- **Edges (──→):** Chain composition relationships
- **Clusters:** Groups of related voices (same universality class)
- **Color coding:** 
  - Blue: primitive voices (no dependencies)
  - Green: composite voices (built from others)
  - Red: voices with certificate warnings
  - Gold: prime voices (irreducible)

**Interactions:**
- Click node: show voice details
- Drag node: reposition in visualization
- Hover edge: show composition details
- Right-click: context menu (inspect, modify, remove)

### 2. Invariant Panel (Top Right)

**Purpose:** Real-time monitoring of preserved invariants

**Displays:**
- Bar charts for each tracked invariant
- Threshold indicators (yellow = warning, red = violation)
- Historical trends (sparklines)
- Prime voice counter

**Interactions:**
- Click invariant: show detailed breakdown
- Toggle visibility of specific invariants
- Set alert thresholds

### 3. Critical Line Projection (Bottom Left)

**Purpose:** Show spectral structure using zeta function visualization

**Visual Elements:**
- Horizontal axis: imaginary part Im(s)
- Vertical line: critical line Re(s) = 1/2
- Points (×): known zeta zeros
- Colored regions: spectral energy density
- Voice markers: position of voice spectral signatures

**Interactions:**
- Zoom/pan along imaginary axis
- Hover over zeros: show numerical values
- Click voice marker: highlight in main map

### 4. Chain Flow Monitor (Bottom Right)

**Purpose:** Show active chain execution and RG flow convergence

**Displays:**
- Current chain steps
- RG flow trajectory
- Convergence status
- Performance metrics

**Interactions:**
- Step through chain execution
- Pause/resume flow
- Export flow data

## API Hooks for Integration

### JavaScript Interface

```javascript
// Initialize ZetaCore with OPIC geometry
const zeta = new ZetaCore({
    container: '#zeta-map',
    geometry: opicGeometry,  // From initialize_field_geometry
    options: {
        topology: 'euclidean',
        dimension: 2,
        showInvariants: true,
        showCriticalLine: true
    }
});

// Load voice composition
zeta.loadVoices(voiceDefinitions);

// Update in real-time as chain executes
zeta.onChainStep((step) => {
    zeta.highlightVoice(step.voice);
    zeta.updateInvariants(step.invariants);
});

// Apply spectral filter
zeta.applyZetaFilter({
    criticalLineProjection: true,
    cutoffFrequency: 100
});

// Monitor RG flow
zeta.startRGFlow({
    operator: rgOperator,
    initialState: currentGeometry,
    steps: 10,
    onConvergence: (result) => {
        console.log('RG flow converged at step', result.convergence_step);
    }
});
```

### Python Backend Integration

```python
# In OPIC runtime, export geometry for visualization
from src.opic.parser import initialize_field_geometry
from src.aquifer import zeta_spectral_filter, rg_flow

# Parse code and build geometry
geometry = initialize_field_geometry(opic_source_code)

# Apply spectral analysis
spectrum = extract_voice_spectrum(geometry['voices'])
filtered = zeta_spectral_filter(spectrum, critical_line_projection=True)

# Run RG flow
flow_result = rg_flow(
    operator=coarse_grain_voices,
    initial_state=geometry,
    steps=10
)

# Export for UI
zeta_data = {
    'geometry': geometry,
    'spectrum': filtered,
    'rg_flow': flow_result
}

# Serve to frontend
serve_zeta_visualization(zeta_data)
```

## Technology Stack

### Frontend
- **D3.js:** Graph visualization for topological map
- **Three.js:** 3D visualization for complex geometries
- **React:** Component framework for UI panels
- **WebSocket:** Real-time updates from OPIC runtime

### Backend
- **Flask/FastAPI:** REST API for geometry data
- **NumPy/SciPy:** Numerical computations
- **NetworkX:** Graph analysis for voice dependencies

## Future Enhancements

1. **3D Topology Visualization:** Explore higher-dimensional field geometries
2. **Animation:** Show RG flow as smooth animation
3. **Collaborative Mode:** Multiple users explore same geometry
4. **Voice Editor:** Directly modify voices in the topological map
5. **Benchmark Overlay:** Show performance metrics on topology
6. **Certificate Validation UI:** Visual verification of cryptographic signatures
7. **Export Formats:** Save visualizations as SVG, PNG, or interactive HTML

## File Organization

```
ui/zeta_core/
├── sketch.md                 (this file)
├── src/
│   ├── index.html           (main entry point)
│   ├── components/
│   │   ├── TopologicalMap.jsx
│   │   ├── InvariantPanel.jsx
│   │   ├── CriticalLineView.jsx
│   │   └── ChainFlowMonitor.jsx
│   ├── lib/
│   │   ├── geometry.js      (geometry manipulation)
│   │   ├── spectral.js      (spectral analysis viz)
│   │   └── rg.js            (RG flow visualization)
│   └── styles/
│       └── zeta.css
├── api/
│   ├── server.py            (Flask/FastAPI backend)
│   ├── geometry_endpoint.py
│   └── realtime_ws.py       (WebSocket handler)
└── tests/
    └── ui_tests.js
```

## Development Roadmap

**Phase 1: Prototype (Current)**
- [x] UI sketch and mockups
- [ ] Basic topological map with D3.js
- [ ] Static geometry loading

**Phase 2: Integration**
- [ ] Connect to OPIC parser output
- [ ] Real-time invariant monitoring
- [ ] Basic spectral visualization

**Phase 3: Advanced Features**
- [ ] RG flow animation
- [ ] Interactive voice editing
- [ ] 3D topology support

---

*ZetaCore transforms abstract field geometry into tangible, interactive experience.*
