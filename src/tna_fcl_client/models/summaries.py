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


class Summary(BaseXmlModel, tag="summary"):
    """
    Summary is a simple summary of an Akomo Ntosi judicial record
    """

    uri: str = element()
    name: str = element()
    judgment_date: date = element(tag="judgmentDate")
    court: str = element()
    citation: str = element()


class Summaries(BaseXmlModel, tag="summaries"):
    """
    Summaries is a list of Summary
    """

    summaries: List[Summary] = element(tag="summary")


def summaries_deserialize(xml: str) -> Summaries:
    """
    summaries_deserialize deserialises an xml string to a list of
    Summaries.
    """
    return Summaries.from_xml(xml)
