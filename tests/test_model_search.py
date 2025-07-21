"""
Test the summaries.SearchSummaries xml deserializer
"""

import pytest
from ml_akn_client.models import search

SEARCH_XML = b"""<?xml version="1.0"?>
<summaries>
  <summary>
    <uri>/documents/ewca_civ_2005_312.xml</uri>
    <name>NCR Ltd v Riverland Portfolio No1 Ltd</name>
    <judgmentDate>2005-03-21</judgmentDate>
    <court>EWCA-Civil</court>
    <citation>[2005] EWCA Civ 312</citation>
    <snippets>
      <snippet>&lt;span class="highlight"&gt;Norwich&lt;/span&gt; Union Life Insurance Society v Shockmore&lt;span class="highlight"&gt;Norwich&lt;/span&gt; Union&lt;span class="highlight"&gt;Norwich&lt;/span&gt; Union</snippet>
    </snippets>
  </summary>
  <summary>
    <uri>/documents/ewhc_ch_2004_324.xml</uri>
    <name>Design Progression Ltd v Thurloe Properties Ltd</name>
    <judgmentDate>2004-02-25</judgmentDate>
    <court>EWHC-Chancery</court>
    <citation>[2004] EWHC 324 (Ch)</citation>
    <snippets>
      <snippet>&lt;span class="highlight"&gt;Norwich&lt;/span&gt; Union Life Insurance Society v Shipmoor LtdAs Sir Richard Scott V.C. pertinently commented in the &lt;span class="highlight"&gt;Norwich&lt;/span&gt; Union case </snippet>
    </snippets>
  </summary>
</summaries>
"""


def test_search_empty():
    """
    Test to ensure search raises a SummariesException when fed
    empty xml.
    """
    with pytest.raises(search.SearchSummariesException):
        search.search_summaries_deserialize(b"")

    # also check this raises the base Summaries Exception
    with pytest.raises(search.SummariesException):
        search.search_summaries_deserialize(b"")


def test_search_invalid():
    """
    Test to ensure search raises a SummariesException when fed incorrect xml. This test
    replaces the court element which should raise a core pydantic ValidationError.
    """
    broken_summaries = SEARCH_XML.replace(b"court", b"playground")
    with pytest.raises(search.SummariesException):
        search.search_summaries_deserialize(broken_summaries)


def test_search_ok():
    """
    Test if SEARCH_XML can be deserialized into a list of two
    decorated Summary within a SearchSummary.
    """
    s = search.search_summaries_deserialize(SEARCH_XML)
    assert len(s.summaries) == 2
    assert (
        "Union Life Insurance Society v Shockmore" in s.summaries[0].snippets[0].snippet
    )
