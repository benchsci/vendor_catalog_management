"""Test file for various processing pieces including translation lists and
more."""

import tempfile

from benchsci.vendor_catalog.library_translation.backend.bsproduct.epitope import epitope_extraction
from benchsci.vendor_catalog.library_translation.backend.bsproduct.packaging import (
    generate_translation_lists_files,
)
from benchsci.vendor_catalog.library_translation.backend.bsproduct.translation import translate_details

# Real Data Files
TESTS_DATA_FOLDER = "benchsci/vendor_catalog/library_translation/tests/data/"
DETAILS_FILE = "%sMitoSciences_Details.txt" % TESTS_DATA_FOLDER
TRANSLATION_DICT = "%stranslation_database.txt" % TESTS_DATA_FOLDER
# TRANSLATION_DICT = "%stranslation_list_preloaded_UPDATED.csv" % TESTS_DATA_FOLDER
HOST_LIST = "%sHost_List.txt" % TESTS_DATA_FOLDER
REACTIVITIES_LIST = "%sReactivities_List.txt" % TESTS_DATA_FOLDER
APPLICATIONS_LIST = "%sApplications_List.txt" % TESTS_DATA_FOLDER
CONJUGATION_LIST = "%sConjugation_List.txt" % TESTS_DATA_FOLDER
EPITOPE_FILE = "%sepitope_table.csv" % TESTS_DATA_FOLDER


def test_epitope_extraction(
    details_file=DETAILS_FILE, epitope_pattern_file=EPITOPE_FILE
):
    """Test the epitope extraction process.

    :param details_file: Details file to load in
    :param epitope_pattern_file: The pattern file
    :return: data-frames representing the returned data
    """
    df1, df2 = epitope_extraction(details_file, epitope_pattern_file)
    assert df1 is not None
    assert df2 is not None


def test_generate_translation_lists(
    details_file=DETAILS_FILE, translation_dict_file=TRANSLATION_DICT
):
    """Test generation of the translation lists.

    :param details_file: the details file to read in
    :param translation_dict_file: the translation dict file
    :return: dataframe
    """
    with tempfile.NamedTemporaryFile() as file_pointer:
        result_df = generate_translation_lists_files(
            details_file, translation_dict_file, file_pointer.name
        )
        assert result_df is not None


def test_translate(
    details_file=DETAILS_FILE,
    host_list=HOST_LIST,
    reactivities_list=REACTIVITIES_LIST,
    applications_list=APPLICATIONS_LIST,
    conjugation_list=CONJUGATION_LIST,
):
    """Test combination of the translation lists into actual details file.

    :param details_file: ..
    :param host_list: ..
    :param reactivities_list: ..
    :param applications_list: ..
    :param conjugation_list: ..
    :return: tbd
    """
    data_frame = translate_details(
        details_file, host_list, reactivities_list, applications_list, conjugation_list
    )
    assert data_frame is not None
