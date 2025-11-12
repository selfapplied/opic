#!/usr/bin/env python3
"""
Add Domain-Specific Knowledge — Add detailed biology, chemistry, physics knowledge
Now with field equation mappings!
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from biology_field_mapper import BiologyFieldMapper
from astronomy_field_mapper import AstronomyFieldMapper
from pharmacology_evolution_mapper import PharmacologyEvolutionMapper
from cancer_autoimmune_mapper import CancerAutoimmuneMapper

# Domain-specific knowledge entries
DOMAIN_KNOWLEDGE = [
    # Biology - Cell Biology
    {"title": "Mitochondria", "text": "Mitochondria are organelles found in cells that produce energy through cellular respiration. They are often called the powerhouses of the cell. Mitochondria generate ATP, which is the primary energy currency of cells.", "domain": "biology"},
    {"title": "Cellular Respiration", "text": "Cellular respiration is the process by which cells convert glucose and oxygen into ATP, carbon dioxide, and water. This process occurs in mitochondria and produces energy for cellular functions.", "domain": "biology"},
    {"title": "ATP", "text": "ATP, or adenosine triphosphate, is the primary energy molecule in cells. It is produced by mitochondria through cellular respiration and used to power cellular processes.", "domain": "biology"},
    {"title": "Protein Synthesis", "text": "Protein synthesis is the process by which cells build proteins from amino acids. It occurs in ribosomes and involves transcription of DNA to RNA and translation of RNA to proteins.", "domain": "biology"},
    {"title": "DNA Replication", "text": "DNA replication is the process by which DNA makes copies of itself. It occurs before cell division and ensures genetic information is passed to daughter cells.", "domain": "biology"},
    {"title": "Cell Membrane", "text": "The cell membrane is a phospholipid bilayer that surrounds cells. It controls what enters and exits the cell and maintains cell structure.", "domain": "biology"},
    
    # Chemistry
    {"title": "Chemical Reaction", "text": "A chemical reaction is a process that transforms one set of chemical substances into another. It involves breaking and forming chemical bonds.", "domain": "chemistry"},
    {"title": "Molecule", "text": "A molecule is a group of atoms bonded together. Molecules can be simple like water (H2O) or complex like DNA.", "domain": "chemistry"},
    {"title": "Atom", "text": "An atom is the basic unit of matter. It consists of a nucleus containing protons and neutrons, surrounded by electrons.", "domain": "chemistry"},
    
    # Physics
    {"title": "Energy", "text": "Energy is the capacity to do work. It comes in many forms including kinetic energy, potential energy, thermal energy, and chemical energy.", "domain": "physics"},
    {"title": "Force", "text": "Force is a push or pull that can cause an object to accelerate. Newton's laws describe how forces affect motion.", "domain": "physics"},
    {"title": "Quantum Mechanics", "text": "Quantum mechanics is the branch of physics that describes the behavior of matter and energy at atomic and subatomic scales. It includes wave-particle duality and uncertainty principle.", "domain": "physics"},
    
    # More Biology
    {"title": "Ribosome", "text": "Ribosomes are cellular structures where protein synthesis occurs. They read messenger RNA and assemble amino acids into proteins.", "domain": "biology"},
    {"title": "Nucleus", "text": "The nucleus is the control center of the cell. It contains DNA and regulates gene expression and cell division.", "domain": "biology"},
    {"title": "Organelle", "text": "Organelles are specialized structures within cells that perform specific functions. Examples include mitochondria, ribosomes, and the nucleus.", "domain": "biology"},
    {"title": "Genetics", "text": "Genetics is the study of genes, heredity, and genetic variation. It explains how traits are passed from parents to offspring.", "domain": "biology"},
    {"title": "Evolution", "text": "Evolution is the process by which species change over time through natural selection, genetic drift, and mutation.", "domain": "biology"},
    
    # Mathematics
    {"title": "Algebra", "text": "Algebra is a branch of mathematics that uses symbols and letters to represent numbers and quantities in formulas and equations.", "domain": "mathematics"},
    {"title": "Geometry", "text": "Geometry is the branch of mathematics concerned with shapes, sizes, and properties of space. It includes Euclidean and non-Euclidean geometry.", "domain": "mathematics"},
    {"title": "Calculus", "text": "Calculus is the mathematical study of continuous change. It includes differential calculus and integral calculus.", "domain": "mathematics"},
    
    # More domain-specific entries
    {"title": "Photosynthesis", "text": "Photosynthesis is the process by which plants convert light energy into chemical energy. It produces glucose and oxygen from carbon dioxide and water.", "domain": "biology"},
    {"title": "Enzyme", "text": "Enzymes are proteins that catalyze biochemical reactions. They speed up chemical reactions in cells without being consumed.", "domain": "biology"},
    {"title": "Chromosome", "text": "Chromosomes are structures made of DNA and proteins that carry genetic information. Humans have 23 pairs of chromosomes.", "domain": "biology"},
    {"title": "Amino Acid", "text": "Amino acids are the building blocks of proteins. There are 20 standard amino acids that combine to form proteins.", "domain": "biology"},
    {"title": "Nucleotide", "text": "Nucleotides are the building blocks of DNA and RNA. They consist of a sugar, phosphate group, and nitrogenous base.", "domain": "biology"},
    
    # Astronomy - Spectroscopy
    {"title": "Stellar Spectrum", "text": "A stellar spectrum is the distribution of electromagnetic radiation from a star. It reveals the star's composition, temperature, and motion through spectral lines.", "domain": "astronomy"},
    {"title": "Spectral Lines", "text": "Spectral lines are dark or bright lines in a spectrum caused by absorption or emission of light at specific wavelengths. Each element produces characteristic spectral lines.", "domain": "astronomy"},
    {"title": "Redshift", "text": "Redshift is the increase in wavelength of light from distant objects due to cosmic expansion. It reveals the recession velocity and distance of galaxies.", "domain": "astronomy"},
    {"title": "Element Identification", "text": "Elements in stars are identified by analyzing spectral lines. Each element produces characteristic spectral lines at specific wavelengths.", "domain": "astronomy"},
    {"title": "Stellar Classification", "text": "Stars are classified by their spectral type (O, B, A, F, G, K, M) based on their spectra. Spectral type indicates temperature and composition.", "domain": "astronomy"},
    
    # Physics - Quantum Vacuum
    {"title": "Zero-Point Energy", "text": "Zero-point energy is the minimum energy that a quantum field can have, even in vacuum. It is given by E₀ = (1/2)ħω for each field mode.", "domain": "physics"},
    {"title": "Vacuum Fluctuations", "text": "Vacuum fluctuations are temporary changes in energy in empty space due to the uncertainty principle. They follow ΔE Δt ≥ ħ/2.", "domain": "physics"},
    {"title": "Planck Length", "text": "The Planck length is the fundamental length scale in physics, approximately 1.6×10⁻³⁵ meters. It is the scale where quantum gravity becomes important.", "domain": "physics"},
    {"title": "Planck Constant", "text": "The Planck constant h relates the energy of a photon to its frequency: E = hν. The reduced Planck constant ħ = h/2π is fundamental to quantum mechanics.", "domain": "physics"},
    {"title": "Casimir Effect", "text": "The Casimir effect is a force between two parallel plates in vacuum due to zero-point energy. It demonstrates that vacuum is not truly empty.", "domain": "physics"},
    {"title": "Dark Energy", "text": "Dark energy is the energy of empty space that causes cosmic acceleration. It is related to the cosmological constant and vacuum energy density.", "domain": "physics"},
    
    # Physics - Temporal Dynamics
    {"title": "Time Flow", "text": "Time flow is the progression of time. In field theory, time flow equals field flow, where temporal unfolding is field evolution ∂Φ/∂t.", "domain": "physics"},
    {"title": "Arrow of Time", "text": "The arrow of time is the direction of time determined by entropy increase. In field theory, time arrow equals field arrow, where entropy increase equals field entropy increase.", "domain": "physics"},
    {"title": "Time Dilation", "text": "Time dilation is the slowing of time for moving observers in special relativity. It follows t = γ t₀ where γ = 1/√(1 - v²/c²).", "domain": "physics"},
    {"title": "Time-Energy Uncertainty", "text": "Time-energy uncertainty is the fundamental limit on simultaneous precision of time and energy: ΔE Δt ≥ ħ/2.", "domain": "physics"},
    
    # Complex Systems - Fluid & Ecological
    {"title": "Jetstream", "text": "Jetstreams are fast-flowing air currents in the upper atmosphere. They form from pressure gradients and Coriolis effect, following atmospheric field flow equations.", "domain": "physics"},
    {"title": "Algal Bloom", "text": "Algal blooms are rapid increases in algae population. They follow population field dynamics with logistic growth: N(t) = K/(1+((K-N₀)/N₀)e^(-rt)).", "domain": "biology"},
    {"title": "Virus", "text": "Viruses are molecular field propagators that infect cells. Viral infection equals field coupling, replication equals field replication, following molecular field equations.", "domain": "biology"},
    {"title": "Viral Propagation", "text": "Viral propagation follows field propagation equations. The SIR model describes spread: I(t) ≈ I₀ e^((β-γ)t) where β is transmission rate and γ is recovery rate.", "domain": "biology"},
    
    # Linguistics - Language Evolution
    {"title": "Language Evolution", "text": "Language evolution equals field evolution. Language change, spread, and interaction all follow field equations. Linguistic forms evolve: f(t) = f₀ e^(rt).", "domain": "linguistics"},
    {"title": "Language Change", "text": "Language change equals field evolution. Phonetic, semantic, and grammatical changes follow field evolution equations. Change probability: P(change) = 1 - e^(-rt).", "domain": "linguistics"},
    {"title": "Language Spread", "text": "Language spread equals field propagation. Languages spread through populations following field diffusion equations: N(t) ∝ N₀ e^(-D/r²t). Geographic distance affects spread rate.", "domain": "linguistics"},
    {"title": "Language Contact", "text": "Language contact equals field interaction. Languages borrow features through contact, following field interaction equations. Borrowing rate ∝ contact intensity × population size.", "domain": "linguistics"},
    {"title": "Language Divergence", "text": "Language divergence equals field divergence. Languages diverge from proto-languages following field divergence equations: similarity = e^(-rt). Over time, languages become less similar.", "domain": "linguistics"},
    
    # Chemistry - Organic Chemistry
    {"title": "SN2 Reaction", "text": "SN2 reaction equals field substitution. Nucleophile substitutes leaving group following field substitution equations: product = field.substitute(substrate, nucleophile).", "domain": "chemistry"},
    {"title": "SN1 Reaction", "text": "SN1 reaction equals field substitution (two-step). Substrate dissociates to carbocation, then nucleophile substitutes following field dissociation and substitution equations.", "domain": "chemistry"},
    {"title": "E2 Elimination", "text": "E2 elimination equals field elimination. Base removes leaving group, forming alkene following field elimination equations: alkene = field.eliminate(substrate, base).", "domain": "chemistry"},
    {"title": "Aromaticity", "text": "Aromaticity equals field aromaticity. Hückel's rule: 4n+2 π electrons equals aromatic (field stability). Aromatic compounds follow field aromaticity equations.", "domain": "chemistry"},
    {"title": "Chemical Bond", "text": "Chemical bonds equal field bonds. Bond energy equals field potential, follows coulomb.compute_potential. Covalent, ionic, and hydrogen bonds all follow field bond equations.", "domain": "chemistry"},
    {"title": "Functional Group", "text": "Functional groups equal field groups. Electron-withdrawing groups equal field withdrawal, electron-donating groups equal field donation. Electronic effects affect reactivity through field effects.", "domain": "chemistry"},
    {"title": "Chirality", "text": "Chirality equals field handedness. Enantiomers equal field mirrors. Stereochemistry follows field stereochemistry equations at dimension D≈3.0.", "domain": "chemistry"},
    {"title": "Reaction Rate", "text": "Reaction rate equals field rate. Arrhenius equation: k = A e^(-Ea/RT). Activation energy equals field barrier, temperature affects rate through field energy.", "domain": "chemistry"},
    
    # Neuroscience - Neural Field Dynamics
    {"title": "Neuron", "text": "Neurons equal field units. Membrane potential equals field potential, threshold equals field threshold. Action potential equals field spike, follows field spike equations.", "domain": "neuroscience"},
    {"title": "Action Potential", "text": "Action potential equals field spike. When membrane potential exceeds threshold, neuron fires following field spike equations. Spike propagates along axon via field propagation.", "domain": "neuroscience"},
    {"title": "Synapse", "text": "Synapses equal field connections. Synaptic transmission equals field transmission. Neurotransmitters equal field propagators, binding to receptors equals field coupling.", "domain": "neuroscience"},
    {"title": "Neural Network", "text": "Neural networks equal field networks. Neural activation equals field activation: σ(x) = 1/(1+e^(-x)). Neural learning equals field learning, weight updates follow field update equations.", "domain": "neuroscience"},
    {"title": "Consciousness", "text": "Consciousness equals field consciousness. Requires dimension D≥5 (from Field Spec §8.10). Integrated information Φ equals field integration. Awareness equals field awareness, self-model equals field self-model.", "domain": "neuroscience"},
    {"title": "Memory", "text": "Memory equals field memory. Storage equals field.store, retrieval equals field.retrieve. Memory formation follows field memory equations, involving synaptic plasticity and field updates.", "domain": "neuroscience"},
    {"title": "Attention", "text": "Attention equals field attention. Attended input equals field.attend(input, attention_weights). Attention mechanisms follow field attention equations, selecting relevant information.", "domain": "neuroscience"},
    
    # Economics - Market Field Dynamics
    {"title": "Supply and Demand", "text": "Supply and demand equal field supply and demand. Supply equals field source, demand equals field sink. Market equilibrium equals field equilibrium, price equals field potential.", "domain": "economics"},
    {"title": "Market Equilibrium", "text": "Market equilibrium equals field equilibrium. When supply equals demand, market reaches equilibrium price following field equilibrium equations.", "domain": "economics"},
    {"title": "Price", "text": "Price equals field potential. Price adjusts to balance supply and demand, following field potential equations. Market dynamics equal field dynamics.", "domain": "economics"},
    
    # Statistics - Statistical Field Dynamics
    {"title": "Probability", "text": "Probability equals field probability. Probability distributions equal field distributions. Normal distribution equals field normal distribution, following field probability equations.", "domain": "statistics"},
    {"title": "Normal Distribution", "text": "Normal distribution equals field normal distribution. PDF: f(x) = (1/√(2πσ²)) e^(-(x-μ)²/(2σ²)). Mean equals field center, variance equals field spread.", "domain": "statistics"},
    {"title": "Correlation", "text": "Correlation equals field correlation. Measures field relationships between variables: r = cov(X,Y) / (σ_X σ_Y). Correlation reveals field connections.", "domain": "statistics"},
    {"title": "Mean", "text": "Mean equals field center. Average value equals field center of distribution. Mean locates the field center of probability distribution.", "domain": "statistics"},
    {"title": "Variance", "text": "Variance equals field spread. Measures field spread of distribution. Standard deviation equals square root of variance, measures field spread.", "domain": "statistics"},
    
    # Pharmacology - Catalysts & Receptors
    {"title": "Enzyme", "text": "Enzymes equal field catalysts. Lower activation energy (field barrier) to speed up reactions. Michaelis-Menten kinetics: v = (Vmax [S]) / (Km + [S]). Enzyme catalysis equals field catalysis.", "domain": "biology"},
    {"title": "Cell Receptor", "text": "Cell receptors equal field receptors. Receptor binding equals field binding, follows binding isotherm: [RL] = ([R] [L]) / (Kd + [L]). Binding affinity equals field coupling strength. Signal transduction equals field propagation.", "domain": "biology"},
    {"title": "Pharmacokinetics", "text": "Pharmacokinetics equals field kinetics. Absorption, distribution, metabolism, excretion (ADME) all follow field equations. Drug clearance: C(t) = C₀ e^(-kt). Pharmacokinetics follows field kinetic equations.", "domain": "biology"},
    
    # Evolution - Modern Evolutionary Theory
    {"title": "Natural Selection", "text": "Natural selection equals field selection. Populations evolve through field selection, selecting fitter variants. Selection coefficient determines rate of field evolution.", "domain": "biology"},
    {"title": "Genetic Drift", "text": "Genetic drift equals field drift. Random changes in allele frequencies follow field drift equations. Drift is stronger in smaller populations.", "domain": "biology"},
    {"title": "Mutation", "text": "Mutation equals field perturbation. Genetic mutations perturb the field, creating variation. Mutation rate determines field perturbation rate.", "domain": "biology"},
    {"title": "Gene Flow", "text": "Gene flow equals field flow. Migration between populations creates field flow, mixing gene pools. Gene flow follows field flow equations.", "domain": "biology"},
    {"title": "Modern Evolutionary Synthesis", "text": "Modern evolutionary synthesis equals field synthesis. Combines natural selection (field selection), genetic drift (field drift), mutation (field perturbation), and gene flow (field flow) into unified field evolution.", "domain": "biology"},
    
    # Cancer - Cancer Field Dynamics
    {"title": "Cancer", "text": "Cancer equals field cancer. Tumor growth equals field growth, mutations equal field perturbations. Angiogenesis equals field angiogenesis, metastasis equals field metastasis. Immune evasion equals field evasion.", "domain": "biology"},
    {"title": "Tumor Growth", "text": "Tumor growth equals field growth. Follows exponential or logistic growth: N(t) = N₀ e^(rt) or N(t) = K / (1 + ((K-N₀)/N₀)e^(-rt)). Growth rate determines field growth rate.", "domain": "biology"},
    {"title": "Mutation Accumulation", "text": "Cancer mutations equal field perturbations. Mutations accumulate: M(t) = M₀ + μ × divisions. Driver mutations drive cancer progression following field perturbation equations.", "domain": "biology"},
    {"title": "Angiogenesis", "text": "Angiogenesis equals field angiogenesis. Tumors induce new blood vessel formation following field angiogenesis equations. Angiogenesis enables tumor growth and metastasis.", "domain": "biology"},
    {"title": "Metastasis", "text": "Metastasis equals field metastasis. Cancer cells invade and spread following field metastasis equations. Metastasis involves invasion, intravasation, circulation, extravasation, and colonization.", "domain": "biology"},
    {"title": "Immune Evasion", "text": "Immune evasion equals field evasion. Cancer cells evade immune system following field evasion equations. Evasion probability: P(evasion) = 1 - (antigenicity × surveillance).", "domain": "biology"},
    
    # Autoimmune Diseases - Autoimmune Field Dynamics
    {"title": "Autoimmune Disease", "text": "Autoimmune diseases equal field autoimmune. Tolerance breakdown equals field breakdown. Autoantibody production equals field production. Inflammation equals field inflammation, tissue damage equals field damage.", "domain": "biology"},
    {"title": "Tolerance Breakdown", "text": "Immune tolerance breakdown equals field breakdown. When self-antigen exceeds tolerance threshold, autoimmunity develops. Tolerance breakdown follows field breakdown equations.", "domain": "biology"},
    {"title": "Autoantibody", "text": "Autoantibodies equal field autoantibodies. Autoantibody production equals field production. Autoantibodies bind self-tissues, causing field inflammation and tissue damage.", "domain": "biology"},
    {"title": "Autoimmune Inflammation", "text": "Autoimmune inflammation equals field inflammation. Autoantibodies bind self-tissues, causing field inflammation. Inflammation leads to tissue damage following field damage equations.", "domain": "biology"},
    {"title": "Checkpoint Inhibition", "text": "Cancer immunotherapy equals field checkpoint inhibition. Checkpoint inhibitors activate immune system against cancer. Checkpoint inhibition equals field checkpoint inhibition.", "domain": "biology"},
]

def add_domain_knowledge():
    """Add domain-specific knowledge to the knowledge base with field mappings"""
    project_root = Path(__file__).parent.parent
    knowledge_file = project_root / "data" / "bert_knowledge_base.json"
    
    # Load existing knowledge base
    if knowledge_file.exists():
        with open(knowledge_file) as f:
            knowledge_base = json.load(f)
    else:
        knowledge_base = {}
    
    print(f"Existing entries: {len(knowledge_base)}")
    
    # Initialize field mappers
    biology_mapper = BiologyFieldMapper(project_root)
    astronomy_mapper = AstronomyFieldMapper(project_root)
    pharmacology_evolution_mapper = PharmacologyEvolutionMapper(project_root)
    cancer_autoimmune_mapper = CancerAutoimmuneMapper(project_root)
    
    # Add domain knowledge with field mappings
    import hashlib
    added = 0
    for entry in DOMAIN_KNOWLEDGE:
        # Create hash for deduplication
        text_hash = hashlib.md5(entry["text"].encode()).hexdigest()[:16]
        
        if text_hash not in knowledge_base:
            # Map concepts to field equations
            field_mapping = None
            entry_title_lower = entry["title"].lower()
            
            # Let OPIC determine domain concepts naturally - no hardcoded term matching
            # Field mappers will handle concept detection through field operations
            
            if entry["domain"] == "biology":
                # Let OPIC determine concept type through field operations
                if field_mapping:  # Use field mapping if available
                    # Use pharmacology/evolution mapper for enzyme, receptor, evolution entries
                    explanation = pharmacology_evolution_mapper.explain_pharmacology_evolution(entry["title"])
                    if explanation.get("concepts"):
                        field_mapping = {
                            "scale": "pharmacological" if is_pharmacology else "evolutionary",
                            "dimension": 3.0 if is_pharmacology else 3.5,
                            "concepts": explanation.get("concepts", []),
                            "explanation": explanation.get("explanation", "")
                        }
                elif is_cancer or is_autoimmune:
                    # Use cancer/autoimmune mapper for cancer, autoimmune entries
                    explanation = cancer_autoimmune_mapper.explain_cancer_autoimmune(entry["title"])
                    if explanation.get("concepts"):
                        field_mapping = {
                            "scale": "cancer" if is_cancer else "autoimmune",
                            "dimension": 3.5,
                            "concepts": explanation.get("concepts", []),
                            "explanation": explanation.get("explanation", "")
                        }
                else:
                    # Create knowledge entry with field mapping
                    knowledge_entry = biology_mapper.add_biology_knowledge(
                        question=entry["title"],
                        answer=entry["text"]
                    )
                    field_mapping = knowledge_entry.get("field_properties", {})
            elif entry["domain"] == "astronomy":
                # Map astronomy concepts to field equations
                explanation = astronomy_mapper.explain_astronomy_as_field(entry["title"])
                if explanation.get("field_mappings"):
                    field_mapping = {
                        "scale": explanation["scale"],
                        "dimension": explanation["dimension"],
                        "field_mappings": explanation["field_mappings"]
                    }
            
            # Create knowledge entry (will be processed by ingestion)
            knowledge_base[text_hash] = {
                "text": entry["text"],
                "title": entry["title"],
                "domain": entry["domain"],
                "phi_k": 0.0,  # Will be computed during ingestion
                "zeros": [],
                "source": "domain_knowledge",
                "word_count": len(entry["text"].split()),
                "field_mapping": field_mapping  # Add field equation mapping
            }
            added += 1
    
    # Save updated knowledge base
    with open(knowledge_file, 'w') as f:
        json.dump(knowledge_base, f, indent=2)
    
    print(f"Added {added} domain-specific entries")
    print(f"Total entries: {len(knowledge_base)}")
    
    # Now recompute phi_k and zeros for new entries
    print("\nRecomputing field properties for new entries...")
    from opic_executor import OpicExecutor
    executor = OpicExecutor(project_root)
    
    updated = 0
    for entry_hash, entry in knowledge_base.items():
        if entry.get("source") == "domain_knowledge" and entry.get("phi_k") == 0.0:
            text = entry.get("text", "")
            if text:
                # Compute field properties with proper zeta calibration
                doc_field = executor._call_primitive("aperture.chain", {"text": text})
                aperture = doc_field.get("aperture", {})
                phi_k = aperture.get("discourse", {}).get("phi_k", 0.0)
                
                # Construct full hierarchical spectrum
                spectrum = []
                # Letters
                for letter in aperture.get("letters", []):
                    if isinstance(letter, dict) and letter.get("phi_k"):
                        spectrum.append(float(letter["phi_k"]))
                # Words
                for word in aperture.get("words", []):
                    if isinstance(word, dict) and word.get("phi_k"):
                        spectrum.append(float(word["phi_k"]))
                # Sentences
                for sentence in aperture.get("sentences", []):
                    if isinstance(sentence, dict) and sentence.get("phi_k"):
                        spectrum.append(float(sentence["phi_k"]))
                # Discourse
                if phi_k:
                    spectrum.append(float(phi_k))
                
                if not spectrum:
                    spectrum = [float(phi_k)] if phi_k else [0.0]
                
                # Compute zeros using FULL spectrum (proper zeta calibration)
                region = {"min": 0.0, "max": 10.0}
                zeros = executor._call_primitive("zeta.zero.solver", {
                    "phi_k": spectrum,  # Full spectrum
                    "region": region,
                    "tolerance": 0.001
                })
                
                # Clean zeros for JSON
                zeros_clean = []
                for zero in zeros:
                    if isinstance(zero, dict):
                        zero_clean = {
                            "real": zero.get("real", 0.0),
                            "imaginary": zero.get("imaginary", 0.0),
                        }
                        zeros_clean.append(zero_clean)
                
                entry["phi_k"] = float(phi_k)
                entry["zeros"] = zeros_clean
                updated += 1
                
                if updated % 10 == 0:
                    print(f"  Updated {updated} entries...")
    
    # Save again with computed properties
    with open(knowledge_file, 'w') as f:
        json.dump(knowledge_base, f, indent=2)
    
    print(f"\n✓ Updated {updated} entries with field properties")
    print(f"✓ Knowledge base now has {len(knowledge_base)} entries")

if __name__ == "__main__":
    print("=" * 60)
    print("Adding Domain-Specific Knowledge")
    print("=" * 60)
    add_domain_knowledge()

