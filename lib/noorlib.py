#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Codes specifically related to Noormags website."""

from re import compile as re_compile

from lib.commons import dict_to_sfn_cit_ref, fetch
from lib.bibtex import parse as bibtex_parse


BIBTEX_ARTICLE_ID_SEARCH = re_compile(
    r'(?<=CitationHandler\.ashx\?id=)\d+'
).search
RIS_ARTICLE_ID_SEARCH = re_compile(r'(?<=RIS&id=)\d+').search


def noorlib_sfn_cit_ref(url: str, date_format: str = '%Y-%m-%d') -> tuple:
    """Create the response namedtuple."""
    dictionary = bibtex_parse(get_bibtex(url))
    dictionary['date_format'] = date_format
    # risr = get_ris(url)[1]
    # dictionary = risr.parse(ris)[1]
    return dict_to_sfn_cit_ref(dictionary)


def get_bibtex(noorlib_url):
    """Get bibtex file content from a noormags url. Return as string."""
    pagetext = fetch(noorlib_url).text
    article_id = BIBTEX_ARTICLE_ID_SEARCH(pagetext)[0]
    url = 'http://www.noorlib.ir/View/HttpHandler/CitationHandler.ashx?id=' +\
          article_id + '&format=BibTex'
    return fetch(url).text


def get_ris(noorlib_url):
    # This is copied from noormags module (currently not supported but may
    # be)[1]
    """Get ris file content from a noormags url. Return as string."""
    pagetext = fetch(noorlib_url).text
    article_id = RIS_ARTICLE_ID_SEARCH(pagetext)[0]
    url = 'http://www.noormags.com/view/CitationHandler.ashx?format=RIS&id=' +\
          article_id
    return fetch(url).text
