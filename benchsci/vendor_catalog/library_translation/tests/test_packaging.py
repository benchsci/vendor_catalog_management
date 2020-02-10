"""Test the translation packaging.py module."""

import pytest

from benchsci.vendor_catalog.library_translation.backend.bsproduct.packaging import (  # create_list,; get_translation_dict,
    unique_list,
)


@pytest.mark.skip(reason="incomplete")
def test_unique_list():
    """Test that unique list correct returns a unique list of terms from the
    dataframe."""
    data = {
        "letters": ["a", "a", "c", "d"],
    }
    my_list = unique_list(data, "letters")
    print(my_list)


@pytest.mark.skip(reason="incomplete")
def test_create_list():
    """Test the creation of a list for library translation."""
    # get_translation_dict()
    # create_list()
