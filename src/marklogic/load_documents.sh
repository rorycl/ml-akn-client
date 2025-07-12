#!/bin/bash

# This script selects 10 xml files on the Find Case Law service of The
# UK National Archives and uploads them to the MarkLogic database
# specified in the variables file specified.
#
# The files are provided under The Open Justice licence which allows for
# the copying, publishing, distributing and tramitting of case law data.

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

# setup environment
mkdir -p tmp

# get an xml file from "find case law service"
get_xml_file() {
	local url=$1
	local filename=$2
	wget -O "tmp/${filename}" "${url}"
}

# upload an xml file to the marklogic server
upload_xml_to_marklogic() {
	# set the collection association for this file
	local collection='collection=examples'
	# filepath is the location of the file on the disk eg tmp/ewhc_ch_2025_16.xml
	local filePath=$1
	# savePath is the path on the markdown server eg /documents/xyz.xml
	local savePath=$2
    curl --digest --user ${ML_USERNAME}:${ML_PASSWORD} -X PUT \
        -T ${filePath} \
    	-H 'Content-type: application/xml' \
        "http://${ML_HOST}:${ML_PORT}/LATEST/documents?uri=${savePath}&${collection}"
}

# names and urls of documents on the TNA Find Case Law service
declare -A documents
documents["ewhc_ch_2008_1582.xml"]="https://caselaw.nationalarchives.gov.uk/ewhc/ch/2008/1582/data.xml"
documents["ewca_civ_2009_99.xml"]="https://caselaw.nationalarchives.gov.uk/ewca/civ/2009/99/data.xml"
documents["ewhc_ch_2025_16.xml"]="https://caselaw.nationalarchives.gov.uk/ewhc/ch/2025/16/data.xml"
documents["ewhc_ch_2004_324.xml"]="https://caselaw.nationalarchives.gov.uk/ewhc/ch/2004/324/data.xml"
documents["ewhc_qb_2020_1353.xml"]="https://caselaw.nationalarchives.gov.uk/ewhc/qb/2020/1353/data.xml"
documents["ewca_civ_2018_2414.xml"]="https://caselaw.nationalarchives.gov.uk/ewca/civ/2018/2414/data.xml"
documents["ewca_civ_2014_885.xml"]="https://caselaw.nationalarchives.gov.uk/ewca/civ/2014/885/data.xml"
documents["ewca_civ_2004_184.xml"]="https://caselaw.nationalarchives.gov.uk/ewca/civ/2004/184/data.xml"
documents["ewca_civ_2005_312.xml"]="https://caselaw.nationalarchives.gov.uk/ewca/civ/2005/312/data.xml"
documents["ewca_civ_2003_1759.xml"]="https://caselaw.nationalarchives.gov.uk/ewca/civ/2003/1759/data.xml"

# main
for doc in "${!documents[@]}"; do 
	url=${documents[$doc]}
	echo "fetching $url to $doc"
	get_xml_file $url $doc

	filePath="tmp/$doc"
	savePath="/documents/${doc}"
	echo "uploading $filePath to marklogic at $savePath"
	upload_xml_to_marklogic $filePath $savePath
done

# cleanup files on disk
rm -rf tmp
