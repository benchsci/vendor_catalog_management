"""Test a few things regarding invisible characters."""

from benchsci.vendor_catalog.library_translation.backend.bsproduct.packaging import (
    replace_invisible_characters,
)


def test_no_break_space():
    """test no break space is replaced."""
    inv_str = u"\u00A0ACTER"
    assert replace_invisible_characters(inv_str) == u"<INVCHAR>ACTER"


def test_normal_space():
    """test normal space not replaced."""
    inv_str = u"TEST ACTER"
    assert replace_invisible_characters(inv_str) == inv_str


def test_zero_width_space():
    """test zero width space is replaced."""
    inv_str = u"TEST\u200bACTER"
    assert replace_invisible_characters(inv_str) == u"TEST<INVCHAR>ACTER"


def test_normal_word():
    """test normal word is not replaced."""
    inv_str = u"TestWord"
    assert replace_invisible_characters(inv_str) == inv_str


def test_tab():
    """test tab character is replaced."""
    inv_str = u"Test \t Tab"
    assert replace_invisible_characters(inv_str) == u"Test <INVCHAR> Tab"
