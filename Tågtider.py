import requests
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import json

stations_dict = {'Ingen':'', 'Arvika station': 'Ar', 'Charlottenberg station':'Cg', 'Degefors':'Dg', 'Fagerås':'Fgå', 'Karlskoga Dalbacksgatan':'Kasd', 'Karlskoga centrum':'Ksac', 'Karlstads central':'Ks', 'Karlstads yttre hamn':'Ksyh', 'Karlstad Välsviken':'Kvä', 'Karlstad östra':'Kö', 'Kil':'Kil', 'Kils omformarstation':'Kilo', 'Kristinehamn':'Khn', 'Molkom':'Mko', 'Sunne':'Sun', 'Säffle':'Sfl', 'Torsby':'Toy', 'Åmol':'Ål', 'Åmols djuphamn':'Åldj', 'Åmols östra':'Ålö', 'Reparationsplats, Kristinehamn':'Rkhn'}
timeHours = {1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:10, 11:11, 12:12, 13:13, 14:14, 15:15, 16:16, 17:17, 18:18, 19:19, 20:20, 21:21, 22:22, 23:23, 24:24}
timeMins = {00:00, 5:5, 10:10, 15:15, 20:20, 25:25, 30:30, 35:35, 40:40, 45:45, 50:50, 55:55}

api_key = '9fcb5b87d02d4edb92e6d5f85917ab7b'

def getDepartures():
    request = f"""<REQUEST>
<LOGIN authenticationkey="{api_key}" />
<QUERY objecttype="TrainAnnouncement" schemaversion="1.3" orderby="AdvertisedTimeAtLocation">
<FILTER>
<AND>
<EQ name="ActivityType" value="Avgang" />
<EQ name="LocationSignature" value="{stations_dict[stationerfr.get()]}" />
<OR>
<AND>
<GT name="AdvertisedTimeAtLocation" value="$dateadd(05:00:00)" />
<LT name="AdvertisedTimeAtLocation" value="$dateadd(10:00:00)" />
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

    for dep in departures:
        to = stations_dict[stationerto.get()]
        if (to == ""):
            stationer_text.insert(1., dep)
            stationer_text.insert(1., '\n')
        if (dep['ToLocation'][0]['LocationName'] == to):
            stationer_text.insert(1., dep)
            stationer_text.insert(1., '\n')
        elif (dep['ViaToLocation'][0]['LocationName'] == to):
            stationer_text.insert(1., dep)
            stationer_text.insert(1., '\n')
        elif (dep['ViaFromLocation'][0]['LocationName'] == to):
            stationer_text.insert(1., dep)
            stationer_text.insert(1., '\n')

def swapDestinations():
    temp = None
    temp = stationerto.get()
    stationerto.set(stationerfr.get())
    stationerfr.set(temp)

#----------------------
root = tk.Tk()
root.title('Tågtider')

canvas = tk.Canvas(root, height=500, width=400, bg="grey")
canvas.pack()

frame = tk.Frame(root, bg="dark grey")
frame.place(relwidth=1, relheight=0.8, relx=0, rely=0.1, )

logoFont = tkFont.Font(family="Agency FB", size="60")
stationtolabel = tk.Label(canvas, text="Tågtider", font="logoFont", bg="grey", height="3", width="20")
stationtolabel.place(relx=0.7, rely=0)

button=tk.Button(root, text='Hämta avgångar', fg='red', command= getDepartures)
button.place(relwidth=0.3, height=50)

stationfrlabel = tk.Label(frame, text="Avgång",)
stationfrlabel.place(relx=0.04, rely=0.05)

stationtolabel = tk.Label(frame, text="Ankomst",)
stationtolabel.place(relx=0.04, rely=0.25)

stationerfr = ttk.Combobox(frame, state='readonly')
stationerfr['values'] = list(stations_dict.keys())
stationerfr.set('Ingen')
stationerfr.place(relx=0, rely=0.1)

stationerto = ttk.Combobox(frame, state='readonly')
stationerto['values'] = list(stations_dict.keys())
stationerto.set('Ingen')
stationerto.place(relx=0, rely=0.30)

button=tk.Button(frame, text='swap', command= swapDestinations)
button.place(relx=0.4, rely=0.1, relheight=0.15)

fromTimeEntryH = ttk.Combobox(frame, state='readonly')
fromTimeEntryH['values'] = list(timeHours.keys())
fromTimeEntryH.place(relx=0.04, rely=0.15, relwidth=0.1)
fromTimeEntryM = ttk.Combobox(frame, state='readonly')
fromTimeEntryM['values'] = list(timeMins.keys())
fromTimeEntryM.place(relx=0.14, rely=0.15, relwidth=0.1)

toTimeEntryH = ttk.Combobox(frame, state='readonly')
toTimeEntryH['values'] = list(timeHours.keys())
toTimeEntryH.place(relx=0.04, rely=0.35, relwidth=0.1)
toTimeEntryM = ttk.Combobox(frame, state='readonly')
toTimeEntryM['values'] = list(timeMins.keys())
toTimeEntryM.place(relx=0.14, rely=0.35, relwidth=0.1)

stationer_text = tk.Text(frame, bg="dark grey")
stationer_text.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

root.mainloop()