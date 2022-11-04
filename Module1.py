"""
1. Laat de gebruiker een opmerking maken
2. Kijk of het niet te lang of te kort is
3. Kies een random station
4. Laat de gebruiker een naam invoeren
5. Als er niks wordt ingevoerd of de naam te lang is, vul 'anoniem'in
6. Haalt de tijd van de opmerking op
7. Schrijft de volgende data bij in het CSV bestand
8. Herhaal alle stappen tot het programma wordt gesloten
"""

# imports
import random
import time
import os
import psycopg2

# list of possible locations
locaties = ["Arnhem", "Utrecht", "Den Haag"]


# a function the lets the user input a review
def opmerkingMaken():
    # input a review
    opmerking = input("Wat vind u van dit station? Max 140 karakters: ")
    # if too long or too short, give errormessage and try again, otherwise return the review
    if(len(opmerking) > 140):
        print("Sorry, het bericht dat u ingevoerd heeft is te lang, probeer het opnieuw.")
        return opmerkingMaken()
    elif(len(opmerking) == 0):
        print("Sorry, u heeft niks ingevoerd, probeer het opnieuw")
        return opmerkingMaken()
    return opmerking


# while the code is running repeat the following
while True:
    # choose a random station out of the 3
    station = locaties[random.randint(0, 2)]

    # input a username
    naam = input("Goedendag, wat is uw naam? Om anoniem te blijven vul in 'anoniem': ")
    if(naam == "" or len(naam) > 30):
        # sets username to anonymous if too short or too long
        naam = "anoniem"

    # calls review function
    opmerking = opmerkingMaken()

    # get time at which the review has been made
    datumTijd = time.strftime('%a %d %b %Y, %H:%M:%S', time.localtime())

    # makes connection with the database
    file = open("postrgre_info.txt", "r")
    data = (file.read()).split(";")
    name = data[0]
    ww = data[1]
    connection = psycopg2.connect(user=name, password=ww, host="localhost", database="ProjectZuil")
    cursor = connection.cursor()

    # takes the next review id out of the database
    cursor.execute('select * from opmerking')
    opmerkingnr = len(cursor.fetchall())

    data = (opmerkingnr, opmerking, datumTijd, naam, station)
    # pushes data to the database
    query = "INSERT INTO opmerking (opmerkingnr, opmerking, datumtijd, gebruikersnaam, stationnaam) VALUES (%s,%s,%s,%s,%s)"
    cursor.execute(query, data)

    # saves database queries and closes connection
    connection.commit()
    cursor.close()
    connection.close()

    #   thank user, wait 5 seconds and clear CLI
    print("Bedankt voor uw feedback, we doen ons best om dagelijks te verbeteren, fijne dag!")
    time.sleep(5)
    os.system('CLS')


