# tna-fcl-client

Example client for interacting with TNA Akoma Ntosi *Find Case Law* files.

> [!NOTE]
> This repo is a work in progress. Progress is noted below in the
> [database](#database) and [client](#client) sections.

An example Python client module called `CaseLawClient` for interacting
with a MarkLogic server utilising XQuery server-side modules to process
Akoma Ntosi format XML files used for parliamentary, legislative and
judiciary documents as implemented by The National Archives (TNA) for
the [Find Case Law](https://caselaw.nationalarchives.gov.uk/)
initiative.

Deployment of this repo as set out [in the database
README](./src/marklogic/README.md) includes incorporating Find Case Law
records. These documents can be freely accessed and re-used under the
[Open Justice Licence](https://caselaw.nationalarchives.gov.uk/re-use-find-case-law-records).

## Example

An example of using the client `get_summaries` client method:

```
$ source ../variables.env 
$ python
>>> import caselawclient as clc
>>> from ml_akn_client.models import summaries
>>> from ml_akn_client.server import marklogic as ml
>>> import os
>>> http_client = ml.MarkLogicHTTPClient(
...         scheme="http",
...         host=os.environ["ML_HOST"],
...         port=int(os.environ["ML_PORT"]),
...         username=os.environ["ML_USERNAME"],
...         password=os.environ["ML_PASSWORD"],
...     )
>>> client = clc.CaseLawClient(http_client)
>>> s = client.get_summaries()
>>> s.summaries[0]
Summary(uri='/documents/ewca_civ_2014_885.xml', name='Youssefi v Mussellwhite',
        judgment_date=datetime.date(2014, 7, 2), court='EWCA-Civil', citation='[2014] EWCA Civ 885')
>>> s = client.get_summaries(sort_by="date")
>>> s.summaries[0]
Summary(uri='/documents/ewhc_ch_2025_16.xml', name='SBP 2 S.À.R.L v 2 SOUTHBANK TENANT LIMITED',
        judgment_date=datetime.date(2025, 1, 7), court='EWHC-Chancery', citation='[2025] EWHC 16 (Ch)')
>>> s = client.get_summaries(sort_by="date", sort_direction="asc")
>>> s.summaries[0]
Summary(uri='/documents/ewca_civ_2003_1759.xml', name='Tiffany Investments Ltd. & Anor v Bircham & Co Nominees (No 2) Ltd. & Ors',
        judgment_date=datetime.date(2003, 12, 4), court='EWCA-Civil', citation='[2003] EWCA Civ 1759')

```

## Aim

The aim of this repo is to become conversant with processing Akoma Ntosi
format files provided by the TNA's Find Case Law service using a
MarkLogic database and Python to provide a simple Python client to a
local database.

The exemplar client methods are intended to be:

* `get_summaries`
  Get case summaries for all documents in the `examples` collection of
  the `documents` database.

* `search`
  Find documents in the `examples` collection of the `documents`
  database using simple search terms which will return a summary of each
  document together with some "search snippets" from the search query.

* `get_document`
  Show a document in the `documents` database. 

A clean architecture model is used to separate data processing and the
marshalling and use of that data by Python. Data transformations are
performed server-side using XQuery and XSLT to minimise post-processing
for performance and re-use of code by different consumers.

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
- [x] install and register "search" query and endpoint
- [ ] install and register "get document" query and endpoint
- [ ] automate all of the above

Please read `src/marklogic/README.md` to setup the database, content and
server-side functions.

## Client

The `src/ml_akn_client/` part of this repo provides the Python API
client implemented using authenticated http GET calls and pydantic
models.

- [x] setup poetry project
- [x] setup project environment with pytest, ruff, mypy and coc-tsserver
- [x] add initial python "summaries" pydantic model
- [x] add "summaries" test
- [x] add initial python http client
- [x] add http client tests
- [x] join summaries model and http client in main CaseLawClient, tests
- [ ] extend to "search" model, tests
- [ ] add CaseLawClient tests
- [ ] extend to "get document" model, tests

The Python code is developed using `poetry` and `ruff`.

To run the tests run `poetry run pytest` or `make test`.

## Architecture

```
.
├── LICENCE
├── Makefile
├── poetry.lock
├── pyproject.toml
├── README.md
├── src
│   ├── marklogic
│   │   ├── admin-checks.sh
│   │   ├── deploy.sh
│   │   ├── helloworld.sh
│   │   ├── helloworld.xqy
│   │   ├── load_documents.sh
│   │   ├── ml-workspace.xml
│   │   ├── README.md
│   │   └── summaries.xqy
│   ├── README.md
│   ├── ml_akn_client
│   │   ├── caselawclient.py
│   │   ├── __init__.py
│   │   ├── models
│   │   │   ├── __init__.py
│   │   │   └── summaries.py
│   │   └── server
│   │       ├── __init__.py
│   │       └── marklogic.py
│   └── variables_example.env
└── tests
    ├── __init__.py
    └── test_summaries.py

7 directories, 23 files

```

## Licence

Licensed under the [MIT Licence](LICENCE).

