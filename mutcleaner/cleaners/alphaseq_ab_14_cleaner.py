# tidymut/cleaners/alphaseq_ab_14_cleaner.py
from __future__ import annotations

import re
import pandas as pd
from typing import TYPE_CHECKING
from dataclasses import dataclass, field
from pathlib import Path
import logging

from .base_config import BaseCleanerConfig
from .basic_cleaners import (
    add_columns,
    read_dataset,
    extract_and_rename_columns,
    filter_and_clean_data,
    convert_data_types,
    average_labels_by_name,
    convert_to_mutation_dataset_format,
    infer_mutations_from_sequences,
)

from ..core.dataset import MutationDataset
from ..core.pipeline import Pipeline, create_pipeline

if TYPE_CHECKING:
    from typing import Any, Callable, Dict, List, Optional, Tuple, Union

__all__ = [
    "CDNAProteolysisCleanerConfig",
    "create_cdna_proteolysis_cleaner",
    "clean_cdna_proteolysis_dataset",
]


def __dir__() -> List[str]:
    return __all__


# Create module logger
logger = logging.getLogger(__name__)


@dataclass
class AlphaseqAb14CleanerConfig(BaseCleanerConfig):
    """
    Configuration class for AlphaseqAb14 dataset cleaner.
    Inherits from BaseCleanerConfig and adds AlphaseqAb14-specific configuration options.

    Simply run `tidymut.download_alphaseq_ab_14_source_file()` to download the dataset.

    Alternatively, the raw AlphaseqAb14 file can be obtained from:

    - Zenodo: https://zenodo.org/records/7992926, File `Tsuboyama2023_Dataset2_Dataset3_20230416.csv` in `Processed_K50_dG_datasets.zip`
    - Hugging Face: https://huggingface.co/datasets/xulab-research/TidyMut/blob/main/AlphaseqAb14/Tsuboyama2023_Dataset2_Dataset3_20230416.csv

    Attributes
    ----------
    column_mapping : Dict[str, str]
        Mapping from source to target column names
    filters : Dict[str, Callable]
        Filter conditions for data cleaning
    type_conversions : Dict[str, str]
        Data type conversion specifications
    validate_mut_workers : int
        Number of workers for mutation validation, set to -1 to use all available CPUs
    validate_wt_workers : int
        Number of workers for wildtype sequence validation, set to -1 to use all available CPUs
    label_columns : List[str]
        List of score columns to process
    primary_label_column : str
        Primary score column for the dataset
    """

    # Column mapping configuration
    column_mapping: Dict[str, str] = field(
        default_factory=lambda: {
            "Sequence": "mut_sequence",
            "Target": "target",
            "Pred_affinity": "label",
            "POI": "POI",
        }
    )

    # Data filtering configuration
    filters: Dict[str, Callable] = field(
        default_factory=lambda: {
            "target": "MIT_Target",
            "POI": lambda s: s.str.startswith('14L', na=False)
        }
    )

    # Type conversion configuration
    type_conversions: Dict[str, str] = field(
        default_factory=lambda: {"label": "float"}
    )

    # columns to be added with constant values 
    columns_to_add: Dict[str, Any] = field(
        default_factory=lambda: {
            "name": "Ab_14",
            "wt_sequence": "EVQLVETGGGLVQPGGSLRLSCAASGFTLNSYGISWVRQAPGKGPEWVSVIYSDGRRTFYGDSVKGRFTISRDTSTNTVYLQMNSLRVEDTAVYYCAKGRAAGTFDSWGQGTLVTVSSGGGGSGGGGSGGGGSDVVMTQSPESLAVSLGERATISCKSSQSVLYESRNKNSVAWYQQKAGQPPKLLIYWASTRESGVPDRFSGSGSGTDFTLTISSLQAEDAAVYYCQQYHRLPLSFGGGTKVEIK",
        }
    )

    # Processing parameters
    process_workers: int = 32

    # Score columns configuration
    label_columns: List[str] = field(default_factory=lambda: ["label"])
    primary_label_column: str = "label"

    # Override default pipeline name
    pipeline_name: str = "AlphaseqAb14CleanerPipeline"

    def validate(self) -> None:
        """Validate AlphaseqAb14-specific configuration parameters

        Raises
        ------
        ValueError
            If configuration is invalid
        """
        # Call parent validation
        super().validate()

        # Validate score columns
        if not self.label_columns:
            raise ValueError("label_columns cannot be empty")

        if self.primary_label_column not in self.label_columns:
            raise ValueError(
                f"primary_label_column '{self.primary_label_column}' "
                f"must be in label_columns {self.label_columns}"
            )

        # Validate column mapping
        required_mappings = {"Sequence", "Target", "Pred_affinity", "POI"}
        missing = required_mappings - set(self.column_mapping.keys())
        if missing:
            raise ValueError(f"Missing required column mappings: {missing}")


def create_alphaseq_ab_14_cleaner(
    dataset_or_path: Optional[Union[pd.DataFrame, str, Path]] = None,
    config: Optional[
        Union[AlphaseqAb14CleanerConfig, Dict[str, Any], str, Path]
    ] = None,
) -> Pipeline:
    """Create AlphaseqAb14 dataset cleaning pipeline

    Parameters
    ----------
    dataset_or_path : Optional[Union[pd.DataFrame, str, Path]], default=None
        Raw dataset DataFrame or file path to AlphaseqAb14 dataset.
    config : Optional[Union[AlphaseqAb14CleanerConfig, Dict[str, Any], str, Path]]
        Configuration for the cleaning pipeline. Can be:
        - AlphaseqAb14CleanerConfig object
        - Dictionary with configuration parameters (merged with defaults)
        - Path to JSON configuration file (str or Path)
        - None (uses default configuration)

    Returns
    -------
    Pipeline
        Pipeline: The cleaning pipeline used

    Raises
    ------
    TypeError
        If config has invalid type
    ValueError
        If configuration validation fails
    """
    # Handle configuration parameter
    if config is None:
        final_config = AlphaseqAb14CleanerConfig()
    elif isinstance(config, AlphaseqAb14CleanerConfig):
        final_config = config
    elif isinstance(config, dict):
        # Partial configuration - merge with defaults
        default_config = AlphaseqAb14CleanerConfig()
        final_config = default_config.merge(config)
    elif isinstance(config, (str, Path)):
        # Load from file
        final_config = AlphaseqAb14CleanerConfig.from_json(config)
    else:
        raise TypeError(
            f"config must be AlphaseqAb14CleanerConfig, dict, str, Path or None, "
            f"got {type(config)}"
        )

    # Log configuration summary
    logger.info(
        f"AlphaseqAb14 dataset will cleaning with pipeline: {final_config.pipeline_name}"
    )
    logger.debug(f"Configuration:\n{final_config.get_summary()}")

    try:
        # Create pipeline
        pipeline = create_pipeline(dataset_or_path, final_config.pipeline_name)

        # Add cleaning steps
        pipeline = (
            pipeline.delayed_then(
                extract_and_rename_columns,
                column_mapping=final_config.column_mapping,
            )
            .delayed_then(
                filter_and_clean_data, 
                filters=final_config.filters,
                drop_na_columns=final_config.label_columns,
            )
            .delayed_then(
                convert_data_types, type_conversions=final_config.type_conversions
            )
            .delayed_then(
                average_labels_by_name,
                name_columns=(
                    final_config.column_mapping.get("Sequence", "Sequence"),
                ),
                label_columns=final_config.label_columns,
            )
            .delayed_then(
                add_columns,
                columns_to_add=final_config.columns_to_add,
            )
            .delayed_then(
                infer_mutations_from_sequences,
                wt_sequence_column="wt_sequence",
                mut_sequence_column=final_config.column_mapping.get("Sequence", "Sequence"),
                num_workers=final_config.process_workers,
            )
            .delayed_then(
                convert_to_mutation_dataset_format,
                name_column="name",
                mutation_column="inferred_mutations",
                sequence_column="wt_sequence",
                mutated_sequence_column=final_config.column_mapping.get("Sequence", "Sequence"),
                label_column=final_config.primary_label_column,
                is_zero_based=True,
            )
        )

        # Create pipeline based on dataset_or_path type
        if isinstance(dataset_or_path, (str, Path)):
            pipeline.add_delayed_step(read_dataset, 0)
        elif not isinstance(dataset_or_path, pd.DataFrame):
            raise TypeError(
                f"dataset_or_path must be pd.DataFrame or str/Path, "
                f"got {type(dataset_or_path)}"
            )

        return pipeline

    except Exception as e:
        logger.error(f"Error in creating AlphaseqAb14 cleaning pipeline: {str(e)}")
        raise RuntimeError(
            f"Error in creating AlphaseqAb14 cleaning pipeline: {str(e)}"
        )


def clean_alphaseq_ab_14_dataset(
    pipeline: Pipeline,
) -> Tuple[Pipeline, MutationDataset]:
    """Clean AlphaseqAb14 dataset using configurable pipeline

    Parameters
    ----------
    pipeline : Pipeline
        AlphaseqAb14 dataset cleaning pipeline

    Returns
    -------
    Tuple[Pipeline, MutationDataset]
        - Pipeline: The cleaned pipeline
        - MutationDataset: The cleaned AlphaseqAb14 dataset

    Examples
    --------
    Use default configuration:

    >>> pipeline = create_alphaseq_ab_14_cleaner(df)  # df is raw AlphaseqAb14 dataset file

    Use partial configuration:

    >>> pipeline = create_alphaseq_ab_14_cleaner(df, config={
    ...     "validate_mut_workers": 8,
    ... })

    Load configuration from file:

    >>> pipeline = create_alphaseq_ab_14_cleaner(df, config="config.json")
    >>> pipeline, dataset = clean_alphaseq_ab_14_dataset(pipeline)
    """
    try:
        # Run pipeline
        pipeline.execute()

        # Extract results
        alphaseq_ab_14_dataset_df, alphaseq_ab_14_ref_seq = pipeline.data
        alphaseq_ab_14_dataset = MutationDataset.from_dataframe(
            alphaseq_ab_14_dataset_df, alphaseq_ab_14_ref_seq
        )

        logger.info(
            f"Successfully cleaned AlphaseqAb14 dataset: "
            f"{len(alphaseq_ab_14_dataset_df)} mutations from {len(alphaseq_ab_14_ref_seq)} proteins"
        )

        return pipeline, alphaseq_ab_14_dataset
    except Exception as e:
        logger.error(
            f"Error in running AlphaseqAb14 dataset cleaning pipeline: {str(e)}"
        )
        raise RuntimeError(
            f"Error in running AlphaseqAb14 dataset cleaning pipeline: {str(e)}"
        )
