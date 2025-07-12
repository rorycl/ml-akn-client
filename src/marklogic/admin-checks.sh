#!/bin/bash

set -e

source ../variables.env

ML_PORT=8002

echo "-----------------------------------------------------"
echo "rest apis"
echo "-----------------------------------------------------"

curl --anyauth --user ${ML_USERNAME}:${ML_PASSWORD} -X GET \
	"http://${ML_HOST}:${ML_PORT}/LATEST/rest-apis"

echo "-----------------------------------------------------"
echo "rest apis for Documents database"
echo "-----------------------------------------------------"

curl --anyauth --user ${ML_USERNAME}:${ML_PASSWORD} -X GET \
	"http://${ML_HOST}:${ML_PORT}/LATEST/rest-apis?database=Documents"

