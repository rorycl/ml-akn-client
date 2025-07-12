# tna-fcl-client

Example API client for processing TNA Akoma Ntosi Find Case Law files.

An example Python client for a MarkLogic server utilising XQuery
server-side modules to process Akoma Ntosi format XML files used for
parliamentary, legislative and judiciary documents as implemented by
The National Archives (TNA) for the [Find Case
Law](https://caselaw.nationalarchives.gov.uk/) initiative.

## Aim

The aim of this repo is to become conversant with processing Akoma Ntosi
format files provided by the TNA's Find Case Law service using MarkLogic
and Python to provide a simple Python API client to a local database.

The exemplar API calls are intended to be:

* `get_case_summaries`
  Get case summaries for all documents in the `examples` collection of
  the `documents` database.

* `search`
  Find documents in the `examples` collection of the `documents`
  database using simple search terms.

* `get_document`
  Show a document in the `documents` database. 

A clean architecture model is used to separate data processing and the
marshalling and use of that data by Python. Data transformations are
performed server-side to minimise post-processing for performance and
re-use of code by differnt consumers.

## Database

The `src/marklogic` part of this repo sets up a MarkLogic database,
populates the "Documents" database with xml files from the Find Case Law
service and loads several Xquery `.xqy` into the MarkLogic REST server
to provide server-side functions for the above API calls.

[initial loading and summaries.xqy implemented]

Please read `src/marklogic/README.md` to setup the database, content and
server-side functions.

## Client

[still to be implemented]

The `src/tna_fcl_client/` part of this repo provides the Python API
client implemented using authenticated http GET calls and pydantic
models.

The Python code is developed using `poetry` and `ruff`.

To run the tests run `poetry run pytest`.

## Licence

Licensed under the [MIT Licence](LICENCE).

