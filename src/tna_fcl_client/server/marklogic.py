"""
marklogic.py

A class for interacting with a MarkLogic REST server over HTTP.

Started by: rorycl
Date      : 13 July 2025
"""

import requests
from requests import RequestException, HTTPError
from requests.auth import HTTPDigestAuth

# needed for marklogic multipart responses
from requests_toolbelt.multipart import decoder, ImproperBodyPartContentException

# needed for creating post content
from json import dumps
from urllib.parse import urljoin

from typing import Literal, ClassVar

# MarkLogic fixed paths and timeout
ML_MODULE_INVOCATION_PATH: str = "/LATEST/invoke"
ML_MODULE_INTERNAL_PATH: str = "/ext/"
ML_SERVER_TIMEOUT: int = 3  # 3 seconds


class LocalMLException(Exception):
    """
    LocalMLException is the base exception for any exception in this
    module.
    """

    pass


class LocalContentException(LocalMLException):
    """
    LocalContentException reports a content error in a MarkLogic server
    response.
    """

    pass


class MisconfigurationException(LocalMLException):
    """
    A MisconfigurationException reports misconfiguration.
    """

    pass


class MarkLogicHTTPClient:
    """
    MarkLogicHTTPClient is a class for interacting with a MarkLogic HTTP
    server.

    The connection is always used making digest authentication.
    """

    hostpath: str  # the basepath to the server host
    auth: HTTPDigestAuth  # the digest authentication string

    # summaries: permitted values
    summaries_sort_by = Literal["name", "date", "court", "citation"]
    summaries_order_by = Literal["desc", "asc"]

    def __init__(
        self,
        scheme: str = "http",
        host: str = "localhost",
        port: int = 8000,
        username: str = "",
        password: str = "",
    ):
        # checks
        if (host == "localhost" or host == "127.0.0.1") and scheme != "http":
            raise MisconfigurationException("http only used for local connections")
        if host == "" or port < 80:
            raise MisconfigurationException("empty host or low port received")
        if username == "" or password == "":
            raise MisconfigurationException(
                "empty usernames and passwords not accepted"
            )
        if username == password:
            raise MisconfigurationException("https://xkcd.com/792/ reuse exception")

        # define instance variables
        self.hostpath = f"{scheme}://{host}:{port}"
        self.auth = HTTPDigestAuth(username, password)

    def _post_to_module(self, module_endpoint: str, vars: dict[str, str]) -> bytes:
        """
        _post_to_module is a local method for making a POST request to a
        MarkLogic module, for example an XQuery endpoint.

        @module_endpoint: typically the name of an xqy query, such as
        "summaries.xqy".
        @vars: typically the vars (if any) to provide to the module for
        processing on the server.

        This supports the equivalent of the following curl command:
        ```
        curl --digest --user user:pass -X POST \
             -H "Content-type: application/x-www-form-urlencoded" \
             --data-urlencode module=/ext/endpoint.xqy \
             --data-urlencode vars='{"key": "value"}' \
             http://host:port/LATEST/invoke
        ```
        """
        if module_endpoint == "":
            raise MisconfigurationException("empty module_endpoint provided")

        # the form data for the POST request body.
        payload = {
            "module": urljoin(ML_MODULE_INTERNAL_PATH, module_endpoint),
            "vars": dumps(vars),  # The 'vars' value itself is a JSON string
        }

        module_url = urljoin(self.hostpath, ML_MODULE_INVOCATION_PATH)
        try:
            r = requests.post(
                module_url,
                auth=self.auth,
                data=payload,
                headers={"Accept": "application/xml"},
                timeout=ML_SERVER_TIMEOUT,
            )
            r.raise_for_status()
        except requests.HTTPError as e:
            raise LocalMLException(f"HTTP exception: {e}") from e
        except RequestException as e:
            raise LocalMLException(f"Request failed: {e}") from e

        first_multipart_part = self.decode_multipart(
            r.content, r.headers.get("content-type", "")
        )
        return first_multipart_part

    def decode_multipart(
        self,
        data: bytes,
        content_type: str,
        offset: int = 0,
        encoding: str = "utf-8",
    ) -> bytes:
        """
        decode_multipart decodes parts from a multipart byte sequence,
        @data: normally a request response.content
        @content_type: normally `response.headers.get('content-type', "")`
        @offset: the part number to return (normally 0)
        @encoding: utf-8 unless otherwise specified
        See https://github.com/requests/toolbelt/blob/master/requests_toolbelt/multipart/decoder.py
        """
        if not data:
            return b""
        try:
            decoded = decoder.MultipartDecoder(data, content_type)
        except ImproperBodyPartContentException as e:
            raise LocalContentException(f"Decoding failed: {e}") from e
        if not decoded.parts:
            raise LocalContentException(
                f"decoder error: no parts found to decode in {data!r}"
            )
        if offset > (len(decoded.parts) - 1):
            l = len(decoded.parts)
            raise LocalContentException(
                f"decoder error: no part {offset} found: len {l}"
            )
        return decoded.parts[offset].content  # content is bytes, text is unicode

    def summaries(
        self,
        sort_by: summaries_sort_by,
        sort_direction: summaries_order_by,
    ) -> bytes:
        """
        Summaries gets a list of summaries of documents in the database
        sorted by the sort_by field and ordered either "desc" or "asc".
        The XQuery counterpart to this is marklogic/summaries.xqy
        """
        return self._post_to_module(
            module_endpoint="summaries.xqy",
            vars={"sort_by": sort_by, "sort_direction": sort_direction},
        )
