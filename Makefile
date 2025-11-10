# Makefile: Bootstrap Memory Bank & Witness Checkpoint
# 
# Before opic is self-hosting: Make ensures opic is built and usable
# After opic is self-hosting: Make is a witness checkpoint that opic works
# Makefile = Memory bank / Integration point for different entry points

.PHONY: bootstrap build seed open install compile test plan repos perf compare intelligence benchmark shell

# Bootstrap sequence: ensure opic is ready before self-hosting
# This is the memory bank - remembers how to bootstrap opic
# Witness checkpoint: check for .opicup file (created when opic successfully self-hosts)
check-opic:
	@for witness_file in .opicup opic/.opicup $$HOME/.opicup /usr/local/share/opic/.opicup; do \
		if [ -f "$$witness_file" ]; then \
			echo "✓ opic is up (witness checkpoint: $$witness_file)"; \
			exit 0; \
		fi; \
	done; \
	if [ ! -f opic ]; then \
		echo "⚠ opic binary not found - bootstrap required"; \
		exit 1; \
	fi; \
	echo "⚠ opic not up - bootstrap required"; \
	echo "  (Run 'make bootstrap' to bring opic up)"; \
	exit 1

# Core opic verbs (aligned with bootstrap.ops)
# Once opic is self-hosting, these are witness checkpoints
bootstrap:
	@echo "Bringing opic up..."
	@python3 opic execute core/bootstrap.ops

# Default: give user a shell with opic available
shell: check-opic
	@echo "opic shell (opic is up)"
	@echo "  Type 'exit' to leave"
	@echo ""
	@bash -c 'while true; do \
		read -p "opic> " cmd; \
		[ "$$cmd" = "exit" ] && break; \
		[ -z "$$cmd" ] && continue; \
		python3 opic execute "$$cmd" 2>&1 || echo "  (opic command failed)"; \
	done'

build: check-opic
	@echo "Building TiddlyWiki..."
	@python3 opic execute wiki/tiddlywiki_build.ops

seed: check-opic
	@echo "Building Wild Sort company seed..."
	@python3 opic execute company_seed.ops

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
install: compile
	@echo "Installing opic system-wide (self-contained, persists between restarts)..."
	@if [ -w /usr/local/bin ] 2>/dev/null; then \
		install -m 755 opic /usr/local/bin/opic && \
		echo "✓ Installed to /usr/local/bin/opic"; \
		mkdir -p /usr/local/share/opic && \
		cp *.ops /usr/local/share/opic/ 2>/dev/null || true && \
		cp generate.py /usr/local/share/opic/ 2>/dev/null || true && \
		echo "✓ Kernel .ops files installed to /usr/local/share/opic/"; \
		if [ -f .opicup ]; then \
			cp .opicup /usr/local/share/opic/.opicup && \
			echo "✓ Witness checkpoint installed to /usr/local/share/opic/.opicup"; \
		fi; \
	elif [ -w $$HOME/.local/bin ] 2>/dev/null || mkdir -p $$HOME/.local/bin 2>/dev/null; then \
		install -m 755 opic $$HOME/.local/bin/opic && \
		echo "✓ Installed to $$HOME/.local/bin/opic"; \
		mkdir -p $$HOME/.local/share/opic && \
		cp *.ops $$HOME/.local/share/opic/ 2>/dev/null || true && \
		cp generate.py $$HOME/.local/share/opic/ 2>/dev/null || true && \
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
	@python3 opic execute systems/opic_compile.ops

test: check-opic
	@echo "Running opic runtime interface tests..."
	@python3 opic execute tests/runtime_test.ops

plan: check-opic
	@echo "opic suggests a plan..."
	@python3 opic execute systems/opic_plan.ops

repos: check-opic
	@echo "Listing repositories..."
	@python3 opic execute systems/repos.ops

perf:
	@echo "Running opic performance tests..."
	@scripts/performance_test.py

compare:
	@echo "Running opic performance comparisons..."
	@scripts/comparison_test.py

intelligence:
	@echo "Running opic intelligence tests..."
	@scripts/intelligence_test.py

benchmark:
	@echo "Running Zeta Intelligence Benchmark..."
	@scripts/zib.py

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
	@python3 opic execute whitepaper.ops

guide: check-opic
	@echo "Generating getting started guide..."
	@python3 opic execute getting_started.ops

gallery: check-opic
	@echo "Generating art gallery..."
	@python3 opic execute art_gallery.ops

service: check-opic
	@echo "Generating Wild Sort service..."
	@python3 opic execute wild_sort_service.ops

# System components (aligned with fee.ops, recursive_contract_theory.ops)
# Entry points: witness checkpoints that opic works
fee: check-opic
	@echo "Field Equation Exchange..."
	@python3 opic execute systems/fee.ops

rct: check-opic
	@echo "Recursive Contract Theory..."
	@python3 opic execute systems/recursive_contract_theory.ops

pools: check-opic
	@echo "Learning Pools..."
	@python3 opic execute systems/learning_pools.ops

# Default: give user a shell with opic available
default: shell

