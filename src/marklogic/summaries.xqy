(:
project : tna-fcl-client 
type    : marklogic xquery .xqy file

purpose : summarize database documents in AKN + TNA format
          AKN: Akoma Ntoso Naming Convention Version 3.0 
          TNA: The UK National Archives AKN extensions

author  : Rory Campbell-Lange
started : 12 July 2025
:)

xquery version "1.0-ml";

declare namespace akn="http://docs.oasis-open.org/legaldocml/ns/akn/3.0";
declare namespace tna="https://caselaw.nationalarchives.gov.uk/akn";

(: parameters :)
declare variable $sort_by as xs:string external := "name";
declare variable $sort_direction as xs:string external := "asc";

(: construct summary data :)
let $summaries :=
    for $doc in collection("examples")
    let $meta := $doc/akn:akomaNtoso/akn:judgment/akn:meta
    return
      <summary>
        <uri>{fn:document-uri($doc)}</uri>
        <name>{$meta/akn:identification/akn:FRBRWork/akn:FRBRname/@value/string()}</name>
        <judgmentDate>{$meta/akn:identification/akn:FRBRWork/akn:FRBRdate[@name='judgment']/@date/string()}</judgmentDate>
        <court>{$meta/akn:proprietary/tna:court/text()}</court>
        <citation>{$meta/akn:proprietary/tna:cite/text()}</citation>
      </summary>

(: sort summaries by default ascending :)
let $sorted_summaries :=
    for $summary in $summaries
    order by
        (: sort key switch :)
        switch ($sort_by)
            case "name" return $summary/name
            case "date" return xs:date($summary/judgmentDate) (: Cast to xs:date for correct sorting :)
            case "court" return $summary/court
            case "citation" return $summary/citation
            default return xs:date($summary/judgmentDate)
    ascending
    return $summary

(: reverse ordering if required :)
let $final_summaries :=
    if ($sort_direction = "desc")
    then fn:reverse($sorted_summaries)
    else $sorted_summaries

(: wrap summaries in "summaries" root element :)
return
    <summaries>
        {$final_summaries}
    </summaries>
