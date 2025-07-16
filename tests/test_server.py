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
