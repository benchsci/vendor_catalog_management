"""Module for the translation of catalog files."""

import pandas as pd

from benchsci.vendor_catalog.library_translation.backend.bsproduct.csv_utils import read_csv, read_details_csv


def translate(x, translation_dict):
    """translate."""
    unique_list = list()
    x = str(x)
    unique_list.extend([k.strip() for k in x.split(",")])
    translated_list = list()
    for item in unique_list:
        if item in translation_dict.keys() and translation_dict[item] != "REMOVE":
            translated_list.append(translation_dict[item])
    return ",".join(translated_list)


def translate_details(
    details_file, host_list, reactivities_list, applications_list, conjugation_list
):
    """Map translated and QAed lists back to Details file.

    Arguments:
        details_file {str} -- details
        host_list {str} -- host list file
        reactivities_list {str} -- rxt list file
        applications_list {str} -- apps list file
        conjugation_list {str} -- conjugations list file
    """

    data_frame = read_details_csv(details_file)

    cols = ["host", "reactivity", "applications", "conjugation"]
    list_files = [host_list, reactivities_list, applications_list, conjugation_list]
    for col, list_file in zip(cols, list_files):

        list_df = read_csv(list_file)
        list_df.fillna("", inplace=True)
        list_dict = pd.Series(
            list_df.Translated.values, index=list_df.Original
        ).to_dict()
        data_frame[col] = data_frame[col].apply(
            lambda x, ld=list_dict: translate(x, ld)
        )

    return data_frame
