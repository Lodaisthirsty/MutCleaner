# MutCleaner

[![License badge](https://img.shields.io/badge/License-BSD_3--Clause-yellow?logo=opensourceinitiative&logoColor=white)](https://github.com/xulab-research/MutCleaner/blob/main/LICENSE)
[![PyPI version badge](https://img.shields.io/pypi/v/mutcleaner?logo=python&logoColor=white&color=orange)](https://pypi.org/project/mutcleaner/)
[![Docs](https://github.com/xulab-research/MutCleaner/actions/workflows/docs.yml/badge.svg)](https://xulab-research.github.io/MutCleaner/)

MutCleaner is an extensible Python toolkit for cleaning and standardizing biological mutation datasets, integrating dataset-specific cleaning pipelines with core abstractions for protein, nucleotide, and codon-level mutation representations.

* **Documentation**: https://xulab-research.github.io/MutCleaner/
* **Cleaning Examples**: https://xulab-research.github.io/MutCleaner/user_guide/cleaners.html

## Overview

MutCleaner is an extensible Python toolkit for cleaning, standardizing, and analyzing biological mutation datasets. It currently focuses on protein variant data while providing core abstractions for DNA, RNA, protein sequences, and codon-level mutation representations.

The package combines dataset-specific cleaning pipelines with reusable sequence and mutation utilities, enabling reproducible preprocessing of large-scale mutational datasets for downstream bioinformatics and machine learning analyses.

### Key Capabilities

- **Mutation dataset cleaning and standardization**: Harmonize mutation annotations, sequences, labels, and metadata across heterogeneous biological mutation datasets.
- **Sequence representation and validation**: Utilities for DNA, RNA, and protein sequences, including validation, transcription, reverse transcription, translation, and mutation application.
- **Mutation parsing and transformation**: Tools for parsing amino-acid and codon-level mutations, inferring mutations from sequences, applying mutations to reference sequences, and converting codon mutations into amino-acid changes.
- **Modular pipeline architecture**: A composable pipeline interface for building reproducible dataset-cleaning workflows.
- **Parallel and scalable dataset processing**: Multi-core utilities for mutation validation, mutation application, and sequence-based mutation inference, supporting efficient processing of large tabular mutation datasets.

## Installation

### Requirements

- Python 3.13+
- Dependencies are automatically installed via pip.

### Install via pip

```bash
pip install mutcleaner
```

### Development Installation

```bash
git clone https://github.com/xulab-research/MutCleaner.git MutCleaner
cd MutCleaner
pip install -e .
```

To install development dependencies for testing and documentation:

```bash
pip install -e ".[dev]"
```

## Quick Start

See the [Data Cleaners Usage Guide](https://xulab-research.github.io/MutCleaner/user_guide/cleaners.html) for more examples.

### Supported Datasets

| Dataset Name    | Reference                                                                           | File                                               | Link                                                                          |
| --------------- | ----------------------------------------------------------------------------------- | -------------------------------------------------- | ----------------------------------------------------------------------------- |
| cDNAProteolysis | Mega-scale experimental analysis of protein folding stability in biology and design | Tsuboyama2023_Dataset2_Dataset3_20230416.csv       | https://zenodo.org/records/7992926                                            |
| ProteinGym      | ProteinGym: Large-Scale Benchmarks for Protein Design and Fitness Prediction        | DMS_ProteinGym_substitutions.zip                   | https://proteingym.org/download                                               |
| HumanDomainome  | Site-saturation mutagenesis of 500 human protein domains                            | SupplementaryTable2.txt or SupplementaryTable4.txt | https://www.nature.com/articles/s41586-024-08370-4                            |
| ddG             | None                                                                                | M1261.csv, S461.csv, S669.csv, S783.csv, S8754.csv | https://huggingface.co/datasets/xulab-research/MutCleaner/tree/main/ddG_datasets |
| dTm             | None                                                                                | S4346.csv, S557.csv, S571.csv                      | https://huggingface.co/datasets/xulab-research/MutCleaner/tree/main/dTm_datasets |
| ArchStabMS1E10  | The genetic architecture of protein stability                                       | ArchStabMS_1E10.csv                                | https://huggingface.co/datasets/xulab-research/MutCleaner/blob/main/archstabms1e_10/archstabms_1e10.csv |
| Antitoxin ParD3 | Protein design using structure-based residue preferences                            | Antitoxin_ParD3.csv                                | https://huggingface.co/datasets/xulab-research/MutCleaner/blob/main/AntitoxinParD3 |
| CTXM            | Network of epistatic interactions in an enzyme active site revealed by DMS          | CTXM_cefotaxime.csv or CTXM_ampicillin.csv         | https://huggingface.co/datasets/xulab-research/MutCleaner/tree/main/CTXM |
| hMb             | Decoding Stability and Epistasis in Human Myoglobin by Deep Mutational Scanning and Codon-level Machine Learning | Human_Myoglobin.csv | https://huggingface.co/datasets/xulab-research/MutCleaner/tree/main/HumanMyoglobin |
| TrpB            | A combinatorially complete epistatic fitness landscape in an enzyme active site     | TrpB.csv                                           | https://huggingface.co/datasets/xulab-research/MutCleaner/tree/main/TrpB |

### Processing cDNAProteolysis Dataset

Here's a complete example demonstrating MutCleaner's capabilities with the cDNAProteolysis mutation dataset:

```python
from mutcleaner import cdna_proteolysis_cleaner
from mutcleaner import download_cdna_proteolysis_source_file

# Create a cDNAProteolysis cleaning pipeline using MutCleaner's default pipeline.
cdna_proteolysis_filepath = download_cdna_proteolysis_source_file(
    "dir_path",
    "file_name",
)["filename"]

cdna_proteolysis_cleaning_pipeline = cdna_proteolysis_cleaner.create_cdna_proteolysis_cleaner(
    cdna_proteolysis_filepath,
)

# Clean and process the dataset.
cdna_proteolysis_cleaning_pipeline, cdna_proteolysis_dataset = (
    cdna_proteolysis_cleaner.clean_cdna_proteolysis_dataset(
        cdna_proteolysis_cleaning_pipeline,
    )
)

# Save the processed dataset.
cdna_proteolysis_dataset.save("output/cleaned_cdna_proteolysis_data")
```

### Basic Sequence Operations

```python
from mutcleaner.core.sequence import DNASequence

# DNA sequence analysis.
dna = DNASequence("ATGCGATCGTAA")

print(f"Reverse complement: {dna.reverse_complement()}")
print(f"Transcription: {dna.transcribe()}")
print(f"Translation: {dna.translate()}")
```

## Core Features

### Sequence Data Manipulation

- **Sequence validation**: Validate DNA, RNA, and protein sequences against predefined alphabets.
- **Sequence transformation**: Support transcription, reverse transcription, translation, and reverse-complement operations.
- **Batch processing**: Process large tabular mutation datasets through reusable cleaning utilities.

### Mutation Analysis

- **Mutation parsing**: Parse amino-acid and codon-level mutation annotations.
- **Mutation inference**: Infer mutation annotations by comparing reference and mutated sequences.
- **Mutation transformation**: Apply mutation annotations to reference sequences and convert codon-level mutations into amino-acid changes.

### Data Cleaning and Preprocessing

- **Standardization**: Harmonize mutation names, sequences, labels, and metadata across heterogeneous datasets.
- **Duplicate handling**: Remove or aggregate redundant mutation records according to dataset-specific rules.
- **Dataset-specific cleaners**: Provide reusable cleaning pipelines for commonly used mutation datasets.

### Pipeline Architecture

- **Modular design**: Compose cleaning workflows from reusable processing components.
- **Parallel processing**: Use multi-core processing for mutation validation, mutation application, and sequence-based mutation inference.
- **Progress tracking**: Monitor long-running cleaning tasks with progress bars and structured execution summaries.

## Examples and Use Cases

### Custom Processing Pipeline

```python
import pandas as pd

from mutcleaner.cleaners.basic_cleaners import (
    extract_and_rename_columns,
    filter_and_clean_data,
    convert_data_types,
    validate_mutations,
    convert_to_mutation_dataset_format,
)
from mutcleaner.cleaners.cdna_proteolysis_custom_cleaners import (
    validate_wt_sequence,
    average_labels_by_name,
    subtract_labels_by_wt,
)
from mutcleaner.core.dataset import MutationDataset
from mutcleaner.core.pipeline import create_pipeline

dataset = pd.read_csv("path/to/Tsuboyama2023_Dataset2_Dataset3_20230416.csv")

pipeline = create_pipeline(dataset, "cdna_proteolysis_cleaner")
clean_result = (
    pipeline.then(
        extract_and_rename_columns,
        column_mapping={
            "WT_name": "name",
            "aa_seq": "mut_seq",
            "mut_type": "mut_info",
            "ddG_ML": "ddG",
        },
    )
    .then(filter_and_clean_data, filters={"ddG": lambda x: x != "-"})
    .then(convert_data_types, type_conversions={"ddG": "float"})
    .then(
        validate_mutations,
        mutation_column="mut_info",
        mutation_sep="_",
        is_zero_based=False,
        num_workers=16,
    )
    .then(
        average_labels_by_name,
        name_columns=("name", "mut_info"),
        label_columns="ddG",
    )
    .then(
        validate_wt_sequence,
        name_column="name",
        mutation_column="mut_info",
        sequence_column="mut_seq",
        wt_identifier="wt",
        num_workers=16,
    )
    .then(
        subtract_labels_by_wt,
        name_column="name",
        label_columns="ddG",
        mutation_column="mut_info",
        in_place=True,
    )
    .then(
        convert_to_mutation_dataset_format,
        name_column="name",
        mutation_column="mut_info",
        mutated_sequence_column="mut_seq",
        score_column="ddG",
        is_zero_based=True,
    )
)

cdna_proteolysis_dataset_df, cdna_proteolysis_ref_seq = clean_result.data
cdna_proteolysis_dataset = MutationDataset.from_dataframe(
    cdna_proteolysis_dataset_df,
    cdna_proteolysis_ref_seq,
)

execution_info = pipeline.get_execution_summary()
artifacts = pipeline.artifacts
pipeline.save_structured_data("cdna_proteolysis_cleaner_pipeline.pkl")
```

## Citation

If you use MutCleaner in your research, please cite:

```bibtex
@software{mutcleaner,
  title={
    MutCleaner: An efficient framework for cleaning, standardizing, and processing biological mutation data.
  },
  author={YukunR and Ziyu Shi},
  year={2026},
  url={https://github.com/xulab-research/MutCleaner}
}
```

## License

This project is licensed under the BSD 3-Clause License. See the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/xulab-research/MutCleaner/issues)
- **Discussions**: [GitHub Discussions](https://github.com/xulab-research/MutCleaner/discussions)