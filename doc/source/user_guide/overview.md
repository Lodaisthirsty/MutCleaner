# Overview

This guide provides usage examples for data cleaning modules organized by dataset source:

- [**Human Domainome Dataset**](#human-domainome-dataset): Site-saturation mutagenesis of 500 human protein domains.
- [**ProteinGym DMS Substitutions Dataset**](#proteingym-dms-substitutions-dataset): Large-scale benchmarks for protein design and fitness prediction.
- [**cDNA Proteolysis Dataset**](#cdna-proteolysis-dataset): Mega-scale experimental analysis of protein folding stability in biology and design.
- [**ddG-dTm Dataset**](#ddg-dtm-dataset): A collection of datasets providing single- and multiple-mutant measurements, labeled by the thermodynamic parameter (ΔΔG or ΔTm).
- [**ArchStabMS1E10 Epistasis Dataset**](#archstabms1e10-epistasis-dataset): High-order multi-mutant libraries (“1e10”) measuring protein stability for GRB2-SH3 and SRC.
- [**Antitoxin ParD3 Epistasis Dataset**](#antitoxin-pard3-epistasis-dataset): The antitoxin ParD3 3-position library is a combinatorially exhaustive dataset of 8,000 variants demonstrating that simple, independent per-residue mutation preferences are sufficient to almost perfectly predict combinatorial protein fitness.
- [**TrpB Epistasis Dataset**](#trpb-epistasis-dataset): A combinatorially complete sequence-fitness landscape comprising 160,000 variants across four active-site residues of the enzyme tryptophan synthase, capturing significant epistatic interactions to serve as a benchmark for model-guided enzyme engineering.
- [**Human Myoglobin Epistasis Dataset**](#human-myoglobin-epistasis-dataset): A deep mutational scanning library detailing the expression fitness scores for near-comprehensive single-codon mutations and a small fraction of double-codon mutations in yeast surface-displayed human myoglobin, which was used to train machine learning models for predicting epistatic effects and discovering stability-enhancing variants.
- [**CTXM Epistasis Dataset**](#ctxm-epistasis-dataset): A large-scale pairwise deep mutational scanning dataset of the CTX-M-14 β-lactamase active site, covering 49,096 double mutants across 17 active-site residues. Fitness measurements were obtained from functional selection under ampicillin and cefotaxime, providing substrate-dependent fitness landscapes for studying epistasis, compensatory mutations, and antibiotic resistance prediction.
- [**RBD-ACE2 Dataset**](#rbd-ace2-dataset): SARS-CoV-2 RBD sequences with ACE2 binding affinity scores, labeled by `log10Ka` where higher values indicate stronger ACE2 binding affinity.
- [**RBD-Antibody Dataset**](#rbd-antibody-dataset): SARS-CoV-2 RBD antibody escape data with `score` computed as the negative logarithm of escape. Higher scores indicate weaker escape, reflecting better binding capacity.