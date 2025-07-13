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


def main():
    try:
        client = ml.MarkLogicHTTPClient(
            scheme="http",
            host=os.environ["ML_HOST"],
            port=int(os.environ["ML_PORT"]),
            username=os.environ["ML_USERNAME"],
            password=os.environ["ML_PASSWORD"],
        )
        part = client.summaries(sort_by="name", sort_direction="desc")
        print(part)

    except (ml.LocalMLException, KeyError) as err:
        print(f"An error occurred: {err}")
        return

    try:
        s = summaries.summaries_deserialize(part)
    except summaries.SummariesException as err:
        print(f"Deserialization error occurred: {err}")
        return

    for summary in s:
        print(summary)


if __name__ == "__main__":
    main()
