# Primorial-Masked Spectral Sensing: Encoding & Decoding Protocol v0.1

**We test decoding advantage; we do not claim P=NP.**

This is structured sensing/steganography: can primorial-masked flow fields encode and decode computational problems better than baselines?

## The Question

How do **P=NP**, **primorials**, and **field equations** relate?

## Three Threads

### 1. P=NP — Computational Complexity

**Question**: Can problems with polynomial-time verification be solved in polynomial time?

**Core tension**: 
- **P**: Problems solvable in polynomial time
- **NP**: Problems verifiable in polynomial time
- **P=NP?**: Is verification equivalent to solution?

### 2. Primorials — Arithmetic Structure

**Definition**: `p# = ∏_{i=1}^n p_i` (product of first n primes)

**In our flow solver**: Coprime mask `M(|k|) = 1 if gcd(|k|, p#) = 1 else β`

**Properties**:
- Arithmetic sieve: filters modes based on number-theoretic properties
- Creates structured patterns in Fourier spectrum
- Connects discrete arithmetic to continuous field dynamics

### 3. Field Equations — Physical Evolution

**Navier-Stokes**: `∂_t u = Π(-u·∇u) + νΔu + f`

**ζ-field**: `dΦ/dt = ∇·J + S`

**Properties**:
- Evolution equations: state → state'
- Verification: check invariants (divL2, Parseval, energy budget)
- Solution: compute evolution

## The Connection Hypothesis

### Field Evolution as Computation

**Field equations encode computational problems**:
- **State space**: All possible field configurations
- **Evolution**: Computational steps (RK4, projection, etc.)
- **Solution**: Finding the evolved state
- **Verification**: Checking invariants (divL2 < 1e-12, Parseval, etc.)

### Primorials as Arithmetic Filters

**Primorial masks filter field modes**:
- Select modes coprime to p# → arithmetic structure
- Create spectral patterns → information encoding
- Filter = computation → which modes survive?

**Key insight**: Primorials create **arithmetic sieves** that:
1. Filter Fourier modes based on number theory
2. Create structured patterns in field spectrum
3. Encode information in arithmetic properties

### P=NP as Field Verification

**Field verification**:
- **Check invariants**: divL2, Parseval, energy budget
- **Polynomial time**: O(N³) to check divergence, energy, etc.
- **Solution**: O(N³ × steps) to evolve field

**Question**: Can verifying field invariants be as hard as computing evolution?

**Primorial connection**: 
- Primorial masks create **arithmetic structure** in field
- This structure might encode **computational problems**
- Verifying arithmetic properties (gcd, primality) relates to P=NP

## Concrete Experiment: Encode–Evolve–Decode (Falsifiable)

### Goal

**Test whether primorial-masked flow gives any computational advantage in decoding NP-style structure vs baselines.**

### 1. Formalize the Pipeline

**Instance → spectrum (encoder)**: Map 3-SAT formula Φ(n vars, m clauses) to initial spectrum û₀(k) by assigning clause literals to disjoint k-shells; use public scheme, documented and invertible.

**Evolve (flow)**: Run incompressible 3D solver with: projection every RK stage, 2/3 dealiasing, same ν, dt, k_f; compare mask=off vs mask=primorial(2310).

**Observables (measurement)**: At fixed times, record E(k), few low-order moments, small set of linear probes in k-space (keep polynomial in n).

**Decoder**: Attempt to recover satisfying assignment from observables.

### 2. Claims to Test (Pre-Registered)

**C1 (completeness)**: If Φ is satisfiable, decoder returns witness with probability ≥ 0.9 using polynomial time and polynomially many observables.

**C2 (soundness)**: If Φ is unsatisfiable, decoder rejects with probability ≥ 0.9.

**C3 (advantage)**: Masked flow achieves strictly higher success or lower sample complexity than:
- Baseline flow (mask off)
- Random linear filter (same sparsity)
- Linear evolution (heat equation)

### 3. Metrics

Success rate vs n, m; wall-time; sample complexity; mutual information I(assignment; observables) estimated via classifier-based MI or variational bounds; robustness to noise; seed stability.

### 4. Controls

**Shuffle instance–wavenumber mapping** (permute shells) → decoder should fail if relies on accidental correlations.

**Swap primorial(2310) for matched-density random mask** → if performance stays same, primorial arithmetic wasn't key.

**Disable nonlinearity** (linearized flow) → checks whether nonlinearity does useful "mixing."

### 5. Acceptance

**Only if C1–C3 beat all controls with clear stats (CI, p-values) do we claim decoding advantage.** That's still not P=NP; it's an empirical computational effect to study.

## Concrete Experiment

### Test: Primorial Mask → Computational Encoding

1. **Encode problem**: Map SAT/3-SAT → field initial condition
2. **Apply primorial mask**: Filter modes coprime to p#
3. **Evolve field**: Run Navier-Stokes
4. **Read spectrum**: Extract solution from E(k) patterns
5. **Verify**: Check invariants (polynomial time)

**If P=NP**: Invariants reveal solution → verification = solution

### Arithmetic Structure → Information

**Primorial masks create**:
- **Spectral dents**: Patterns in E(k) at arithmetic shells
- **Mode selection**: Only coprime modes survive
- **Information encoding**: Arithmetic properties encode computation

**Question**: Can these arithmetic patterns encode computational problems?

## Connection to opic Architecture

**opic's dual structure**:
- **Left flank (Category)**: Discrete, logical, morphic
- **Right flank (Field)**: Continuous, analytic, resonant

**Primorials bridge**: Arithmetic structure connects discrete (primes) to continuous (field)

**Certificate operator**: Unitary transformation equating both halves

**Note**: This is about structured sensing, not P=NP proof.

## References

- Primorial masks in `systems/flow3d_mask.ops`
- Field equations in `systems/flow3d_core.ops`
- ζ-field framework in `docs/theory.md`
- Riemann Hypothesis structure in `docs/riemann_whitepaper.md`

