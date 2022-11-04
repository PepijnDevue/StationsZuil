"""
1.  Laat de moderator inloggen met naam en mailadres, check of het mailadres al eerder is gebruikt, zo niet sla het op in de database
2.	Lees alle ongekeurde opmerkingen uit de datebase
3.	Sla de data op in een 2D lijst.
4.	Loop door de opmerkingen van de lijst, laat ze 1 voor 1 van oud tot nieuw op het scherm zien.
5.	Geef per opmerking de gebruiker (de moderator) de optie om het goed of af te keuren.
6.	Sla alle nieuwe bijhorende data op (keurdatumtijd, moderatormail en of het goedgekeurd is of niet).
7.	Update de informatie van de desbetreffende opmerking met deze data
8.	Ga door naar de volgende opmerking.
"""
# imports
import os
import time
import psycopg2


# function that checks whether the review has been accepted or rejected
def approve():
    # gets input
    moderation = input("Als het bericht goed wordt gekeurd, typ 'goedgekeurd', anders typ 'afgekeurd': ")

    # checks which of the two options have been chosen, if answer is unclear, repeats function
    if (moderation == "goedgekeurd"):
        return True
    elif (moderation == "afgekeurd"):
        return False
    else:
        print("Oordeel niet goed geformeerd, typ aub 'goedgekeurd' of 'afgekeurd'")
        return approve()

# input moderator logins
modName = input("Goedemiddag moderator van NS, wat is uw naam?: ")
modMail = input("Wat is uw werkmail?: ")
print("Dankuwel "+ modName + ", werkze!")

# makes connection with the database
file = open("postrgre_info.txt", "r")
data = (file.read()).split(";")
name = data[0]
password = data[1]
connection = psycopg2.connect(user=name, password=password, host="localhost", database="ProjectZuil")
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
    data = (modMail, modName)
    cursor.execute(query, data)
    connection.commit()

# wait 3 seconds and clear the CLI
time.sleep(3)
os.system("CLS")

# makes connection with the database
connection = psycopg2.connect(user=name, password=password, host="localhost", database="ProjectZuil")
cursor = connection.cursor()

# get all unmoderated reviews from the database
cursor.execute('select * from opmerking where goedgekeurd is null')
approveList = cursor.fetchall()

# saves database queries and closes connection
connection.commit()
cursor.close()
connection.close()

# loop through unmoderated reviews
for i in approveList:
    # shows the review on the screen and calls the moderating function
    print("Het bericht wordt hieronder getoond \n\n'" + i[2] + "'\n")
    moderation = approve()

    # confirm the moderators decision
    if (moderation == True):
        print("\nU heeft het bericht goedgekeurd")
    else:
        print("\nU heeft het bericht afgekeurd")

    # get the time of moderation
    dateTime = time.strftime('%a %d %b %Y, %H:%M:%S', time.localtime())

    # make connection with the database
    connection = psycopg2.connect(user=name, password=password, host="localhost", database="ProjectZuil")
    cursor = connection.cursor()

    # updates reviewdata with moderatingdata
    query = 'update opmerking set goedgekeurd = %s, keurdatumtijd = %s, mail = %s where opmerkingnr = %s'
    cursor.execute(query, (moderation, dateTime, modMail, i[0]))

    # saves database queries and closes connection
    connection.commit()
    cursor.close()
    connection.close()

    # waits 3 seconds and clear CLI
    time.sleep(3)
    os.system('CLS')