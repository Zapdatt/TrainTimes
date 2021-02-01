import requests
import tkinter as tk
from tkinter import ttk
import json

stations_dict = {'Arvika station': 'Ar', 'Charlottenberg station':'Cg', 'Degefors':'Dg', 'Fagerås':'Fgå', 'Karlskoga Dalbacksgatan':'Kasd', 'Karlskoga centrum':'Ksac', 'Karlstads central':'Ks', 'Karlstads yttre hamn':'Ksyh', 'Karlstad Välsviken':'Kvä', 'Karlstad östra':'Kö', 'Kil':'Kil', 'Kils omformarstation':'Kilo', 'Kristinehamn':'Khn', 'Molkom':'Mko', 'Sunne':'Sun', 'Säffle':'Sfl', 'Torsby':'Toy', 'Åmol':'Ål', 'Åmols djuphamn':'Åldj', 'Åmols östra':'Ålö', 'Reparationsplats, Kristinehamn':'Rkhn'}

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
<GT name="AdvertisedTimeAtLocation" value="$dateadd(07:00:00)" />
<LT name="AdvertisedTimeAtLocation" value="$dateadd(10:00:00)" />
</AND>
</OR>
</AND>
</FILTER>
<INCLUDE>AdvertisedTrainIdent</INCLUDE>
<INCLUDE>AdvertisedTimeAtLocation</INCLUDE>
<INCLUDE>TrackAtLocation</INCLUDE>
<INCLUDE>ToLocation</INCLUDE>
</QUERY>
</REQUEST>"""

    url = 'https://api.trafikinfo.trafikverket.se/v1.3/data.json'
    response = requests.post(url, data = request, headers = {'Content-Type': 'text/xml'}, )

    response_json = json.loads(response.text)
    departures = response_json["RESPONSE"]['RESULT'][0]['TrainAnnouncement']

    stationer_text.delete(1.0,"end")

    for dep in departures:
        stationer_text.insert(1., dep)
        stationer_text.insert(1., '\n')
          
#----------------------
root = tk.Tk()
canvas = tk.Canvas(root, height=500, width=965)
canvas.pack()

button=tk.Button(root, text='Hämta avgångar', fg='red', command= getDepartures)
button.place(relwidth=0.1, height=50)

stationerfr = ttk.Combobox(canvas, state='readonly')
stationerfr['values'] = list(stations_dict.keys())
stationerfr.place(relx=0, rely=0.5)
stationerto = ttk.Combobox(canvas, state='readonly')
stationerto['values'] = list(stations_dict.keys())
stationerto.place(relx=0, rely=0.6)

button=tk.Button(root, text='swap') #command= swapDestinations)
button.place(relx=0.05, rely=0.55)

fromTimeEntry = tk.Entry(canvas, text="from")
fromTimeEntry.place(relx=0.2, rely=0.5)
toTimeEntry = tk.Entry(canvas, text="to")
toTimeEntry.place(relx=0.2, rely=0.6)

stationer_text = tk.Text(canvas)
stationer_text.place(relx=0.3, rely=0, relwidth=0.7, relheight=1)

root.mainloop()