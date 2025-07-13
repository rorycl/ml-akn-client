# tna-fcl-client

Example API client for processing TNA Akoma Ntosi *Find Case Law* files.

An example Python client for a MarkLogic server utilising XQuery
server-side modules to process Akoma Ntosi format XML files used for
parliamentary, legislative and judiciary documents as implemented by
The National Archives (TNA) for the [Find Case
Law](https://caselaw.nationalarchives.gov.uk/) initiative.

## Aim

The aim of this repo is to become conversant with processing Akoma Ntosi
format files provided by the TNA's Find Case Law service using a
MarkLogic database and Python to provide a simple Python API client to a
local database.

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
performed server-side using XQuery to minimise post-processing for
performance and re-use of code by different consumers.

## Database

The `src/marklogic` part of this repo sets up a MarkLogic database,
populates the "Documents" database with xml files from the Find Case Law
service and loads several Xquery `.xqy` into the MarkLogic REST server
to provide server-side functions to support the above API calls.

In the below todo, "ml" refers to the "MarkLogic database and server".

- [x] install and setup ml
- [x] upload example AKN files into ml
- [x] install initial summaries `.xqy` query into ml
- [x] register initial summaries `.xqy` query as an ml endpoint
- [ ] install and register "get document" query and endpoint
- [ ] install and register "search" query and endpoint
- [ ] automate all of the above

Please read `src/marklogic/README.md` to setup the database, content and
server-side functions.

## Client

The `src/tna_fcl_client/` part of this repo provides the Python API
client implemented using authenticated http GET calls and pydantic
models.

- [x] setup poetry project
- [x] setup project environment with pytest, ruff, mypy and coc-tsserver
- [x] add initial python "summaries" pydantic model
- [x] add "summaries" test
- [ ] add initial python http client
- [ ] add http client test
- [ ] join summaries model and http client in main Client, tests
- [ ] extend to "get document" model, tests
- [ ] extend to "search" model, tests

The Python code is developed using `poetry` and `ruff`.

To run the tests run `poetry run pytest` or `make test`.

## Licence

Licensed under the [MIT Licence](LICENCE).

