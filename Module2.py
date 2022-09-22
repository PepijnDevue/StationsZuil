"""
1.	Open het csv bestand met de informatie van de opmerkingen.
2.	Sla de data op in een 2D lijst.
3.	Loop door de opmerkingen van de lijst, laat ze 1 voor 1 van oud tot nieuw op het scherm zien.
4.	Geef per opmerking de gebruiker (de moderator) de optie om het goed of af te keuren.
5.	Als het goedgekeurd wordt speel stap 6 tm 7 af.
6.	Sla alle bijbehorende data van de opmerking op plus de datum en tijd van de beoordeling en het email adres van de moderator.
7.	Voeg deze data toe aan de postgre sql database.
8.	Ga door naar de volgende opmerking.
9.	Na het beoordelen van elke opmerking uit het csv bestand moet het gewist worden.
"""
import csv
import os
import time

def goedkeuren():
    goedkeuring = input("Als het bericht goed wordt gekeurd, typ 'goedgekeurd', anders typ 'afgekeurd': ")
    if (goedkeuring == "goedgekeurd"):
        return True
    elif (goedkeuring == "afgekeurd"):
        return False
    else:
        print("Oordeel niet goed geformeerd, typ aub 'goedgekeurd' of 'afgekeurd'")
        goedkeuren()

modNaam = input("Goedemiddag moderator van NS, wat is uw naam?: ")
modMail = input("Wat is uw werkmail?: ")
print("Dankuwel "+ modNaam + ", werkze!")
time.sleep(3)
os.system("CLS")

file = open('opmerkingen.csv', 'r')
reader = csv.reader(file)
data = list(reader)
file.close()

for i in data:
    if(i != []):
        print("Het bericht wordt hieronder getoond \n\n'" + i[0] + "'\n")
        goedkeuring = input("Als het bericht goed wordt gekeurd, typ 'goedgekeurd', anders typ 'afgekeurd': ")
        if (goedkeuring == "goedgekeurd"):
            goedgekeurd = True
            print("\nU heeft het bericht goedgekeurd")
        else:
            goedgekeurd = False
            print("\nU heeft het bericht afgekeurd")
        newData = i
        newData.append(goedgekeurd)
        newData.append(time.strftime('%a %d %b %Y, %H:%M:%S', time.localtime()))
        newData.append(modNaam)
        newData.append(modMail)
        print(newData)
        #-------------------------------------------------------------------------------
        #Voeg data toe aan PostgreSQL
        #-------------------------------------------------------------------------------
        time.sleep(3)
        os.system('CLS')

file = open('opmerkingen.csv', 'w')
writer = csv.writer(file)
writer.writerow([])
file.close()
