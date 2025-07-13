"""
summaries.py

A simple MarkLogic XML unmarshalling module for unmarshalling Akoma
Ntosi (AKN) legal files. summaries.py unmarshall simple summaries of AKN
files.

Started by: rorycl
Date      : 12 July 2025
"""

from datetime import date
from typing import List

from pydantic_xml import BaseXmlModel, element
from pydantic_xml.errors import BaseError
from xml.etree.ElementTree import ParseError


class SummariesException(Exception):
    """
    SummariesException wraps exceptions caused by serialization or
    deserialization of Summaries.
    """

    pass


class Summary(BaseXmlModel, tag="summary"):
    """
    Summary is a simple summary of an Akomo Ntosi judicial record.
    """

    uri: str = element()
    name: str = element()
    judgment_date: date = element(tag="judgmentDate")
    court: str = element()
    citation: str = element()


class Summaries(BaseXmlModel, tag="summaries"):
    """
    Summaries is a list of Summary.
    """

    summaries: List[Summary] = element(tag="summary")


def summaries_deserialize(xml: bytes) -> Summaries:
    """
    summaries_deserialize deserialises an xml string to a list of
    Summaries.
    """
    if xml == b"":
        raise SummariesException("provided xml bytes are empty")
    try:
        return Summaries.from_xml(xml)
    except BaseError:
        raise SummariesException(BaseError)
    except ParseError:
        raise SummariesException(ParseError)
    except:
        raise
