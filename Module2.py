"""
1.  Laat de moderator inloggen met naam en mailadres, check of het mailadres al eerder is gebruikt, zo niet sla het op in de database
2.	Open het csv bestand met de informatie van de opmerkingen.
3.	Sla de data op in een 2D lijst.
4.	Loop door de opmerkingen van de lijst, laat ze 1 voor 1 van oud tot nieuw op het scherm zien.
5.	Geef per opmerking de gebruiker (de moderator) de optie om het goed of af te keuren.
6.	Sla alle bijbehorende data van de opmerking, of het goedgekeurd is of niet op plus de datum en tijd van de beoordeling en het email adres van de moderator.
7.	Voeg deze data toe aan de postgre sql database.
8.	Ga door naar de volgende opmerking.
9.	Na het beoordelen van elke opmerking uit het csv bestand moet het gewist worden.
"""
# imports
import csv
import os
import time
import psycopg2


# function that checks wether the review has been accepted or rejected
def goedkeuren():
    # gets input
    goedkeuring = input("Als het bericht goed wordt gekeurd, typ 'goedgekeurd', anders typ 'afgekeurd': ")

    # checks which of the two options have been chosen, if answer is unclear, repeats function
    if (goedkeuring == "goedgekeurd"):
        return True
    elif (goedkeuring == "afgekeurd"):
        return False
    else:
        print("Oordeel niet goed geformeerd, typ aub 'goedgekeurd' of 'afgekeurd'")
        return goedkeuren()

# input moderator logins
modNaam = input("Goedemiddag moderator van NS, wat is uw naam?: ")
modMail = input("Wat is uw werkmail?: ")
print("Dankuwel "+ modNaam + ", werkze!")

# makes connection with the database
file = open("postrgre_info.txt", "r")
data = (file.read()).split(";")
name = data[0]
ww = data[1]
connection = psycopg2.connect(user=name, password=ww, host="localhost", database="ProjectZuil")
cursor = connection.cursor()

# checks if mail has been used before
cursor.execute('SELECT * FROM moderator')
itterations = 0
duplicate = False
for i in cursor.fetchall():
    itterations += 1
    if (i[0] == modMail):
        duplicate = True

# if mail has not been used before, put the moderator logins in the database
if itterations == 0 or duplicate == False:
    query = "INSERT INTO moderator (mail, naam) VALUES (%s,%s)"
    data = (modMail, modNaam)
    cursor.execute(query, data)
    connection.commit()

# wait 3 seconds and clear the CLI
time.sleep(3)
os.system("CLS")

# opens CSV file and reads the review data
file = open('opmerkingen.csv', 'r')
reader = csv.reader(file)
data = list(reader)
file.close()

#loops through the list of reviews
for i in data:
    if(i != []):
        # shows the review on the screen and calls the moderating function
        print("Het bericht wordt hieronder getoond \n\n'" + i[0] + "'\n")
        goedgekeurd = goedkeuren()

        # confirm the moderators decision
        if (goedgekeurd == True):
            print("\nU heeft het bericht goedgekeurd")
        else:
            print("\nU heeft het bericht afgekeurd")

        # connect to the database
        connection = psycopg2.connect(user=name, password=ww, host="localhost", database="ProjectZuil")
        cursor = connection.cursor()

        # takes the next review id out of the database
        cursor.execute('select * from opmerking')
        opmerkingnr = len(cursor.fetchall())

        # puts all necesarry data in a tuple (reviewID, review, reviewdata, username, station, wether the review has been accepted or not, moderatingdate, moderatormail)
        newData = (opmerkingnr, i[0], i[1], i[2], i[3], goedgekeurd, time.strftime('%a %d %b %Y, %H:%M:%S', time.localtime()), modMail)

        # pushes data to the database
        query = "INSERT INTO opmerking (opmerkingnr, opmerking, datumtijd, gebruikersnaam, stationnaam, goedgekeurd, keurdatumtijd, mail) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query, newData)

        # saves database queries and closes connection
        connection.commit()
        cursor.close()
        connection.close()

        # waits 3 seconds and clear CLI
        time.sleep(3)
        os.system('CLS')

# clears CSV file
file = open('opmerkingen.csv', 'w')
writer = csv.writer(file)
writer.writerow([])
file.close()
