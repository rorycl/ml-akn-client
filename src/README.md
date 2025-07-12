# SETUP

Environment setup instructions.

## MarkLogic

### Run docker

Use the instructions here to run Docker:

https://github.com/marklogic/marklogic-docker 

Then run

```
docker run -d -it -p 8000:8000 -p 8001:8001 -p 8002:8002 \
	progressofficial/marklogic-db
```

### Load content

* Landlord Protect Ltd. v St Anselm Development Company Ltd
  https://caselaw.nationalarchives.gov.uk/ewhc/ch/2008/1582/data.xml
  ewhc_ch_2008_1582.xml

* SBP 2 S.À.R.L v 2 SOUTHBANK TENANT LIMITED
  https://caselaw.nationalarchives.gov.uk/ewhc/ch/2025/16/data.xml
  ewhc_ch_2025_16.xml

* Design Progression Ltd v Thurloe Properties Ltd
  https://caselaw.nationalarchives.gov.uk/ewhc/ch/2004/324/data.xml
  ewch_ch_2004_324.xml

