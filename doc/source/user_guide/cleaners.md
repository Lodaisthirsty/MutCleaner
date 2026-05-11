# Data Cleaners Usage Guide

## Overview

This guide provides usage examples for data cleaning modules organized by dataset source:

- [**Human Domainome Dataset**](#human-domainome-dataset): Site-saturation mutagenesis of 500 human protein domains
- [**ProteinGym**](#proteingym): Large-Scale Benchmarks for Protein Design and Fitness Prediction
- [**cDNA Proteolysis Dataset**](#cdna-proteolysis-dataset): Mega-scale experimental analysis of protein folding stability in biology and design
- [**ddG-dTm dataset**](#ddg-dtm-dataset): A collection of datasets providing single- and multiple-mutant measurements, labeled by thermodynamic parameters (ΔΔG, ΔTm)
- [**ArchStabMS1E10 Epistasis Dataset**](#archstabms1e10-epistasis-dataset): High-order multi-mutant libraries (“1e10”) measuring protein stability for GRB2-SH3 and SRC.
- [**Antitoxin ParD3 Epistasis Dataset**](#antitoxin-pard3-epistasis-dataset): The antitoxin ParD3 3-position library is a combinatorially exhaustive dataset of 8,000 variants demonstrating that simple, independent per-residue mutation preferences are sufficient to almost perfectly predict combinatorial protein fitness.
- [**TrpB Epistasis Dataset**](#trpb-epistasis-dataset): a combinatorially complete sequence-fitness landscape comprising 160,000 variants across four active-site residues of the enzyme tryptophan synthase, capturing significant epistatic interactions to serve as a benchmark for model-guided enzyme engineering.
- [**Human Myoglobin Epistasis Dataset**](#human-myoglobin-epistasis-dataset): A deep mutational scanning library detailing the expression fitness scores for near-comprehensive single-codon and small-fraction double-codon mutations in yeast surface-displayed human myoglobin, which was used to train machine learning models for predicting epistatic effects and discovering stability-enhancing variants.
- [**CTXM Epistasis Dataset**](#ctxm-epistasis-dataset): A large-scale pairwise deep mutational scanning dataset of the CTX-M-14 $\beta$-lactamase active site, covering 49,096 double mutants across 17 active-site residues. Fitness measurements were obtained from functional selection under ampicillin and cefotaxime, providing substrate-dependent fitness landscapes for studying epistasis, compensatory mutations, and antibiotic resistance prediction.
- [**RBD-ACE2 Dataset**](#rbd-ace2-dataset): SARS-CoV-2 RBD sequences with ACE2 binding affinity scores, labeled by `log10Ka` where higher values indicate stronger ACE2 binding affinity.
- [**RBD-Antibody Dataset**](#rbd-antibody-dataset): SARS-CoV-2 RBD antibody escape data with `score` computed as the negative logarithm of escape. Higher scores indicate weaker escape, reflecting better binding capacity.

---

## Prerequisites

```bash
pip install mutcleaner
```

---

## Human Domainome Dataset

### File Preparation
You can download the source file directly by running (see {py:func}`mutcleaner.utils.download_human_domainome_source_file` for details):
```python
from mutcleaner import download_human_domainome_source_file
filepaths = download_human_domainome_source_file("path/to/target/folder")
```

Alternatively, you can download it from [Nature](https://www.nature.com/articles/s41586-024-08370-4) or [Hugging Face](https://huggingface.co/datasets/xulab-research/mutcleaner/tree/main/human_domainome) (See `SupplementaryTable2.txt`)

The Hugging Face dataset already includes the reference FASTA. If you are not using that source, you’ll need to provide the FASTA yourself (i.e., the reviewed Human (9606) proteome from  [UNIPROT](https://rest.uniprot.org/uniprotkb/stream?download=true&format=fasta&query=%28*%29+AND+%28model_organism%3A9606%29+AND+%28reviewed%3Atrue%29)).

### Basic Usage

**Cleaning Pipeline**

```python
from mutcleaner.cleaners import (
    create_human_domainome_sup2_cleaner, 
    clean_human_domainome_sup2_dataset
)

# File settings
dataset_filepath = "path/to/dataset/file"
# Clean data
hd_cleaning_pipeline = create_human_domainome_sup2_cleaner(dataset_filepath)
hd_cleaning_pipeline, hd_dataset = clean_human_domainome_sup2_dataset(hd_cleaning_pipeline)
```

**Advanced Settings**

See {py:class}`mutcleaner.cleaners.HumanDomainomeSup2CleanerConfig` for details.

## ProteinGym

### File Preparation
You can download the source file directly by running (see {py:func}`mutcleaner.utils.download_protein_gym_source_file` for details):
```python
from mutcleaner import download_protein_gym_source_file
filepaths = download_protein_gym_source_file("path/to/target/folder")
```

Alternatively, you can download it from [ProteinGym](https://marks.hms.harvard.edu/proteingym/ProteinGym_v1.3/DMS_ProteinGym_substitutions.zip) or [Hugging Face](https://huggingface.co/datasets/xulab-research/mutcleaner/tree/main/ProteinGym_DMS_substitutions)

### Basic Usage

**Cleaning Pipeline**

```python
from mutcleaner.cleaners import (
    create_protein_gym_cleaner,
    clean_protein_gym_dataset
)

# File settings
dataset_filepath = "path/to/dataset/file"
# Clean data
pg_cleaning_pipeline = create_protein_gym_cleaner(dataset_filepath)
pg_cleaning_pipeline, pg_dataset = clean_protein_gym_dataset(pg_cleaning_pipeline)
```

**Advanced Settings**

See {py:class}`mutcleaner.cleaners.ProteinGymCleanerConfig` for details.

## cDNA Proteolysis Dataset

### File Preparation
You can download the source file directly by running (see {py:func}`mutcleaner.utils.download_cdna_proteolysis_source_file` for details):
```python
from mutcleaner import download_cdna_proteolysis_source_file
filepaths = download_cdna_proteolysis_source_file("path/to/target/folder")
```

Alternatively, you can download it from [Zenodo](https://zenodo.org/records/7992926) ("'Tsuboyama2023_Dataset2_Dataset3_20230416.csv' in 'Processed_K50_dG_datasets.zip'") or [Hugging Face](https://huggingface.co/datasets/xulab-research/mutcleaner/tree/main/cDNA_proteolysis)

### ΔΔG as Label (Default Pipeline)

**Cleaning Pipeline**

```python
from mutcleaner.cleaners import (
    create_cdna_proteolysis_cleaner,
    clean_cdna_proteolysis_dataset
)

# File settings
dataset_filepath = "path/to/dataset/file"
# Clean data
cdnap_cleaning_pipeline = create_cdna_proteolysis_cleaner(dataset_filepath)
cdnap_cleaning_pipeline, cdnap_dataset = clean_cdna_proteolysis_dataset(cdnap_cleaning_pipeline)
```

### ΔG as Label

**Cleaning Pipeline**
```python
from mutcleaner.cleaners import (
    CDNAProteolysisCleanerConfig, 
    create_cdna_proteolysis_cleaner,
    clean_cdna_proteolysis_dataset
)

# File settings
dataset_filepath = "path/to/dataset/file"

# Set cleaning configs
cdnap_cleaning_config = CDNAProteolysisCleanerConfig()
cdnap_cleaning_config.column_mapping = {
    "WT_name": "name",
    "aa_seq": "mut_seq",
    "mut_type": "mut_info",
    "dG_ML": "label_cDNAProteolysis",
}
# Clean data
cdnap_cleaning_pipeline = create_cdna_proteolysis_cleaner(dataset_filepath, cdnap_cleaning_config)
cdnap_cleaning_pipeline, cdnap_dataset = clean_cdna_proteolysis_dataset(cdnap_cleaning_pipeline)
```

## ddG-dTm Dataset

### File Preparation

You can download the source file directly by running (see {py:func}`mutcleaner.utils.download_ddg_dtm_source_file` for details):
```python
from mutcleaner import download_ddg_dtm_source_file

# Download all datasets
filepaths = download_ddg_dtm_source_file("path/to/target/folder")

# Or specify a particular dataset, e.g.
filepath = download_ddg_dtm_source_file("path/to/target/folder", sub_dataset = "S571")
```

### Basic Usage

{py:func}`mutcleaner.cleaners.ddg_dtm_cleaners.create_ddg_dtm_cleaner` can automatically recognize the label column (ddG or dTm). For example:

```python
from mutcleaner.cleaners import (
    create_ddg_dtm_cleaner,
    clean_ddg_dtm_dataset
)

# File settings
dataset_filepath = "path/to/dataset/file"

# Clean data
ddgdtm_cleaning_pipeline = create_ddg_dtm_cleaner(dataset_filepath)
ddgdtm_cleaning_pipeline, ddgdtm_dataset = clean_ddg_dtm_dataset(ddgdtm_cleaning_pipeline)
```

### Advanced Settings

See {py:class}`mutcleaner.cleaners.DdgDtmCleanerConfig` for details.

## ArchStabMS1E10 Epistasis Dataset

### File Preparation

You can download the source file directly by running (see {py:func}`mutcleaner.utils.download_archstabms1e10_source_file` for details):
```python
from mutcleaner import download_archstabms1e10_source_file
filepaths = download_archstabms1e10_source_file("path/to/target/folder")
```

### Basic Usage

```python
from mutcleaner.cleaners import (
    create_archstabms_1e10_cleaner,
    clean_archstabms_1e10_dataset
)

# File settings
dataset_filepath = "path/to/dataset/file"

# Clean data
archstabms_cleaning_pipeline = create_archstabms_1e10_cleaner(dataset_filepath)
archstabms_cleaning_pipeline, archstabms_dataset = clean_archstabms_1e10_dataset(
    archstabms_cleaning_pipeline
)
```

### Advanced Settings

See {py:class}`mutcleaner.cleaners.ArchStabMS1E10CleanerConfig` for details.

## Antitoxin ParD3 Epistasis Dataset

### File Preparation

You can download the source file directly by running (see {py:func}`mutcleaner.utils.download_antitoxin_pard3_source_file` for details):
```python
from mutcleaner import download_antitoxin_pard3_source_file
filepaths = download_antitoxin_pard3_source_file("path/to/target/folder")
```

### Basic Usage

```python
from mutcleaner.cleaners import (
    create_antitoxin_pard3_cleaner,
    clean_antitoxin_pard3_dataset
)

# File settings
dataset_filepath = "path/to/dataset/file"

# Clean data
antitoxin_pard3_cleaning_pipeline = create_antitoxin_pard3_cleaner(dataset_filepath)
antitoxin_pard3_cleaning_pipeline, antitoxin_pard3_dataset = clean_antitoxin_pard3_dataset(
    antitoxin_pard3_cleaning_pipeline
)
```

### Advanced Settings

See {py:class}`mutcleaner.cleaners.AntitoxinParD3CleanerConfig` for details.

## TrpB Epistasis Dataset

### File Preparation

You can download the source file directly by running (see {py:func}`mutcleaner.utils.download_trpb_source_file` for details):
```python
from mutcleaner import download_trpb_source_file
filepaths = download_trpb_source_file("path/to/target/folder")
```

### Basic Usage

```python
from mutcleaner.cleaners import (
    create_trpb_cleaner,
    clean_trpb_dataset
)

# File settings
dataset_filepath = "path/to/dataset/file"

# Clean data
trpb_cleaning_pipeline = create_trpb_cleaner(dataset_filepath)
trpb_cleaning_pipeline, trpb_dataset = clean_trpb_dataset(trpb_cleaning_pipeline)
```

### Advanced Settings

See {py:class}`mutcleaner.cleaners.TrpBCleanerConfig` for details.

## Human Myoglobin Epistasis Dataset


### File Preparation

You can download the source file directly by running (see {py:func}`mutcleaner.utils.download_human_myoglobin_source_file` for details):
```python
from mutcleaner import download_human_myoglobin_source_file
filepaths = download_human_myoglobin_source_file("path/to/target/folder")
```

### Basic Usage

```python
from mutcleaner.cleaners import (
    create_human_myoglobin_cleaner,
    clean_human_myoglobin_dataset,
)

# File settings
dataset_filepath = "path/to/dataset/file"

# Clean data
human_myoglobin_cleaning_pipeline = create_human_myoglobin_cleaner(dataset_filepath)
human_myoglobin_cleaning_pipeline, human_myoglobin_dataset = clean_human_myoglobin_dataset(
    human_myoglobin_cleaning_pipeline
)
```

### Advanced Settings

See {py:class}`mutcleaner.cleaners.HumanMyoglobinCleanerConfig` for details.

## CTXM Epistasis Dataset


### File Preparation

You can download the source file directly by running (see {py:func}`mutcleaner.utils.download_ctxm_source_file` for details):
```python
from mutcleaner import download_ctxm_source_file
filepaths = download_ctxm_source_file("path/to/target/folder")
```

### Basic Usage

```python
from mutcleaner.cleaners import (
    create_ctxm_cleaner,
    clean_ctxm_dataset,
)

# File settings
dataset_filepath = "path/to/dataset/file"

# Clean data
ctxm_cleaning_pipeline = create_ctxm_cleaner(dataset_filepath)
ctxm_cleaning_pipeline, ctxm_dataset = clean_ctxm_dataset(ctxm_cleaning_pipeline)
```

### Advanced Settings

See {py:class}`mutcleaner.cleaners.CTXMCleanerConfig` for details.


## RBD-ACE2 Dataset

### File Preparation

You can download the source file directly by running (see {py:func}`mutcleaner.utils.download_rbd_ace2_source_file` for details):
```python
from mutcleaner import download_rbd_ace2_source_file
filepaths = download_rbd_ace2_source_file("path/to/target/folder")
```

You can also download and process a specific sub-dataset:

```python
from mutcleaner import download_rbd_ace2_source_file
filepaths = download_rbd_ace2_source_file(
    "path/to/target/folder",
    sub_dataset="Omicron_EG5_FLip_BA286",
)
```

Supported sub-datasets:
- `Omicron_EG5_FLip_BA286`
- `Omicron_XBB_BQ`
- `Omicron`
- `DMS_variants`
- `Delta`

Alternatively, you can download it from [Hugging Face](https://huggingface.co/datasets/Zoey13891350636/RBD_ACE2).

### Basic Usage

```python
from mutcleaner import download_rbd_ace2_source_file
from mutcleaner.cleaners import clean_rbd_ace2_dataset, create_rbd_ace2_cleaner

filepaths = download_rbd_ace2_source_file(
    "path/to/target/folder",
    sub_dataset="Omicron_EG5_FLip_BA286",
)
dataset_filepath = next(iter(filepaths.values()))

rbd_ace2_cleaning_pipeline = create_rbd_ace2_cleaner(dataset_filepath)
rbd_ace2_cleaning_pipeline, rbd_ace2_dataset = clean_rbd_ace2_dataset(
    rbd_ace2_cleaning_pipeline
)
```

### Advanced Settings

See {py:class}`mutcleaner.cleaners.RBDACE2CleanerConfig` for details.

## RBD-Antibody Dataset

### File Preparation

You can download the source file directly by running (see {py:func}`mutcleaner.utils.download_rbd_antibody_source_file` for details):
```python
from mutcleaner import download_rbd_antibody_source_file
filepaths = download_rbd_antibody_source_file("path/to/target/folder")
```

You can also download and process a specific sub-dataset:

```python
from mutcleaner import download_rbd_antibody_source_file
filepaths = download_rbd_antibody_source_file(
    "path/to/target/folder",
    sub_dataset="AZ_Abs",
)
```

Supported sub-datasets:
- `AZ_Abs`
- `HAARVI_sera`
- `Moderna`
- `Rockefeller`
- `Vir_mAbs`
- `clinical_Abs`

Alternatively, you can download it from [Hugging Face](https://huggingface.co/datasets/Zoey13891350636/RBD_Antibody).

### Basic Usage

```python
from mutcleaner import download_rbd_antibody_source_file
from mutcleaner.cleaners import clean_rbd_antibody_dataset, create_rbd_antibody_cleaner

filepaths = download_rbd_antibody_source_file(
    "path/to/target/folder",
    sub_dataset="AZ_Abs",
)
dataset_filepath = next(iter(filepaths.values()))

rbd_antibody_cleaning_pipeline = create_rbd_antibody_cleaner(dataset_filepath)
rbd_antibody_cleaning_pipeline, rbd_antibody_dataset = clean_rbd_antibody_dataset(
    rbd_antibody_cleaning_pipeline
)
```

### Advanced Settings

See {py:class}`mutcleaner.cleaners.RBDAntibodyCleanerConfig` for details.
