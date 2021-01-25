import requests
import tkinter as tk
from tkinter import ttk
import json

stations_dict = {'Karlstad':'Ks', 'Arvika': 'Ar', 'Kristinehamn':'Khn'}

api_key = '9fcb5b87d02d4edb92e6d5f85917ab7b'

def getDepartures():
    request = f"""<REQUEST>
<LOGIN authenticationkey="{api_key}" />
<QUERY objecttype="TrainAnnouncement" schemaversion="1.3" orderby="AdvertisedTimeAtLocation">
<FILTER>
<AND>
<EQ name="ActivityType" value="Avgang" />
<EQ name="LocationSignature" value="{stations_dict[stationer.get()]}" />
<OR>
<AND>
<GT name="AdvertisedTimeAtLocation" value="$dateadd(07:00:00)" />
<LT name="AdvertisedTimeAtLocation" value="$dateadd(10:00:00)" />
</AND>
<AND>
<LT name="AdvertisedTimeAtLocation" value="$dateadd(00:30:00)" />
<LT name="EstimatedTimeAtLocation" value="$dateadd(10:00:00)" />
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
canvas = tk.Canvas(root, height=500, width=1000)
canvas.pack()

button=tk.Button(root, text='Hämta avgångar', fg='red', command= getDepartures)
button.place(relwidth=0.1, height=50)

stationer = ttk.Combobox(canvas, state='readonly')
stationer['values'] = list(stations_dict.keys())
stationer.place(relx=0, rely=0.5)

stationer_text = tk.Text(canvas)
stationer_text.place(relx=0.3, rely=0, relwidth=0.7, relheight=1)

root.mainloop()