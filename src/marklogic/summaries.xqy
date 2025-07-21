(: file: summaries.xqy :)
xquery version "1.0-ml";

(: import summaries library module :)
import module namespace lib = "http://caselaw.nationalarchives.gov.uk/lib/summaries"
  at "/ext/summaries-lib.xqy";

(: local function :)
declare function local:perform-summaries(
  $sort_by as xs:string,
  $sort_direction as xs:string
) as element(summaries)
{
  (: generate summaries by calling the library function for each doc :)
  let $unsorted_summaries :=
    for $doc in collection("examples")
    return lib:get-summary($doc)

  (: sort summaries using the library function :)
  let $sorted_summaries := lib:sort-summaries(
    $unsorted_summaries,
    $sort_by,
    $sort_direction
  )

  (: wrap the result :)
  return
    <summaries>
      {$sorted_summaries}
    </summaries>
};

(: main :)
declare variable $sort_by as xs:string external := "date";
declare variable $sort_direction as xs:string external := "desc";
local:perform-summaries($sort_by, $sort_direction)
