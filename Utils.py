import requests 
import pandas as pd
import datetime
from pandas import DataFrame
import altair as alt
from altair import datum
import pydeck as pdk
#import matplotlib.pyplot as plt
#import matplotlib.dates as mdates
#from matplotlib.pyplot import figure


def getData(tipo:str):
    if tipo=='regioni':
        data = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv" )
    if tipo=='province':
        data = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province.csv" )
    data["data"] = pd.to_datetime(data["data"]).apply(lambda x: x.date())
    return data   
  
    


cols = {
    "codice_regione": "Codice Regione",
    "denominazione_regione": "Denominazione Regione",
    "ricoverati_con_sintomi": "Ricoverati Con Sintomi",
    "terapia_intensiva": "Terapia Intensiva",
    "totale_ospedalizzati": "Totale Ospedalizzati",
    "isolamento_domiciliare": "Isolamento Domiciliare",
    "totale_attualmente_positivi": "Totale Attualmente Positivi",
    "nuovi_attualmente_positivi": "Nuovi Attualmente Positivi",
    "dimessi_guariti": "Dimessi Guariti",
    "totale_casi": "Casi Totali",
    "deceduti": "Deceduti",
    "tamponi": "Tamponi",
    "stato": "Stato",
    "data": "Data",
}
  
azioni = [
    "ricoverati_con_sintomi",
    "terapia_intensiva",
    "totale_ospedalizzati",
    "isolamento_domiciliare",
    "totale_attualmente_positivi",
    "nuovi_attualmente_positivi",
    "dimessi_guariti",
    "totale_casi",
    "deceduti",
    "tamponi"
    ]



def filtra(filtered_data):
    zeri =[]
    prov = []
    for i,val in filtered_data.iterrows():
        if val.totale_casi!=0:
            for index in range((val.totale_casi)):
                zeri.append([val.lat,val.lon])
            prov.append([val.denominazione_provincia,val.totale_casi])

    prov = pd.DataFrame(prov)  
    df = pd.DataFrame(zeri) 
    df.rename(columns={1:'lon',
                          0:'lat'}, 
                 inplace=True)

    prov.rename(columns={0:'Provincia',
                          1:'Casi'}, 
                 inplace=True)

    prov.sort_values(by=['Casi'], inplace=True, ascending=False)
    prov.set_index('Provincia',inplace=True)
    return df,prov



def altair_scatter(dataset, x, y, totale):
    
    brush = alt.selection_interval()

    plot = (
        alt.Chart(dataset, height=400, width=600)#'container')
        .mark_point(filled=True, opacity=0.8)
        .mark_line(point=True)
        .encode(x=x, y=y, color=alt.condition(brush, totale, alt.value('lightgray'))) 
    ).add_selection(brush)#.interactive()
        
    bars = alt.Chart(dataset, height=100, width=600).mark_bar().encode(
        y=totale,
        color=alt.Color(totale),
        x=y
        ).transform_filter(brush)
    
    
    
    return plot & bars




def altair_chart(dataset, x, y):

    bars = alt.Chart(dataset, height=200, width=800).mark_bar().encode( #800
        y=alt.X(x,sort=None),
        color=y,
        x=y) 
    return bars




def crea_mappa(df):
    mappa =(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=41.902782,
         longitude=12.496366,
         zoom=4.5,
         get_radius=1000,
         pitch=20,
     ),
     layers=[
         pdk.Layer(
            'HexagonLayer',
            data=df,
            get_position='[lon, lat]',
            radius=1000,
            elevation_scale=50,
            elevation_range=[0, 3000],
            #pickable=True,
            extruded=True,
            coverage=10,
         ),
     ],
    ))
    return mappa



def FattoreAumento(reg: bool, regione: str, df: pd.DataFrame, azione:str ):
    index=0
    val=0
    y = []  
    nome='denominazione_regione'
    if not reg:
        nome='denominazione_provincia'    
    data = []  
    for i,valore in df.iterrows():
        if(valore[nome] == regione):
            if(index==0):
                val = valore[azione]
            elif(index!=0):
                if val!=0:
                    y.append(round(valore[azione]/(val),4))
                else:
                    y.append(round(valore[azione],4))
                val=valore[azione]
                data.append(valore.data)
            index+=1
            print(valore)    
    print(y)
    
    return altair_scatter(df,data,y,"")
   # PlottingData(data,y,regione,azione)


def TotaleAumento(reg: bool,regione: str, df: pd.DataFrame, azione:str ):
    index=0
    val=0
    y = [] 
    
    data = []
    nome='denominazione_regione'
    if not reg:
        nome='denominazione_provincia'
    for i,valore in df.iterrows():
        if(valore[nome] == regione):
            if(index==0):
                val = valore[azione]
            elif(index!=0):
                y.append(valore[azione]-val)
                val=valore[azione]
                data.append(valore.data)
            index+=1
               

    #PlottingData(data,y,regione,azione)
    return altair_scatter(df,data,y,"")
    
    
def TotaleValori(reg: bool,regione: str, df: pd.DataFrame, azione:str ):
    y = []  
    data = []  
    nome='denominazione_regione'
    if not reg:
        nome='denominazione_provincia'
    for i,valore in df.iterrows():
        if(valore[nome] == regione):
                y.append(valore[azione])
                data.append(valore.data)
        print(valore)    
    print(regione , y)
    #PlottingData(data,y,regione,azione)
    return altair_scatter(df,data,y,"")
    
#fig, ax = plt.subplots()

#def PlottingData(x,y,regione:str,azione:str):
   
 #   ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
 #   fig.autofmt_xdate()
 #   plt.xlabel('data')
 #   plt.ylabel(azione)
 #   plt.plot(x,y, label=regione)

 #   plt.title('Aumento ' + azione)
  #  fig.set_size_inches(18.5, 10.5, forward=True)
 #   plt.legend();
  #  plt.grid(True)








def getLocations(data:pd.DataFrame, tipo:bool):
    locations=[]
    nome='denominazione_regione'
    if not tipo:
        nome='denominazione_provincia'
    for i,val in data.iterrows():
        locations.append(val[nome])
    locations=list(set(locations))
    return locations

def printLocations(locations:[]):
    for location in locations:
        print(location)
    

dataRegioni = getData('regioni')
dataProvince = getData('province')
province = getLocations(dataProvince,False)
regioni = getLocations(dataRegioni,True)



#for regione in regioni:
#    TotaleAumento(True,regione,dataRegioni,'tamponi')






#plt.show()