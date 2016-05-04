#opdracht 3x

import sys
from SPARQLWrapper import SPARQLWrapper, JSON

lidwoorden = ["de", "het", "een"]

def print_example_queries():
	print("Wat is de startdatum van de Olympische Spelen 2012?")
	print("Wat is de plaats van de Olympische Zomerspelen 2008?")
	print("Wat is de lengte van Usain Bolt?")
	print("Wie is de trainer van Usain Bolt?")

def create_and_fire_query(line):
	print("Je vraag is: ", line)
	propX = find_prop(line)
	conceptY = find_concept(line)
	print(propX)
	print(conceptY)
	answer = query(propX, conceptY)	
	return(answer)

def find_prop(line):
	##ad-hoc: only works when prop is one word and on 3rd position in sentence
	line = line.split()
	#remove lidwoorden
	if line[2] in lidwoorden:
		propX = line[3]
	else: 
		propX = line[2]

	return(propX)


def find_concept(line):
	##ad hoc: only works when concept follows after "van"
	#transform concept into a string
	concept = line.split("van")[1]
	concept = concept.replace("?", "")
	concept = concept.replace("de", "")
	concept = concept.replace("het", "")
	concept = concept.strip()
	
	#search concept string in paircounts
	page = ["url", 0]

	for pair in open("pairCounts"):
		if str(concept) in pair:
			pair = pair.split('\t')
			#sort by frequency
			if int(pair[2]) > page[1]:
				page[0] = pair[1]
				page[1] = int(pair[2])

	#return concept url with highest frequency			
	conceptY = page[0]
	return(conceptY)

def query(propX, conceptY):
	##possible properties
	#persons
	lengte = ["lengte", "hoogte"]
	gewicht = ["gewicht", "zwaarte", "kilogram"]
	geboorte = ["geboortedatum", "geboorte"]
	trainer = ["trainer", "coach", "meester"]
	geboorteplaats = ["geboorteplaats", "geboortestad", "geboorteplek"]
	#games
	locatie = ["locatie", "plaats", "plek"]
	datumopening = ["opening", "openingsdatum", "start"]
	datumsluiting = ["sluiting", "sluitingsdatum", "slot"]
	vakkeldrager = ["fakkeldrager", "fakkelman", "fakkelvrouw"]
	opener = ["opener", "openingsmeester", "openingspersoon"]

	#queries for specific properties

	if propX in gewicht:
		answer = function("""SELECT ?gewicht
				WHERE {
				<resource_url> <http://dbpedia.org/ontology/Person/weight> ?gewicht.
				}""", conceptY)
		return(answer)


def function(sparql_query, conceptY):
    sparql = SPARQLWrapper("http://nl.dbpedia.org/sparql")
    sparql_query = sparql_query.replace("resource_url", conceptY)
    sparql.setQuery(sparql_query)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for result in results["results"]["bindings"]:
        for arg in result :
            answer = result[arg]["value"]
            return(answer)		

def main(argv):
	print_example_queries()
	for line in sys.stdin:
		#haalt whitespace aan het einde van line weg
		line = line.rstrip()
		answer = create_and_fire_query(line)
		print(answer)

if __name__ == "__main__":
	main(sys.argv)

