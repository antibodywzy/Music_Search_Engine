import rdflib
g = rdflib.ConjunctiveGraph('SPARQLStore')
g.open('https://query.wikidata.org/sparql')
start_date = "1470-01-01T00:00:00Z"
end_date = "1990-12-31T00:00:00Z"
query = """
SELECT ?artist ?artistLabel
WHERE {
  {?artist wdt:P106 wd:Q639669.} UNION {?artist wdt:P31 wd:Q215380.}
  FILTER((?birthday >= "1800-01-01T00:00:00Z"^^xsd:dateTime) && (?birthday <= "1990-12-31T00:00:00Z"^^xsd:dateTime))
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
"""
qresult = g.query(query)
performer = []
for row in qresult:
    performer.append(row)
print(performer)