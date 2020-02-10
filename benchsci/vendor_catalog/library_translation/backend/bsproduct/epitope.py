"""" epitope extraction."""

import re

import pandas as pd

from benchsci.vendor_catalog.library_translation.backend.bsproduct.csv_utils import read_csv, read_details_csv


def load_pattern_from_file(epitope_translation_file):
    """Load pattern from file."""
    epitope_frame = read_csv(epitope_translation_file)
    return load_pattern(epitope_frame)


def load_pattern(epitope_translation):
    """Load pattern from frame."""
    pattern = dict()
    for _, row in epitope_translation.iterrows():
        pattern[str(row[0]).lower()] = str(row[1])
    return pattern


# pattern = {
#     "N-Terminus": "N Terminus",
#     "C-Terminus", "N Terminus",
#     "C Terminus", "C terminal",
#     "N terminal", "C-terminal",
#     "N-terminal", "internal region",
#     "internal sequence",
#     "central region",
#     "middle region",
#     "carboxy terminus",
#     "amino terminus"
# }


def read_csv_for_epitope(details_file):
    """Read in the details file and return data frames."""

    data_frame = read_details_csv(details_file)
    epitope_columns = [
        "vendor",
        "sku",
        "name",
        "immunogen",
        "epitope",
        "specificity",
        "sequence",
        "start",
        "stop",
    ]
    data = pd.DataFrame(columns=epitope_columns)
    return data_frame, data


def epitope_extraction(details_file, epitope_pattern_file):
    """Epitope extraction."""

    data_frame, data = read_csv_for_epitope(details_file)
    pattern = load_pattern_from_file(epitope_pattern_file)
    for idx, det_row in data_frame.iterrows():
        searchable_text = (
            str(det_row["immunogen"]) + str(det_row["epitope"]) + str(det_row["name"])
        )
        out = []
        for param in pattern:
            if param.lower() in searchable_text.lower() and pattern[param] not in out:
                out.append(pattern[param])

        data_frame.loc[idx, "specificity_ex"] = ",".join(out)
        sequence_match = re.search(r"[A-Z]{10,}", searchable_text)
        match = re.search(r"\w*\d+-\w*\d+", searchable_text)
        dat = dict()
        dat["start"] = ""
        dat["stop"] = ""
        dat["sequence"] = ""
        if sequence_match:
            sequence = str(sequence_match.group())
            data_frame.loc[idx, "immunogen_ex"] = sequence

        if match:
            found = match.group().split("-")
            dat["start"] = found[0]
            dat["start"] = re.search(r"\d+", dat["start"]).group()
            dat["stop"] = found[-1]
            dat["stop"] = re.search(r"\d+", dat["stop"]).group()

        data.loc[len(data)] = [
            det_row["vendor"],
            det_row["sku"],
            det_row["name"],
            det_row["immunogen"],
            det_row["epitope"],
            ",".join(out),
            dat["sequence"],
            dat["start"],
            dat["stop"],
        ]

    return data_frame, data
