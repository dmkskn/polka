import pytest

import polka


def test_books():
    books = polka.books()
    assert isinstance(books, list)
    assert isinstance(books[0], polka.Book)
