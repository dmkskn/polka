import pytest

import polka


BOOK_ID = 523
BOOK_TITLE = "Герой нашего времени"
BOOK_AUTHORS = ["Михаил Лермонтов"]
PUNDIT_ID = 312


@pytest.fixture(scope="module")
def book():
    book = polka.Book(BOOK_ID)
    book.rawdata.update(polka.rawbook(BOOK_ID))
    polka.Book._importance = polka._importance()
    return book


@pytest.fixture
def empty_book():
    return polka.Book(BOOK_ID)


@pytest.fixture(scope="module")
def pundit():
    pundit = polka.Pundit(PUNDIT_ID)
    pundits = polka.rawpundits()
    pundit.rawdata.update([p for p in pundits if p["id"] == PUNDIT_ID][0])
    pundit.rawdata.update({"posts": polka.rawpunditposts(PUNDIT_ID)})
    pundit.rawdata.update({"favs": polka.rawpunditfavs(PUNDIT_ID)})
    return pundit


@pytest.fixture
def empty_pundit():
    return polka.Pundit(PUNDIT_ID)


def test_book_loads_data(empty_book: polka.Book):
    assert empty_book._n_requests == 0
    empty_book.title
    empty_book.description
    empty_book.pundit
    empty_book.questions
    empty_book.sources
    empty_book.year
    assert empty_book._n_requests == 1
    empty_book.importance
    assert empty_book._n_requests == 2
    empty_book.importance
    assert empty_book._n_requests == 2


def test_book_title_attr(book: polka.Book):
    assert book.title == BOOK_TITLE


def test_book_desc_attr(book: polka.Book):
    assert isinstance(book.description, str)


def test_book_authors(book: polka.Book):
    assert book.authors == BOOK_AUTHORS


def test_book_importance_attr(book: polka.Book):
    assert isinstance(book.importance, float)
    assert book.importance == float(polka._importance()[book.id])


def test_book_pundit_attr(book: polka.Book):
    assert isinstance(book.pundit, polka.Pundit)


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


def test_pundit_loads_data(empty_pundit: polka.Pundit):
    assert empty_pundit._n_requests == 0
    empty_pundit.name
    empty_pundit.credit
    empty_pundit.description
    assert empty_pundit._n_requests == 1
    empty_pundit.wrote_about
    empty_pundit.wrote_about
    assert empty_pundit._n_requests == 2
    empty_pundit.favorites
    empty_pundit.favorites
    assert empty_pundit._n_requests == 3


def test_pundit_name_attr(pundit: polka.Pundit):
    assert isinstance(pundit.name, str)


def test_pundit_credit_attr(pundit: polka.Pundit):
    assert isinstance(pundit.credit, str)


def test_pundit_description_attr(pundit: polka.Pundit):
    assert isinstance(pundit.description, str)


def test_pundit_wrote_about_attr(pundit: polka.Pundit):
    assert isinstance(pundit.wrote_about, list)
    if pundit.wrote_about:
        assert isinstance(pundit.wrote_about[0], polka.Book)


def test_pundit_favorites_attr(pundit: polka.Pundit):
    assert isinstance(pundit.favorites, list)
    if pundit.favorites:
        assert isinstance(pundit.favorites[0], pundit.Book)
