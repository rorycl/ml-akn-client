(: file: search.xqy :)
xquery version "1.0-ml";

declare namespace akn="http://docs.oasis-open.org/legaldocml/ns/akn/3.0";
import module namespace search = "http://marklogic.com/appservices/search" at "/MarkLogic/appservices/search/search.xqy";

(: import summaries library module :)
import module namespace lib = "http://caselaw.nationalarchives.gov.uk/lib/summaries"
  at "/ext/summaries-lib.xqy";

(: local function :)
declare function local:perform-search(
  $query as xs:string,
  $sort_by as xs:string,
  $sort_direction as xs:string
) as element(summaries)
{
    (: 
     : search configuration items
     : per-match-tokens  : max number of tokens (typically words) per matching node that surround the highlighted term(s) in the snippet
     : max-matches       : The maximum number of nodes containing a highlighted term that will display in the snippet.
     : max-snippet-chars : Limit total snippet size to this many characters
     : See               : https://docs.progress.com/bundle/marklogic-server-use-search-11/page/topics/query-options.html
     :)
    let $per-match-tokens := 30
    let $max-matches := 3  
    let $max-snippet-chars := 200

    (: define XSLT transformation :)
    let $transformer :=
      <xsl:stylesheet version="2.0"
                      xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                      xmlns:search="http://marklogic.com/appservices/search"
                      exclude-result-prefixes="search">
        <xsl:output method="xml" indent="no" omit-xml-declaration="yes"/>
        <xsl:strip-space elements="*"/>
        <xsl:template match="@*|node()">
          <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
          </xsl:copy>
        </xsl:template>
        <xsl:template match="search:highlight">
          <span class="highlight">
            <xsl:apply-templates/>
          </span>
        </xsl:template>
      </xsl:stylesheet>

    (: define search options :)
    let $options :=
      <options xmlns="http://marklogic.com/appservices/search">
        <transform-results apply="snippet"/>
        <snippet-format>xml</snippet-format>
        <preferred-matches>
          <element ns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" name="p"/> (: only search the "p" or paragraph items :)
        </preferred-matches>

        <per-match-tokens>{$per-match-tokens}</per-match-tokens> 
        <max-matches>{$max-matches}</max-matches>
        <max-snippet-chars>{$max-snippet-chars}</max-snippet-chars>
        
        (: highlight config is not parametarized at this point :)
        <highlight/>
        <term>
          <term-option>case-insensitive</term-option>
          <term-option>stemmed</term-option>
        </term>
      </options>

    (: generate unsorted summaries, decorated with snippets :)
    let $unsorted_summaries :=
      for $result in search:search($query, $options)/search:result
      let $doc := fn:doc($result/@uri)

      let $summary := lib:get-summary($doc)
      let $snippets := $result/search:snippet
      return
        (: return the summary, adding any snippets :)
        element summary {
          $summary/node(),  (: copy all nodes from the base summary :)
          if ($snippets) then
            (: 
             : This block is concerned with escaping the search:highlight elements
             : within the search:match results to hand back to the client.
             : Each snippet is extracted and then put in a temporary root
             : element, then the XSLT transformer applied. Finally the
             : sequence of transformed nodes are quoted and string-joined.
             : I'm hoping to learn of a better way of doing this.
             :)
            <snippets>
            {
              for $s in $snippets
              let $wrapped-input := <temp-root>{$s/search:match/node()}</temp-root>
              let $transformed-wrapper := xdmp:xslt-eval($transformer, $wrapped-input)
              (: join the sequence of items (some of which are nodes) in transformed-wrapper into a string by iterating over each item :)
              let $clean-html := fn:string-join(
                for $node in $transformed-wrapper/temp-root/node()
                  return xdmp:quote($node)
              )
              (: add <raw>{$wrapped-input}</raw> within snippet for debugging :)
              return
                <snippet>{$clean-html}</snippet>
            }
            </snippets>
          else ()
        }

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
declare variable $query as xs:string external;
declare variable $sort_by as xs:string external;
declare variable $sort_direction as xs:string external;
local:perform-search($query, $sort_by, $sort_direction)
