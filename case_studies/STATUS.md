# Case Studies Status - One by One Review

## 1. COSMOLOGY

**Files:** include-free `main.ops`

**Output:** `.out/case_studies/core/cosmology/predictions.out`

**Status:** ✅ Emits CMB / NFW / BAO field report

---

## 2. REASONING

**Files:** include-free `main.ops`

**Output:** `.out/case_studies/core/reasoning/explanations.out`

**Status:** ✅ Narrative reasoning & self-explanation

---

## 3. TESTS

**Files:** include-free `main.ops`

**Output:** `.out/case_studies/core/tests/tests.out`

**Status:** ✅ Describes field-based test harness

---

## 4. COMPRESSION

**Files:** include-free `main.ops`

**Output:** `.out/case_studies/core/compression/compression.out`

**Status:** ✅ Field-first compression narrative

---

## 5. EMERGENT

**Files:** include-free `main.ops`

**Output:** `.out/case_studies/core/emergent/emergent.out`

**Status:** ✅ Actor-coupled modeling summary

---

## 6. SOLVE

**Files:** include-free `main.ops`

**Output:** `.out/case_studies/core/solve/solve.out`

**Status:** ✅ Solve → emit report

---

## Next Steps

## 7. WHITEPAPER (Typst)

**Files:** `systems/whitepaper.ops`

**Output:** `docs/whitepaper/invariant_whitepaper.typ` + `docs/whitepaper/invariant_whitepaper.pdf`

**Status:** ✅ Generates lemma/theorem/proof whitepaper via `make typst`

---

## Next Steps

1. Keep the Makefile targets in sync with the `.out` reports and the typst whitepaper.
2. When adding a new case study, follow the same pattern: include-free `main.ops`, `make <target>`, output under `.out/case_studies/<path>/`.

