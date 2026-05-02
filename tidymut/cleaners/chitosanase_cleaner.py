# tidymut/cleaners/cdna_proteolysis_cleaner.py
from __future__ import annotations

import pandas as pd
from typing import TYPE_CHECKING
from dataclasses import dataclass, field
from pathlib import Path
import logging

from .base_config import BaseCleanerConfig
from .basic_cleaners import (
    read_dataset,
    extract_and_rename_columns,
    filter_and_clean_data,
    convert_data_types,
    validate_mutations,
    convert_to_mutation_dataset_format,
    subtract_labels_by_wt,
    add_columns,
)
from .rbd_custom_cleaners import apply_mutations_preserving_wild_type

from ..core.dataset import MutationDataset
from ..core.pipeline import Pipeline, create_pipeline

if TYPE_CHECKING:
    from typing import Any, Callable, Dict, List, Optional, Tuple, Union

__all__ = [
    "ChitosanaseCleanerConfig",
    "create_chitosanase_cleaner",
    "clean_chitosanase_dataset",
]


def __dir__() -> List[str]:
    return __all__


# Create module logger
logger = logging.getLogger(__name__)


@dataclass
class ChitosanaseCleanerConfig(BaseCleanerConfig):
    """
    Configuration class for chitosanase dataset cleaner.
    Inherits from BaseCleanerConfig and adds chitosanase-specific configuration options.

    Simply run `tidymut.download_chitosanase_source_file()` to download the dataset.

    Alternatively, the raw chitosanase file can be obtained from:

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
            "aa_mut": "mut_info",
            "Tm": "label_chitosanase",
            "sequence": "wt_sequence",
        }
    )

    # Data filtering configuration
    filters: Dict[str, Callable] = field(
        default_factory=lambda: {
            "label_chitosanase": lambda s: pd.to_numeric(
                s.astype(str).str.strip(), errors="coerce"
            ).notna()
        }
    )

    # Type conversion configuration
    type_conversions: Dict[str, str] = field(
        default_factory=lambda: {"label_chitosanase": "float"}
    )

    # Mutation validation parameters
    validate_mut_workers: int = 16

    # Wildtype validation parameters
    validate_wt_workers: int = 16

    # Score columns configuration
    label_columns: List[str] = field(default_factory=lambda: ["label_chitosanase"])
    primary_label_column: str = "label_chitosanase"

    # Override default pipeline name
    pipeline_name: str = "ChitosanaseCleanerPipeline"

    def validate(self) -> None:
        """Validate chitosanase-specific configuration parameters

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
        required_mappings = {"aa_mut", "Tm", "sequence"}
        missing = required_mappings - set(self.column_mapping.keys())
        if missing:
            raise ValueError(f"Missing required column mappings: {missing}")


def create_chitosanase_cleaner(
    dataset_or_path: Optional[Union[pd.DataFrame, str, Path]] = None,
    config: Optional[
        Union[ChitosanaseCleanerConfig, Dict[str, Any], str, Path]
    ] = None,
) -> Pipeline:
    """Create chitosanase dataset cleaning pipeline

    Parameters
    ----------
    dataset_or_path : Optional[Union[pd.DataFrame, str, Path]], default=None
        Raw dataset DataFrame or file path to chitosanase dataset.
    config : Optional[Union[ChitosanaseCleanerConfig, Dict[str, Any], str, Path]]
        Configuration for the cleaning pipeline. Can be:
        - ChitosanaseCleanerConfig object
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
        final_config = ChitosanaseCleanerConfig()
    elif isinstance(config, ChitosanaseCleanerConfig):
        final_config = config
    elif isinstance(config, dict):
        # Partial configuration - merge with defaults
        default_config = ChitosanaseCleanerConfig()
        final_config = default_config.merge(config)
    elif isinstance(config, (str, Path)):
        # Load from file
        final_config = ChitosanaseCleanerConfig.from_json(config)
    else:
        raise TypeError(
            f"config must be ChitosanaseCleanerConfig, dict, str, Path or None, "
            f"got {type(config)}"
        )

    # Log configuration summary
    logger.info(
        f"Chitosanase dataset will be cleaned with pipeline: {final_config.pipeline_name}"
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
            .delayed_then(filter_and_clean_data, filters=final_config.filters)
            .delayed_then(
                convert_data_types, type_conversions=final_config.type_conversions
            )
            .delayed_then(
                add_column,
                dataset_name="Chitosanase",
                column_name="name",
            )
            .delayed_then(
                validate_mutations,
                mutation_column=final_config.column_mapping.get("aa_mut", "aa_mut"),
                mutation_sep=",",
                is_zero_based=False,
                exclude_patterns=["WT"],
                num_workers=final_config.validate_mut_workers,
            )
            .delayed_then(
                apply_mutations_preserving_wild_type,
                sequence_column=final_config.column_mapping.get("sequence", "sequence"),
                name_column="name",
                mutation_column=final_config.column_mapping.get("aa_mut", "aa_mut"),
            )
            .delayed_then(
                subtract_labels_by_wt,
                name_column="name",
                label_columns=final_config.label_columns,
                mutation_column=final_config.column_mapping.get("aa_mut", "aa_mut"),
                wt_identifier="WT",
                in_place=True,
            )
            .delayed_then(
                convert_to_mutation_dataset_format,
                name_column="name",
                mutation_column=final_config.column_mapping.get("aa_mut", "aa_mut"),
                mutated_sequence_column="mut_seq",
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
        logger.error(f"Error in creating chitosanase cleaning pipeline: {str(e)}")
        raise RuntimeError(
            f"Error in creating chitosanase cleaning pipeline: {str(e)}"
        )


def clean_chitosanase_dataset(
    pipeline: Pipeline,
) -> Tuple[Pipeline, MutationDataset]:
    """Clean chitosanase dataset using configurable pipeline

    Parameters
    ----------
    pipeline : Pipeline
        chitosanase dataset cleaning pipeline

    Returns
    -------
    Tuple[Pipeline, MutationDataset]
        - Pipeline: The cleaned pipeline
        - MutationDataset: The cleaned chitosanase dataset

    Examples
    --------
    Use default configuration:

    >>> pipeline = create_chitosanase_cleaner(df)  # df is raw chitosanase dataset file

    Use partial configuration:

    >>> pipeline = create_chitosanase_cleaner(df, config={
    ...     "validate_mut_workers": 8,
    ... })

    Load configuration from file:

    >>> pipeline = create_chitosanase_cleaner(df, config="config.json")
    >>> pipeline, dataset = clean_chitosanase_dataset(pipeline)
    """
    try:
        # Run pipeline
        pipeline.execute()

        # Extract results
        chitosanase_dataset_df, chitosanase_ref_seq = pipeline.data
        chitosanase_dataset = MutationDataset.from_dataframe(
            chitosanase_dataset_df, chitosanase_ref_seq
        )

        logger.info(
            f"Successfully cleaned chitosanase dataset: "
            f"{len(chitosanase_dataset_df)} mutations from {len(chitosanase_ref_seq)} proteins"
        )

        return pipeline, chitosanase_dataset
    except Exception as e:
        logger.error(
            f"Error in running chitosanase dataset cleaning pipeline: {str(e)}"
        )
        raise RuntimeError(
            f"Error in running chitosanase dataset cleaning pipeline: {str(e)}"
        )
