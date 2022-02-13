import string
import sys
from enum import Enum

import bs4
import requests
from bs4 import BeautifulSoup


class Seria(Enum):
    WITCHER = 10975
    METRO_UNIVERSUM = 18125
    METRO = 16282
    HARRY_POTTER = 143
    SONG_OF_ICE_AND_FIRE = 202


class Author(Enum):
    STEPHEN_KING = 13997
    J_K_ROWING = 3701
    ANDRZEJ_SAPKOWSKI = 3291
    J_R_R_TOLKIEN = 3216
    GEORGE_R_R_MARTIN = 19287
    REMIGIUSZ_MROZ = 82094
    JAN_PAWEL_II = 13689
    WIESLAWA_SZYMBORSKA = 14851


def get_quotes_from_seria(seria: Seria, limit: int = sys.maxsize):
    return __get_quotes_for_url(lambda page: __get_seria_url(seria, page), limit)


def get_quotes_from_author(author: Author, limit: int = sys.maxsize):
    return __get_quotes_for_url(lambda page: __get_author_url(author, page), limit)


def __get_author_url(author: Author, page: int):
    return "https://lubimyczytac.pl/cytaty?listId=quoteListFull&authors[]=" \
           + str(author.value) + "&tab=All&phrase=&sortBy=popular&paginatorType=Standard&page=" + str(page)


def __get_seria_url(seria: Seria, page: int):
    return "https://lubimyczytac.pl/cytaty?listId=quoteListFull&serieIds[]=" \
           + str(seria.value) + "&tab=All&phrase=&sortBy=popular&paginatorType=Standard&page=" + str(page)

def __get_quotes_for_url(url_getter, limit):
    res = []
    last = ['tmp']
    page = 0

    while len(last) > 0 and limit > len(res):
        last = __get_quotes_from_page(url_getter, page)
        for val in last:
            res.append(val)
        page = page + 1
    return res[:limit]



def __get_page_content(url: string):
    return requests.get(url).content


def __get_quotes_from_page(__url_getter, page: int):
    soup = BeautifulSoup(__get_page_content(__url_getter(page)), "html.parser")

    results = soup.find(id="quoteListFullPaginator")
    job_elements = results.find_all("div", class_="quotes__content")
    res = []

    for job_element in job_elements:
        text = __get_filtered_text(job_element.find("p").contents)
        author = job_element.find("a", class_="quotes__singleAuthor--author")
        book = job_element.find("a", class_="quotes__singleAuthor--book")
        res.append([text, author.contents[0] if author is not None else None, book.contents[0] if book is not None else None])
    return res


def __get_filtered_text(values: list):
    _filtered = filter(lambda x: type(x) is not bs4.element.Tag, values)
    _filtered = map(lambda x: x.lstrip(), _filtered)
    return '\n'.join(_filtered)
