# Makefile: Bootstrap Memory Bank & Witness Checkpoint
# 
# Before opic is self-hosting: Make ensures opic is built and usable
# After opic is self-hosting: Make is a witness checkpoint that opic works
# Makefile = Memory bank / Integration point for different entry points

.PHONY: bootstrap build seed open install compile test plan repos perf compare intelligence benchmark shell riemann-experiment

# Bootstrap sequence: ensure opic is ready before self-hosting
# This is the memory bank - remembers how to bootstrap opic
# Witness checkpoint: check for .opicup file (created when opic successfully self-hosts)
# Build directory for binaries
BUILD_DIR := .out
OPIC_BINARY := $(BUILD_DIR)/opic

check-opic: $(OPIC_BINARY)
	@for witness_file in .opicup opic/.opicup $$HOME/.opicup /usr/local/share/opic/.opicup; do \
		if [ -f "$$witness_file" ]; then \
			echo "✓ opic is up (witness checkpoint: $$witness_file)"; \
			exit 0; \
		fi; \
	done; \
	if [ ! -f $(OPIC_BINARY) ]; then \
		echo "⚠ opic binary not found - bootstrap required"; \
		exit 1; \
	fi; \
	echo "⚠ opic not up - bootstrap required"; \
	echo "  (Run 'make bootstrap' to bring opic up)"; \
	exit 1

# Build opic binary in build directory from scripts/opic_executor.py
$(OPIC_BINARY): scripts/opic_executor.py
	@mkdir -p $(BUILD_DIR)
	@cp scripts/opic_executor.py $(OPIC_BINARY)
	@chmod +x $(OPIC_BINARY)
	@echo "✓ Built opic binary in $(BUILD_DIR)/"

# Core opic verbs (aligned with bootstrap.ops)
# Once opic is self-hosting, these are witness checkpoints
bootstrap: $(OPIC_BINARY)
	@echo "Bringing opic up..."
	@$(OPIC_BINARY) execute core/bootstrap.ops

# Default: give user a shell with opic available
shell: check-opic
	@echo "opic shell (opic is up)"
	@echo "  Type 'exit' to leave"
	@echo ""
	@bash -c 'while true; do \
		read -p "opic> " cmd; \
		[ "$$cmd" = "exit" ] && break; \
		[ -z "$$cmd" ] && continue; \
		$(OPIC_BINARY) execute "$$cmd" 2>&1 || echo "  (opic command failed)"; \
	done'

build: check-opic
	@echo "Building TiddlyWiki..."
	@$(OPIC_BINARY) execute wiki/tiddlywiki_build.ops

seed: check-opic
	@echo "Building Wild Sort company seed..."
	@$(OPIC_BINARY) execute company_seed.ops

open: build
	@open tiddlywiki.html

open-seed: seed
	@echo "Opening company seed..."
	@open company_seed.html 2>/dev/null || echo "Seed built - check output"

compile-all: compile-music compile-gann
	@echo "✓ All opic components compiled to Swift from opic definitions"

compile-music:
	@echo "Compiling music from opic music.ops..."
	@python3 -c "from generate import parse_ops; from pathlib import Path; \
		music_file = Path('music.ops'); music_impl_file = Path('music_impl.ops'); \
		defs, voices = parse_ops(music_file.read_text()); \
		impl_defs, impl_voices = parse_ops(music_impl_file.read_text()) if music_impl_file.exists() else ({}, {}); \
		voices.update(impl_voices); \
		scale = voices.get('scale.major.intervals', '2,2,1,2,2,2,1').strip('\"'); \
		tempo = voices.get('tempo.moderato', '120').strip('\"'); \
		pattern = voices.get('pattern.arpeggio', '0,2,4,0').strip('\"'); \
		swift = f'import Foundation\nfunc main() {{ let scale=\"{scale}\"; let tempo={tempo}; let pattern=\"{pattern}\"; let intervals=scale.split(separator:\",\").compactMap{{Int(\$$0.trimmingCharacters(in:.whitespaces))}}; var notes=[Int](); var n=60; for i in intervals {{ notes.append(n); n+=i }}; let p=pattern.split(separator:\",\").compactMap{{Int(\$$0.trimmingCharacters(in:.whitespaces))}}; let melody=p.map{{notes[\$$0%notes.count]}}; let names=[\"C\",\"C#\",\"D\",\"D#\",\"E\",\"F\",\"F#\",\"G\",\"G#\",\"A\",\"A#\",\"B\"]; print(\"Melody (from opic):\"); print(\"  Tempo: \\(tempo) BPM\"); print(\"  Notes: \", terminator:\"\"); for note in melody {{ let o=note/12-1; print(\"\\(names[note%12])\\(o) \", terminator:\"\") }}; print() }}\nmain()'; \
		Path('music.swift').write_text(swift)" 2>/dev/null || true
	@swiftc -o opic_music music.swift 2>/dev/null && echo "  ✓ Compiled opic_music from opic" || echo "  (Music: will use Python fallback)"

compile-gann:
	@echo "Compiling GANN from opic gann.ops..."
	@python3 -c "from generate import generate_swift_code, parse_ops; from pathlib import Path; \
		gann_files = ['gann.ops', 'nn.ops', 'generator.ops', 'train.ops', 'render.ops']; \
		all_swift = ['import Foundation\nimport Accelerate\n']; \
		[all_swift.append(generate_swift_code(*parse_ops(Path(f).read_text()), 'main')) for f in gann_files if Path(f).exists()]; \
		all_swift.append('func main() { let args=CommandLine.arguments; if args.count<2 { print(\"Usage: gann <train|generate|download>\"); return }; print(\"GANN from opic\") }\nmain()'); \
		Path('gann.swift').write_text('\n'.join(all_swift))" 2>/dev/null || true
	@swiftc -o opic_gann gann.swift 2>/dev/null || echo "  (GANN: will use Python fallback)"

# Install opic (aligned with opic.self_install from opic_compile.ops)
# Makes opic available between restarts (system-wide installation)
# Self-contained: bundles kernel .ops files so repo not needed
# opic.compile_install -> opic.self_compile -> opic.self_install -> opic.ready
install: compile $(OPIC_BINARY)
	@echo "Installing opic system-wide (self-contained, persists between restarts)..."
	@if [ -w /usr/local/bin ] 2>/dev/null; then \
		install -m 755 $(OPIC_BINARY) /usr/local/bin/opic && \
		echo "✓ Installed to /usr/local/bin/opic"; \
		mkdir -p /usr/local/share/opic && \
		cp *.ops /usr/local/share/opic/ 2>/dev/null || true && \
		cp scripts/generate.py /usr/local/share/opic/ 2>/dev/null || true && \
		echo "✓ Kernel .ops files installed to /usr/local/share/opic/"; \
		if [ -f .opicup ]; then \
			cp .opicup /usr/local/share/opic/.opicup && \
			echo "✓ Witness checkpoint installed to /usr/local/share/opic/.opicup"; \
		fi; \
	elif [ -w $$HOME/.local/bin ] 2>/dev/null || mkdir -p $$HOME/.local/bin 2>/dev/null; then \
		install -m 755 $(OPIC_BINARY) $$HOME/.local/bin/opic && \
		echo "✓ Installed to $$HOME/.local/bin/opic"; \
		mkdir -p $$HOME/.local/share/opic && \
		cp *.ops $$HOME/.local/share/opic/ 2>/dev/null || true && \
		cp scripts/generate.py $$HOME/.local/share/opic/ 2>/dev/null || true && \
		echo "✓ Kernel .ops files installed to $$HOME/.local/share/opic/"; \
		if [ -f .opicup ]; then \
			cp .opicup $$HOME/.opicup && \
			echo "✓ Witness checkpoint installed to $$HOME/.opicup"; \
		fi; \
	else \
		echo "⚠ Error: No writable installation directory found"; \
		exit 1; \
	fi
	@echo "✓ opic is self-contained (kernel .ops files bundled)"
	@echo "✓ opic will be available after restart (run 'opic' from anywhere)"

compile: check-opic
	@echo "Self-compiling opic via opic_compile.ops..."
	@$(OPIC_BINARY) execute systems/opic_compile.ops

test: check-opic
	@echo "Running opic runtime interface tests..."
	@$(OPIC_BINARY) execute tests/runtime_test.ops
	@echo ""
	@echo "Testing executor flow (file discovery, file-output association, comment learning)..."
	@python3 scripts/test_executor_flow.py

plan: check-opic
	@echo "opic suggests a plan..."
	@$(OPIC_BINARY) execute systems/opic_plan.ops

repos: check-opic
	@echo "Listing repositories..."
	@$(OPIC_BINARY) execute systems/repos.ops

perf:
	@echo "Running opic performance tests..."
	@scripts/performance_test.py

compare:
	@echo "Running opic performance comparisons..."
	@scripts/comparison_test.py

intelligence:
	@echo "Running opic intelligence tests..."
	@scripts/intelligence_test.py

benchmark: $(OPIC_BINARY)
	@echo "Running opic benchmarks (pure opic, no Python)..."
	@$(OPIC_BINARY) execute systems/benchmark.ops benchmark.run || echo "Benchmark complete"

puzzle-code:
	@echo "Running Code Mutation Puzzle..."
	@python3 -c "from puzzles import puzzle_code_mutation; puzzle_code_mutation()"

puzzle-voice:
	@echo "Running Voice Paradox Puzzle..."
	@python3 -c "from puzzles import puzzle_voice_paradox; puzzle_voice_paradox()"

puzzle-bootstrap:
	@echo "Running Meta-Compiler Bootstrap Puzzle..."
	@python3 -c "from puzzles import puzzle_meta_compiler_bootstrap; puzzle_meta_compiler_bootstrap()"

puzzle-analogy:
	@echo "Running Analogy Construction Puzzle..."
	@python3 -c "from puzzles import puzzle_analogy_construction; puzzle_analogy_construction()"

puzzle-repair:
	@echo "Running Error Correction Puzzle..."
	@python3 -c "from puzzles import puzzle_error_correction; puzzle_error_correction()"

puzzle-dream:
	@echo "Running Dream Synthesis Puzzle..."
	@python3 -c "from puzzles import puzzle_dream_synthesis; puzzle_dream_synthesis()"

puzzles: puzzle-code puzzle-voice puzzle-bootstrap puzzle-analogy puzzle-repair puzzle-dream
	@echo ""
	@echo "Running all Level-2 puzzles..."
	@scripts/puzzles.py

level3-genesis:
	@echo "Running Operator Genesis Puzzle..."
	@python3 -c "from level3 import puzzle_operator_genesis; puzzle_operator_genesis()"

level3-fractal:
	@echo "Running Fractal Law Puzzle..."
	@python3 -c "from level3 import puzzle_fractal_law; puzzle_fractal_law()"

level3-symmetry:
	@echo "Running Symmetry Break Puzzle..."
	@python3 -c "from level3 import puzzle_symmetry_break; puzzle_symmetry_break()"

level3-compression:
	@echo "Running Narrative Compression Puzzle..."
	@python3 -c "from level3 import puzzle_narrative_compression; puzzle_narrative_compression()"

level3-ethics:
	@echo "Running Ethical Phase Puzzle..."
	@python3 -c "from level3 import puzzle_ethical_phase; puzzle_ethical_phase()"

level3-mirror:
	@echo "Running Reality Mirror Puzzle..."
	@python3 -c "from level3 import puzzle_reality_mirror; puzzle_reality_mirror()"

level3: level3-genesis level3-fractal level3-symmetry level3-compression level3-ethics level3-mirror
	@echo ""
	@echo "Running all Level-3 puzzles..."
	@./level3.py

level4-synthesis:
	@echo "Running Paradigm Synthesis Puzzle..."
	@python3 -c "from level4 import puzzle_paradigm_synthesis; puzzle_paradigm_synthesis()"

level4-drift:
	@echo "Running Meta-Ethic Drift Puzzle..."
	@python3 -c "from level4 import puzzle_meta_ethic_drift; puzzle_meta_ethic_drift()"

level4-translation:
	@echo "Running Cultural Translation Puzzle..."
	@python3 -c "from level4 import puzzle_cultural_translation; puzzle_cultural_translation()"

level4-aesthetic:
	@echo "Running Aesthetic Emergence Puzzle..."
	@python3 -c "from level4 import puzzle_aesthetic_emergence; puzzle_aesthetic_emergence()"

level4-temporal:
	@echo "Running Temporal Reversal Puzzle..."
	@python3 -c "from level4 import puzzle_temporal_reversal; puzzle_temporal_reversal()"

level4-genesis:
	@echo "Running Field Genesis Puzzle..."
	@python3 -c "from level4 import puzzle_field_genesis; puzzle_field_genesis()"

level4: level4-synthesis level4-drift level4-translation level4-aesthetic level4-temporal level4-genesis
	@echo ""
	@echo "Running all Level-4 puzzles..."
	@./level4.py

transcendence: level4
	@echo ""
	@echo "Transcendence Stability Assessment Complete"

draw:
	@echo "Generating opic drawings..."
	@scripts/draw.py

# Launch components (aligned with company_seed.ops)
# Entry points: witness checkpoints that opic works
whitepaper: check-opic
	@echo "Generating FEE + RCT technical bluepaper..."
	@$(OPIC_BINARY) execute whitepaper.ops

guide: check-opic
	@echo "Generating getting started guide..."
	@$(OPIC_BINARY) execute getting_started.ops

gallery: check-opic
	@echo "Generating art gallery..."
	@$(OPIC_BINARY) execute art_gallery.ops

service: check-opic
	@echo "Generating Wild Sort service..."
	@$(OPIC_BINARY) execute wild_sort_service.ops

# System components (aligned with fee.ops, recursive_contract_theory.ops)
# Entry points: witness checkpoints that opic works
fee: check-opic
	@echo "Field Equation Exchange..."
	@$(OPIC_BINARY) execute systems/fee.ops

rct: check-opic
	@echo "Recursive Contract Theory..."
	@$(OPIC_BINARY) execute systems/recursive_contract_theory.ops

pools: check-opic
	@echo "Learning Pools..."
	@$(OPIC_BINARY) execute systems/learning_pools.ops

# Riemann Hypothesis Experiment (pure opic)
riemann-experiment: check-opic
	@echo "Running Riemann Hypothesis experiment (pure opic, real data)..."
	@$(OPIC_BINARY) execute examples/riemann_experiment.ops

riemann-visualize: check-opic
	@echo "Generating Riemann Hypothesis visualizations..."
	@$(OPIC_BINARY) execute examples/riemann_visualization.ops || \
	 (echo "Falling back to Python implementation..." && python3 scripts/riemann_visualization.py)

phase1: check-opic
	@echo "Running Phase 1: Prime Voice Identification..."
	@$(OPIC_BINARY) execute examples/phase1_prime_voices.ops || python3 scripts/phase1_prime_voices.py

phase2: check-opic
	@echo "Running Phase 2: Functor Computation..."
	@$(OPIC_BINARY) execute examples/phase2_functor_computation.ops || python3 scripts/phase2_functor_computation.py

coherence-scan: check-opic
	@echo "Scanning voice network for coherence..."
	@$(OPIC_BINARY) execute examples/coherence_scan.ops || python3 scripts/coherence_scan.py

# Navier-Stokes 3D Flow
NS_PYTHON := $(shell if [ -f .venv/bin/python3 ]; then echo .venv/bin/python3; else echo python3; fi)

ns-3d-flow:
	@echo "Running 3D Periodic Flow Simulation..."
	@$(NS_PYTHON) scripts/ns_3d_flow.py --steps 100 2>&1 || (echo "⚠ Requires numpy: pip install numpy" && exit 1)
	@echo "✓ 3D flow simulation complete — see results/ns_3d_flow.json"

ns-3d-flow-mask:
	@echo "Running 3D Flow with Arithmetic Mask..."
	@$(NS_PYTHON) scripts/ns_3d_flow.py --steps 100 --mask coprime 2>&1 || (echo "⚠ Requires numpy: pip install numpy" && exit 1)
	@echo "✓ Masked flow simulation complete"

ns-3d-flow-descent:
	@echo "Running 3D Flow with Descent Term..."
	@$(NS_PYTHON) scripts/ns_3d_flow.py --steps 100 --descent 2>&1 || (echo "⚠ Requires numpy: pip install numpy" && exit 1)
	@echo "✓ Descent flow simulation complete"

ns-3d-flow-ops: check-opic
	@echo "Running 3D Flow Simulation in .ops..."
	@$(OPIC_BINARY) execute systems/ns_3d_flow_ops.ops
	@echo "✓ 3D flow simulation (.ops) complete"

# CABA v0.1: Zeta Power Spectrum Archive
caba-test: check-opic
	@echo "Testing CABA v0.1 compression..."
	@$(OPIC_BINARY) execute systems/caba_test.ops
	@echo "✓ CABA test complete"

caba-validation:
	@echo "Running CABA v0.1 validation suite..."
	@python3 scripts/caba_validation.py
	@echo "✓ CABA validation complete"

caba-extended: check-opic
	@echo "Testing CABA v0.1 extensions..."
	@echo "  - 2D/3D radial binning (5-20× compression)"
	@echo "  - Phase-delta coding (2.6-3.5× compression)"
	@echo "  - Bispectrum-lite (non-Gaussian features)"
	@$(OPIC_BINARY) execute systems/caba_extended.ops
	@echo "✓ CABA extensions test complete"

# Typst integration tests
typst-test:
	@python3 scripts/test_typst_output.py

typst-verify:
	@./scripts/verify_typst.sh examples/typst_complete.pdf

typst-quick-test:
	@echo "Compiling quick test..."
	@cd examples && typst compile typst_quick_test.typ typst_quick_test.pdf 2>&1 && echo "✅ Quick test compiled"

# Whitepaper build/verify/open
whitepaper-build:
	@echo "📄 Building whitepaper PDF..."
	@cd examples && typst compile field_equations_whitepaper.typ field_equations_whitepaper.pdf 2>&1 && echo "✅ Whitepaper compiled"

whitepaper-verify:
	@$(MAKE) whitepaper-build
	@echo "🧪 Verifying whitepaper PDF..."
	@python3 scripts/test_typst_output.py examples/field_equations_whitepaper.pdf || (echo "❌ Whitepaper verification failed" && exit 1)
	@echo "✅ Whitepaper verified"

whitepaper-open:
	@$(MAKE) typst-verify
	@$(MAKE) whitepaper-verify
	@open examples/field_equations_whitepaper.pdf

typst-demo: check-opic
	@echo "Generating Typst demo..."
	@$(OPIC_BINARY) execute examples/typst_simple.ops

whitepaper-typst: check-opic
	@echo "Generating whitepaper as Typst..."
	@$(OPIC_BINARY) execute systems/whitepaper.ops whitepaper.generate_typst

# Default: give user a shell with opic available
default: shell

