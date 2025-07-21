(: file: lib-summaries.xqy :)
xquery version "1.0-ml";

(: library module for summaries. 
 : functions in this module:
 : local-lib:get-summary  : get summary data from an AKN document
 : local-lib:sort-summary : sort summary data (possibly decorated) by a summary element 
 :)
module namespace local-lib = "http://caselaw.nationalarchives.gov.uk/lib/summaries";

declare namespace akn="http://docs.oasis-open.org/legaldocml/ns/akn/3.0";
declare namespace uk="https://caselaw.nationalarchives.gov.uk/akn";

(:~
 : create a single <summary> element from a given document node.
 : @param $doc  A document node() for a single case law document.
 : @return      A single <summary> element.
 :)

(: local function :)
declare function local-lib:get-summary(
  $doc as node()
) as element(summary)
{
  let $meta := $doc/akn:akomaNtoso/akn:judgment/akn:meta
  return
    <summary>
      <uri>{fn:document-uri($doc)}</uri>
      <name>{$meta/akn:identification/akn:FRBRWork/akn:FRBRname/@value/string()}</name>
      <judgmentDate>{$meta/akn:identification/akn:FRBRWork/akn:FRBRdate[@name='judgment']/@date/string()}</judgmentDate>
      <court>{$meta/akn:proprietary/uk:court/text()}</court>
      <citation>{$meta/akn:proprietary/uk:cite/text()}</citation>
    </summary>
};

(:~
 : sorts a sequence of <summary> elements.
 : @param $summaries      A sequence of <summary> elements.
 : @param $sort_by        The field to sort by.
 : @param $sort_direction The direction of the sort.
 : @return                A sorted sequence of <summary> elements.
 : note that summaries can be "decorated" with other elements, so this
 : is an extensible pattern.
 :)
declare function local-lib:sort-summaries(
  $summaries as element(summary)*,
  $sort_by as xs:string,
  $sort_direction as xs:string
) as element(summary)*
{
  let $sorted_summaries :=
    for $summary in $summaries
    order by
      switch ($sort_by)
        case "name" return $summary/name
        case "date" return xs:date($summary/judgmentDate)
        case "court" return $summary/court
        case "citation" return $summary/citation
        default return xs:date($summary/judgmentDate)
    ascending
    return $summary

  return
    if ($sort_direction = "desc") then
      fn:reverse($sorted_summaries)
    else
      $sorted_summaries
};
