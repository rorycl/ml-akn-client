(: 
See https://docs.progress.com/bundle/marklogic-server-develop-rest-api-11/page/topics/extensions.html#id_75293
:)
xquery version "1.0-ml";
declare variable $word1 as xs:string external;
declare variable $word2 as xs:string external;
($word1, $word2, fn:concat($word1, " ", $word2))

