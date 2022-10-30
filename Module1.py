import random
import time
import csv
import os

locaties = ["Arnhem", "Utrecht", "Den Haag"]

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
    if(naam == "" or len(naam) > 30):
        naam = "anoniem"
    opmerking = opmerkingMaken()
    datumTijd = time.strftime('%a %d %b %Y, %H:%M:%S', time.localtime())
    file = open('opmerkingen.csv', 'a')
    writer = csv.writer(file)
    data = [opmerking, datumTijd, naam, station]
    writer.writerow(data)
    file.close()
    print("Bedankt voor uw feedback, we doen ons best om dagelijks te verbeteren, fijne dag!")
    time.sleep(5)
    os.system('CLS')


