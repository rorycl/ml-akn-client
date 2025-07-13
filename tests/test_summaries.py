"""
Test the summaries.Summaries xml deserializer
"""

from tna_fcl_client.models import summaries

summaries_xml = r"""<?xml version="1.0"?>
<summaries>
  <summary>
    <uri>/documents/ewca_civ_2018_2414.xml</uri>
    <name>Barrow &amp; Anoe v Kazim &amp; Ors</name>
    <judgmentDate>2018-10-31</judgmentDate>
    <court>EWCA-Civil</court>
    <citation>[2018] EWCA Civ 2414</citation>
  </summary>
  <summary>
    <uri>/documents/ewhc_qb_2020_1353.xml</uri>
    <name>Croydon London Borough Council v Kalonga</name>
    <judgmentDate>2020-06-02</judgmentDate>
    <court>EWHC-QBD</court>
    <citation>[2020] EWHC 1353 (QB)</citation>
  </summary>
</summaries>
"""


def test_summaries():
    s = summaries.summaries_deserialize(summaries_xml)
    assert len(s.summaries) == 2
    assert s.summaries[0].citation == "[2018] EWCA Civ 2414"
