#!/bin/bash

set -e

source ../variables.env

# check necessary variables
if [ -z "${ML_USERNAME}" ]; then
	echo "ML_USERNAME (often admin) not defined, quitting"
	exit 1
fi
if [ -z "${ML_PASSWORD}" ]; then
	echo "ML_PASSWORD not defined, quitting"
	exit 1
fi
if [ -z "${ML_HOST}" ]; then
	echo "ML_HOST (normally localhost) not defined, quitting"
	exit 1
fi
if [ -z "${ML_PORT}" ]; then
	echo "ML_PORT (normally 8000) not defined, quitting"
	exit 1
fi
if [ -z "${ML_ADMIN_PORT}" ]; then
	echo "ML_ADMIN_PORT (normally 8002) not defined, quitting"
	exit 1
fi
if [ -z "${ML_ADMIN_DATABASE}" ]; then
	echo "ML_ADMIN_DATABASE (normally Documents) not defined, quitting"
	exit 1
fi

SHOW_DATABASES=0
SET_STEMMING=1

if [ $SHOW_DATABASES -gt 0 ]; then
    # admin: show databases
    curl --digest --user ${ML_USERNAME}:${ML_PASSWORD} -X GET \
      "http://${ML_HOST}:${ML_ADMIN_PORT}/manage/v2/databases/"
fi

# ----------------------------------------------------------------------
# admin

if [ $SET_STEMMING -gt 0 ]; then
    # Ensure search stemming is on at the administrative level;
    #   choices are basic, advanced or off.
    # General documentation:
    #   https://docs.marklogic.com/REST/management/databases
    # Specific documentation:
    #   https://docs.marklogic.com/REST/PUT/manage/v2/databases/[id-or-name]/properties
    #   /manage/v2/databases/{id|name}/properties
    echo "Setting stemmed searches to basic: http://${ML_HOST}:${ML_ADMIN_PORT}/manage/v2/databases/${ML_ADMIN_DATABASE}/properties"
    curl --digest --user ${ML_USERNAME}:${ML_PASSWORD} -X PUT \
      --header "Content-Type:application/xml" \
      -d '<database-properties xmlns="http://marklogic.com/manage"><stemmed-searches>basic</stemmed-searches></database-properties>' \
      --fail-with-body \
      "http://${ML_HOST}:${ML_ADMIN_PORT}/manage/v2/databases/${ML_ADMIN_DATABASE}/properties"
fi

# ----------------------------------------------------------------------
# summaries-lib (a general-purpose summaries library module)

# deploy summaries-lib
FILE=summaries-lib.xqy
ENDPOINT=summaries-lib.xqy

echo "---------------------------------------------------------"
echo "deploying $FILE to $ENDPOINT"
echo "---------------------------------------------------------"

curl --digest --user ${ML_USERNAME}:${ML_PASSWORD} -X PUT -i \
	-H "Content-type: application/xquery" \
	--data-binary @${FILE} \
    --fail-with-body \
	"http://${ML_HOST}:${ML_PORT}/v1/ext/${ENDPOINT}"

# ----------------------------------------------------------------------
# summaries

# deploy summaries
FILE=summaries.xqy
ENDPOINT=summaries.xqy

echo "---------------------------------------------------------"
echo "deploying $FILE to $ENDPOINT"
echo "---------------------------------------------------------"

curl --digest --user ${ML_USERNAME}:${ML_PASSWORD} -X PUT -i \
	-H "Content-type: application/xquery" \
	--data-binary @${FILE} \
    --fail-with-body \
	"http://${ML_HOST}:${ML_PORT}/v1/ext/${ENDPOINT}"


echo "---------------------------------------------------------"
echo "querying $ENDPOINT"
echo "---------------------------------------------------------"

curl --digest --user ${ML_USERNAME}:${ML_PASSWORD} -i -X POST \
    -H "Content-type: application/x-www-form-urlencoded" \
    --data-urlencode module=/ext/${ENDPOINT} \
	--data-urlencode vars='{"sort_by": "date", "sort_direction": "desc"}' \
    --fail-with-body \
    http://${ML_HOST}:${ML_PORT}/LATEST/invoke

# ----------------------------------------------------------------------
# search

# deploy search
FILE=search.xqy
ENDPOINT=search.xqy

echo "---------------------------------------------------------"
echo "deploying $FILE to $ENDPOINT"
echo "---------------------------------------------------------"

curl --digest --user ${ML_USERNAME}:${ML_PASSWORD} -X PUT -i \
	-H "Content-type: application/xquery" \
	--data-binary @${FILE} \
    --fail-with-body \
	"http://${ML_HOST}:${ML_PORT}/v1/ext/${ENDPOINT}"

echo "---------------------------------------------------------"
echo "querying $ENDPOINT"
echo "---------------------------------------------------------"

curl --digest --user ${ML_USERNAME}:${ML_PASSWORD} -i -X POST \
    -H "Content-type: application/x-www-form-urlencoded" \
    --data-urlencode module=/ext/${ENDPOINT} \
	--data-urlencode vars='{"query": "norwich", "sort_by": "date", "sort_direction": "desc"}' \
    --fail-with-body \
    http://${ML_HOST}:${ML_PORT}/LATEST/invoke
