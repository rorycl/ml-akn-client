"""
search.py

search extends summaries by adding a <snippets></snippets> element containing a List of
one or more <snippet>, an html escaped search result snippet as returned by a MarkLogic
search:search routine.

Please see summaries for documentation about the base classs.

Started by: rorycl
Date      : 21 July 2025
"""

from typing import List

from pydantic_xml import BaseXmlModel, element
from pydantic_xml.errors import BaseError
from xml.etree.ElementTree import ParseError

from .summaries import Summary, SummariesException


class SearchSummariesException(SummariesException):
    """
    SummariesSearchException extends SummariesException, reporting errors relating to
    the serialization or deserialization of SearchSummaries
    """

    pass


class Snippet(BaseXmlModel, tag="snippet"):
    """
    Snippet is an html-escaped snippet element resulting from a MarkLogic search:search
    result, escaped on the server.
    """

    snippet: str = element()


class SearchSummary(Summary, tag="summary"):
    """
    Search Summary extends Summary, adding a "snippet" element with one or more
    "snippets" of contextual information from a search across Akomo Ntosi judicial
    records.
    """

    snippets: List[Snippet] = element(tag="snippets")


class SearchSummaries(BaseXmlModel, tag="summaries"):
    """
    Summaries is a list of Summary.
    """

    summaries: List[SearchSummary] = element(tag="summary")


def search_summaries_deserialize(xml: bytes) -> SearchSummaries:
    """
    search_summaries_deserialize deserialises an xml string to a list of
    SearchSummaries.
    """
    if xml == b"":
        raise SearchSummariesException("provided xml bytes are empty")
    try:
        return SearchSummaries.from_xml(xml)
    except BaseError:
        raise SearchSummariesException(BaseError)
    except ParseError:
        raise SearchSummariesException(ParseError)
    except:
        raise
