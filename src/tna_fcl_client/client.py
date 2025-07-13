"""
client.py

A client for retrieving data from XQuery modules in a MarkLogic REST server.

Started by: rorycl
Date      : 13 July 2025

"""

from tna_fcl_client.models import summaries
from tna_fcl_client.server import marklogic as ml

# temporary code
import os


class ClientException(Exception):
    pass


class Client:
    def __init__(self):
        """
        Initialise a Client with a MarkLogic server connection configuration.
        """
        self.client = ml.MarkLogicHTTPClient(
            scheme="http",
            host=os.environ["ML_HOST"],
            port=int(os.environ["ML_PORT"]),
            username=os.environ["ML_USERNAME"],
            password=os.environ["ML_PASSWORD"],
        )

    def get_summaries(
        self, sort_by: str = "name", sort_direction: str = "desc"
    ) -> summaries.Summaries:
        """
        get_summaries retrieves AKN document summaries from the
        MarkLogic server and deserializes these into a Summeries object.
        """
        try:
            part = self.client.summaries(sort_by, sort_direction)
        except ml.LocalMLException as err:
            raise ClientException(f"Request failed: {err}") from err

        try:
            s = summaries.summaries_deserialize(part)
        except summaries.SummariesException as err:
            raise ClientException(f"Deserialisation failed: {err}") from err
        return s


if __name__ == "__main__":
    client = Client()
    s = client.get_summaries()
    for sm in s.summaries:
        print(sm)
