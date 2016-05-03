#opdracht 3x

import sys
from SPARQLWrapper import SPARQLWrapper, JSON

def print_example_queries():
	print("Wat is de startdatum van de Olympische Spelen 2012?")
	print("Wat is de plaats van de Olympische Zomerspelen 2008?")
	print("Wat is de lengte van Usain Bolt?")
	print("Wie is de trainer van Usain Bolt?")

def find_concept(concept):
	for line in open("pairCounts"):
		if concept in line:
			line = line.split('\t')
			concept_Y = (line[1])
			return concept_Y

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

