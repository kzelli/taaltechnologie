import socket
import sys
from SPARQLWrapper import SPARQLWrapper, JSON
import sys
from lxml import etree

def print_example_queries():
	#examples of queries that are possible with this program
	print("Dit programma kan diverse vragen beantwoorden. \n")
	print("Mogelijke vragen over personen: \n")
	print("Wat is de lengte van Usain Bolt?")
	print("Wat is het gewicht van Usain Bolt?")
	print("Wanneer is Usain Bolt geboren?")
	print("Waar is Usain Bolt geboren?")
	print("Wie is de trainer van Usain Bolt? \n")
	print("Mogelijke vragen over gebeurtenissen: \n")
	print("Waar waren de Olympische Zomerspelen 2008?")
	print("Wat is de startdatum van de Olympische Spelen 2008?")
	print("Wanneer sloten de Olympische Spelen 2008?")
	print("Hoeveel landen deden mee aan de Olympische Spelen 2008?")
	print("Hoeveel atleten deden mee aan de Olympische Spelen 2008? \n \n")

# parse input sentence and return alpino output as an xml element tree
def alpino_parse(sent, host='zardoz.service.rug.nl', port=42424):
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect((host,port))
	sent = sent + "\n\n"
	sentbytes= sent.encode('utf-8')
	s.sendall(sentbytes)
	bytes_received= b''
	while True:
		byte = s.recv(8192)
		if not byte:
			break
		bytes_received += byte
	# print(bytes_received.decode(’utf-8’), file=sys.stderr)
	xml = etree.fromstring(bytes_received)
	return xml

def tree_yieldprop(xml):
	# gets several attributes from nodes in sentence 
    leaves = xml.xpath('descendant-or-self::node[@word]')
    words = []
    for l in leaves:
    	posword = []
    	posword.append(l.attrib["pos"])
    	posword.append((l.attrib["word"]).lower())
    	posword.append(l.attrib["rel"])
    	# add the infinitve of a verb
    	if posword[0] == "verb":
    		posword.append(l.attrib["lemma"])
    	words.append(posword)
    return words

def find_prop(parsed_question):
	# find sort prop based on question type
	for word in parsed_question:
		if "whd" in word:
			if "wie" in word:
				return(person_question(parsed_question))
			elif "wat" in word:
				return(object_question(parsed_question))
			elif "wanneer" in word:
				return(time_question(parsed_question))
			elif "waar" in word:
				return(location_question(parsed_question))
		elif "adj" in word:
			if "hoeveel" in word:
				return(number_question(parsed_question))

def person_question(parsed_question):
	# props based on persons
	for word in parsed_question:
		if "hd" in word:
			if "noun" in word:
				propX = word[1]
				return(propX)

def object_question(parsed_question):
	# props based on data about persons
	for word in parsed_question:
		if "hd" in word:
			if "noun" in word:
				propX = word[1]
				return(propX)

def time_question(parsed_question):
	# props about time and dates
	opening = ["openen", "beginnen"]
	sluiting = ["sluiten", "aflopen", "eindigen"]
	for word in parsed_question:
		if "geboren" in word:
			propX = "geboorte"
			return(propX)
		for prop in opening:
			if prop in word:
				propX = "opening"
				return(propX)
		for prop in sluiting:
			if prop in word:
				propX = "sluiting"
				return(propX)

def location_question(parsed_question):
	# props about location
	for word in parsed_question:
		if "geboren" in word:
			propX = "geboorteplaats"
			return(propX)

	propX = "locatie"
	return(propX)

def number_question(parsed_question):
	# props about amount or numbers
	for word in parsed_question:
		if "atleten" in word:
			propX = "nummeratleten"
			return(propX)
		if "landen" in word:
			propX = "nummerlanden"
			return(propX)


def find_concept(parsed_question):
	# find the concept based on "mwp" pos
	conceptlist = []
	concept = None

	for word in parsed_question:
		if "mwp" in word:
			conceptlist.append(word[1].capitalize())
			concept = ' '.join(conceptlist)
	
	if concept == None:
		print("The program could not found a relevant concept to answer the question.")
		return(None)

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
	#events
	locatie = ["locatie", "plaats", "plek"]
	datumopening = ["opening", "openingsdatum", "start", "startdatum"]
	datumsluiting = ["sluiting", "sluitingsdatum", "slot"]
	fakkeldrager = ["fakkeldrager", "fakkelman", "fakkelvrouw"]
	opener = ["opener", "openingsmeester", "openingspersoon"]
	#time
	tijd = ["tijd"]
	#number
	atleten = ["nummeratleten"]
	landen = ["nummerlanden"]

	#queries for specific properties

	if propX in lengte:
		answer = function("""SELECT ?lengte
				WHERE {
				<resource_url> <http://dbpedia.org/ontology/Person/height> ?lengte.
				}""", conceptY)
		return(answer)

	if propX in gewicht:
		answer = function("""SELECT ?gewicht
				WHERE {
				<resource_url> <http://dbpedia.org/ontology/Person/weight> ?gewicht.
				}""", conceptY)
		return(answer)

	if propX in geboorte:
		answer = function("""SELECT ?geboorte
				WHERE {
				<resource_url> <http://nl.dbpedia.org/property/geboortedatum> ?geboorte.
				}""", conceptY)
		return(answer)

	if propX in trainer:
		answer = function("""SELECT ?trainer
				WHERE {
				<resource_url> <http://nl.dbpedia.org/property/trainer> ?trainer.
				}""", conceptY)
		return(answer)

	if propX in geboorteplaats:
		answer = function("""SELECT ?geboorteplaats
				WHERE {
				<resource_url> <http://nl.dbpedia.org/property/geboorteplaats> ?geboorteplaats.
				}""", conceptY)
		return(answer)
	
	if propX in locatie:
		answer = function("""SELECT ?locatie
				WHERE {
				<resource_url> <http://dbpedia.org/ontology/location> ?locatie.
				}""", conceptY)
		return(answer)

	if propX in datumopening:
		answer = function("""SELECT ?opening
				WHERE {
				<resource_url> <http://nl.dbpedia.org/property/opening> ?opening.
				}""", conceptY)
		return(answer)

	if propX in datumsluiting:
		answer = function("""SELECT ?sluiting
				WHERE {
				<resource_url> <http://nl.dbpedia.org/property/sluiting> ?sluiting.
				}""", conceptY)
		return(answer)

	if propX in fakkeldrager:
		answer = function("""SELECT ?fakkeldrager
				WHERE {
				<resource_url> <http://dbpedia.org/ontology/torchBearer> ?fakkeldrager.
				}""", conceptY)
		return(answer)

	if propX in opener:
		answer = function("""SELECT ?opener
				WHERE {
				<resource_url> <http://nl.dbpedia.org/property/opener> ?opener.
				}""", conceptY)
		return(answer)
	
	if propX in tijd:
		answer = function("""SELECT ?tijd
				WHERE {
				<resource_url> <http://nl.dbpedia.org/property/jaar> ?tijd.
				}""", conceptY)
		return(answer)

	if propX in atleten:
		answer = function("""SELECT ?atleten
				WHERE {
				<resource_url> <http://dbpedia.org/ontology/numberOfParticipatingAthletes> ?atleten.
				}""", conceptY)
		return(answer)

	if propX in landen:
		answer = function("""SELECT ?landen
				WHERE {
				<resource_url> <http://dbpedia.org/ontology/numberOfParticipatingNations> ?landen.
				}""", conceptY)
		return(answer)



def function(sparql_query, conceptY):
	#SPARQL query based on lecture slides
    sparql = SPARQLWrapper("http://nl.dbpedia.org/sparql")
    sparql_query = sparql_query.replace("resource_url", conceptY)
    sparql.setQuery(sparql_query)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for result in results["results"]["bindings"]:
        for arg in result :
            answer = result[arg]["value"]
            return(answer)


def create_and_fire_query(line):
	xml = alpino_parse(line)
	result = (tree_yieldprop(xml))
	#print(result)
	conceptY = find_concept(result)
	propX = find_prop(result)
	return(query(propX, conceptY))

def main(argv):
	print_example_queries()
	for line in sys.stdin:
		#remove whitspace at end of line
		line = line.rstrip()

		#get the property and the concept of the question and the answer to the question based on query
		answer = create_and_fire_query(line)

		print(answer)

if __name__ == "__main__":
	main(sys.argv)