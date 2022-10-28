"""
Voor layout startscherm zie ('Layout scherm.jpg') en voor layout stationsscherm zie ('Layout2.jpg')
1.  Maak een keuzemenu met layout startscherm met 3 knoppen
2.  Open het scherm layout2 met de titel van het station
2.	Haal de laatste 5 opmerkingen over het station uit de database
3.	Haal de stationsfaciliteiten van het station uit de database
6.	Haal de weerinformatie van de stad van het station voor de komende uren
4.	Laat deze gegevens volgens de layout op het scherm zien
7.	Herhaal de volgende stappen tot het programma sluit
8.	Haal elke 5 minuten nieuwe weerinformatie op
9.	Kijk elke 5 seconden of er nieuwe opmerkingen zijn
10.	Update de nieuwe informatie op t scherm
"""
from tkinter import *
import time
import psycopg2
from PIL import Image,ImageTk

def menu_klok():
    try:
        global Canvas, klok
        tijd = time.strftime('%H:%M', time.localtime())
        klok.config(text=tijd)
        root.after(1000, menu_klok)
    except:
        pass

def main_layout(stad):
    root = Tk()
    canvas = Canvas(root, height=720, width=1280)
    ns_blue = "#%02x%02x%02x" % (0, 48, 130)

    #lines  etc
    canvas.create_rectangle(0, 0, 1280, 100, fill=(ns_blue))
    canvas.create_rectangle(0, 650, 1280, 720, fill=(ns_blue))
    canvas.create_text(160, 50, text=stad, fill="white", font=('Sans 50 bold'))

    #weather

    #facilities
    file = open("postrgre_info.txt", "r")
    data = (file.read()).split(";")
    name = data[0]
    ww = data[1]
    connection = psycopg2.connect(user=name, password=ww, host="localhost", database="ProjectZuil")
    cursor = connection.cursor()
    query = 'SELECT * FROM station where stationnaam = %s'
    cursor.execute(query, (stad,))
    data = cursor.fetchall()
    facility_lst = []
    if data[0][2]:
        facility_lst.append("ovfiets")
    if data[0][3]:
        facility_lst.append("lift")
    if data[0][4]:
        facility_lst.append("pr")
    if data[0][5]:
        facility_lst.append("toilet")
    facility_img_lst = []
    for i in range(len(facility_lst)):
        facility_img_lst.append(ImageTk.PhotoImage(Image.open("img_{}.png".format(facility_lst[i]))))
        canvas.create_image(1250 - i*80, 685, image=facility_img_lst[i])


    #Messages

    #Clock
    klok = Label(text="", font=('Sans 50 bold'), bg=ns_blue, fg="white")
    klok.place(x=1100, y=10)
    menu_klok()

    canvas.pack()
    root.mainloop()

root = Tk()

def enter_main(stad):
    global root
    root.destroy()
    main_layout(stad)

def exit_menu_esc(key):
    if key.keysym == "Escape":
        root.destroy()
        quit()

def exit_menu_click():
    root.destroy()
    quit()

def menu_layout():
    global klok
    canvas = Canvas(root, height=720, width=1280)
    ns_blue = "#%02x%02x%02x" % (0, 48, 130)
    canvas.create_rectangle(0, 0, 1280, 100, fill=(ns_blue))
    canvas.create_rectangle(0, 620, 1280, 720, fill=(ns_blue))
    canvas.create_text(640, 200, text="Goedemorgen,", fill=ns_blue, font=('Sans 50 bold'))
    canvas.create_text(640, 300, text="Kies een station:", fill=ns_blue, font=('Sans 50 bold'))
    klok = Label(text="", font=('Sans 50 bold'), bg=ns_blue, fg="white")
    klok.place(x=1100, y=10)
    menu_klok()
    utrecht_knop = Button(canvas, text= "Utrecht", command= lambda: enter_main("Utrecht"), bd = 4, fg = ns_blue, font="Sans 30 bold")
    utrecht_knop.place(x=200, y=400)
    arnhem_knop = Button(canvas, text="Arnhem", command=lambda: enter_main("Arnhem"), bd = 4, fg = ns_blue, font="Sans 30 bold")
    arnhem_knop.place(x=540, y=400)
    den_haag_knop = Button(canvas, text="Den Haag", command=lambda: enter_main("Den Haag"), bd = 4, fg = ns_blue, font="Sans 30 bold")
    den_haag_knop.place(x=880, y=400)
    canvas.focus_set()
    canvas.bind('<KeyPress>', exit_menu_esc)
    root.protocol("WM_DELETE_WINDOW", exit_menu_click)
    canvas.pack()
    root.mainloop()


def updatedb():
    #update laatste 5 opmerkingen (1 minuut)
    pass


def update_weather():
    #refresh weather info (5 sec)
    pass


def main_loop():
    menu_layout()
    while True:
        updatedb()
        update_weather()

main_loop()