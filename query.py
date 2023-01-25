
import rdflib


class query:
    def get_genre_list(self):
        g = rdflib.ConjunctiveGraph('SPARQLStore')
        g.open('https://query.wikidata.org/sparql')

        query = """

        SELECT DISTINCT ?genre ?genreLabel WHERE {
          ?genre wdt:P31 wd:Q188451.
          SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
        } 
        """
        qresult = g.query(query)
        genre = []
        id = []
        for row in qresult:
            temp = row[1].n3().strip('"@en')
            genre.append(temp)
            temp = row[0].n3().strip('<http://www.wikidata.org/entity/>')
            id.append(temp)
        res = dict()
        for i in range(len(genre)):
            res[genre[i]] = id[i]
        return res

    def get_genre_id(self, genre, genre_list):
        return genre_list[genre]

    def get_result(self, genre_id):
        g = rdflib.ConjunctiveGraph('SPARQLStore')
        g.open('https://query.wikidata.org/sparql')
        start_date = "1470-01-01T00:00:00Z"
        end_date = "1990-12-31T00:00:00Z"
        query = f"""
        SELECT DISTINCT  ?albumLabel ?genre ?genreLabel ?performer ?performerLabel ?language ?languageLabel ?release ?spotify     WHERE {{
          ?album wdt:P31 wd:Q482994.
          ?album wdt:P577 ?pubdate.
          ?album wdt:P136  wd:{genre_id}.
          ?album wdt:P175 ?performer.
          ?album wdt:P407 ?language.
          ?album wdt:P577 ?release.
          ?album wdt:P2205 ?spotify.


          FILTER((?pubdate >= "{start_date}"^^xsd:dateTime) && (?pubdate <= "{end_date}"^^xsd:dateTime))
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}

        }} LIMIT 10
        """
        qresult = g.query(query)

        return qresult

    def query_main(self, genre):
        genre_list = self.get_genre_list()
        genre_id = self.get_genre_id(genre, genre_list)
        res = self.get_result(genre_id)
        return res
