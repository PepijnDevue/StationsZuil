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

def main_layout(stad):
    #layout
    print(stad)

root = Tk()

def enter_main(stad):
    global root
    root.destroy()
    main_layout(stad)
def menu_layout():
    canvas = Canvas(root, height=720, width=1280)
    ns_blue = "#%02x%02x%02x" % (0, 48, 130)
    canvas.create_rectangle(0, 0, 1280, 100, fill=(ns_blue))
    canvas.create_rectangle(0, 620, 1280, 720, fill=(ns_blue))
    canvas.create_text(640, 200, text="Goedemorgen,", fill=ns_blue, font=('Sans 50 bold'))
    canvas.create_text(640, 300, text="Kies een station:", fill=ns_blue, font=('Sans 50 bold'))
    utrecht_knop = Button(canvas, text= "Utrecht", command= lambda: enter_main("Utrecht"), bd = 4, fg = ns_blue, font="Sans 30 bold")
    utrecht_knop.place(x=200, y=400)
    arnhem_knop = Button(canvas, text="Arnhem", command=lambda: enter_main("Arnhem"), bd = 4, fg = ns_blue, font="Sans 30 bold")
    arnhem_knop.place(x=540, y=400)
    den_haag_knop = Button(canvas, text="Den Haag", command=lambda: enter_main("Den Haag"), bd = 4, fg = ns_blue, font="Sans 30 bold")
    den_haag_knop.place(x=880, y=400)
    canvas.pack()
    root.mainloop()




def updatedb():
    #update laatste 5 opmerkingen (1 minuut)
    db = 1


def update_weather():
    #refresh weather info (5 sec)
    weather = 1


def main_loop():
    menu_layout()
    while True:
        updatedb()
        update_weather()

main_loop()