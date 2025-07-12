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

# deploy hello world
# See https://docs.progress.com/bundle/marklogic-server-develop-rest-api-11/page/topics/extensions.html#id_75293

curl --anyauth --user ${ML_USERNAME}:${ML_PASSWORD} -X POST -i \
    -H "Content-type: application/x-www-form-urlencoded" \
    -H "Accept: multipart/mixed" \
    --data-urlencode xquery@helloworld.xqy \
    --data-urlencode vars='{"word1":"hello","word2":"cruel world"}' \
	"http://${ML_HOST}:${ML_PORT}/LATEST/eval"
