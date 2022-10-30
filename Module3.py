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
import requests
from io import BytesIO

def menu_klok_tick():
    try:
        global Canvas, klok
        tijd = time.strftime('%H:%M', time.localtime())
        klok.config(text=tijd)
        root.after(1000, menu_klok_tick)
    except:
        pass

def main_klok_tick():
    try:
        global Canvas, main_klok
        tijd = time.strftime('%H:%M', time.localtime())
        main_klok.config(text=tijd)
        root.after(1000, main_klok_tick)
    except:
        pass


def exit_main_esc(key):
    global main_root
    if key.keysym == "Escape":
        main_root.destroy()
        quit()

def exit_main_click():
    global main_root
    main_root.destroy()
    quit()


def main_layout(stad):
    global main_root, main_klok
    main_root = Tk()
    main_canvas = Canvas(main_root, height=720, width=1280)
    ns_blue = "#%02x%02x%02x" % (0, 48, 130)
    ns_light_blue = "#%02x%02x%02x" % (200, 220, 255)

    #lines  etc
    main_canvas.create_rectangle(0, 100, 800, 210, fill=ns_light_blue)
    main_canvas.create_rectangle(0, 320, 800, 430, fill=ns_light_blue)
    main_canvas.create_rectangle(0, 540, 800, 650, fill=ns_light_blue)
    main_canvas.create_rectangle(800, 100, 1280, 650, fill=ns_light_blue)
    main_canvas.create_line(0, 210, 800, 210, fill=ns_blue)
    main_canvas.create_line(0, 320, 800, 320, fill=ns_blue)
    main_canvas.create_line(0, 430, 800, 430, fill=ns_blue)
    main_canvas.create_line(0, 540, 800, 540, fill=ns_blue)
    main_canvas.create_rectangle(800, 0, 803, 720, fill=ns_blue)
    main_canvas.create_rectangle(0, 0, 1280, 100, fill=(ns_blue))
    main_canvas.create_rectangle(0, 650, 1280, 720, fill=(ns_blue))
    main_canvas.create_text(160, 50, text=stad, fill="white", font=('Sans 50 bold'))


    #weather
    city = requests.get("https://api.openweathermap.org/data/2.5/weather?q=Utrecht&lang=nl&appid=b59def085bea9cb5dad8e6dff7cc627f").json()
    description = city['weather'][0]['description']
    icon = "http://openweathermap.org/img/wn/{}@2x.png".format(city['weather'][0]['icon'])
    tempC = city['main']['temp'] - 273.15
    windspeed = city['wind']['speed']
    img_data = requests.get(icon).content
    icon_image = ImageTk.PhotoImage((Image.open(BytesIO(img_data))).resize((250, 250)))
    main_canvas.create_image(1100, 400, image=icon_image)



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
        main_canvas.create_image(1250 - i*80, 685, image=facility_img_lst[i])


    #Messages
    query = "select * from opmerking where stationnaam = %s and goedgekeurd = 'true' order by opmerkingnr desc limit 5;"
    cursor.execute(query, (stad,))
    data = cursor.fetchall()
    opmerkingen = []
    gebruikersnamen = []
    bericht_data = []
    for i in range(len(data)):
        datum = str(data[i][1]).split(" ")[0].split('-')[2] + "-" + str(data[i][1]).split(" ")[0].split("-")[1]
        opmerking = data[i][2]
        gebruiker = data[i][3]
        y = i*110 + 160
        opmerkingen.append(main_canvas.create_text(200, y, text=opmerking, fill=ns_blue, font='Sans 35'))
        gebruikersnamen.append(main_canvas.create_text(50, y - 45, text=gebruiker, fill=ns_blue, font='Sans 20'))
        bericht_data.append(main_canvas.create_text(760, y - 45, text=datum, fill=ns_blue, font='Sans 20'))

    #aanpassen fontgrootte en x-waarde bericht en gebruikersnaam met lengte bericht



    #Clock
    main_klok = Label(text="dcf", font=('Sans 50 bold'), bg=ns_blue, fg="white")
    main_klok.place(x=1100, y=10)
    main_klok_tick()

    #exit usage
    main_canvas.focus_set()
    main_canvas.bind('<KeyPress>', exit_main_esc)
    main_root.protocol("WM_DELETE_WINDOW", exit_main_click)

    main_canvas.pack()
    main_root.mainloop()

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
    menu_klok_tick()
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