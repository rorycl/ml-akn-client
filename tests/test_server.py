"""
Test the MarkLogic (ML/ml) server core functions
"""

import pytest
from tna_fcl_client.server import marklogic as ml
from requests.auth import HTTPDigestAuth
import secrets


@pytest.fixture
def random_password():
    return secrets.token_urlsafe(10)


# inputs to test_marklogic_http_client_init_failures
@pytest.mark.parametrize(
    "test_name, client_kwargs, expected_exception",
    [
        (
            "default client no args",
            {},
            ml.MisconfigurationException,
        ),
        (
            "port too low",
            {"port": 79},
            ml.MisconfigurationException,
        ),
        (
            "username same as password",
            {"username": "usamep", "password": "usamep"},
            ml.MisconfigurationException,
        ),
        (
            "empty username",
            {"username": ""},
            ml.MisconfigurationException,
        ),
    ],
)
def test_marklogic_http_client_init_failures(
    test_name, client_kwargs, expected_exception
):
    """
    Test initialisation fail suitably for MarkLogicHTTPClient.
    """
    with pytest.raises(expected_exception):
        ml.MarkLogicHTTPClient(**client_kwargs)


def test_marklogic_http_client_init_success(random_password):
    """
    Test initialisation success for MarkLogicHTTPClient.
    """
    client = ml.MarkLogicHTTPClient(username="admin", password=random_password)
    assert client.hostpath == "http://localhost:8000"
    assert isinstance(client.auth, HTTPDigestAuth)


def test_marklogic_decode_multipart():
    """
    Tests to check that the ml client can decode multipart content ok.
    Note that the requests_toolbelt multipart decoder here:
        https://github.com/requests/toolbelt/blob/master/requests_toolbelt/multipart/decoder.py
    is used. The tests are here:
        https://github.com/requests/toolbelt/blob/master/tests/test_multipart_decoder.py
    Note that multipart data uses CRLF line endings.
    """
    data = str.encode(r"""
--dac511ebedeba9ed
Content-Type: application/xml
X-Primitive: element()
X-Path: /summaries

<summaries><summary><uri>/documents/ewca_civ_2014_885.xml</uri><name>Youssefi v Mussellwhite</name><judgmentDate>2014-07-02</judgmentDate><court>EWCA-Civil</court><citation>[2014] EWCA Civ 885</citation></summary><summary><uri>/documents/ewca_civ_2003_1759.xml</uri><name>Tiffany Investments Ltd. &amp; Anor v Bircham &amp; Co Nominees (No 2) Ltd. &amp; Ors</name><judgmentDate>2003-12-04</judgmentDate><court>EWCA-Civil</court><citation>[2003] EWCA Civ 1759</citation></summary><summary><uri>/documents/ewhc_ch_2025_16.xml</uri><name>SBP 2 S.À.R.L v 2 SOUTHBANK TENANT LIMITED</name><judgmentDate>2025-01-07</judgmentDate><court>EWHC-Chancery</court><citation>[2025] EWHC 16 (Ch)</citation></summary><summary><uri>/documents/ewca_civ_2005_312.xml</uri><name>NCR Ltd v Riverland Portfolio No1 Ltd</name><judgmentDate>2005-03-21</judgmentDate><court>EWCA-Civil</court><citation>[2005] EWCA Civ 312</citation></summary><summary><uri>/documents/ewca_civ_2004_184.xml</uri><name>Lay &amp; Ors v Ackerman &amp; Anor</name><judgmentDate>2004-03-04</judgmentDate><court>EWCA-Civil</court><citation>[2004] EWCA Civ 184</citation></summary><summary><uri>/documents/ewhc_ch_2008_1582.xml</uri><name>Landlord Protect Ltd. v St Anselm Development Company Ltd.</name><judgmentDate>2008-07-08</judgmentDate><court>EWHC-Chancery</court><citation>[2008] EWHC 1582 (Ch)</citation></summary><summary><uri>/documents/ewca_civ_2009_99</uri><name>Landlord Protect Ltd v St Anselm Development Company Ltd</name><judgmentDate>2009-02-20</judgmentDate><court>EWCA-Civil</court><citation>[2009] EWCA Civ 99</citation></summary><summary><uri>/documents/ewca_civ_2009_99.xml</uri><name>Landlord Protect Ltd v St Anselm Development Company Ltd</name><judgmentDate>2009-02-20</judgmentDate><court>EWCA-Civil</court><citation>[2009] EWCA Civ 99</citation></summary><summary><uri>/documents/ewhc_ch_2004_324.xml</uri><name>Design Progression Ltd v Thurloe Properties Ltd</name><judgmentDate>2004-02-25</judgmentDate><court>EWHC-Chancery</court><citation>[2004] EWHC 324 (Ch)</citation></summary><summary><uri>/documents/ewhc_qb_2020_1353.xml</uri><name>Croydon London Borough Council v Kalonga</name><judgmentDate>2020-06-02</judgmentDate><court>EWHC-QBD</court><citation>[2020] EWHC 1353 (QB)</citation></summary><summary><uri>/documents/ewca_civ_2018_2414.xml</uri><name>Barrow &amp; Anoe v Kazim &amp; Ors</name><judgmentDate>2018-10-31</judgmentDate><court>EWCA-Civil</court><citation>[2018] EWCA Civ 2414</citation></summary></summaries>
--dac511ebedeba9ed--
""").replace(b"\n", b"\r\n")

    client = ml.MarkLogicHTTPClient(username="admin", password=random_password)
    client.decode_multipart(
        data=data, content_type="multipart/mixed; boundary=dac511ebedeba9ed", offset=0
    )

    with pytest.raises(ml.LocalContentException):
        client.decode_multipart(
            data=data,
            content_type="multipart/mixed; boundary=dac511ebedeba9ed",
            offset=1,
        )

    with pytest.raises(ml.LocalContentException):
        client.decode_multipart(
            data=b"xyz",
            content_type="multipart/mixed; boundary=dac511ebedeba9ed",
            offset=0,
        )
