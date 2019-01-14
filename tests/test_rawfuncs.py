import pytest

import polka


def test_rawbooks():
    assert isinstance(polka.rawbooks(), list)


def test_rawbook():
    assert "Герой нашего времени" in polka.rawbook(523)["title"]


def test_rawsearch():
    assert isinstance(polka.rawsearch("Грибоедов"), list)


def test_rawlists():
    assert isinstance(polka.rawlists(), list)


def test_rawpundits():
    assert isinstance(polka.rawpundits(), list)
