import pytest

import polka


def test_rawbooks():
    assert isinstance(polka.rawbooks(), dict)


def test_rawbook():
    assert "Герой нашего времени" in polka.rawbook(523)["title"]


def test_rawsearch():
    assert isinstance(polka.rawsearch("Грибоедов"), list)


def test_rawlists():
    assert isinstance(polka.rawlists(), dict)


def test_rawlist():
    assert isinstance(polka.rawlist(85), dict)


def test_rawpundits():
    assert isinstance(polka.rawpundits(), dict)


def test_rawpunditposts():
    assert isinstance(polka.rawpunditposts(312), dict)


def test_rawpunditfavs():
    assert isinstance(polka.rawpunditfavs(312), dict)


def test_rawmaterials():
    rawmaterials = polka.rawmaterials()
    assert isinstance(rawmaterials, dict)
    assert rawmaterials["title"] == "Материалы"


def test_rawpodcasts():
    rawpodcasts = polka.rawpodcasts()
    assert isinstance(rawpodcasts, dict)
    assert rawpodcasts["title"] == "Материалы"


def test_rawblogs():
    rawblogs = polka.rawblogs()
    assert isinstance(rawblogs, dict)
    assert rawblogs["title"] == "Материалы"
