"""
Maak een programma dat het volgende in een opnieuw blijft doen zolang het draait:
1.	Vraag de gebruiker om zijn/haar naam en onthoud dat, als dit niet gedaan wordt maak de gebruiker dan anoniem
2.	Kies een random stationslocatie uit een lijst van 3
3.	Vraag de gebruiker om zijn/haar opmerking over het station en sla dat op
4.	Onthoud de tijd en datum waarop deze opmerking gemaakt is
5.	Sla deze gegevens bij elkaar op in een CSV
"""
import random
import time
locaties = ["Rotterdam", "Utrecht", "Den Haag"]

def opmerkingMaken():
    opmerking = input("Wat vind u van dit station? Max 140 karakters: ")
    if(len(opmerking) > 140):
        print("Sorry, het bericht dat u ingevoerd heeft is te lang, probeer het opnieuw.")
        return opmerkingMaken()
    elif(len(opmerking) == 0):
        print("Sorry, u heeft niks ingevoerd, probeer het opnieuw")
        return opmerkingMaken()
    return opmerking

while True:
    station = locaties[random.randint(0, 2)]
    naam = input("Goedendag, wat is uw naam? Om anoniem te blijven vul in 'anoniem': ")
    if(naam == ""):
        naam = "anoniem"
    opmerking = opmerkingMaken()
    datumTijd = time.strftime('%a %d %b %Y, %H:%M:%S', time.localtime())



