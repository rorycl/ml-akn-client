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

# deploy summaries
FILE=summaries.xqy
ENDPOINT=summaries.xqy

curl --digest --user ${ML_USERNAME}:${ML_PASSWORD} -X PUT -i \
	-H "Content-type: application/xquery" \
	--data-binary @${FILE} \
	"http://${ML_HOST}:${ML_PORT}/v1/ext/${ENDPOINT}"
	
# should return:
#
# HTTP/1.1 204 Updated
# Server: MarkLogic
# Content-Length: 0
# Connection: Keep-Alive
# Keep-Alive: timeout=5

curl --digest --user ${ML_USERNAME}:${ML_PASSWORD} -i -X POST \
     -H "Content-type: application/x-www-form-urlencoded" \
     --data-urlencode module=/ext/${ENDPOINT} \
	 --data-urlencode vars='{"sort_by": "date", "sort_direction": "desc"}' \
     http://${ML_HOST}:${ML_PORT}/LATEST/invoke

# should return something like: 
# 
# HTTP/1.1 200 OK
# Server: MarkLogic 11.3.1
# Set-Cookie: TxnID=null; path=/; SameSite=Lax
# Content-Type: multipart/mixed; boundary=bb095a5d570af3af
# Content-Length: 840
# Connection: Keep-Alive
# Keep-Alive: timeout=5
# 
# 
# --bb095a5d570af3af
# Content-Type: application/xml
# X-Primitive: element()
# X-Path: /summaries
# 
# <summaries><summary><uri>/documents/ewhc_ch_2025_16.xml</uri><name>SBP 2 S.À.R.L v 2 SOUTHBANK TENANT LIMITED</name><judgmentDate>2025-01-07</judgmentDate><court>EWHC-Chancery</court><citation>[2025] EWHC 16 (Ch)</citation></summary><summary><uri>/documents/ewhc_ch_2008_1582.xml</uri><name>Landlord Protect Ltd. v St Anselm Development Company Ltd.</name><judgmentDate>2008-07-08</judgmentDate><court>EWHC-Chancery</court><citation>[2008] EWHC 1582 (Ch)</citation></summary><summary><uri>/documents/ewhc_ch_2004_324.xml</uri><name>Design Progression Ltd v Thurloe Properties Ltd</name><judgmentDate>2004-02-25</judgmentDate><court>EWHC-Chancery</court><citation>[2004] EWHC 324 (Ch)</citation></summary></summaries>
# --bb095a5d570af3af--



