# README

src directory readme

## What's here

The python sources are in `ml_akn_client/` which consists of a single
module file of the same name and the directories `server` (for MarkLogic
REST server interaction) and `models` (for deserializing xml)`.

The marklogic sources are in `marklogic/` and include Docker
instructions and deployment script. See the [marklogic
readme](./marklogic/README.md).

## First run

As set out in the database readme, initialise and run the MarkLogic
docker instance, populate the security credentials, put these in
`variables.env` and then proceed to load the database contents.

Following that the python client can be used and/or tests run.

