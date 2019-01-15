import pytest

import polka


def test_books():
    books = polka.books()
    assert isinstance(books, list)
    assert isinstance(books[0], polka.Book)


def test_pundits():
    pundits = polka.pundits()
    assert isinstance(pundits, list)
    assert isinstance(pundits[0], polka.Pundit)


def test_lists():
    lists = polka.lists()
    assert isinstance(lists, list)
    assert isinstance(lists[0], polka.Compilation)
