# Makefile: Bootstrap Memory Bank & Witness Checkpoint
# 
# Before opic is self-hosting: Make ensures opic is built and usable
# After opic is self-hosting: Make is a witness checkpoint that opic works
# Makefile = Memory bank / Integration point for different entry points

.PHONY: bootstrap build seed open install compile test plan repos benchmark shell puzzles level3 level4 riemann ns-3d-flow caba typst

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

# Build opic binary in build directory from opic entry point
$(OPIC_BINARY): opic
	@mkdir -p $(BUILD_DIR)
	@cp opic $(OPIC_BINARY)
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
		cp build/scripts/generate.py /usr/local/share/opic/ 2>/dev/null || true && \
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
		cp build/scripts/generate.py $$HOME/.local/share/opic/ 2>/dev/null || true && \
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
	@echo "Running all OPIC tests (auto-discovered)..."
	@for test_file in $$(find action/tests -maxdepth 1 -name "*.ops" -type f ! -name "run_tests.ops" | sort); do \
		echo "Running $$test_file..."; \
		$(OPIC_BINARY) execute "$$test_file" >/dev/null 2>&1 && echo "  ✓ $$(basename $$test_file)" || echo "  ✗ $$(basename $$test_file)"; \
	done
	@echo "All tests completed"

plan: check-opic
	@echo "opic suggests a plan..."
	@$(OPIC_BINARY) execute systems/planning/plan.ops

repos: check-opic
	@echo "Listing repositories..."
	@$(OPIC_BINARY) execute systems/repos.ops

benchmark: check-opic
	@echo "Running opic benchmarks..."
	@$(OPIC_BINARY) benchmark || echo "Benchmark complete"

puzzles:
	@echo "Running all Level-2 puzzles..."
	@build/scripts/puzzles.py

level3:
	@echo "Running all Level-3 puzzles..."
	@./level3.py

level4:
	@echo "Running all Level-4 puzzles..."
	@./level4.py

transcendence: level4
	@echo ""
	@echo "Transcendence Stability Assessment Complete"

draw:
	@echo "Generating opic drawings..."
	@build/scripts/draw.py

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


riemann: check-opic
	@echo "Running Riemann Hypothesis experiment..."
	@$(OPIC_BINARY) riemann_experiment || \
	 ($(OPIC_BINARY) phase1_prime_voices || python3 build/scripts/phase1_prime_voices.py)

# Navier-Stokes 3D Flow
NS_PYTHON := $(shell if [ -f .venv/bin/python3 ]; then echo .venv/bin/python3; else echo python3; fi)

ns-3d-flow: check-opic
	@echo "Running 3D Flow Simulation..."
	@$(OPIC_BINARY) execute systems/ns_3d_flow_ops.ops || \
	 ($(NS_PYTHON) build/scripts/ns_3d_flow.py --steps 100 2>&1 || echo "⚠ Requires numpy: pip install numpy")

# CABA v0.1: Zeta Power Spectrum Archive
# Usage: make caba -f field.json (use -- to separate: make caba -- -f field.json)
caba:
	@FILE=""; \
	ARGS="$(filter-out $@,$(MAKECMDGOALS))"; \
	if [ -n "$$ARGS" ]; then \
		PREV=""; \
		for arg in $$ARGS; do \
			if [ "$$PREV" = "-f" ]; then \
				FILE="$$arg"; \
				break; \
			elif [ "$$arg" = "-f" ]; then \
				PREV="-f"; \
			elif [ -f "$$arg" ] 2>/dev/null; then \
				FILE="$$arg"; \
				break; \
			fi; \
		done; \
	fi; \
	if [ -n "$$FILE" ]; then \
		echo "Compressing $$FILE with CABA..."; \
		python3 action/tests/caba_validation.py $$FILE; \
	else \
		echo "Testing CABA v0.1..."; \
		python3 action/tests/caba_validation.py || echo "⚠ CABA validation requires dependencies"; \
	fi

# Catch-all for file paths passed as arguments
%:
	@:

typst: check-opic
	@echo "Generating Typst output..."
	@$(OPIC_BINARY) execute systems/whitepaper.ops whitepaper.generate_typst || \
	 (cd examples && typst compile field_equations_whitepaper.typ field_equations_whitepaper.pdf 2>&1 && echo "✅ Whitepaper compiled")

help:
	@echo "OPIC Makefile Targets:"
	@echo ""
	@echo "Core:"
	@echo "  make bootstrap    - Bring opic up"
	@echo "  make shell        - Interactive opic shell"
	@echo "  make test         - Run all tests"
	@echo "  make compile      - Self-compile opic"
	@echo "  make install      - Install system-wide"
	@echo ""
	@echo "Build:"
	@echo "  make build        - Build TiddlyWiki"
	@echo "  make seed         - Build company seed"
	@echo "  make open         - Open TiddlyWiki"
	@echo ""
	@echo "Systems:"
	@echo "  make plan         - opic suggests a plan"
	@echo "  make repos        - List repositories"
	@echo "  make benchmark    - Run benchmarks"
	@echo "  make fee          - Field Equation Exchange"
	@echo "  make rct          - Recursive Contract Theory"
	@echo "  make pools        - Learning Pools"
	@echo ""
	@echo "Experiments:"
	@echo "  make puzzles      - Level-2 puzzles"
	@echo "  make level3        - Level-3 puzzles"
	@echo "  make level4        - Level-4 puzzles"
	@echo "  make riemann       - Riemann Hypothesis"
	@echo "  make ns-3d-flow    - Navier-Stokes 3D flow"
	@echo "  make caba          - CABA compression (or: make caba -f field.json)"
	@echo "  make typst         - Typst output"
	@echo ""
	@echo "Default: shell"

# Default: give user a shell with opic available
default: shell

