"""
Test the MarkLogic (ML/ml) server core functions
"""

import pytest
from tna_fcl_client.server import marklogic as ml
from requests.auth import HTTPDigestAuth
import secrets


@pytest.fixture
def random_password():
    """
    Provides a random string to be used as a password.
    """
    return secrets.token_urlsafe(10)


# -- initialization testing --#


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


# -- multipart testing --#


@pytest.fixture
def valid_multipart_response():
    """
    Provides a tuple of (content_bytes, content_type_header).
    """
    boundary = "some-reader-boundary"
    content_type = f"multipart/mixed; boundary={boundary}"
    body = (
        f"--{boundary}\r\n"
        "Content-Type: application/xml\r\n"
        "\r\n"
        "<result>splendid</result>\r\n"
        f"--{boundary}--\r\n"
    ).encode("utf-8")
    return (body, content_type)


def test_decode_multipart_success(random_password, valid_multipart_response):
    """
    Tests decoding a valid multipart body
    """
    client = ml.MarkLogicHTTPClient(username="admin", password=random_password)
    data, content_type = valid_multipart_response
    result = client.decode_multipart(data=data, content_type=content_type)
    assert result == b"<result>splendid</result>"


@pytest.mark.parametrize(
    "test_data, content_type, offset, expected_exception, error_msg",
    [
        (
            b"--boundary\r\n\r\npart1\r\n--boundary--",
            "multipart/mixed; boundary=boundary",
            1,
            ml.LocalContentException,
            "no part 1 found",
        ),
        (
            b"not a multipart body",
            "multipart/mixed; boundary=boundary",
            0,
            ml.LocalContentException,
            "Decoding failed",
        ),
        (
            b"",
            "any",
            0,
            None,
            "empty data should return empty bytes",
        ),  # Special case
    ],
    ids=["offset too high", "malformed data", "empty data"],
)
def test_decode_multipart_failure(
    random_password, test_data, content_type, offset, expected_exception, error_msg
):
    """
    Tests multipart decoding failure modes and edge cases.
    """
    client = ml.MarkLogicHTTPClient(username="admin", password=random_password)
    if expected_exception:
        with pytest.raises(expected_exception) as err:
            client.decode_multipart(
                data=test_data, content_type=content_type, offset=offset
            )
        assert error_msg in str(err.value)
    else:
        # Handling the non-exception case which returns empty bytes
        result = client.decode_multipart(
            data=test_data, content_type=content_type, offset=offset
        )
        assert result == b""


# -- post testing --#


"""
For information about how to use requests-mock, please see the docs at
https://requests-mock.readthedocs.io/en/latest/
The code below uses the `mock.[METHOD]` approach -- see 
https://requests-mock.readthedocs.io/en/latest/response.html.
"""


def test_post_to_module_success(
    requests_mock, random_password, valid_multipart_response
):
    """
    Tests a mocked POST to a MarkLogic module that should return success.
    """
    client = ml.MarkLogicHTTPClient(username="admin", password=random_password)
    response_body, content_type = valid_multipart_response

    # setup mock response
    requests_mock.post(
        "http://localhost:8000/LATEST/invoke",
        content=response_body,
        status_code=200,
        headers={"Content-Type": content_type},
    )

    # do mocked post
    result = client._post_to_module(
        module_endpoint="test.xqy", vars={"status": "prettygood"}
    )
    history = requests_mock.request_history

    # check result and history
    assert result == b"<result>splendid</result>"
    assert len(history) == 1
    assert history[0].method == "POST"
    assert "test.xqy" in history[0].text
    assert "prettygood" in history[0].text


def test_post_to_module_error(requests_mock, random_password, valid_multipart_response):
    """
    Tests a mocked POST to a MarkLogic module that returns a 500 error.
    """
    client = ml.MarkLogicHTTPClient(username="admin", password=random_password)

    # setup mock response for a 500 error
    requests_mock.post(
        "http://localhost:8000/LATEST/invoke",
        status_code=500,
        reason="Internal Server Error",
    )
    with pytest.raises(
        ml.LocalMLException,
        match="Internal Server Error for url: http://localhost:8000/LATEST/invoke",
    ):
        client._post_to_module(module_endpoint="test.xqy", vars={})
