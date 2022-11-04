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
import psycopg2
from tkinter import *
import time


ns_blue = "#%02x%02x%02x" % (0, 48, 130)
ns_light_blue = "#%02x%02x%02x" % (200, 220, 255)


# main function
def main():

    # get logins for database
    file = open("postrgre_info.txt", "r")
    data = (file.read()).split(";")
    dbusername = data[0]
    password = data[1]


    # clock update function
    def clock_tick():
        current_time = time.strftime('%H:%M', time.localtime())
        clock.config(text=current_time)
        root.after(1000, clock_tick)


    # enter moderatingscreen function
    def enter_screen():
        global  approveList, i

        # makes connection with the database
        connection = psycopg2.connect(user=dbusername, password=password, host="localhost", database="ProjectZuil")
        cursor = connection.cursor()

        # get all unmoderated reviews from the database
        cursor.execute('select * from opmerking where goedgekeurd is null')
        approveList = cursor.fetchall()

        # saves database queries and closes connection
        connection.commit()
        cursor.close()
        connection.close()
        i = 0

        def next_review(approved):
            global i

            # get the time of moderation
            dateTime = time.strftime('%a %d %b %Y, %H:%M:%S', time.localtime())

            # make connection with the database
            connection = psycopg2.connect(user=dbusername, password=password, host="localhost", database="ProjectZuil")
            cursor = connection.cursor()

            # updates reviewdata with moderatingdata
            print(i)
            query = 'update opmerking set goedgekeurd = %s, keurdatumtijd = %s, mail = %s where opmerkingnr = %s'
            cursor.execute(query, (approved, dateTime, modMail, approveList[i][0]))

            # saves database queries and closes connection
            connection.commit()
            cursor.close()
            connection.close()

            i += 1
            if len(approveList) > i:
                review.config(text=approveList[i][2])
            else:
                goed.destroy()
                nietgoed.destroy()
                review.destroy()
                canvas.create_text(640, 360, text="Dat waren de opmerkingen, bedankt!", anchor='center', font='Sans 50 bold', fill=ns_blue)
                root.after(3000, exit)

        if name.get() != "" and mail.get() != "":
            modName = name.get()
            modMail = mail.get()

            canvas.delete('start')
            name.destroy()
            mail.destroy()
            login.destroy()
            # make connection with the database
            connection = psycopg2.connect(user=dbusername, password=password, host="localhost", database="ProjectZuil")
            cursor = connection.cursor()

            # checks if mail has been used before
            cursor.execute('SELECT * FROM moderator')
            itterations = 0
            duplicate = False
            for data in cursor.fetchall():
                itterations += 1
                if (data[0] == modMail):
                    duplicate = True

            # if mail has not been used before, put the moderator logins in the database
            if itterations == 0 or duplicate == False:
                query = "INSERT INTO moderator (mail, naam) VALUES (%s,%s)"
                data = (modMail, modName)
                cursor.execute(query, data)
            connection.commit()
            cursor.close()
            connection.close()



            review = Label(canvas, text=approveList[0][2], font=('Sans 50 bold'), fg=ns_blue)
            review.place(x=640, y=250, anchor='n')

            goed = Button(canvas, text="goedgekeurd", command= lambda: next_review(True), bd=4, fg=ns_blue, font="Sans 30 bold")
            goed.place(x=330, y=450)

            nietgoed = Button(canvas, text="afgekeurd", padx=35, command=lambda: next_review(False), bd=4, fg=ns_blue, font="Sans 30 bold")
            nietgoed.place(x=675, y=450)



    root = Tk()

    canvas = Canvas(root, height=720, width=1280)

    canvas.create_rectangle(0, 0, 1280, 100, fill=(ns_blue))
    canvas.create_rectangle(0, 620, 1280, 720, fill=(ns_blue))
    canvas.create_text(640, 180, text="Goedendag moderator van NS", anchor='n', font='Sans 40 bold', fill=ns_blue, tag='start')
    canvas.create_text(420, 310, text='Naam:', font='Sans 20', fill=ns_blue, anchor='nw', tag='start')
    canvas.create_text(420, 400, text='Mail:', font='Sans 20', fill=ns_blue, anchor='nw', tag='start')

    name = Entry(canvas, font='Sans 20', fg=ns_blue, justify='center', width=20)
    name.place(x = 510, y= 310)

    mail = Entry(canvas, font='Sans 20', fg=ns_blue, justify='center', width=20)
    mail.place(x=510, y=400)

    login = Button(canvas, text="Log in", command=enter_screen, bd=4, fg=ns_blue,font="Sans 20")
    login.place(x=600, y=500)

    canvas.focus_set()

    # create a clock
    clock = Label(canvas, text="", font=('Sans 50 bold'), bg=ns_blue, fg="white")
    clock.place(x=1100, y=10)
    clock_tick()

    canvas.pack()
    root.mainloop()

if __name__ == "__main__":
    main()