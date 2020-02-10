"""Module for the packaging of translated catalog files."""

import unicodedata

import pandas as pd

from benchsci.vendor_catalog.library_translation.backend.bsproduct.csv_utils import (
    read_csv,
    read_details_csv,
    write_dataframe_to_csv,
)


def check_invisible_characters(data_frame):
    """check for invisible characters in a dataframe."""
    data_frame = data_frame.applymap(replace_invisible_characters)
    inv_df = data_frame.applymap(lambda x: "<INVCHAR>" in str(x))
    if any(inv_df.values.flatten()):
        return data_frame
    return None


def check_invisible_characters_to_csv(data_frame, invis_file_out):
    """check for invisible characters in a dataframe and write csv out."""
    df_out = check_invisible_characters(data_frame)
    if df_out:
        write_dataframe_to_csv(df_out, invis_file_out)


def replace_invisible_characters(test_string):
    """Replaces invisible characters and returns string with invisible
    characters tagged."""
    if any(
        [
            unicodedata.category(x)[0] in ["C", "Z"] and x != u"\u0020"
            for x in str(test_string)
        ]
    ):
        # when the character is a control character or a separator other than space, replace it with <INVCHAR>
        return "".join(
            [
                "<INVCHAR>"
                if unicodedata.category(x)[0] in ["C", "Z"] and x != u"\u0020"
                else x
                for x in str(test_string)
            ]
        )

    return test_string


# Translation Stuff


def translate_list(unique_list_param, translation_dict):
    """Gets a list of names and using the translation dictionary, translates
    them.

    :param unique_list_param: {list} List of names
    :param translation_dict: {dict} Translation dict
    :return:
    """
    translated_list = []
    for name in unique_list_param:
        if name in translation_dict.keys():
            translated_list.append(translation_dict[name])
        else:
            translated_list.append(None)
    return translated_list


def unique_list(data_frame, column):
    """Retrieve a unique list of values from a pandas dataframe column."""
    unique_list_param = list()
    for val in data_frame[column].tolist():
        if val:
            val = str(val)
            unique_list_param.extend([k.strip() for k in val.split(",")])
    unique_list_param = list(set(unique_list_param))
    return unique_list_param


def create_list(data_frame, column, translate_dict):
    """Given a dataframe and column, finds the set of unique values in the
    column and then returns a translated list using translate_list function.

    :param data_frame: pandas dataframe containing the details catalog library
    :param column: column we're creating a list for
    :param translate_dict: the translation dictionary
    :return: pandas dataframe containing library with the original type, the unique list and the translated list
    """

    unique_list_of_items = list(set(unique_list(data_frame, column)))
    translated_list = translate_list(unique_list_of_items, translate_dict)

    return pd.DataFrame(
        {
            "Library": column,
            "Original": unique_list_of_items,
            "Translated": translated_list,
        }
    )


def get_translation_dict(data_frame):
    """get translation dict.

    :param data_frame: data-frame
    :return:
    """

    data_frame = data_frame.loc[:, "original":"translated"]
    translation_dict = pd.Series(
        data_frame.translated.values, index=data_frame.translated
    ).to_dict()
    return translation_dict


def generate_translation_lists_files(details_file, translation_dict_file, file_out):
    """Generate the lists from files."""
    data_frame = read_details_csv(details_file)
    df_trans = read_csv(translation_dict_file)  # , sep=",")
    combined = generate_translation_lists(data_frame, df_trans)
    return write_dataframe_to_csv(combined, file_out)


def generate_translation_lists(details_file_df, translation_dict_file_df):
    """Packages host, reactivity and applications into lists and sliced views
    of the dataframe.

    :param details_file_df: df containing the details file data
    :param translation_dict_file_df: df containing the translation dict rules
    :return:
    """
    translation_dict = get_translation_dict(translation_dict_file_df)
    hosts = create_list(details_file_df, "host", translation_dict)
    reactivity = create_list(details_file_df, "reactivity", translation_dict)
    apps = create_list(details_file_df, "applications", translation_dict)
    conjugation = create_list(details_file_df, "conjugation", translation_dict)
    return pd.concat([hosts, reactivity, apps, conjugation])
