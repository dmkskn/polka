import pytest

import polka


BOOK_ID = 523
BOOK_TITLE = "Герой нашего времени"
BOOK_AUTHORS = ["Михаил Лермонтов"]
PUNDIT_ID = 312
COMPILATION_ID = 85
PODCAST_ID = 654
BLOG_ID = 659


@pytest.fixture(scope="module")
def book():
    book = polka.Book(BOOK_ID)
    book.rawdata.update(polka.rawbook(BOOK_ID))
    polka.Book._importance = polka._importance()
    return book


@pytest.fixture
def empty_book():
    return polka.Book(BOOK_ID)


@pytest.fixture
def book_without_article():
    return [book for book in polka.books() if not book.has_article][0]


@pytest.fixture(scope="module")
def pundit():
    pundit = polka.Pundit(PUNDIT_ID)
    pundits = polka.rawpundits()["people"]
    pundit.rawdata.update([p for p in pundits if p["id"] == PUNDIT_ID][0])
    pundit.rawdata.update({"posts": polka.rawpunditposts(PUNDIT_ID)["books"]})
    pundit.rawdata.update({"favs": polka.rawpunditfavs(PUNDIT_ID)["books"]})
    return pundit


@pytest.fixture
def empty_pundit():
    return polka.Pundit(PUNDIT_ID)


@pytest.fixture(scope="module")
def compilation():
    comp = polka.Compilation(COMPILATION_ID)
    comps = polka.rawlists()["compilations"]
    comp.rawdata.update([c for c in comps if c["id"] == COMPILATION_ID][0])
    comp.rawdata.update(polka.rawlist(COMPILATION_ID))
    return comp


@pytest.fixture
def empty_list():
    return polka.Compilation(COMPILATION_ID)


@pytest.fixture(scope="module")
def podcast():
    podcast = polka.Podcast(PODCAST_ID)
    podcasts = polka.rawpodcasts()["items"]
    podcast.rawdata.update([p for p in podcasts if p["id"] == PODCAST_ID][0])
    podcast.rawdata.update(polka.rawpodcast(PODCAST_ID))
    return podcast


@pytest.fixture
def empty_podcast():
    return polka.Podcast(PODCAST_ID)


@pytest.fixture(scope="module")
def blog():
    blog = polka.Blog(BLOG_ID)
    blogs = polka.rawblogs()["items"]
    blog.rawdata.update([b for b in blogs if b["id"] == BLOG_ID][0])
    blog.rawdata.update(polka.rawblog(BLOG_ID))
    return blog


@pytest.fixture
def empty_blog():
    return polka.Blog(BLOG_ID)


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


def test_book_url_attr(book: polka.Book):
    assert book.url == f"https://polka.academy/articles/{book.id}"


def test_book_url_attr_if_it_has_not_article(book_without_article: polka.Book):
    assert book_without_article.url is None


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


def test_book_questions_attr(book: polka.Book):
    assert isinstance(book.questions, list)
    if book.questions:
        for item in book.questions:
            assert isinstance(item, polka.Question)
            assert isinstance(item.question, str)
            assert isinstance(item.answer, str)
            assert isinstance(item.answer_with_notes, str)


def test_book_questions_attr_if_it_has_not_article(book_without_article):
    assert book_without_article.questions is None


def test_book_pundit_attr_if_it_has_not_article(book_without_article):
    assert book_without_article.pundit is None


def test_book_sources_attr_if_it_has_not_article(book_without_article):
    assert book_without_article.sources is None


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


def test_pundit_url_attr(pundit: polka.Pundit):
    assert pundit.url == f"https://polka.academy/experts/{pundit.id}"


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


def test_compilation_loads_data(empty_list: polka.Compilation):
    assert empty_list._n_requests == 0
    empty_list.title
    empty_list.description
    empty_list.books
    assert empty_list._n_requests == 1
    empty_list.short_description
    empty_list.max_year
    empty_list.min_year
    assert empty_list._n_requests == 2


def test_compilation_url_attr(compilation: polka.Compilation):
    assert compilation.url == f"https://polka.academy/lists/{compilation.id}"


def test_compilation_title_attr(compilation: polka.Compilation):
    assert isinstance(compilation.title, str)


def test_compilation_description_attr(compilation: polka.Compilation):
    assert isinstance(compilation.description, str)


def test_compilation_short_description_attr(compilation: polka.Compilation):
    assert isinstance(compilation.short_description, str)


def test_compilation_max_year_attr(compilation: polka.Compilation):
    assert isinstance(compilation.max_year, int)


def test_compilation_min_year_attr(compilation: polka.Compilation):
    assert isinstance(compilation.min_year, int)


def test_compilation_books_attr(compilation: polka.Compilation):
    assert isinstance(compilation.books, list)
    assert isinstance(compilation.books[0], polka.Book)


def test_podcast_loads_data(empty_podcast: polka.Podcast):
    assert empty_podcast._n_requests == 0
    empty_podcast.short_description
    assert empty_podcast._n_requests == 1
    empty_podcast.lead
    assert empty_podcast._n_requests == 2


def test_podcast_url_attr(podcast: polka.Podcast):
    assert podcast.url == f"https://polka.academy/materials/{podcast.id}"


def test_podcast_title_attr(podcast: polka.Podcast):
    assert isinstance(podcast.title, str)


def test_podcast_short_description_attr(podcast: polka.Podcast):
    assert isinstance(podcast.short_description, str)


def test_podcast_lead_attr(podcast: polka.Podcast):
    assert isinstance(podcast.lead, str)


def test_blog_loads_data(empty_blog: polka.Blog):
    assert empty_blog._n_requests == 0
    empty_blog.short_description
    assert empty_blog._n_requests == 1
    empty_blog.lead
    assert empty_blog._n_requests == 2


def test_blog_url_attr(blog: polka.Blog):
    assert blog.url == f"https://polka.academy/materials/{blog.id}"


def test_blog_title_attr(blog: polka.Blog):
    assert isinstance(blog.title, str)


def test_blog_short_description_attr(blog: polka.Blog):
    assert isinstance(blog.short_description, str)


def test_blog_lead_attr(blog: polka.Blog):
    assert isinstance(blog.lead, str)
