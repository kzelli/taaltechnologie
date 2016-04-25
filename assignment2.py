
from SPARQLWrapper import SPARQLWrapper, JSON
import sys

#function() prints the question to the user, then runs the query and outputs
#the result to the user.

def function(question, sparql_query):
    print(question)
    sparql = SPARQLWrapper("http://nl.dbpedia.org/sparql")
    sparql.setQuery(sparql_query)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for result in results["results"]["bindings"]:
        for arg in result :
            answer = arg + " : " + result[arg]["value"]
            print(answer)

#outputs the answer of question number based on shell input
def main():
    question_number = sys.argv[1]
    
    if question_number == "1":
        function("Wie droeg de Nederlandse vlag tijdens de Olympische Spelen in 1964?", """PREFIX dbpedia: <http://nl.dbpedia.org/resource/>
PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>

select ?flagbearer where {
  dbpedia:Nederland_op_de_Olympische_Zomerspelen_1964 dbpedia-owl:flagBearer ?flagbearer
}""")

    if question_number == "2":
        function("Tijdens welke Olympische Spelen won Nederland de meeste gouden medailles?",
                 """SELECT ?spelen ?goud
WHERE {
?spelen dcterms:subject category-nl:Nederland_op_de_Olympische_Spelen .
?spelen prop-nl:goud ?goud .
}
ORDER BY DESC(xsd:float(str(?goud))) LIMIT 1""")

    if question_number == "3":
        function("Wie zijn olympische kampioenen afkomstig uit Noord Korea?",
                 """SELECT ?northkorea
WHERE {
?northkorea dcterms:subject category-nl:Noord-Koreaans_olympisch_kampioen .
}""")

    if question_number == "4":
        function("Wie won de zilveren medaille voor de rodelwedstrijd voor dubbels tijdens de Olympische Winterspelen in 2014?",
                 """PREFIX dbpedia: <http://nl.dbpedia.org/resource/>
select ?medal where {
  dbpedia:Rodelen_op_de_Olympische_Winterspelen_2014_-_Dubbels dbpedia-owl:silverMedalist ?medal
}""")

    if question_number == "5":
        function("Hoe vaak heeft Kiribati ooit meegedaan aan de Olympische Spelen?", """
SELECT count(?kiribati)
WHERE {
?kiribati dcterms:subject category-nl:Kiribati_op_de_Olympische_Spelen .
}""")

    if question_number == "6":
        function("Hoeveel sporters uit Jamaica deden mee aan de Olympische Spelen in 2014?", """
PREFIX dbpedia: <http://nl.dbpedia.org/resource/>

select ?jamaica where {
  dbpedia:Jamaica_op_de_Olympische_Winterspelen_2014 dbpedia-owl:numberOfCompetitors ?jamaica
}""")

    if question_number == "7":
        function("Door wie werden de Olympische Spelen in 1936 geopend?", """PREFIX dbpedia: <http://nl.dbpedia.org/resource/>

select ?opener where {
  dbpedia:Olympische_Zomerspelen_1936 dbpedia-owl:officialOpenedBy ?opener
}""")

    if question_number == "8":
        function("Wanneer was korfbal een olympische sport?", """
SELECT ?jaar
WHERE {
?korfbal dcterms:subject category-nl:Korfbal_op_de_Olympische_Spelen .
?korfbal prop-nl:jaar ?jaar .
}""")

    if question_number == "9":
        function("Hoeveelste was Estland op de medailleranking tijdens de Zomerspelen in 2004?", """PREFIX dbpedia: <http://nl.dbpedia.org/resource/>

select ?rank where {
  dbpedia:Estland_op_de_Olympische_Zomerspelen_2004 dbpedia-owl:rankInFinalMedalCount ?rank
}""")

    if question_number == "10":
        function("Waar speelden de Olympische Spelen in 1976 zich af?", """PREFIX dbpedia: <http://nl.dbpedia.org/resource/>

select ?locatie where {
  dbpedia:Olympische_Zomerspelen_1976 dbpedia-owl:location ?locatie
}""")

main()
