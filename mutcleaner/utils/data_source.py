# mutcleaner/utils/data_source.py

DATASETS = {
    "cDNA Proteolysis Dataset": {
        "paper_title": "Mega-scale experimental analysis of protein folding stability in biology and design",
        "official_doi": "https://zenodo.org/records/7992926",
        "files": [
            "'Tsuboyama2023_Dataset2_Dataset3_20230416.csv' in 'Processed_K50_dG_datasets.zip'"
        ],
        "huggingface_repos": [
            "datasets/xulab-research/TidyMut/resolve/main/cDNA_proteolysis/Tsuboyama2023_Dataset2_Dataset3_20230416.csv?download=true"
        ],
        "file_name": ["Tsuboyama2023_Dataset2_Dataset3_20230416.csv"],
    },
    "ProteinGym DMS Substitutions Dataset": {
        "paper_title": "ProteinGym: Large-Scale Benchmarks for Protein Design and Fitness Prediction",
        "official_doi": "https://doi.org/10.1101/2023.12.07.570727",
        "files": ["DMS_ProteinGym_substitutions.zip"],
        "huggingface_repos": [
            "datasets/xulab-research/TidyMut/resolve/main/ProteinGym_DMS_substitutions/DMS_ProteinGym_substitutions.zip?download=true"
        ],
        "file_name": ["ProteinGym_DMS_substitutions.zip"],
    },
    "Human Domainome Dataset": {
        "paper_title": "Site-saturation mutagenesis of 500 human protein domains",
        "official_doi": "https://doi.org/10.1038/s41586-024-08370-4",
        "files": [
            "SupplementaryTable2.txt",
            "wild_type.fasta",
        ],
        "huggingface_repos": [
            "datasets/xulab-research/TidyMut/resolve/main/human_domainome/SupplementaryTable2.txt?download=true",
            "datasets/xulab-research/TidyMut/resolve/main/human_domainome/SupplementaryTable4.txt?download=true",
            "datasets/xulab-research/TidyMut/resolve/main/human_domainome/wild_type.fasta?download=true",
        ],
        "file_name": [
            "SupplementaryTable2.txt",
            "SupplementaryTable4.txt",
            "wild_type.fasta",
        ],
        "sub_datasets": {
            "Sup2": {
                "files": ["SupplementaryTable2.txt"],
                "huggingface_repos": [
                    "datasets/xulab-research/TidyMut/resolve/main/human_domainome/SupplementaryTable2.txt?download=true"
                ],
                "file_name": ["SupplementaryTable2.txt"],
            },
            "Sup4": {
                "files": ["SupplementaryTable4.txt", "wild_type.fasta"],
                "huggingface_repos": [
                    "datasets/xulab-research/TidyMut/resolve/main/human_domainome/SupplementaryTable4.txt?download=true",
                    "datasets/xulab-research/TidyMut/resolve/main/human_domainome/wild_type.fasta?download=true",
                ],
                "file_name": ["SupplementaryTable4.txt", "wild_type.fasta"],
            },
        },
    },
    "ΔΔG Dataset": {
        "paper_title": "Improving the prediction of protein stability changes upon mutations by geometric learning and a pre-training strategy",
        "official_doi": "https://doi.org/10.1038/s43588-024-00716-2",
        "files": ["M1261.csv", "S461.csv", "S669.csv", "S783.csv", "S8754.csv"],
        "huggingface_repos": [
            "datasets/xulab-research/TidyMut/resolve/main/ddG_datasets/M1261.csv?download=true",
            "datasets/xulab-research/TidyMut/resolve/main/ddG_datasets/S461.csv?download=true",
            "datasets/xulab-research/TidyMut/resolve/main/ddG_datasets/S669.csv?download=true",
            "datasets/xulab-research/TidyMut/resolve/main/ddG_datasets/S783.csv?download=true",
            "datasets/xulab-research/TidyMut/resolve/main/ddG_datasets/S8754.csv?download=true",
        ],
        "file_name": [
            "M1261.csv",
            "S461.csv",
            "S669.csv",
            "S783.csv",
            "S8754.csv",
        ],
        "sub_datasets": {
            "M1261": {
                "files": ["M1261.csv"],
                "huggingface_repos": [
                    "datasets/xulab-research/TidyMut/resolve/main/ddG_datasets/M1261.csv?download=true"
                ],
                "file_name": ["M1261.csv"],
            },
            "S461": {
                "files": ["S461.csv"],
                "huggingface_repos": [
                    "datasets/xulab-research/TidyMut/resolve/main/ddG_datasets/S461.csv?download=true"
                ],
                "file_name": ["S461.csv"],
            },
            "S669": {
                "files": ["S669.csv"],
                "huggingface_repos": [
                    "datasets/xulab-research/TidyMut/resolve/main/ddG_datasets/S669.csv?download=true"
                ],
                "file_name": ["S669.csv"],
            },
            "S783": {
                "files": ["S783.csv"],
                "huggingface_repos": [
                    "datasets/xulab-research/TidyMut/resolve/main/ddG_datasets/S783.csv?download=true"
                ],
                "file_name": ["S783.csv"],
            },
            "S8754": {
                "files": ["S8754.csv"],
                "huggingface_repos": [
                    "datasets/xulab-research/TidyMut/resolve/main/ddG_datasets/S8754.csv?download=true"
                ],
                "file_name": ["S8754.csv"],
            },
        },
    },
    "ΔTm Dataset": {
        "paper_title": "Improving the prediction of protein stability changes upon mutations by geometric learning and a pre-training strategy",
        "official_doi": "https://doi.org/10.1038/s43588-024-00716-2",
        "files": ["S4346.csv", "S557.csv"],
        "huggingface_repos": [
            "datasets/xulab-research/TidyMut/resolve/main/dTm_datasets/S4346.csv?download=true",
            "datasets/xulab-research/TidyMut/resolve/main/dTm_datasets/S557.csv?download=true",
        ],
        "file_name": [
            "S4346.csv",
            "S557.csv",
        ],
        "sub_datasets": {
            "S4346": {
                "files": ["S4346.csv"],
                "huggingface_repos": [
                    "datasets/xulab-research/TidyMut/resolve/main/dTm_datasets/S4346.csv?download=true"
                ],
                "file_name": ["S4346.csv"],
            },
            "S557": {
                "files": ["S557.csv"],
                "huggingface_repos": [
                    "datasets/xulab-research/TidyMut/resolve/main/dTm_datasets/S557.csv?download=true"
                ],
                "file_name": ["S557.csv"],
            },
        },
    },
    "ArchStabMS1E10 Epistasis Dataset": {
        "paper_title": "The genetic architecture of protein stability",
        "official_doi": "https://doi.org/10.1038/s41586-024-07966-0",
        "files": ["Supplementary Table 4"],
        "huggingface_repos": [
            "datasets/xulab-research/TidyMut/blob/main/ArchStabMS1E10/ArchStabMS_1E10.csv?download=true"
        ],
        "file_name": ["ArchStabMS_1E10.csv"],
    },
    "Human Myoglobin Epistasis Dataset":{
        "paper_title": "Decoding Stability and Epistasis in Human Myoglobin by Deep Mutational Scanning and Codon-level Machine Learning",
        "official_doi": "https://doi.org/10.1101/2024.02.24.581358",
        "files": ["CODON_DATASET_Myoglobin.tsv"],
        "huggingface_repos": [
            "datasets/xulab-research/TidyMut/blob/main/HumanMyoglobin/Human_Myoglobin.csv?download=true"
        ],
        "file_name": ["Human_Myoglobin.csv"],
    },
    "CTXM Epistasis Dataset":{
        "paper_title": "CTX-M_datasets",
        "official_doi": "https://doi.org/10.1073/pnas.2313513121",
        "files": [
            "github.com/Palzkill-Lab/CTXM_epistasis/blob/main/fitness_data/Doubles_A3_processed.txt",
            "github.com/Palzkill-Lab/CTXM_epistasis/blob/main/fitness_data/Doubles_C2_processed.txt"
        ],
        "huggingface_repos": [
            "datasets/xulab-research/TidyMut/blob/main/CTXM/CTXM_ampicillin.csv?download=true",
            "datasets/xulab-research/TidyMut/blob/main/CTXM/CTXM_cefotaxime.csv?download=true",
        ],
        "file_name": [
            "CTXM_ampicillin.csv",
            "CTXM_cefotaxime.csv"
        ],
        "sub_datasets": {
            "CTXM_ampicillin": {
                "files": ["github.com/Palzkill-Lab/CTXM_epistasis/blob/main/fitness_data/Doubles_A3_processed.txt"],
                "huggingface_repos": [
                    "datasets/xulab-research/TidyMut/blob/main/CTXM/CTXM_ampicillin.csv?download=true"
                ],
                "file_name": ["CTXM_ampicillin.csv"],
            },
            "CTXM_cefotaxime": {
                "files": ["github.com/Palzkill-Lab/CTXM_epistasis/blob/main/fitness_data/Doubles_C2_processed.txt"],
                "huggingface_repos": [
                    "datasets/xulab-research/TidyMut/blob/main/CTXM/CTXM_cefotaxime.csv?download=true"
                ],
                "file_name": ["CTXM_cefotaxime.csv"],
            }
        }
    },
    "TrpB Epistasis Dataset":{
        "paper_title": "TrpB_datasets",
        "official_doi": "https://doi.org/10.1073/pnas.2400439121",
        "files": ["huggingface.co/datasets/SaProtHub/Dataset-TrpB_fitness_landsacpe/blob/main/dataset.csv"],
        "huggingface_repos": [
            "datasets/xulab-research/TidyMut/blob/main/TrpB/TrpB.csv?download=true"
        ],
        "file_name": ["TrpB.csv"],
    },
    "Antitoxin ParD3 Epistasis Dataset":{
        "paper_title": "Antitoxin_ParD3_datasets",
        "official_doi": "https://doi.org/10.1038/s41467-024-45621-4",
        "files": ["github.com/ddingding/CoVES/blob/main/data/DMS_data/df_mut_all_norm.csv"],
        "huggingface_repos": [
            "datasets/xulab-research/TidyMut/blob/main/AntitoxinParD3/Antitoxin_ParD3.csv?download=true"
        ],
        "file_name": ["Antitoxin_ParD3.csv"],
    },
    "RBD Antibody Dataset": {
        "paper_title": "RBD_Antibody_datasets",
        "official_doi": None,
        "files": [
            "SARS-CoV-2-RBD_MAP_AZ_Abs_scores.csv",
            "SARS-CoV-2-RBD_MAP_HAARVI_sera_scores.csv",
            "SARS-CoV-2-RBD_MAP_Moderna_scores.csv",
            "SARS-CoV-2-RBD_MAP_Rockefeller_scores.csv",
            "SARS-CoV-2-RBD_MAP_Vir_mAbs_scores.csv",
            "SARS-CoV-2-RBD_MAP_clinical_Abs_scores.csv",
        ],
        "huggingface_repos": [
            "datasets/xulab-research/RBD_Antibody/resolve/main/SARS-CoV-2-RBD_MAP_AZ_Abs_scores.csv?download=true",
            "datasets/xulab-research/RBD_Antibody/resolve/main/SARS-CoV-2-RBD_MAP_HAARVI_sera_scores.csv?download=true",
            "datasets/xulab-research/RBD_Antibody/resolve/main/SARS-CoV-2-RBD_MAP_Moderna_scores.csv?download=true",
            "datasets/xulab-research/RBD_Antibody/resolve/main/SARS-CoV-2-RBD_MAP_Rockefeller_scores.csv?download=true",
            "datasets/xulab-research/RBD_Antibody/resolve/main/SARS-CoV-2-RBD_MAP_Vir_mAbs_scores.csv?download=true",
            "datasets/xulab-research/RBD_Antibody/resolve/main/SARS-CoV-2-RBD_MAP_clinical_Abs_scores.csv?download=true",
        ],
        "file_name": [
            "SARS-CoV-2-RBD_MAP_AZ_Abs_scores.csv",
            "SARS-CoV-2-RBD_MAP_HAARVI_sera_scores.csv",
            "SARS-CoV-2-RBD_MAP_Moderna_scores.csv",
            "SARS-CoV-2-RBD_MAP_Rockefeller_scores.csv",
            "SARS-CoV-2-RBD_MAP_Vir_mAbs_scores.csv",
            "SARS-CoV-2-RBD_MAP_clinical_Abs_scores.csv",
        ],
        "sub_datasets": {
            "AZ_Abs": {
                "files": ["SARS-CoV-2-RBD_MAP_AZ_Abs_scores.csv"],
                "huggingface_repos": [
                    "datasets/xulab-research/RBD_Antibody/resolve/main/SARS-CoV-2-RBD_MAP_AZ_Abs_scores.csv?download=true"
                ],
                "file_name": ["SARS-CoV-2-RBD_MAP_AZ_Abs_scores.csv"],
            },
            "HAARVI_sera": {
                "files": ["SARS-CoV-2-RBD_MAP_HAARVI_sera_scores.csv"],
                "huggingface_repos": [
                    "datasets/xulab-research/RBD_Antibody/resolve/main/SARS-CoV-2-RBD_MAP_HAARVI_sera_scores.csv?download=true"
                ],
                "file_name": ["SARS-CoV-2-RBD_MAP_HAARVI_sera_scores.csv"],
            },
            "Moderna": {
                "files": ["SARS-CoV-2-RBD_MAP_Moderna_scores.csv"],
                "huggingface_repos": [
                    "datasets/xulab-research/RBD_Antibody/resolve/main/SARS-CoV-2-RBD_MAP_Moderna_scores.csv?download=true"
                ],
                "file_name": ["SARS-CoV-2-RBD_MAP_Moderna_scores.csv"],
            },
            "Rockefeller": {
                "files": ["SARS-CoV-2-RBD_MAP_Rockefeller_scores.csv"],
                "huggingface_repos": [
                    "datasets/xulab-research/RBD_Antibody/resolve/main/SARS-CoV-2-RBD_MAP_Rockefeller_scores.csv?download=true"
                ],
                "file_name": ["SARS-CoV-2-RBD_MAP_Rockefeller_scores.csv"],
            },
            "Vir_mAbs": {
                "files": ["SARS-CoV-2-RBD_MAP_Vir_mAbs_scores.csv"],
                "huggingface_repos": [
                    "datasets/xulab-research/RBD_Antibody/resolve/main/SARS-CoV-2-RBD_MAP_Vir_mAbs_scores.csv?download=true"
                ],
                "file_name": ["SARS-CoV-2-RBD_MAP_Vir_mAbs_scores.csv"],
            },
            "clinical_Abs": {
                "files": ["SARS-CoV-2-RBD_MAP_clinical_Abs_scores.csv"],
                "huggingface_repos": [
                    "datasets/xulab-research/RBD_Antibody/resolve/main/SARS-CoV-2-RBD_MAP_clinical_Abs_scores.csv?download=true"
                ],
                "file_name": ["SARS-CoV-2-RBD_MAP_clinical_Abs_scores.csv"],
            },
        },
    },
    "RBD ACE2 Dataset": {
        "paper_title": "RBD_ACE2_datasets",
        "official_doi": None,
        "files": [
            "SARS-CoV-2-RBD_DMS_Omicron-EG5-FLip-BA286_bc_binding.csv",
            "SARS-CoV-2-RBD_DMS_Omicron-XBB-BQ_bc_binding.csv",
            "SARS-CoV-2-RBD_DMS_Omicron_bc_binding.csv",
            "SARS-CoV-2-RBD_DMS_variants_bc_binding.csv",
            "SARS-CoV-2-RBD_Delta_bc_binding.csv",
        ],
        "huggingface_repos": [
            "datasets/xulab-research/RBD_ACE2/resolve/main/SARS-CoV-2-RBD_DMS_Omicron-EG5-FLip-BA286_bc_binding.csv?download=true",
            "datasets/xulab-research/RBD_ACE2/resolve/main/SARS-CoV-2-RBD_DMS_Omicron-XBB-BQ_bc_binding.csv?download=true",
            "datasets/xulab-research/RBD_ACE2/resolve/main/SARS-CoV-2-RBD_DMS_Omicron_bc_binding.csv?download=true",
            "datasets/xulab-research/RBD_ACE2/resolve/main/SARS-CoV-2-RBD_DMS_variants_bc_binding.csv?download=true",
            "datasets/xulab-research/RBD_ACE2/resolve/main/SARS-CoV-2-RBD_Delta_bc_binding.csv?download=true",
        ],
        "file_name": [
            "SARS-CoV-2-RBD_DMS_Omicron-EG5-FLip-BA286_bc_binding.csv",
            "SARS-CoV-2-RBD_DMS_Omicron-XBB-BQ_bc_binding.csv",
            "SARS-CoV-2-RBD_DMS_Omicron_bc_binding.csv",
            "SARS-CoV-2-RBD_DMS_variants_bc_binding.csv",
            "SARS-CoV-2-RBD_Delta_bc_binding.csv",
        ],
        "sub_datasets": {
            "Omicron_EG5_FLip_BA286": {
                "files": ["SARS-CoV-2-RBD_DMS_Omicron-EG5-FLip-BA286_bc_binding.csv"],
                "huggingface_repos": [
                    "datasets/xulab-research/RBD_ACE2/resolve/main/SARS-CoV-2-RBD_DMS_Omicron-EG5-FLip-BA286_bc_binding.csv?download=true"
                ],
                "file_name": ["SARS-CoV-2-RBD_DMS_Omicron-EG5-FLip-BA286_bc_binding.csv"],
            },
            "Omicron_XBB_BQ": {
                "files": ["SARS-CoV-2-RBD_DMS_Omicron-XBB-BQ_bc_binding.csv"],
                "huggingface_repos": [
                    "datasets/xulab-research/RBD_ACE2/resolve/main/SARS-CoV-2-RBD_DMS_Omicron-XBB-BQ_bc_binding.csv?download=true"
                ],
                "file_name": ["SARS-CoV-2-RBD_DMS_Omicron-XBB-BQ_bc_binding.csv"],
            },
            "Omicron": {
                "files": ["SARS-CoV-2-RBD_DMS_Omicron_bc_binding.csv"],
                "huggingface_repos": [
                    "datasets/xulab-research/RBD_ACE2/resolve/main/SARS-CoV-2-RBD_DMS_Omicron_bc_binding.csv?download=true"
                ],
                "file_name": ["SARS-CoV-2-RBD_DMS_Omicron_bc_binding.csv"],
            },
            "DMS_variants": {
                "files": ["SARS-CoV-2-RBD_DMS_variants_bc_binding.csv"],
                "huggingface_repos": [
                    "datasets/xulab-research/RBD_ACE2/resolve/main/SARS-CoV-2-RBD_DMS_variants_bc_binding.csv?download=true"
                ],
                "file_name": ["SARS-CoV-2-RBD_DMS_variants_bc_binding.csv"],
            },
            "Delta": {
                "files": ["SARS-CoV-2-RBD_Delta_bc_binding.csv"],
                "huggingface_repos": [
                    "datasets/xulab-research/RBD_ACE2/resolve/main/SARS-CoV-2-RBD_Delta_bc_binding.csv?download=true"
                ],
                "file_name": ["SARS-CoV-2-RBD_Delta_bc_binding.csv"],
            },
        },
    },
}


def list_datasets_with_built_in_cleaners() -> None:
    """
    List built-in datasets with predefined processing pipelines.

    These are public datasets for which this package includes pre-defined
    data cleaning pipelines. The datasets themselves are not distributed
    with the package and must be downloaded manually.

    You can also define custom cleaner functions for your own datasets using
    the same `@pipeline_step` framework.

    Predefined datasets:

    - cDNA Proteolysis Dataset
    - ProteinGym DMS Substitutions Dataset
    - Human Domainome Dataset
    - ΔΔG Dataset
    - ΔTm Dataset
    - Antitoxin ParD3 Epistasis Dataset
    - TrpB Epistasis Dataset
    - Human Myoglobin Epistasis Dataset
    - CTXM Epistasis Dataset
    - RBD Antibody Dataset
    - RBD ACE2 Dataset
    """
    print("Public datasets with ready-to-use cleaning pipelines:")
    for key, info in DATASETS.items():
        print(f"- {key}: {info['paper_title']}")
        print(f"  - Official DOI: {info['official_doi']}")
    print(
        "\nUse the `show_download_instructions` function to see detailed download instructions."
    )


def show_download_instructions(dataset_key: str) -> None:
    """
    Show download instructions for a specific dataset.
    """
    info = DATASETS.get(dataset_key)
    if not info:
        raise KeyError(f"Dataset key not found: {dataset_key}")

    print(f"Dataset: {info['paper_title']}")
    for i, file in enumerate(info["files"]):
        print(f"  - File: {file}")
        print(f"    - Download link: {info['huggingface_repos'][i]}")
    print(f"\nSub-datasets:")
    for sub_dataset, sub_info in info.get("sub_datasets", {}).items():
        print(f"- Sub-dataset: {sub_dataset}")
        for i, file in enumerate(sub_info["files"]):
            print(f"  - File: {file}")
            print(f"    - Download link: {sub_info['huggingface_repos'][i]}")
