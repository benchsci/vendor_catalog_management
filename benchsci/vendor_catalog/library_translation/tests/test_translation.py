"""test some translation pieces."""

from benchsci.vendor_catalog.library_translation.backend.bsproduct.translation import translate


def test_when_remove_in_dict_then_skip():
    """see method name."""
    test_dict = {"Human": "REMOVE", "Mouse": "Mouse"}
    test_input = "Human,Mouse"
    translated_str = translate(test_input, test_dict)
    assert translated_str == "Mouse"


def test_when_remove_not_in_dict_then_no_effect():
    """see method name."""
    test_dict = {"Human": "Human", "Mouse": "Mouse"}
    test_input = "Human,Mouse"
    translated_str = translate(test_input, test_dict)
    assert translated_str == "Human,Mouse"


def test_when_remove_then_empty_string():
    """see method name."""
    test_dict = {"Human": "REMOVE", "Mouse": "REMOVE"}
    test_input = "Human,Mouse"
    translated_str = translate(test_input, test_dict)
    assert translated_str == ""
