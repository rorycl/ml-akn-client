"""
A client for retrieving Akoma Ntoso format data from a MarkLogic REST server.

This module provides a high-level client called "CaseLawClient" for interacting with a
MarkLogic (ML/ml) database to retrieve data from Akoma Ntoso (AKN) judicial records
files. These files follow those used by the UK's The National Archives (TNA) Find Case
Law (FCL) initiative.

This project provides a means for exploring AKN file server-side processing using XQuery
and XSLT with no XML processing or escaping on the client. This client encapsulates the
details of interaction with an ML database exposed over REST and the related data
deserialization into Pydantic models.

Example Usage:
    import os
    from ml_akn_client.server import marklogic as ml
    from ml_akn_client.client import caselawclient as cl

    # configure the underlying HTTP client with connection details.
    http_client = ml.MarkLogicHTTPClient(
        host=os.environ.get("ML_HOST", "localhost"),
        port=int(os.environ.get("ML_PORT", "8000")),
        username=os.environ["ML_USERNAME"],
        password=os.environ["ML_PASSWORD"],
    )

    # inject the HTTP client into the CaseLawClient.
    client = cl.CaseLawClient(http_client)

    # call a method to retrieve and parse data.
    try:
        summaries_data = client.get_summaries(sort_by="date")
    except cl.ClientException as e:
        print(f"An error occurred: {e}")
    for summary in summaries_data.summaries:
        print(f"{summary.judgment_date}: {summary.name}")

    # search
    try:
        search_data = client.search(query="Scott")
    except cl.ClientException as e:
        print(f"An error occurred: {e}")
    for summary in search_data.summaries:
        print(f"{summary.judgment_date}: {summary.name}")
        for snippet := range summary.snippets:
        print(f"   {snippet.snippet}")

"""

# Started by: rorycl
# Date      : 13 July 2025

from ml_akn_client.models import summaries
from ml_akn_client.models import search
from ml_akn_client.server import marklogic as ml


class ClientException(Exception):
    """
    Base exception for all client-side errors in this module.

    This exception wraps lower-level errors (for example errors from the
    server connection or data parsing) to provide a simple error-handling API
    for the user.

    To inspect the original cause of the error, check the `__cause__`
    attribute.

    Example:
        try:
            s = client.get_summaries()
        except ClientException as e:
            print(f"A client operation failed: {e}")
            if e.__cause__:
                print(f"  Original cause: {e.__cause__}")
    """

    pass


class CaseLawClient:
    """
    A client for retrieving case law data from a MarkLogic server.

    This class provides methods to query specific XQuery modules on the server
    and parse the XML responses into structured Pydantic models. It relies on
    an injected MarkLogicHTTPClient instance for all server communication,
    following a dependency injection pattern.
    """

    def __init__(self, http_client: ml.MarkLogicHTTPClient):
        """
        Initialize the CaseLawClient.

        Args:
            http_client: An initialized and configured MarkLogicHTTPClient
                         instance responsible for handling HTTP communication
                         and authentication with the MarkLogic server.
        """
        self.ml_client = http_client

    def get_summaries(
        self,
        sort_by: ml.MarkLogicHTTPClient.summaries_sort_by = "name",
        sort_direction: ml.MarkLogicHTTPClient.summaries_order_by = "desc",
    ) -> summaries.Summaries:
        """
        Retrieve a list of document summaries from the database.

        get_summaries calls the 'summaries.xqy' module on the MarkLogic server,
        requesting a list of Akoma Ntoso document summaries. The results are
        sorted according to the provided parameters. The raw XML response is
        then deserialized into a `summaries.Summaries` Pydantic object.

        Args:
            sort_by: The field to sort the summaries by.
                     Must be one of "name", "date", "court", or "citation".
                     Defaults to "name".
            sort_direction: The direction of the sort.
                            Must be either "desc" or "asc".
                            Defaults to "desc".

        Returns:
            A `summaries.Summaries` object containing a list of `Summary`
            objects.

        Raises:
            ClientException: If the server request fails, the connection
                             times out, or if the returned XML data cannot be
                             deserialized into the expected format.
        """
        try:
            part = self.ml_client.summaries(sort_by, sort_direction)
        except ml.LocalMLException as err:
            raise ClientException(
                f"Failed to retrieve summaries from server: {err}"
            ) from err

        try:
            s = summaries.summaries_deserialize(part)
        except summaries.SummariesException as err:
            raise ClientException(f"Failed to deserialize summary data: {err}") from err
        return s

    def search(
        self,
        query: str,
        sort_by: ml.MarkLogicHTTPClient.summaries_sort_by = "name",
        sort_direction: ml.MarkLogicHTTPClient.summaries_order_by = "desc",
    ) -> search.SearchSummaries:
        """
        Search for documents containing a term, returning document summaries and snippets.

        search calls the `search.xqy` module on the MarkLogic server, requesting those
        Akoma Ntoso documents which match the search term provided. The result summaries
        include search "snippets" from the matching documents. Results are sorted
        according to the provided parameters as for the `get_summaries` method. The raw
        XML response is deserialized into a `summaries.SearchSummaries` Pydantic object.

        Args:
            query: The search term to use.
            sort_by: The field to sort the summaries by.
                     Must be one of "name", "date", "court", or "citation".
                     Defaults to "name".
            sort_direction: The direction of the sort.
                            Must be either "desc" or "asc".
                            Defaults to "desc".

        Returns:
            A `summaries.SearchSummaries` object containing a list of `Summary` objects
            decorated with search result snippets as returned from the MarkLogic
            `search:search` function.

        Raises:
            ClientException: If the server request fails, the connection
                             times out, or if the returned XML data cannot be
                             deserialized into the expected format.

        """
        try:
            part = self.ml_client.search(query, sort_by, sort_direction)
        except ml.LocalMLException as err:
            raise ClientException(
                f"Failed to retrieve search results from server: {err}"
            ) from err

        try:
            s = search.search_summaries_deserialize(part)
        except summaries.SummariesException as err:  # generic class error
            raise ClientException(f"Failed to deserialize search data: {err}") from err
        print(s)
        return s


# Code for simple demonstrations and ad-hoc testing.
if __name__ == "__main__":
    import os

    try:
        http_client = ml.MarkLogicHTTPClient(
            scheme="http",
            host=os.environ["ML_HOST"],
            port=int(os.environ["ML_PORT"]),
            username=os.environ["ML_USERNAME"],
            password=os.environ["ML_PASSWORD"],
        )
    except KeyError as e:
        print(
            f"Error: Environment variable {e} not set. Please set ML_HOST, ML_PORT, etc."
        )
    except ml.MisconfigurationException as e:
        print(f"HTTP client misconfiguration: {e}")

    # init client
    client = CaseLawClient(http_client)

    # get_summaries
    print("Fetching summaries sorted by name (descending)...")
    try:
        summaries_data = client.get_summaries(sort_by="name", sort_direction="desc")
    except ClientException as e:
        print(f"An error occurred during client operation: {e}")

    if summaries_data.summaries:
        for sm in summaries_data.summaries:
            print(f"  - {sm.citation}: {sm.name}")
    else:
        print("No summaries found.")

    # search
    print("Searching for records with the name 'Scott'...")
    try:
        search_data = client.search(
            query="Scott", sort_by="name", sort_direction="desc"
        )
    except ClientException as e:
        print(f"An error occurred during client operation: {e}")

    if search_data.summaries:
        for sm in search_data.summaries:
            print(f"  - {sm.citation}: {sm.name}")
            for snippet in sm.snippets:
                print(f"    snippet: {snippet.snippet}")
    else:
        print("No search results found.")
