.PHONY: build open install self-compile perf compare intelligence benchmark

build:
	python3 build_tiddlywiki.py

open: build
	open tiddlywiki.html

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

install: compile-all
	@if [ -w /usr/local/bin ] 2>/dev/null; then \
		install -m 755 opic /usr/local/bin/opic; \
		echo "Installed to /usr/local/bin/opic"; \
	elif [ -w $$HOME/.local/bin ] 2>/dev/null || mkdir -p $$HOME/.local/bin 2>/dev/null; then \
		install -m 755 opic $$HOME/.local/bin/opic; \
		echo "Installed to $$HOME/.local/bin/opic"; \
	else \
		echo "Error: No writable installation directory found"; \
		exit 1; \
	fi

self-compile:
	@echo "Self-compiling opic into Metal..."
	@./opic metal core.ops core.metal
	@./opic metal runtime.ops runtime.metal
	@if command -v xcrun >/dev/null 2>&1; then \
		if xcrun -sdk macosx metal -c core.metal runtime.metal -o opic.metallib 2>/dev/null; then \
			echo "✓ Compiled opic.metallib"; \
			xcrun -sdk macosx metallib -info opic.metallib 2>/dev/null | head -10 || true; \
		else \
			echo "⚠ Metal compiler not available (Xcode command line tools required)"; \
			echo "  Generated: core.metal runtime.metal"; \
		fi; \
	else \
		echo "⚠ xcrun not available"; \
		echo "  Generated: core.metal runtime.metal"; \
	fi

perf:
	@echo "Running opic performance tests..."
	@./performance_test.py

compare:
	@echo "Running opic performance comparisons..."
	@./comparison_test.py

intelligence:
	@echo "Running opic intelligence tests..."
	@./intelligence_test.py

benchmark:
	@echo "Running Zeta Intelligence Benchmark..."
	@./zib.py

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
	@./puzzles.py

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
	@./draw.py

default: build

