"""A module provides access to the public polka.academy API."""
import json
import re
from typing import NamedTuple, Optional
from urllib.parse import urlencode
from urllib.request import urlopen
from html import unescape


_BASE = "https://api.polka.academy/"
_BOOKS = f"{_BASE}books?"
_POST = f"{_BASE}posts/{{post_id}}"
_SEARCH = f"{_BASE}search?"
_LISTS = f"{_BASE}compilations"
_PEOPLE = f"{_BASE}people?"
_PEOPLE_POST = f"{_BASE}people/{{post_id}}/posts"
_PEOPLE_FAVS = f"{_BASE}people/{{post_id}}/favs"


_NOTES = re.compile(r"\{([^\|]*)\s*\|\s*([^\}]*)\}")
_SOURCES = re.compile(r"\[([^\|]*)\s*\|\s*(\d+)\s*\|([^\]]*)\]")
_HTMLTAG = re.compile(r"<\s*[^>]*>")


def _get(url, **params):
    response = urlopen(url + urlencode(params))
    response = response.read().decode("utf-8")
    return json.loads(response)


def _clean_text(text):
    text = re.sub(_HTMLTAG, "", text)
    text = unescape(text)
    text = text.replace("\xa0", " ")
    return text


def _importance():
    return {b["id"]: b["importance"] for b in rawbooks()}


def rawbooks(sort_column="rating", sort_direction="desc"):
    params = {"sort_column": sort_column, "sort_direction": sort_direction}
    return _get(_BOOKS, **params)["books"]


def rawbook(book_id):
    return _get(_POST.format(post_id=book_id))


def rawsearch(query):
    return _get(_SEARCH, **{"q": query})


def rawlists():
    return _get(_LISTS)["compilations"]


def rawpundits(type_="all"):
    # type = "all" or "authors" or "experts"
    return _get(_PEOPLE, **{"type": type_})["people"]


def rawpunditposts(pundit_id):
    return _get(_PEOPLE_POST.format(post_id=pundit_id))["books"]


def rawpunditfavs(pundit_id):
    return _get(_PEOPLE_FAVS.format(post_id=pundit_id))["books"]


def books(sort_column="rating", sort_direction="desc"):
    """Returns a list of `Book` instances that has an article.
    Valid values for `sort_column` are "rating" (default), "year",
    "title" and "authors". Valid values for `sort_direction` are
    "desc" (default) and "asc"."""
    books = []
    for data in rawbooks(sort_column, sort_direction):
        books.append(Book(data["id"], rawdata=data))
    return books


def pundits(type_="all"):
    """Returns a list of `Pundit` instances. Valid values for
    `type_` are "all" (default), "authors" and "experts"."""
    pundits = []
    for data in rawpundits(type_):
        pundits.append(Pundit(data["id"], rawdata=data))
    return pundits


class Book:
    """Represents a book."""

    _importance = {}

    def __init__(self, id: Optional[int], *, rawdata: dict = {}):
        self.id = id
        self.rawdata = rawdata
        self._n_requests = 0

    def _getdata(self, key):
        if key not in self.rawdata:
            if key == "author" and "authors" in self.rawdata:
                key = "authors"
            elif key == "importance" and self.has_article:
                Book._importance = _importance()
                self._n_requests += 1
                self.rawdata.update({"importance": Book._importance[self.id]})
            elif self.has_article:
                data = rawbook(self.id)
                self.rawdata.update(data)
                self._n_requests += 1
        return self.rawdata.get(key)

    @property
    def importance(self):
        importance = self._getdata("importance")
        return float(importance) if importance is not None else None

    @property
    def title(self):
        title = self._getdata("title")
        return _clean_text(title)

    @property
    def authors(self):
        return self._getdata("author")

    @property
    def description(self):
        # TODO: add description for books that has not article. (from compilations)
        lead = self._getdata("lead")
        return _clean_text(lead) if lead is not None else lead

    @property
    def pundit(self):
        pundit = self._getdata("pundit")
        return Pundit(pundit["id"], rawdata=pundit) if pundit else pundit

    @property
    def year(self):
        start = self._getdata("date_start")
        end = self._getdata("date_end")
        return Year(start, end)

    @property
    def has_article(self):
        return self.id is not None

    @property
    def questions(self):
        """Returns a list of `Question` instances (just named
        tuples). Each item has `question`, `answer`  and
        `answer_with_notes` attributes.
        """
        questions = []
        for block in self._getdata("blocks"):
            if block["type"] != "question_template":
                continue
            question = _clean_text(block["question"].strip())
            answer_with_notes = _clean_text(block["html"].strip())
            answer = re.sub(_NOTES, r"\1", answer_with_notes)
            answer = re.sub(_SOURCES, r"\1", answer)
            questions.append(Question(question, answer, answer_with_notes))
        return questions

    @property
    def sources(self):
        sources = self._getdata("list")
        return [s["title"] for s in sources] if sources else sources

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            f"(title={self.title!r}, authors={self.authors!r})"
        )

    def __eq__(self, other):
        if other.__class__ is self.__class__:
            return (self.id, self.title) == (other.id, other.title)
        return NotImplemented

    def __lt__(self, other):
        if other.__class__ is self.__class__:
            return self.importance < other.importance
        return NotImplemented

    def __hash__(self):
        return hash((self.id, self.title))


class Pundit:
    "Represents an expert."

    def __init__(self, id: int, *, rawdata: dict = {}):
        self.id = id
        self.rawdata = rawdata
        self._n_requests = 0

    def _getdata(self, key):
        if key not in self.rawdata:
            if key == "posts":
                self.rawdata.update({"posts": rawpunditposts(self.id)})
            elif key == "favs":
                self.rawdata.update({"favs": rawpunditfavs(self.id)})
            else:
                data = [p for p in rawpundits() if p["id"] == self.id][0]
                self.rawdata.update(data)
            self._n_requests += 1
        return self.rawdata.get(key)

    @property
    def name(self):
        return f"{self._getdata('first')} {self._getdata('last')}"

    @property
    def credit(self):
        return _clean_text(self._getdata("credit"))

    @property
    def description(self):
        return _clean_text(self._getdata("description"))

    @property
    def wrote_about(self):
        posts = self._getdata("posts")
        return [Book(d["id"], rawdata=d) for d in posts] if posts else []

    @property
    def favorites(self):
        favs = self._getdata("favs")
        return [Book(d["id"], rawdata=d) for d in favs] if favs else []

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r})"

    def __eq__(self, other):
        if other.__class__ is self.__class__:
            return (self.id, self.name) == (other.id, other.name)
        return NotImplemented

    def __hash__(self):
        return hash((self.id, self.name))


class Compilation:
    pass


class Year(NamedTuple):
    start: Optional[int]
    end: Optional[int]


class Question(NamedTuple):
    question: str
    answer: str
    answer_with_notes: str
