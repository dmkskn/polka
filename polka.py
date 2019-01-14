"""модуль для доступа к API проекта «Полка»."""
from __future__ import annotations

import json
import re
from typing import List, NamedTuple, Optional
from urllib.parse import quote, urlencode
from urllib.request import urlopen


_BASE = "https://api.polka.academy/"
_BOOKS = f"{_BASE}books?"
_POST = f"{_BASE}posts/{{post_id}}"
_SEARCH = f"{_BASE}search?"
_LISTS = f"{_BASE}compilations"
_PEOPLE = f"{_BASE}people?"


def _get(url, **params):
    response = urlopen(url + urlencode(params))
    response = response.read().decode("utf-8")
    response = response.replace("\xa0", " ")
    return json.loads(response)


def rawbooks(sort_column="rating", sort_direction="desc"):
    # sort_column = "rating" or "year" or "title" or "authors"
    # sort_direction = "desc" or "asc"
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


class Book:
    pass


class Expert:
    pass


class Compilation:
    pass
