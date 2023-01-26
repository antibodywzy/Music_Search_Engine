import rdflib
g = rdflib.ConjunctiveGraph('SPARQLStore')
g.open('https://query.wikidata.org/sparql')

query = """
SELECT ?artist ?artistLabel
WHERE {
  {?artist wdt:P106 wd:Q639669.}
  ?artist wdt:P569 ?birthdate.
  FILTER (?birthdate >= "1940-01-01T00:00:00Z"^^xsd:dateTime && ?birthdate <= "2000-12-31T00:00:00Z"^^xsd:dateTime)
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en".}
}



"""
qresult = g.query(query)
performer = []
for row in qresult:
    performer.append(row[1].n3())
print(performer)