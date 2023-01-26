
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
            temp = row[1].n3()[1:-4]
            genre.append(temp)
            temp = row[0].n3().strip('<http://www.wikidata.org/entity/>')
            id.append(temp)
        res = dict()
        for i in range(len(genre)):
            res[genre[i]] = id[i]
        return res

    def get_genre_id(self, genre, genre_list):
        return genre_list.get(genre)

    def get_performer_list(self):
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
        id = []
        for row in qresult:
            temp = row[1].n3()[1:-4]
            performer.append(temp)
            temp = row[0].n3().strip('<http://www.wikidata.org/entity/>')
            id.append(temp)
        res = dict()
        for i in range(len(performer)):
            res[performer[i]] = id[i]
        return res

    def get_performer_id(self, performer, performer_list):
        return performer_list.get(performer)

    def get_result(self, genre_id, performer_id):
        if not genre_id:
            genre_id = '?genre'
        if not performer_id:
            performer_id = '?performer'

        g = rdflib.ConjunctiveGraph('SPARQLStore')
        g.open('https://query.wikidata.org/sparql')
        start_date = "1940-01-01T00:00:00Z"
        end_date = "2000-12-31T00:00:00Z"
        query = f"""
                SELECT DISTINCT  ?albumLabel ?genre ?genreLabel ?performer ?performerLabel ?language ?languageLabel ?release ?spotify     WHERE {{
                  ?album wdt:P31 wd:Q482994.
                  ?album wdt:P577 ?pubdate.
                  ?album wdt:P136 {genre_id}.
                  ?album wdt:P175 {performer_id}.
                  ?album wdt:P407 ?language.
                  ?album wdt:P577 ?release.
                  ?album wdt:P2205 ?spotify.


                  FILTER((?pubdate >= "{start_date}"^^xsd:dateTime) && (?pubdate <= "{end_date}"^^xsd:dateTime))
                  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}

                }} LIMIT 10
                """
        qresult = g.query(query)

        return qresult

    def query_main(self, genre, performer):
        genre_id = None
        performer_id = None
        if genre:
            genre_list = self.get_genre_list()
            genre_id = self.get_genre_id(genre, genre_list)
            genre_id = 'wd:' + genre_id
        if performer:
            performer_list = self.get_performer_list()
            performer_id = self.get_performer_id(performer, performer_list)
            performer_id = 'wd:' + performer_id
        if genre or performer:
            res = self.get_result(genre_id, performer_id)
        else:
            return None
        return res
