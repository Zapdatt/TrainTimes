import requests
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import json

#Dictionaries för stationer och tider
stations_dict = {'Ingen':'', 'Arvika station': 'Ar', 'Charlottenberg station':'Cg', 'Degefors':'Dg', 'Fagerås':'Fgå', 'Karlskoga Dalbacksgatan':'Kasd', 'Karlskoga centrum':'Ksac', 'Karlstads central':'Ks', 'Karlstads yttre hamn':'Ksyh', 'Karlstad Välsviken':'Kvä', 'Karlstad östra':'Kö', 'Kil':'Kil', 'Kils omformarstation':'Kilo', 'Kristinehamn':'Khn', 'Molkom':'Mko', 'Sunne':'Sun', 'Säffle':'Sfl', 'Torsby':'Toy', 'Åmol':'Ål', 'Åmols djuphamn':'Åldj', 'Åmols östra':'Ålö', 'Reparationsplats, Kristinehamn':'Rkhn'}
timeHours = {0:0, 1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:10, 11:11, 12:12, 13:13, 14:14, 15:15, 16:16, 17:17, 18:18, 19:19, 20:20, 21:21, 22:22, 23:23}
timeMins = {00:00, 5:5, 10:10, 15:15, 20:20, 25:25, 30:30, 35:35, 40:40, 45:45, 50:50, 55:55}

#API nyckeln som används. 
api_key = '9fcb5b87d02d4edb92e6d5f85917ab7b'

#Funktion där variabler för tid1 och tid2 definieras. Tid1 används för avgång, tid2 för ankomst. Sedan hämtas trafikinfo från trafikverket.
def getDepartures():
    tid1 = str(fromTimeEntryH.get()) + ':' + str(fromTimeEntryM.get()) + ':' + '00'
    tid2 = str(toTimeEntryH.get()) + ':' + str(toTimeEntryM.get()) + ':' + '00'
    request = f"""<REQUEST>
<LOGIN authenticationkey="{api_key}" />
<QUERY objecttype="TrainAnnouncement" schemaversion="1.3" orderby="AdvertisedTimeAtLocation">
<FILTER>
<AND>
<EQ name="ActivityType" value="Avgang" />
<EQ name="LocationSignature" value="{stations_dict[stationerfr.get()]}" />
<OR>
<AND>
<GT name="AdvertisedTimeAtLocation" value="$dateadd({tid1})" />
<LT name="AdvertisedTimeAtLocation" value="$dateadd({tid2})" />
</AND>
</OR>
</AND>
</FILTER>
<INCLUDE>AdvertisedTrainIdent</INCLUDE>
<INCLUDE>AdvertisedTimeAtLocation</INCLUDE>
<INCLUDE>TrackAtLocation</INCLUDE>
<INCLUDE>ToLocation</INCLUDE>
<INCLUDE>ViaToLocation</INCLUDE>
</QUERY>
</REQUEST>"""

    url = 'https://api.trafikinfo.trafikverket.se/v1.3/data.json'
    response = requests.post(url, data = request, headers = {'Content-Type': 'text/xml'}, )

    response_json = json.loads(response.text)
    departures = response_json["RESPONSE"]['RESULT'][0]['TrainAnnouncement']

    stationer_text.delete(1.0,"end")

    #for loop där den valda stationen jämförs med ToLocation, ViaLocation och ViaFromLocation som alla finns i dep. 
    #Om det är samma läggs stationen samt datumet/tiden då avgången är till i stationer_text tillsammans med "Till: " och "Datum: ". 
    for dep in departures:
        to = stations_dict[stationerto.get()]
        if to == "" or dep['ToLocation'][0]['LocationName'] == to or dep['ViaToLocation'][0]['LocationName'] == to or dep['ViaFromLocation'][0]['LocationName'] == to:
            till = "Till: " + dep['ToLocation'][0]['LocationName']
            #tilln = list(stations_dict.keys())[list(stations_dict.values()).index(till)] Denna delen var menad att ta fram nyckeln (namnet på stationen) med hjälp av det man får ut, det fungerade inte men är kvar ifall det kanske går att fixa i framtiden.
            tid = "Datum: " + dep['AdvertisedTimeAtLocation']
            stationer_text.insert(1., till)
            stationer_text.insert(1., '\n')
            stationer_text.insert(1., tid)
            stationer_text.insert(1., '\n')

#Funktion för att byta plats på de valda stationerna. 
def swapDestinations():
    temp = None
    temp = stationerto.get()
    stationerto.set(stationerfr.get())
    stationerfr.set(temp)

#----------------------
#Början av tkinter... Root skapas och titeln ändras till tågtider. 
root = tk.Tk()
root.title('Tågtider')

#En canvas skapas och en bredd, höjd och bakgrundsfärg bestämms. 
canvas = tk.Canvas(root, height=500, width=400, bg="grey")
canvas.pack()

#En frame skapas och placeras
frame = tk.Frame(root, bg="dark grey")
frame.place(relwidth=1, relheight=0.8, relx=0, rely=0.1, )

#En font och label skapas och labeln placeras. (Fonten verkar inte fungera oavsett vad jag gör med den, men textens storlek ändrades så den fick stå kvar, fråga mig)
topTextFont = tkFont.Font(family="Arial")
stationtolabel = tk.Label(canvas, text="Tågtider", font="topTextFont", bg="grey", height="3", width="20")
stationtolabel.place(relx=0.5, rely=0)

#En knapp skapas och placeras, om man klickar körs funktionen getDepartures.
button=tk.Button(root, text='Hämta avgångar', fg='black', command= getDepartures)
button.place(relwidth=0.3, height=50)

#Två labels för avgång respektive ankomst skapas och placeras.
stationfrlabel = tk.Label(frame, text="Avgång",)
stationfrlabel.place(relx=0.04, rely=0.05)

stationtolabel = tk.Label(frame, text="Ankomst",)
stationtolabel.place(relx=0.04, rely=0.25)

#En combobox för till och en för från skapas. Här kan man välja varifrån och vart man vill söka. Dessa tittar i stations_dict.
#Defualt värdet sätts till ingen. 
stationerfr = ttk.Combobox(frame, state='readonly')
stationerfr['values'] = list(stations_dict.keys())
stationerfr.set('Ingen')
stationerfr.place(relx=0, rely=0.1)

stationerto = ttk.Combobox(frame, state='readonly')
stationerto['values'] = list(stations_dict.keys())
stationerto.set('Ingen')
stationerto.place(relx=0, rely=0.30)

#En knapp för att byta den valda stationen för ankomst och avgång skapas och placeras. Om den klickas körs funktionen swapDestinations
button=tk.Button(frame, text='swap', command= swapDestinations)
button.place(relx=0.4, rely=0.1, relheight=0.15)

#Fyra komboboxes skapas och placeras. Två för avgång och ankomst. I vardera kan man antingen välja timme eller minut. De tittar i timeHours och timeMins.
#Default sätts till 0 och 00 för avgång och 23 och 55 för ankomst.
fromTimeEntryH = ttk.Combobox(frame, state='readonly')
fromTimeEntryH['values'] = list(timeHours.keys())
fromTimeEntryH.set(0)
fromTimeEntryH.place(relx=0.04, rely=0.15, relwidth=0.1)
fromTimeEntryM = ttk.Combobox(frame, state='readonly')
fromTimeEntryM['values'] = list(timeMins.keys())
fromTimeEntryM.set(0)
fromTimeEntryM.place(relx=0.14, rely=0.15, relwidth=0.1)

toTimeEntryH = ttk.Combobox(frame, state='readonly')
toTimeEntryH['values'] = list(timeHours.keys())
toTimeEntryH.set(23)
toTimeEntryH.place(relx=0.04, rely=0.35, relwidth=0.1)
toTimeEntryM = ttk.Combobox(frame, state='readonly')
toTimeEntryM['values'] = list(timeMins.keys())
toTimeEntryM.set(55)
toTimeEntryM.place(relx=0.14, rely=0.35, relwidth=0.1)

#Ett textfält skapas och placeras. 
stationer_text = tk.Text(frame, bg="dark grey")
stationer_text.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

#Kör root
root.mainloop()