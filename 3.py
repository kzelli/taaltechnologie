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
	propX = find_prop(line)
	conceptY = find_concept(line)

def find_prop(line):
	line = line.split()
	if line[2] in lidwoorden:
		propX = line[3]
	else: 
		propX = line[2]

	return(propX)


def find_concept(line):
	#make concept usable to find in paircounts
	concept = line.split("van")[1]
	concept = concept.replace("?", "")
	concept = concept.replace("de", "")
	concept = concept.replace("het", "")
	concept = concept.strip()
	print(concept)

	for pair in open("pairCounts"):
		if str(concept) in pair:
			print(pair)
			pair = pair.split('\t')
			concept_Y = (pair[1])
			print(concept_Y)

#def create_and_fire_query(line):

def main(argv):
	print_example_queries()
	for line in sys.stdin:
		#haalt whitespace aan het einde van line weg
		line = line.rstrip()
		answer = create_and_fire_query(line)
		print(answer)

if __name__ == "__main__":
	main(sys.argv)

