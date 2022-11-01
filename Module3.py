"""
Voor layout startscherm zie ('Layout scherm.jpg') en voor layout stationsscherm zie ('Layout2.jpg')
1.  Maak een keuzemenu met layout startscherm met 3 knoppen
2.  Open het scherm layout stationsscherm met de titel van het station
2.	Haal de laatste 5 opmerkingen over het station uit de database
3.	Haal de stationsfaciliteiten van het station uit de database
6.	Haal de weerinformatie van de stad van het station voor de komende uren
4.	Laat deze gegevens volgens de layout op het scherm zien
7.	Herhaal de volgende stappen tot het programma sluit
8.	Kijk elke 30 seconden of er nieuwe opmerkingen zijn
9.	Update de nieuwe informatie op het scherm
"""

# imports
from tkinter import *
import time
import psycopg2
from PIL import Image,ImageTk
import requests
from io import BytesIO


# start variables
ns_blue = "#%02x%02x%02x" % (0, 48, 130)
ns_light_blue = "#%02x%02x%02x" % (200, 220, 255)
reviews = []
usernames = []
review_date = []



# main function
def main():
    # root creation
    root = Tk()

    #image placeholders
    icon_image = None
    facility_img_lst = [None, None, None, None]


    # exit through ESCAPE function
    def exit_esc(key):
        if key.keysym == "Escape":
            root.destroy()
            quit()


    # exit through cross upper-right corner
    def exit_click():
        root.destroy()
        quit()


    # clock update function
    def clock_tick():
        current_time = time.strftime('%H:%M', time.localtime())
        clock.config(text=current_time)
        root.after(1000, clock_tick)


    # update reviews function
    def update_reviews(cursor):
        # delete current review gui elements
        canvas.delete("reviews_tag")
        canvas.delete("usernames_tag")
        canvas.delete("review_date_tag")

        # get 5 reviews from database
        query = "select * from opmerking where goedgekeurd = 'true' order by opmerkingnr desc limit 5;"
        cursor.execute(query)
        data = cursor.fetchall()

        # loop through list of reviews
        for i in range(len(data)):
            # retrieves usefull information out of the query
            date = str(data[i][1]).split(" ")[0].split('-')[2] + "-" + str(data[i][1]).split(" ")[0].split("-")[1]
            review = data[i][2]
            user = data[i][3]

            # calculation for y-placement of each review
            y = i * 110 + 100

            # resizes font and lines according to review-length
            if (len(review) <= 35):
                # single big line for short reviews
                reviews.append(canvas.create_text(100, y + 45, text=review, fill=ns_blue, font='Sans 35', anchor='nw',tag='reviews_tag'))
            elif (len(review) > 60):
                # two small lines for long reviews
                review1 = review[slice(0, len(review) // 2)]
                review2 = review[slice(len(review) // 2, len(review))]
                reviews.append(canvas.create_text(100, y + 45, text=review1 + "\n" + review2, fill=ns_blue,font='Sans 14', anchor='nw', tag='reviews_tag'))
            else:
                # single small line for medium reviews
                reviews.append(canvas.create_text(100, y + 45, text=review, fill=ns_blue, font='Sans 14', anchor='nw',tag='reviews_tag'))

            # puts username and date of the review on the screen
            usernames.append(canvas.create_text(15, y + 5, text=user, fill=ns_blue, font='Sans 20', anchor='nw',tag='usernames_tag'))
            review_date.append(canvas.create_text(790, y, text=date, fill=ns_blue, font='Sans 20', anchor='ne',tag='bericht_data_tag'))

        # repeats itself after 30 seconds
        root.after(30000, update_reviews)


    # enter main screen after choosing a station
    def enter_screen(station):
        # get image placeholders
        global icon_image, facility_img_lst

        # direct drawing
        canvas.create_rectangle(0, 100, 800, 210, fill=ns_light_blue)
        canvas.create_rectangle(0, 320, 800, 430, fill=ns_light_blue)
        canvas.create_rectangle(0, 540, 800, 650, fill=ns_light_blue)
        canvas.create_rectangle(800, 100, 1280, 650, fill=ns_light_blue)
        canvas.create_line(0, 210, 800, 210, fill=ns_blue)
        canvas.create_line(0, 320, 800, 320, fill=ns_blue)
        canvas.create_line(0, 430, 800, 430, fill=ns_blue)
        canvas.create_line(0, 540, 800, 540, fill=ns_blue)
        canvas.create_line(800, 0, 800, 720, fill=ns_blue)
        canvas.create_text(20, 12, text=station, fill="white", font=('Sans 50 bold'), anchor='nw')


        # requests weather info of according city in Dutch
        city = requests.get("https://api.openweathermap.org/data/2.5/weather?q={}&lang=nl&appid=b59def085bea9cb5dad8e6dff7cc627f".format(station)).json()

        # get data out of the info
        description = city['weather'][0]['description']
        tempC = str(round(city['main']['temp'] - 273.15))
        windpower = str(round(((city['wind']['speed'] / 0.836) ** 2) ** (1 / 3)))

        # get icon image
        icon = "http://openweathermap.org/img/wn/{}@2x.png".format(city['weather'][0]['icon'])
        img_data = requests.get(icon).content
        icon_image = ImageTk.PhotoImage((Image.open(BytesIO(img_data))).resize((250, 250)))

        # put weather data on the screen
        canvas.create_image(1100, 400, image=icon_image)
        canvas.create_text(1250, 150, text=tempC + '\N{DEGREE SIGN}', font='Sans 70 bold', anchor='ne')
        canvas.create_text(1260, 500, text='Windkracht ' + windpower, font='Sans 30 bold', anchor='ne')
        canvas.create_text(1260, 550, text=description.capitalize(), font='Sans 30 bold', anchor='ne')


        # get user info for acces to the database
        file = open("postrgre_info.txt", "r")
        data = (file.read()).split(";")
        name = data[0]
        ww = data[1]

        # establish database connection
        connection = psycopg2.connect(user=name, password=ww, host="localhost", database="ProjectZuil")
        cursor = connection.cursor()

        # get stationinfo from according station
        query = 'SELECT * FROM station where stationnaam = %s'
        cursor.execute(query, (station,))
        data = cursor.fetchall()

        # get facilitydata from the info
        facility_lst = []
        if data[0][2]:
            facility_lst.append("ovfiets")
        if data[0][3]:
            facility_lst.append("lift")
        if data[0][4]:
            facility_lst.append("pr")
        if data[0][5]:
            facility_lst.append("toilet")

        # create images of facilitydata
        facility_img_lst = []
        for i in range(len(facility_lst)):
            # put faciltyicons on the screen
            facility_img_lst.append(ImageTk.PhotoImage(Image.open("img_{}.png".format(facility_lst[i]))))
            canvas.create_image(1250 - i * 80, 685, image=facility_img_lst[i])

        # Messages
        update_reviews(cursor)


    # exit menu function
    def exit_menu(option):
        # destroy menu gui elements
        canvas.delete("menu_tag")
        utrecht_button.destroy()
        arnhem_button.destroy()
        den_haag_button.destroy()

        #call enter_screen function with chosen station
        enter_screen(option)

    # create a canvas
    canvas = Canvas(root, height=720, width=1280)

    # direct drawing for the optionmenu
    canvas.create_rectangle(0, 0, 1280, 100, fill=(ns_blue))
    canvas.create_rectangle(0, 620, 1280, 720, fill=(ns_blue))
    canvas.create_text(640, 200, text="Goedemorgen,", fill=ns_blue, font=('Sans 50 bold'), tag='menu_tag')
    canvas.create_text(640, 300, text="Kies een station:", fill=ns_blue, font=('Sans 50 bold'), tag='menu_tag')

    # create a clock
    clock = Label(canvas, text="", font=('Sans 50 bold'), bg=ns_blue, fg="white")
    clock.place(x=1100, y=10)
    clock_tick()

    # create buttons that will lead to main screen
    utrecht_button = Button(canvas, text="Utrecht", command=lambda: exit_menu("Utrecht"), bd=4, fg=ns_blue,font="Sans 30 bold")
    utrecht_button.place(x=200, y=400)
    arnhem_button = Button(canvas, text="Arnhem", command=lambda: exit_menu("Arnhem"), bd=4, fg=ns_blue, font="Sans 30 bold")
    arnhem_button.place(x=540, y=400)
    den_haag_button = Button(canvas, text="Den Haag", command=lambda: exit_menu("Den Haag"), bd=4, fg=ns_blue, font="Sans 30 bold")
    den_haag_button.place(x=880, y=400)
    canvas.focus_set()

    # exit accessibility
    canvas.bind('<KeyPress>', exit_esc)
    root.protocol("WM_DELETE_WINDOW", exit_click)

    # draw all current canvas elements on the screen and loop gui code
    canvas.pack()
    root.mainloop()

# start code if directly played
if __name__ == "__main__":
    main()
