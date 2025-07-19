# marklogic

MarkLogic is the NoSQL database used by The National Archives (TNA) for
it's "Find Case Law" service and is referenced widely in the TNA
[ds-caselaw-custom-api-client](https://github.com/nationalarchives/ds-caselaw-custom-api-client) github code.

This part of the repo is about setting up MarkLogic in docker and
interacting with it to develop server-side processing of XML documents,
much in the way one might utilise procedural SQL on a database server
such as PostgreSQL or Oracle.

## About MarkLogic

According to [Wikipedia](https://en.wikipedia.org/wiki/MarkLogic), the
MarkLogic database:

> is a multi-model NoSQL database that has evolved from its XML database
> roots to also natively store JSON documents and RDF triples for its
> semantic data model. It uses a distributed architecture that can
> handle hundreds of billions of documents and hundreds of terabytes of
> data.[citation needed] MarkLogic maintains ACID consistency for
> transactions and has a Common Criteria certification security model,
> high availability, and disaster recovery. It is designed to run
> on-premises within public or private cloud computing environments like
> Amazon Web Services.
>
> MarkLogic's Enterprise NoSQL database platform is used in various
> sectors, including publishing, government and finance. It is employed in
> a number of systems currently in production.

## Akoma Ntosi

Based presumably from the experience of developing the
`legislation.gov.uk` service, the Find Case Law project (another TNA
service) uses the Akoma Ntoso XML standard. As described on [the
Legislation.gov.uk technology-choices-factsheet.pdf](https://www.legislation.gov.uk/pdfs/projects/technology-choices-factsheet.pdf):

> Akoma Ntoso is the emerging international standard for representing
> legislation, and is less complex and easier to work with than CLML.
> There is also a wider pool of experts and suppliers.

While the factsheet shows that it was planned to use the "eXist XML
database and Mongo JSON database" it seems that for the Find Case Law
project [MarkLogic was selected](https://www.globalsecuritymag.fr/MarkLogic-helps-UK-National,20221108,132078.html)
for the "The National Archives seeks to replicate, in court judgements
and tribunal decisions, the search ability and data analysis already
possible in their other MarkLogic-powered solutions at
legislation.gov.uk." So perhaps MarkLogic is now used for
legislation.gov.uk too.

The (non-https) [Akoma Ntoso site](http://akomantoso.info/?page_id=25)
gives more detail about this XML standard for parliamentary, legislative
and judiciary documents, as does [Wikipedia](https://en.wikipedia.org/wiki/Akoma_Ntoso).

## XQuery and XML

[W3Schools](https://www.w3schools.com/xml/xquery_intro.asp) has a simple
intro to XML/Xquery and XSLT which is worth a quick review if one is
considering working with XQuery in MarkLogic (or eXist for that matter).

A simple FLWOR example from the W3Schools article:

```xquery
for $x in doc("books.xml")/bookstore/book
where $x/price>30
order by $x/title
return $x/title
```

Which provides the same output as

```
doc("books.xml")/bookstore/book[price>30]/title
```

## MarkLogic: developing server-side applications

Progress software's documentation for MarkLogic can be confusing to
navigate. I found the following resources the most useful to turn to:

* **[Docs and Intro](https://docs.progress.com/bundle/marklogic-server-understand-concepts-11/page/topics/overview.html)**
  An intro to MarkLogic Server as part of the general
  [documentation hub](https://docs.progress.com/category/marklogic-content-hub)
  documentation.

* **[XQuery and XSLT Reference
  Guide](https://docs.progress.com/bundle/marklogic-server-xquery-xslt-reference-11/page/topics/whatis.html)**
  "In MarkLogic Server, XQuery and XSLT are not only used to query XML,
  but are also used as programming languages to create applications.
  They are especially powerful as a programming languages to create web
  applications..."
  The *XPath Quick Reference* in this reference is particularly helpful.

* **[Developing Applications in MarkLogic
  Server](https://docs.progress.com/bundle/marklogic-server-develop-server-side-apps-11/page/topics/appdev.html)**
  A thorough set of articles on developing server applications for
  storing data, building applications using XQuery or server-side
  JavaScript for search and development language, to integrate with the
  inbuilt REST web server and other client APIs.
  The guide focuses primarily on the concepts, techniques and design
  patterns used to build content and search applications in MarkLogic
  Server.

* **[Develop Using the REST API](https://docs.progress.com/bundle/marklogic-server-develop-rest-api-11/page/topics/extensions.html)**
  "The REST Client API provides a set of RESTful services for creating,
  updating, retrieving, deleting and query documents and metadata..."
  The sections on "Manipulating Documents" and "Using and Configuring
  Query Features" were particularly helpful for this project.

* **[Product Documentation](https://docs.marklogic.com/cts:search)**
  Product documentation, for example for all MarkLogic built-in
  functions such as `cts:search`.

* **[Search Developer Guide](https://docs.marklogic.com/guide/search-dev)**
  General information for developing search features in MarkLogic.

* **[search:search documentation](https://docs.marklogic.com/11.0/search:search)**
  Canonical reference for `search:search`. Note that
  `search:search()` has a richer response than `cts:search()` and
  conveniently includes result snippets.

## Other resources

* **[eXist db XQuery Examples Collection](https://en.wikibooks.org/wiki/XQuery)**  
  An extensive resource of XQuery examples by users of eXist db.

* **XQuery 2e: Search Across a Variety of XML Data** 
  Second edition of the O'Reilly book by Priscilla Walmsley

* **XSLT, 2nd Edition** 
  Second edition of the O'Reilly book by Doug Tidwell

* **XSLT 2.0 and XPath 2.0 Programmer's Reference 4th Edition**  
  Fourth edition by Michael Kay (Wrox)  
  Considered by many to be _the_ reference to XSLT and XPath.

## Docker

Simply run:

```docker
docker run -d -it -p 8000:8000 -p 8001:8001 -p 8002:8002 \
	progressofficial/marklogic-db
```

Then log in and set the main server username and password and save it in
`../variables.env` (using `../variables_example.env` as a template).

More information is at https://github.com/marklogic/marklogic-docker

## Load content

Run the `load_documents.sh` script to load documents. You need to have
`curl` and `wget` installed.
