"""CSV Utils."""

import logging

import pandas as pd

DETAILS_FILE_HEADER = [
    "vendor",
    "sku",
    "new_sku",
    "name",
    "url",
    "applications",
    "reactivity",
    "host",
    "clonality",
    "clone",
    "conjugation",
    "conjugate",
    "immunogen",
    "epitope",
    "specificity_ex",
    "immunogen_ex",
    "uniprot",
    "gene",
    "ids",
    "kit",
    "ct",
    "ptm",
    "ana",
]


class SchemaError(Exception):
    """Raised when Input CSV Schema does not conform to expectations."""


def read_details_csv(details_file):
    """Read details file from csv."""
    try:
        data_frame = pd.read_csv(
            open(details_file, "rb"),
            encoding="utf-8",
            engine="c",
            sep="\t",
            header=0,
            index_col=False,
        )
        data_frame.columns = [x.lower() for x in data_frame.columns]
        unique_headers = set(data_frame.columns)
        assert unique_headers == set(DETAILS_FILE_HEADER)
    except AssertionError:
        logging.error("DETAILS FILE SCHEMA ERROR: %s", details_file)
        raise SchemaError(details_file)
    return data_frame


def read_csv(list_file, sep="\t"):
    """helper method to use pandas to read a csv."""
    return pd.read_csv(
        open(list_file, "rb"),
        encoding="utf-8",
        engine="c",
        sep=sep,
        header=0,
        index_col=False,
    )


def write_dataframe_to_csv(data, out_file):
    """Write a dataframe out to csv convenience method."""
    data.to_csv(out_file, encoding="utf-8", sep="\t", index=False)
    return data
