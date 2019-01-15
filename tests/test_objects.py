import pytest

import polka


BOOK_ID = 523
BOOK_TITLE = "Герой нашего времени"
BOOK_AUTHORS = ["Михаил Лермонтов"]


@pytest.fixture(scope="module")
def book():
    book = polka.Book(BOOK_ID)
    book.rawdata.update(polka.rawbook(BOOK_ID))
    polka.Book._importance = polka._importance()
    return book


@pytest.fixture()
def emptry_book():
    return polka.Book(BOOK_ID)


def test_book_loads_data(emptry_book: polka.Book):
    assert emptry_book._n_requests == 0
    assert emptry_book.title
    assert emptry_book.description
    # assert emptry_book.pundit
    assert emptry_book.questions
    assert emptry_book.sources
    assert emptry_book.year
    assert emptry_book._n_requests == 1
    assert emptry_book.importance
    assert emptry_book._n_requests == 2
    assert emptry_book.importance
    assert emptry_book._n_requests == 2


def test_book_title_attr(book: polka.Book):
    assert book.title == BOOK_TITLE


def test_book_desc_attr(book: polka.Book):
    assert isinstance(book.description, str)


def test_book_authors(book: polka.Book):
    assert book.authors == BOOK_AUTHORS


def test_book_importance_attr(book: polka.Book):
    assert isinstance(book.importance, float)
    assert book.importance == float(polka._importance()[book.id])


# def test_book_pundit_attr(book: polka.Book):
#     assert isinstance(book.pundit, polka.Pundit)


def test_book_year_attr(book: polka.Book):
    assert isinstance(book.year, polka.Year)


def test_book_has_article_attr(book: polka.Book):
    assert isinstance(book.has_article, bool)


def test_book_question_attr(book: polka.Book):
    assert isinstance(book.questions, list)
    for item in book.questions:
        assert isinstance(item, polka.Question)
        assert isinstance(item.question, str)
        assert isinstance(item.answer, str)
        assert isinstance(item.answer_with_notes, str)
