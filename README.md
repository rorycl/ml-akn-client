# ml-akn-client

Client for interacting with Akoma Ntosi legal files held on a MarkLogic server.

> [!NOTE]
> This repo is a work in progress. Progress is noted below in the
> [database](#database) and [client](#client) sections.

A Python client module called `ml_akn_client` and stack for interacting
with a MarkLogic server holding Akoma Ntosi (AKN) format XML files used
for parliamentary, legislative and judiciary documents as implemented by
The National Archives (TNA) in its [Find Case
Law](https://caselaw.nationalarchives.gov.uk/) initiative.

A clean architecture model is used to separate data processing and the
marshalling and use of that data by Python. Data transformations are
performed server-side using XQuery and XSLT to minimise post-processing
for performance and re-use of code by different consumers. A central aim
of this approach is to avoid client-side XML processing.

Deployment of this repo as set out [in the database
README](./src/marklogic/README.md) includes incorporating TNA "Find Case
Law" records in AKN format with TNA extensions. (These documents can be
freely accessed and re-used under the [Open Justice
Licence](https://caselaw.nationalarchives.gov.uk/re-use-find-case-law-records).)

## Capabilities

The exemplar system methods are:

* `get_summaries`
  Get case summaries for all documents in the `examples` collection of
  the `documents` database.

* `search`
  Find case summaries from the `examples` collection of the `documents`
  database using simple search terms, return a summary for each document
  together with relevant, html-escaped "search snippets" matching the
  search term in context.

* `judgement`
  Return the summary and html-transformed and escaped judgement for an
  AKN document in HTML format.

## Database

The `src/marklogic` part of this repo sets up a MarkLogic database,
populates the "Documents" database with XML files from the Find Case Law
service and loads several Xquery `.xqy` modules into the MarkLogic REST
server to provide server-side functions to support the API calls.

In the below todo, "ml" refers to the "MarkLogic database and server".

- [x] install and setup ml
- [x] upload example AKN files into ml
- [x] install summaries `.xqy` library into ml
- [x] install initial summaries `.xqy` query 
- [x] register initial summaries `.xqy` query as an ml endpoint
- [x] install and register "search" query and endpoint
- [ ] install and register "judgement" query and endpoint
- [ ] automate all of the above

Please read `src/marklogic/README.md` to setup the database, content and
server-side functions.

## Client

The `src/ml_akn_client/` part of this repo provides the Python API
client to the MarkLogic REST component of the server, implemented using
authenticated http GET calls and pydantic models.

- [x] setup poetry project
- [x] setup project environment with pytest, ruff, mypy and coc-tsserver
- [x] add initial python "summaries" pydantic model
- [x] add "summaries" test
- [x] add initial python http client
- [x] add http client tests
- [x] join summaries model and http client in main CaseLawClient, tests
- [x] extend to "search" model, tests
- [ ] add CaseLawClient tests
- [ ] extend to "get document" model, tests

The Python code is developed using `poetry`, `mypy` and `ruff`.

To run the tests run `poetry run pytest` or `make test`. To check
conformance in general run `make check-all`.

## Licence

Licensed under the [MIT Licence](LICENCE).
